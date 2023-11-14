from pydantic import BaseModel


class GetGraphRequest(BaseModel):
    code: str
    lang: str
    model: str
