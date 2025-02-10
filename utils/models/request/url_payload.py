from pydantic import BaseModel


class URLPayload(BaseModel):
    url: str
