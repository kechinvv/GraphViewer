import pydantic


class ShortCodeDescription(pydantic.BaseModel):
    id: int
    description: str
