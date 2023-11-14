import pydantic


class GoogleAccInfo(pydantic.BaseModel):
    email: str
