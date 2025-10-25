from app.client.base_client import BaseClient
from app.core.token_manager import TokenManager
from app.core.config import settings
from app.core.token_provider import SpotifyTokenProvider

class SpotifyClient(BaseClient):
    def __init__(self, base_url: str = settings.SPOTIFY_ENDPOINT, _token_manager: TokenManager = None):
        self.base_url = base_url
        self._token_manager = _token_manager or TokenManager(SpotifyTokenProvider())

    async def _auth_headers(self: str) -> dict:
        token = await self._token_manager.get_token()
        return {"Authorization": f"Bearer {token}"}
    
    # ====== Public Spotify API methods ======

    async def get_playlist(self, playlist_id: str) -> dict:
        """
        Get Spotify catalog information for a single playlist.
        Docs: https://developer.spotify.com/documentation/web-api/reference/get-playlist
        """
        response = await self._request("GET", f"playlists/{playlist_id}")
        return response.json()
    
    
    async def create_playlist(self, user_id: str, name: str, description: str = "", public: bool = False) -> dict:
        """
        Create a new playlist for a Spotify user.
        Docs: https://developer.spotify.com/documentation/web-api/reference/create-playlist
        Note: This endpoint requires the 'playlist-modify-public' or 'playlist-modify-private' scope.
        """
        data = {
            "name": name,
            "description": description,
            "public": public
        }
        response = await self._request("POST", f"users/{user_id}/playlists", json=data)
        return response.json()
    
    
    
    ## TODO: 
    ## Create playlist
    ## Search for tracks
    ## Add tracks to playlist


def get_spotify_client() -> SpotifyClient:
    return _spotify_client

_spotify_client = SpotifyClient()
