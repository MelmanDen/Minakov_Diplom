from pydantic import BaseModel


class CheckPhishConfig(BaseModel):
    api_key: str
    scan_url: str
    status_url: str
