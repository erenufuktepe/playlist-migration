from typing import Iterable, List
from ..schemas.track import Track
from ..schemas.playlist import Playlist

class ConversionError(Exception):
    pass


def spotify_playlist_to_playlist(data: dict) -> Playlist:
    try:
        return Playlist.model_validate({
            "id": data.get("id"),
            "name": data.get("name"),
            "tracks": spotify_tracks_to_tracks(data.get("tracks", []).get("items", [])),
        })
    except Exception as exc:
        raise ConversionError("spotify_playlist_to_playlist failed") from exc

def spotify_track_to_track(item: dict) -> Track:
    try:
        print(item.get("artists", [])[0].get("name"))
        track_data = {
            "id": item.get("id"),
            "name": item.get("name"),
            "artists": [artist.get("name") for artist in item.get("artists", [])],
        }
        return Track.model_validate(track_data)
    except Exception as exc:
        raise ConversionError("spotify_track_to_track failed") from exc

def spotify_tracks_to_tracks(items: Iterable[dict]) -> List[Track]:
    return [spotify_track_to_track(it.get("track", {})) for it in items]