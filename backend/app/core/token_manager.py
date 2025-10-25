from datetime import datetime, timezone, timedelta
import asyncio
from typing import Mapping, Optional
from app.core.config import settings
from app.core.token_provider import TokenProvider

class Token:
    def __init__(self, access_token: str, expires_at: datetime):
        self.access_token = access_token
        self.expires_at = expires_at

    def is_valid(self) -> bool:
        return datetime.now(timezone.utc) < self.expires_at


class TokenManager:
    def __init__(self, provider: Optional[TokenProvider] = None):
            self._token: Optional[Token] = None
            self._lock = asyncio.Lock()
            self._provider = provider

    async def get_token(self) -> str:
        # fast path without lock
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
        payload = await self._provider.fetch_token()
        access_token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 3600))
        skew = int(getattr(settings, "TOKEN_REFRESH_SKEW", 60))
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(expires_in - skew, 1))
        self._token = Token(access_token=access_token, expires_at=expires_at)