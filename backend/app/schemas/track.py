from pydantic import BaseModel
from typing import List

class Track(BaseModel):
    id: str
    name: str
    artists: List[str]

    model_config = {"extra": "ignore"}