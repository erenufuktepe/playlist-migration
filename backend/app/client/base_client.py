from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Any
import httpx
from app.core.http import get_async_client

class BaseClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    @abstractmethod
    async def _auth_headers(self) -> Dict[str, str]:
        ...

    async def _on_401(self) -> None:
        """Hook subclasses can override to refresh tokens on 401."""
        return None

    async def _get_client(self) -> httpx.AsyncClient:
        return await get_async_client()

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        client = await self._get_client()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.pop("headers", {}) or {}
        headers.update(await self._auth_headers())

        response = await client.request(method, url, headers=headers, **kwargs)

        # 401: refresh once and retry
        if response.status_code == 401:
            try:
                await self._on_401()
            except Exception:
                pass
            headers = await self._auth_headers()
            response = await client.request(method, url, headers=headers, **kwargs)

        # 429: respect Retry-After and retry once
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1") or "1")
            await asyncio.sleep(max(retry_after, 1))
            headers = await self._auth_headers()
            response = await client.request(method, url, headers=headers, **kwargs)

        response.raise_for_status()
        return response

    async def get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        return await self._request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        return await self._request("DELETE", endpoint, **kwargs)
    