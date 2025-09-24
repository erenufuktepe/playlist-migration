import asyncio
from datetime import datetime, timedelta, timezone
import httpx
from app.core.config import settings
from app.core.http import get_async_client

class Token:
    def __init__(self, access_token: str, expires_at: datetime):
        self.access_token = access_token
        self.expires_at = expires_at

    def is_valid(self) -> bool:
        return datetime.now(timezone.utc) < self.expires_at

class TokenManager:
    def __init__(self):
        self._token: Token | None = None
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        if self._token and self._token.is_valid():
            return self._token.access_token

        async with self._lock:
            if self._token and self._token.is_valid():
                return self._token.access_token
            await self._refresh_token()
            return self._token.access_token

    async def force_refresh(self) -> str:
        async with self._lock:
            await self._refresh_token()
            return self._token.access_token

    async def _refresh_token(self) -> None:
        client = await get_async_client()

        data = {
            "grant_type": "client_credentials",
        }
        #if settings.TOKEN_SCOPE:
        #    data["scope"] = settings.TOKEN_SCOPE
        #if settings.TOKEN_AUDIENCE:
        #    data["audience"] = settings.TOKEN_AUDIENCE

        auth = (settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)

        resp = await client.post("https://accounts.spotify.com/api/token", data=data, auth=auth)
        resp.raise_for_status()
        payload = resp.json()

        # Common fields: access_token + expires_in (seconds)
        access_token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 3600))

        # Subtract a small skew so we refresh a bit early
        skew = settings.TOKEN_REFRESH_SKEW
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(expires_in - skew, 1))

        self._token = Token(access_token=access_token, expires_at=expires_at)
        print(access_token, expires_at)

# Singleton for app
token_manager = TokenManager()
