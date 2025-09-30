import httpx
import asyncio
from app.core.token_manager import token_manager
from app.core.http import get_async_client

class SpotifyClient:
    def __init__(self, base_url: str = "https://api.spotify.com/v1"):
        self.base_url = base_url.rstrip("/")

    async def _auth_headers(self: str) -> dict:
        token = await token_manager.get_token()
        return {"Authorization": f"Bearer {token}"}
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        client = await get_async_client()
        url = f"{self.base_url}/{endpoint}"
        headers = kwargs.pop("headers", {})
        # attach auth headers
        headers.update(await self._auth_headers())

        response = await client.request(method, url, headers=headers, **kwargs)

        # 401: token may be expired or invalid — refresh once and retry
        if response.status_code == 401:
            try:
                await token_manager.force_refresh()
            except Exception:
                # let the caller see the original 401 if token refresh fails
                pass
            headers = await self._auth_headers()
            response = await client.request(method, url, headers=headers, **kwargs)

        # 429: rate limited — respect Retry-After and retry once
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            await asyncio.sleep(max(retry_after, 1))
            # refresh auth headers in case token rotated
            headers = await self._auth_headers()
            response = await client.request(method, url, headers=headers, **kwargs)

        # surface HTTP errors
        response.raise_for_status()
        return response

    
    
    # ====== Public Spotify API methods ======


    async def get_playlist(self, playlist_id: str) -> dict:
        """
        Get Spotify catalog information for a single playlist.
        Docs: https://developer.spotify.com/documentation/web-api/reference/get-playlist
        """
        response = await self._request("GET", f"playlists/{playlist_id}")
        return response.json()


spotify_client = SpotifyClient("https://api.spotify.com/v1")
