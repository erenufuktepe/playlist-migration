from pydantic import BaseModel
from typing import List
from .track import Track


class Playlist(BaseModel):
    id: str 
    name: str
    tracks: List[Track] = []

    model_config = {"extra": "ignore"}