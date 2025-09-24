from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routes.routes_spotify import router as spotify_router


app = FastAPI(title="Playlist Migration API")


app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify_router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
