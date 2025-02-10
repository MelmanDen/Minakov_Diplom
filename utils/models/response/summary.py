from pydantic import BaseModel


class Summary(BaseModel):
    malicious: int
    suspicious: int
    undetected: int
    harmless: int
    timeout: int
