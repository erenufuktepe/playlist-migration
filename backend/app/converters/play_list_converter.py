
import logging
from app.schemas.playlist import Playlist
from app.converters.track_converter import TrackConverter

logger = logging.getLogger(__name__)

class PlayListConverterException(Exception):
    pass


class PlayListConverter:
    @staticmethod
    def from_spotify(spotify_playlist_data: dict) -> Playlist:
        try:
            return Playlist.model_validate({
                "id": spotify_playlist_data.get("id"),
                "name": spotify_playlist_data.get("name"),
                "tracks": TrackConverter.from_spotify_tracks(spotify_playlist_data.get("tracks", []).get("items", [])),
            })
        except Exception as exception:
            logger.error(f"Error converting spotify playlist id: {spotify_playlist_data.get('id')}", exc_info=exception)
            raise PlayListConverterException(f"Fail to convert spotify playlist id: {spotify_playlist_data.get('id')}") from exception
