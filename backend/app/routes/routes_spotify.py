from fastapi import APIRouter
from app.client.spotify import spotify_client

router = APIRouter(prefix="/spotify", tags=["spotify"])

@router.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str):
    playlist = await spotify_client.get_playlist(playlist_id)
    return playlist
