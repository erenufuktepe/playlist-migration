import logging
from app.schemas.track import Track

logger = logging.getLogger(__name__)

class TrackConverterException(Exception):
    pass

class TrackConverter:
    @staticmethod
    def from_spotify_track(spotify_track_data: dict) -> Track:
        try:
            spotify_track_data = spotify_track_data.get("track", spotify_track_data)
            track_data = {
                "id": spotify_track_data.get("id"),
                "name": spotify_track_data.get("name"),
                "artists": [artist.get("name") for artist in spotify_track_data.get("artists", [])],
            }
            return Track.model_validate(track_data)
        except Exception as exception:
            logger.error(f"Error converting spotify track id: {spotify_track_data.get('id')}", exc_info=exception)
            raise TrackConverterException(f"Fail to convert spotify track id: {spotify_track_data.get('id')}") from exception
        
    @staticmethod
    def from_spotify_tracks(spotify_tracks_data: list[dict]) -> list[Track]:
        return [TrackConverter.from_spotify_track(track) for track in spotify_tracks_data]