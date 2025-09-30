from pydantic import BaseModel
from typing import List, Optional

class Track(BaseModel):
    id: Optional[str]
    name: str
    artists: List[str]

    model_config = {"extra": "ignore"}