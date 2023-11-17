import pydantic


class AccountInfo(pydantic.BaseModel):
    id: int
    first_name: str
    last_name: str