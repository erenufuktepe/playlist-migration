from typing import List

from pydantic import BaseModel


class Track(BaseModel):
    id: str
    name: str
    artists: List[str]

    model_config = {"extra": "ignore"}
