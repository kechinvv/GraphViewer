from __future__ import annotations

import requests
import os
import pydantic


class AccountInfo(pydantic.BaseModel):
    id: int
    first_name: str
    last_name: str


def get_access_token(code: str) -> str:
    site = 'https://oauth.vk.com/access_token'
    client_id = os.environ['client_id']
    secret = os.environ['client_secret']
    redirect = 'http://localhost:8000/vk'
    url = f"{site}?client_id={client_id}&client_secret={secret}&redirect_uri={redirect}&code={code}"
    res = requests.get(url)
    data: dict = res.json()
    code = data.get('access_token')
    return code


def get_account_info(access_token: str) -> AccountInfo | None:
    site = 'https://api.vk.com/method/users.get'
    result = requests.post(site, data={'access_token': access_token, 'v': '5.131'})
    try:
        user = result.json()['response'][0]
    except Exception:
        return None
    return AccountInfo(**user)

