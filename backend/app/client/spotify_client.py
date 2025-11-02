import logging
from urllib.parse import urlencode
from app.client.base_client import BaseClient
from app.core.token_manager import TokenManager
from app.core.config import settings
from app.client.spotify_token_provider import SpotifyTokenProvider

logger = logging.getLogger(__name__)

from fastapi import Request

from app.schemas.playlist import PlaylistCreateRequest


class SpotifyClientException(Exception):
    pass 

class SpotifyClient(BaseClient):
    def __init__(self, base_url: str = settings.SPOTIFY_ENDPOINT, _token_manager: TokenManager = None):
        self.base_url = base_url
        self._token_manager = _token_manager or TokenManager(SpotifyTokenProvider())

    async def _auth_headers(self: str) -> dict:
        token = await self._token_manager.get_token()
        return {"Authorization": f"Bearer {token}"}

    async def get_authorization_url(self) -> str:
        return await self._token_manager._provider.build_authorization_url()
    
    async def authorize(self, request: Request):
        await self._token_manager.set_code(request)

    # ====== Public Spotify API methods =======

    async def get_playlist(self, playlist_id: str) -> dict:
        """
        Get Spotify catalog information for a single playlist.
        Docs: https://developer.spotify.com/documentation/web-api/reference/get-playlist
        """
        try:
            response = await self.get(f"playlists/{playlist_id}")
            response.raise_for_status()
            return response.json()
        except Exception as exception:
            logger.error(f"Failed to get playlist: {playlist_id}")
            raise SpotifyClientException(f"Failed to get playlist: {playlist_id}") from exception

    async def get_current_user(self) -> dict:
        """
        Get detailed profile information about the current user.
        Docs: https://developer.spotify.com/documentation/web-api/reference/get-current-user-profile
        """
        try:
            response = await self.get("me")
            response.raise_for_status()
            return response.json()
        except Exception as exception:
            logger.error(f"Failed to get current user profile: {exception}")
            raise SpotifyClientException(f"Failed to get current user profile: {exception}") from exception

    async def create_playlist(self, request: PlaylistCreateRequest) -> dict:
        """
        Create a new playlist for a Spotify user.
        Docs: https://developer.spotify.com/documentation/web-api/reference/create-playlist
        Note: This endpoint requires the 'playlist-modify-public' or 'playlist-modify-private' scope.
        """
        try:
            user = await self.get_current_user()
            data = {
                "name": request.name,
                "description": request.description,
                "public": request.public
            }
            response = await self.post(f"users/{user['id']}/playlists", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as exception:
            logger.error(f"Failed to create playlist: {exception}")
            raise SpotifyClientException("Failed to create playlist") from exception

    
    async def search_track(self, query: str, limit: int = 1) -> dict:
        """
        Search for tracks in the Spotify catalog.
        Docs: https://developer.spotify.com/documentation/web-api/reference/search
        """
        try:
            params = {"q": query, "type": "track", "limit": limit}
            query_string = urlencode(params)
            response = await self.get(f"search?{query_string}")
            response.raise_for_status()
            return response.json()
        except Exception as exception:
            logger.error(f"Failed to search tracks: {exception}")
            raise SpotifyClientException("Failed to search tracks") from exception


    async def add_tracks_to_playlist(self, playlist_id: str, track_uris: list) -> dict:
        """
        Add tracks to a Spotify playlist.
        Docs: https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
        """
        try:
            data = {"uris": track_uris}
            response = await self.post(f"playlists/{playlist_id}/tracks", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as exception:
            logger.error(f"Failed to add tracks to playlist: {exception}")
            raise SpotifyClientException("Failed to add tracks to playlist") from exception


def get_spotify_client() -> SpotifyClient:
    return _spotify_client

_spotify_client = SpotifyClient()
