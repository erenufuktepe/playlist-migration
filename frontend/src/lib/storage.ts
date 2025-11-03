const KEY_THEME = "pm_theme";
const KEY_AUTH_PREFIX = "pm_auth_";
const KEY_PENDING_AUTH = "pm_pending_auth";

// NEW: UI state
const KEY_FROM = "pm_from_platform";
const KEY_TO = "pm_to_platform";
const KEY_SRC_PL = "pm_source_playlist_id";
const KEY_DEST_NAME = "pm_dest_name";
const KEY_DEST_DESC = "pm_dest_desc";

export type Theme = "light" | "dark";

export const storage = {
  // theme
  getTheme(): Theme {
    const t = localStorage.getItem(KEY_THEME);
    return t === "light" || t === "dark" ? t : "dark";
  },
  setTheme(t: Theme) {
    localStorage.setItem(KEY_THEME, t);
  },

  // auth
  getAuth(platform: string): boolean {
    return localStorage.getItem(`${KEY_AUTH_PREFIX}${platform}`) === "true";
  },
  setAuth(platform: string, authed: boolean) {
    localStorage.setItem(`${KEY_AUTH_PREFIX}${platform}`, authed ? "true" : "false");
  },

  // pending platform during redirect
  getPendingAuth(): string | null {
    return localStorage.getItem(KEY_PENDING_AUTH);
    },
  setPendingAuth(platform: string | null) {
    if (platform) localStorage.setItem(KEY_PENDING_AUTH, platform);
    else localStorage.removeItem(KEY_PENDING_AUTH);
  },

  // NEW: UI state helpers
  getFrom(): string | "" {
    return localStorage.getItem(KEY_FROM) ?? "";
  },
  setFrom(p: string | "") {
    if (p) localStorage.setItem(KEY_FROM, p);
    else localStorage.removeItem(KEY_FROM);
  },

  getTo(): string | "" {
    return localStorage.getItem(KEY_TO) ?? "";
  },
  setTo(p: string | "") {
    if (p) localStorage.setItem(KEY_TO, p);
    else localStorage.removeItem(KEY_TO);
  },

  getSourcePlaylistId(): string {
    return localStorage.getItem(KEY_SRC_PL) ?? "";
  },
  setSourcePlaylistId(id: string) {
    if (id) localStorage.setItem(KEY_SRC_PL, id);
    else localStorage.removeItem(KEY_SRC_PL);
  },

  getDest(): { name: string; description: string } {
    return {
      name: localStorage.getItem(KEY_DEST_NAME) ?? "",
      description: localStorage.getItem(KEY_DEST_DESC) ?? "",
    };
  },
  setDest(v: { name: string; description: string }) {
    if (v.name) localStorage.setItem(KEY_DEST_NAME, v.name);
    else localStorage.removeItem(KEY_DEST_NAME);
    if (v.description) localStorage.setItem(KEY_DEST_DESC, v.description);
    else localStorage.removeItem(KEY_DEST_DESC);
  },
};
