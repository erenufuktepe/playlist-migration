from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from app.services.spotify_service import SpotifyService, NotFoundError, SpotifyServiceError
from app.client.spotify_client import get_spotify_client

router = APIRouter(prefix="/spotify", tags=["spotify"])

spotify_service = SpotifyService(get_spotify_client())

def get_spotify_service() -> SpotifyService:
    return spotify_service

@router.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str, service: SpotifyService = Depends(get_spotify_service)):
    try:
        return await service.get_playlist(playlist_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Playlist not found")
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")