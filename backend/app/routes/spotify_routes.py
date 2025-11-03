import logging
from typing import Optional

from app.client.spotify_client import get_spotify_client
from app.core.config import settings
from app.schemas.playlist import Playlist, PlaylistCreateRequest
from app.schemas.track import Track
from app.services.spotify_service import SpotifyService, SpotifyServiceError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spotify", tags=["spotify"])

spotify_service = SpotifyService(get_spotify_client())


def get_spotify_service() -> SpotifyService:
    return spotify_service


@router.get("/playlist/{playlist_id}")
async def get_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
) -> Playlist:
    try:
        return await service.get_playlist(playlist_id)
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.get("/authorization-url")
async def get_authorization_url(service: SpotifyService = Depends(get_spotify_service)):
    try:
        return await service.get_authorization_url()
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.get("/callback")
async def spotify_callback(
    request: Request, service: SpotifyService = Depends(get_spotify_service)
):
    try:
        await service.handle_callback(request)
        return RedirectResponse(f"{settings.FRONTEND_HOST}?auth=success")
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.post("/create-playlist", status_code=201)
async def create_playlist(
    request: PlaylistCreateRequest,
    service: SpotifyService = Depends(get_spotify_service),
) -> str:
    try:
        return await service.create_playlist(request)
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.get("/search-track")
async def search_track(
    artist: str, track: str, service: SpotifyService = Depends(get_spotify_service)
) -> Optional[Track]:
    try:
        return await service.search_track(artist, track)
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.post("/playlist/{playlist_id}/add-tracks", status_code=204)
async def add_tracks_to_playlist(
    playlist_id: str,
    track_uris: list[str],
    service: SpotifyService = Depends(get_spotify_service),
) -> None:
    try:
        await service.add_tracks_to_playlist(playlist_id, track_uris)
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc


@router.get("/playlists")
async def get_playlists(
    service: SpotifyService = Depends(get_spotify_service),
) -> list[Playlist]:
    try:
        return await service.get_playlists()
    except SpotifyServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": "Upstream service error", "details": str(exc)},
        ) from exc
