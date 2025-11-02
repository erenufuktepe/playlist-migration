import logging
from typing import Optional
from app.client.spotify_client import SpotifyClient
from app.converters.play_list_converter import PlayListConverter
from app.schemas.playlist import Playlist, PlaylistCreateRequest
from fastapi import Request

logger = logging.getLogger(__name__)


class SpotifyServiceError(Exception):
    pass

class SpotifyService:
    def __init__(self, spotify_client : SpotifyClient = None):
        self.spotify_client = spotify_client or SpotifyClient()

    async def get_authorization_url(self) -> str:
        try:
            url = await self.spotify_client.get_authorization_url()
            return {"authorization_url": url}
        except Exception as exception:
            logger.error("Failed to get Spotify authorization URL")
            raise SpotifyServiceError("Failed to get Spotify authorization URL") from exception

    async def authorize_user(self, request: Request) -> str:
        try:
            await self.spotify_client.authorize(request)
        except Exception as exception:
            logger.error("Failed to get Spotify authorization URL")
            raise SpotifyServiceError("Failed to get Spotify authorization URL") from exception


    async def get_playlist(self, playlist_id: str) -> Playlist:
        try:
            response = await self.spotify_client.get_playlist(playlist_id)
            playlist = PlayListConverter.from_spotify(response)
            return playlist
        except Exception as exception:
            logger.error(f"Failed to fetch playlist from Spotify for: {playlist_id}")
            raise SpotifyServiceError(f"Failed to fetch playlist from Spotify for: {playlist_id}") from exception


    async def create_playlist(self, request: PlaylistCreateRequest) -> None:
        try:
            response = await self.spotify_client.create_playlist(request)
            return response['id'] 
        except Exception as exception:
            logger.error(f"Failed to create playlist on Spotify")
            raise SpotifyServiceError(f"Failed to create playlist on Spotify") from exception
        
    
    async def search_track(self, artist: str, track: str) -> None:
        try:
            query = f"artist:{artist} track:{track}"
            return await self.spotify_client.search_track(query)
        except Exception as exception:
            logger.error(f"Failed to search tracks on Spotify")
            raise SpotifyServiceError(f"Failed to search tracks on Spotify") from exception
        
    
    async def add_tracks_to_playlist(self, playlist_id: str, track_uris: list[str]) -> None:
        try:
            track_uris = [f"spotify:track:{track_uri}" for track_uri in track_uris]
            return await self.spotify_client.add_tracks_to_playlist(playlist_id, track_uris)
        except Exception as exception:
            logger.error(f"Failed to add tracks to playlist on Spotify")
            raise SpotifyServiceError(f"Failed to add tracks to playlist on Spotify") from exception