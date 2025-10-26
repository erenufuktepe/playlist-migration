import logging
from typing import Optional
from app.client.spotify_client import SpotifyClient
from app.converters.play_list_converter import PlayListConverter
from app.schemas.playlist import Playlist

logger = logging.getLogger(__name__)


class SpotifyServiceError(Exception):
    pass

class SpotifyService:
    def __init__(self, spotify_client : SpotifyClient = None):
        self.spotify_client = spotify_client or SpotifyClient()

    async def get_playlist(self, playlist_id: str) -> Playlist:
        try:
            response = await self.spotify_client.get_playlist(playlist_id)
            playlist = PlayListConverter.from_spotify(response)
            return playlist
        except Exception as exception:
            logger.error(f"Failed to fetch playlist from Spotify for: {playlist_id}")
            raise SpotifyServiceError(f"Failed to fetch playlist from Spotify for: {playlist_id}") from exception
