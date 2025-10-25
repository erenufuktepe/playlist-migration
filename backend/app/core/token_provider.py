from abc import ABC, abstractmethod
from typing import Mapping
from app.core.http import get_async_client
from app.core.config import settings

class TokenProvider(ABC):
    @abstractmethod
    async def fetch_token(self) -> Mapping[str, object]:
        """
        Return at least:
          - access_token (str)
          - expires_in (int)  # seconds
        """
        ...

class SpotifyTokenProvider(TokenProvider):
    def __init__(self):
        self.url = "https://accounts.spotify.com/api/token"
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET

    async def fetch_token(self) -> Mapping[str, object]:
        client = await get_async_client()
        data = {"grant_type": "client_credentials"}
        response = await client.post(self.url, data=data, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        return response.json()

    

class AppleTokenProvider(TokenProvider):
    """
    Apple tokens are JWTs you sign locally (no token endpoint). This provider
    generates a JWT using your private key and returns it as access_token.
    """
    def __init__(self, team_id: str, key_id: str, private_key_path: str, ttl: int):
        self.team_id = team_id
        self.key_id = key_id
        self.private_key_path = private_key_path
        self.ttl = ttl

    async def fetch_token(self) -> Mapping[str, object]:
        ...