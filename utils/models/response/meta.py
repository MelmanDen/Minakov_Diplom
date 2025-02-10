from pydantic import BaseModel


class Meta(BaseModel):
    url: str
    url_sha256: str
    image: str
    resolved: bool
