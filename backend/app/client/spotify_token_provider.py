from typing import Mapping, Optional
from app.core.http import get_async_client
from app.core.config import settings
import secrets
from urllib.parse import urlencode
from fastapi import Request

from app.core.token_provider import TokenProvider


SPOTIFY_SCOPES = ["playlist-modify-public", "playlist-modify-private", "user-read-private", "user-read-email"]


class SpotifyTokenProviderException(Exception):
    pass

class SpotifyTokenProvider(TokenProvider):
    def __init__(self):
        self.url = settings.SPOTIFY_AUTH_URL
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.scopes = " ".join(SPOTIFY_SCOPES)
        self.state = secrets.token_urlsafe(32)
        self.code: str = None
        self._refresh_token: str = None
        
        
    async def fetch_token(self) -> Mapping[str, object]:
        client = await get_async_client()
        data = {
            "grant_type": "authorization_code", 
            "code": self.code, 
            "redirect_uri": settings.REDIRECT_URL
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = await client.post(f"{self.url}/api/token", data=data, headers=headers, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        response = response.json()
        self._refresh_token = response.get("refresh_token")
        return response

    async def refresh_token(self) -> Mapping[str, object]:
        client = await get_async_client()
        data = {"grant_type": "refresh_token", "refresh_token": self._refresh_token}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = await client.post(f"{self.url}/api/token", data=data, headers=headers, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        response = response.json()
        self.refresh_token = response.get("refresh_token")
        return response

    async def handle_authorization_code(self, request: Request) -> None:
        self.code = request.query_params.get("code")
        if request.query_params.get("state") != self.state:
            raise SpotifyTokenProviderException("Invalid state parameter")

    async def build_authorization_url(self) -> str:
        state = secrets.token_urlsafe(32)
        self.state = state

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": settings.REDIRECT_URL,
            "scope": self.scopes,
            "state": self.state
        }
        return f"{self.url}/authorize?{urlencode(params, safe=':/').replace('+', '%20')}"
