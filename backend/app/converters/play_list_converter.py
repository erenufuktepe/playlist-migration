import logging

from app.converters.track_converter import TrackConverter
from app.schemas.playlist import Playlist

logger = logging.getLogger(__name__)


class PlayListConverterException(Exception):
    pass


class PlayListConverter:
    @staticmethod
    def from_spotify_playlist(spotify_playlist_data: dict) -> Playlist:
        try:
            return Playlist.model_validate(
                {
                    "id": spotify_playlist_data.get("id"),
                    "name": spotify_playlist_data.get("name"),
                    "tracks": TrackConverter.from_spotify_tracks(
                        spotify_playlist_data.get("tracks", []).get("items", [])
                    ),
                }
            )
        except Exception as exc:
            raise PlayListConverterException(
                f"Fail to convert spotify playlist id {spotify_playlist_data.get('id')} : {exc}"
            ) from exc
