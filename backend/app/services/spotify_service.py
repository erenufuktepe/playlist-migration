# backend/app/services/spotify_service.py
from typing import Optional
from app.client.spotify import spotify_client
from app.converters.spotify import spotify_playlist_to_playlist
from app.schemas.playlist import Playlist

class NotFoundError(Exception):
    pass

class SpotifyServiceError(Exception):
    pass

class SpotifyService:
    def __init__(self):
        self._cache: dict[str, Playlist] = {}

    async def get_playlist(self, playlist_id: str) -> Playlist:
        try:
            raw = await spotify_client.get_playlist(playlist_id)
            playlist = spotify_playlist_to_playlist(raw)
        except Exception as exc:
            raise SpotifyServiceError(f"Failed to fetch playlist from Spotify: {exc}") from exc

        return playlist

def get_spotify_service() -> SpotifyService:
    return SpotifyService()

# singleton instance for other internal uses
spotify_service = SpotifyService()