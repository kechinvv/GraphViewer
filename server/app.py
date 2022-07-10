import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response, status, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from typing import List

from vk import get_account_info, get_access_token, AccountInfo
from session import backend, cookie, verifier
from models import Code
from db import get_db
from schemas import ShortCodeDescription

from python.handler import handler as py_handler
from kotlin.handler import handler as kt_handler
from c.handler import handler as c_handler
from go.handler import handler as go_handler
from java.handler import handler as java_handler
from javascript.handler import handler as js_handler

functions = {'python': ('ast', 'cfg', 'ddg'), 'kotlin': ('ast', 'cfg'), 'c': ('ast', 'cfg', 'ssa'), 'go': ('ast', 'cfg'),
             'java': ('ast', 'cfg'), 'js': ('ast', 'cfg')}
handlers = {"python": py_handler, "kotlin": kt_handler, "c": c_handler, 'go': go_handler, 'java': java_handler,
            'js': js_handler}

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
app.mount("/client", StaticFiles(directory="../client"), name="client")


@app.get("/")
async def root(request: Request):
    return FileResponse('../client/views/index.html')


@app.get("/vk", tags=['User'])
async def vk(code: str):
    code = get_access_token(code)
    if code is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Error')
    user = get_account_info(code)

    session = uuid4()

    await backend.create(session, user)
    res = RedirectResponse('/')
    cookie.attach_to_response(res, session)
    return res


@app.get("/whoami", dependencies=[Depends(cookie)], tags=['User'])
async def whoami(session_data: AccountInfo = Depends(verifier)):
    """VK user info - id & username"""
    return session_data


@app.get("/exit", tags=['User'])
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "exit"


@app.post("/code", dependencies=[Depends(cookie)], tags=['Code'])
async def save_code(language: str, code: str, description: str, session_data: AccountInfo = Depends(verifier), db: Session = Depends(get_db)):
    c = Code(description=description, language=language, code=code, user_id=session_data.id)
    try:
        db.add(c)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return 'ok'


@app.get("/user_code", dependencies=[Depends(cookie)], tags=['Code'], response_model=List[ShortCodeDescription])
async def all_user_code(session_data: AccountInfo = Depends(verifier), db: Session = Depends(get_db)):
    """return all saved user code in short format"""
    all_code = db.query(Code).filter(Code.user_id == session_data.id).all()
    return [ShortCodeDescription(id=c.id, description=c.description) for c in all_code]


@app.get("/code", dependencies=[Depends(cookie)], tags=['Code'])
async def code(code_id: int, session_data: AccountInfo = Depends(verifier), db: Session = Depends(get_db)):
    """return one source code by id"""
    db_code = db.query(Code).filter(Code.user_id == session_data.id, Code.id == code_id).first()
    if db_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_code


@app.delete('/code', dependencies=[Depends(cookie)], tags=['Code'])
async def delete_code(code_id: int, session_data: AccountInfo = Depends(verifier), db: Session = Depends(get_db)):
    db_code = db.query(Code).filter(Code.user_id == session_data.id, Code.id == code_id).first()
    if db_code is None:
        return Response(status_code=status.HTTP_200_OK)
    db.delete(db_code)
    try:
        db.commit()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@app.get('/functions')
async def all_functions():
    """return all available languages and models"""
    return functions


@app.get('/view_graph')
async def view_graph(code: str = example_code, lang: str = "python", model: str = "ast"):
    if lang in functions and model in functions[lang]:
        try:
            data = handlers.get(lang)(code, model)
            return Response(data, media_type=f"text/dot")
        except SyntaxError as e:
            raise HTTPException(400, detail=str(e))
        except Exception as e:
            raise HTTPException(400, detail=str(e))
    else:
        raise HTTPException(400, "Language and model not implemented")


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True, debug=True)
