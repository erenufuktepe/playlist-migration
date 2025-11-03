import { API_BASE, http } from "./api";

export type SpotifyUser = { id: string; display_name?: string };
export type SimplePlaylist = { id: string; name: string };
export type PlaylistTrack = { id: string; name: string; artists: string[] };
export type Playlist = { id: string; name: string; tracks: PlaylistTrack[] };

export const spotifyApi = {
  getAuthorizationUrl: async () => {
    const res = await fetch(`${API_BASE}/spotify/authorization-url`);
    if (!res.ok) throw new Error(await res.text());
    return (await res.json()) as { authorization_url: string };
  },
  me: () => http<SpotifyUser>("/spotify/me"),

  // ⬇️ Add these
  listPlaylists: () => http<SimplePlaylist[]>("/spotify/playlists"),
  getPlaylist: (id: string) => http<Playlist>(`/spotify/playlist/${encodeURIComponent(id)}`),
  createPlaylist: (payload: { name: string; description?: string; public?: boolean }) =>
    http<string>("/spotify/create-playlist", {
      method: "POST",
      body: JSON.stringify({ public: true, description: "", ...payload }),
      headers: { "Content-Type": "application/json" },
    }),
  addTracks: (playlistId: string, trackIdsOrUris: string[]) =>
    http<void>(`/spotify/playlist/${encodeURIComponent(playlistId)}/add-tracks`, {
      method: "POST",
      body: JSON.stringify(trackIdsOrUris),
      headers: { "Content-Type": "application/json" },
    }),
};
