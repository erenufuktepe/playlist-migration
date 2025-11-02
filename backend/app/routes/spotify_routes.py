from app.client.spotify_client import get_spotify_client
from app.core.config import settings
from app.schemas.playlist import PlaylistCreateRequest
from app.services.spotify_service import SpotifyService, SpotifyServiceError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/spotify", tags=["spotify"])

spotify_service = SpotifyService(get_spotify_client())


def get_spotify_service() -> SpotifyService:
    return spotify_service


@router.get("/playlist/{playlist_id}")
async def get_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    try:
        return await service.get_playlist(playlist_id)
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")


@router.get("/authorization-url")
async def get_authorization_url(service: SpotifyService = Depends(get_spotify_service)):
    try:
        return await service.get_authorization_url()
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")


@router.get("/callback")
async def spotify_callback(
    request: Request, service: SpotifyService = Depends(get_spotify_service)
):
    try:
        await service.authorize_user(request)
        return RedirectResponse(f"{settings.FRONTEND_HOST}?auth=success")
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")


@router.post("/create-playlist", status_code=201)
async def create_playlist(
    request: PlaylistCreateRequest,
    service: SpotifyService = Depends(get_spotify_service),
):
    try:
        return await service.create_playlist(request)
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")


@router.get("/search-track")
async def search_track(
    artist: str, track: str, service: SpotifyService = Depends(get_spotify_service)
):
    try:
        return await service.search_track(artist, track)
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")


@router.post("/playlist/{playlist_id}/add-tracks", status_code=204)
async def add_tracks_to_playlist(
    playlist_id: str,
    track_uris: list[str],
    service: SpotifyService = Depends(get_spotify_service),
):
    try:
        await service.add_tracks_to_playlist(playlist_id, track_uris)
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")
