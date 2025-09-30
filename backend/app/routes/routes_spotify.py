from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from app.services.spotify_service import get_spotify_service, SpotifyService, NotFoundError, SpotifyServiceError

router = APIRouter(prefix="/spotify", tags=["spotify"])

@router.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str, svc: SpotifyService = Depends(get_spotify_service)):
    try:
        return await svc.get_playlist(playlist_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Playlist not found")
    except SpotifyServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")