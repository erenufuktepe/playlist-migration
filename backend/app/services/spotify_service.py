from typing import Optional
from app.client.spotify_client import SpotifyClient
from app.converters.spotify import spotify_playlist_to_playlist
from app.schemas.playlist import Playlist

class NotFoundError(Exception):
    pass

class SpotifyServiceError(Exception):
    pass

class SpotifyService:
    def __init__(self, spotify_client : SpotifyClient = None):
        self.spotify_client = spotify_client or SpotifyClient()

    async def get_playlist(self, playlist_id: str) -> Playlist:
        try:
            raw = await self.spotify_client.get_playlist(playlist_id)
            playlist = spotify_playlist_to_playlist(raw)
        except Exception as exc:
            raise SpotifyServiceError(f"Failed to fetch playlist from Spotify: {exc}") from exc

        return playlist
