from pydantic import BaseModel
from typing import Optional, List
from .track import Track


class Playlist(BaseModel):
    id: Optional[str] = None
    name: str
    tracks: List[Track] = []

    model_config = {"extra": "ignore"}