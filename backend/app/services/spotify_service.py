import logging
from typing import Optional

from app.client.spotify_client import SpotifyClient, get_spotify_client
from app.converters.play_list_converter import PlayListConverter
from app.converters.track_converter import TrackConverter
from app.schemas.playlist import Playlist, PlaylistCreateRequest
from app.schemas.track import Track
from fastapi import Request

logger = logging.getLogger(__name__)


class SpotifyServiceError(Exception):
    pass


class SpotifyService:
    """
    Thin service layer around SpotifyClient.
    Accepts an optional SpotifyClient for easier testing/wiring.
    """

    def __init__(self, spotify_client: Optional[SpotifyClient] = None) -> None:
        self.spotify_client = spotify_client or get_spotify_client()

    async def get_authorization_url(self) -> str:
        """Return the Spotify authorization URL (caller will redirect)."""
        try:
            logger.info("Fetching Spotify authorization URL")
            url = await self.spotify_client.get_authorization_url()
            return {"authorization_url": url}
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def handle_callback(self, request: Request) -> None:
        """Handle OAuth callback: validate, exchange code and persist tokens (client does the heavy lifting)."""
        try:
            logger.info("Handling Spotify callback")
            await self.spotify_client.handle_callback(request)
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch playlist from Spotify and convert to internal Playlist schema."""
        try:
            logger.info(f"Fetching playlist from Spotify for ID: {playlist_id}")
            response = await self.spotify_client.get_playlist(playlist_id)
            playlist = PlayListConverter.from_spotify_playlist(response)
            return playlist
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def create_playlist(self, request: PlaylistCreateRequest) -> str:
        """Create a playlist on Spotify and return the new playlist id."""
        try:
            logger.info(f"Creating playlist on Spotify with name: {request.name}")
            response = await self.spotify_client.create_playlist(request)
            return response["id"]
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def search_track(self, artist: str, track: str) -> Optional[Track]:
        """
        Search Spotify for a track. Either provide `q` (raw query) or artist and/or track.
        Returns the first matching Track or None.
        """
        try:
            query = f"artist:{artist} track:{track}"
            response = await self.spotify_client.search_track(query)
            track = response.get("tracks", {}).get("items", [])
            if not track:
                logger.info(f"No tracks found on Spotify for query: {query}")
                return None
            return TrackConverter.from_spotify_track(track[0])
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def add_tracks_to_playlist(
        self, playlist_id: str, track_uris: list[str]
    ) -> None:
        """
        Add track URIs to a playlist. Accepts plain track ids or full spotify:track:<id> URIs.
        """
        try:
            logger.info(f"Adding tracks to playlist on Spotify with ID: {playlist_id}")
            track_uris = [f"spotify:track:{track_uri}" for track_uri in track_uris]
            await self.spotify_client.add_tracks_to_playlist(playlist_id, track_uris)
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc

    async def get_playlists(self) -> list[Playlist]:
        """Get all playlists for the current user."""
        try:
            logger.info("Fetching all playlists for current Spotify user")
            response = await self.spotify_client.get_playlists()
            playlists_data = response.get("items", [])
            playlists = [
                PlayListConverter.from_spotify_playlist(playlist)
                for playlist in playlists_data
            ]
            return playlists
        except Exception as exc:
            raise SpotifyServiceError(exc) from exc
