import { API_BASE, http } from "./api";

export type AppleUser = { id: string; name?: string };
export type SimplePlaylist = { id: string; name: string };
export type Playlist = { id: string; name: string; tracks: { id: string; name: string; artists: string[] }[] };

export const appleApi = {
  getAuthorizationUrl: async () => {
    const res = await fetch(`${API_BASE}/apple/authorization-url`);
    if (!res.ok) throw new Error(await res.text());
    return (await res.json()) as { authorization_url: string };
  },
  me: () => http<AppleUser>("/apple/me"),

  // Stubs — wire these when your Apple routes are available
  listPlaylists: () => http<SimplePlaylist[]>("/apple/playlists"),
  getPlaylist: (id: string) => http<Playlist>(`/apple/playlist/${encodeURIComponent(id)}`),
  createPlaylist: (payload: { name: string; description?: string }) =>
    http<string>("/apple/create-playlist", {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" },
    }),
  addTracks: (playlistId: string, trackIdsOrUris: string[]) =>
    http<void>(`/apple/playlist/${encodeURIComponent(playlistId)}/add-tracks`, {
      method: "POST",
      body: JSON.stringify(trackIdsOrUris),
      headers: { "Content-Type": "application/json" },
    }),
};
