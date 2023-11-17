import os

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response, status, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from typing import List

from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

from apps.schemas.GoogleAccInfo import GoogleAccInfo
from apps.schemas.ShortCodeDescription import ShortCodeDescription
from dot_to_json.deprecated.converter_with_sub import convert_dot_to_json as convert_dot_to_json_with_sub
from dot_to_json.deprecated.request_with_sub import V1GetGraphRequest, map_to_v1response, V1GetGraphResponse
from dot_to_json.converter import convert_dot_to_json
from dot_to_json.request import V2GetGraphRequest, map_to_response, V2GetGraphResponse
from apps.vk import AccountInfo
from apps.session import backend, cookie, verifier
from apps.models import Code
from apps.db import get_db
from fastapi.middleware.cors import CORSMiddleware

from languages.model_builders import *

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

functions = {lang.value: list(map(lambda k: k.value, models.keys())) for lang, models in model_builders.items()}

example_code = """
a = 2 + 2 * (c * d / 2)
b = a + a / 2
if b > 4:
    print('hello')
else:
    print('nooo')
print('exit')
"""

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="a")
app.mount("/client", StaticFiles(directory="../client"), name="client")

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)
# to solve corse problems during develompment
# ideally should be conditionally applied using env variable
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="../dist/assets"), name="static")

@app.get("/")
async def root(request: Request):
    return FileResponse('../dist/index.html')


@app.get("/login", tags=['User'])
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@app.get("/auth", tags=['User'])
async def auth(request: Request):
    response = RedirectResponse(url='/')
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        response = RedirectResponse(url='/')
        return response

    user = token.get('userinfo')
    print(user)
    if user:
        # request.session['user'] = dict(user)
        session = uuid4()
        await backend.create(session, GoogleAccInfo(**user))
        cookie.attach_to_response(response, session)
    return response


@app.get("/whoami", dependencies=[Depends(cookie)], tags=['User'])
def whoami(session_data: AccountInfo = Depends(verifier)):
    """VK user info - id & username"""
    return session_data


@app.get("/exit", tags=['User'])
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "exit"


@app.post("/code", dependencies=[Depends(cookie)], tags=['Code'])
def save_code(language: str, code: str, description: str, session_data: GoogleAccInfo = Depends(verifier),
              db: Session = Depends(get_db)):
    c = Code(description=description, language=language, code=code, email=session_data.email)
    try:
        db.add(c)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return 'ok'


@app.get("/user_code", dependencies=[Depends(cookie)], tags=['Code'], response_model=List[ShortCodeDescription])
def all_user_code(session_data: GoogleAccInfo = Depends(verifier), db: Session = Depends(get_db)):
    """return all saved user code in short format"""
    all_code = db.query(Code).filter(Code.email == session_data.email).all()
    return [ShortCodeDescription(id=c.id, description=c.description) for c in all_code]


@app.get("/code", dependencies=[Depends(cookie)], tags=['Code'])
def code(code_id: int, session_data: GoogleAccInfo = Depends(verifier), db: Session = Depends(get_db)):
    """return one source code by id"""
    db_code = db.query(Code).filter(Code.email == session_data.email, Code.id == code_id).first()
    if db_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_code


@app.delete('/code', dependencies=[Depends(cookie)], tags=['Code'])
def delete_code(code_id: int, session_data: GoogleAccInfo = Depends(verifier), db: Session = Depends(get_db)):
    db_code = db.query(Code).filter(Code.email == session_data.email, Code.id == code_id).first()
    if db_code is None:
        return Response(status_code=status.HTTP_200_OK)
    db.delete(db_code)
    try:
        db.commit()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@app.get('/functions')
def all_functions():
    """return all available languages and models"""
    return functions


@app.get('/view_graph')
def view_graph(code: str = example_code, lang: str = "python", model: str = "ast"):
    model_builder = get_model_builder(lang, model)
    if model_builder is None:
        raise HTTPException(400, "Language and model not implemented")

    try:
        data = model_builder.build(code)
        return Response(data, media_type=f"text/dot")
    except SyntaxError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.post('/v1/view_graph')
def view_graph_v1(request: V1GetGraphRequest) -> V1GetGraphResponse:
    model_builder = get_model_builder(request.lang, request.model)
    if model_builder is None:
        raise HTTPException(400, "Language and model not implemented")

    try:
        data = model_builder.build(request.code)
        response = convert_dot_to_json_with_sub(data, request.lang)
        return map_to_v1response(response)
    except SyntaxError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@app.post('/v2/view_graph')
def view_graph_v2(request: V2GetGraphRequest) -> V2GetGraphResponse:
    model_builder = get_model_builder(request.lang, request.model)
    if model_builder is None:
        raise HTTPException(400, "Language and model not implemented")

    try:
        data = model_builder.build(request.code)
        response = convert_dot_to_json(data, request.lang)
        return map_to_response(response)
    except SyntaxError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(400, detail=str(e))


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True, debug=True)

# @app.get("/vk", tags=['User'])
# async def vk(code: str):
#     code = get_access_token(code)
#     if code is None:
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Error')
#     user = get_account_info(code)
#
#     session = uuid4()
#
#     await backend.create(session, user)
#     res = RedirectResponse('/')
#     cookie.attach_to_response(res, session)
#     return res
