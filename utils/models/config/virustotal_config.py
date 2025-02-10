from pydantic import BaseModel
from typing import Optional


class VirusTotalConfig(BaseModel):
    api_key: str
    scan_url: str
    accept: Optional[str] = "application/json"
