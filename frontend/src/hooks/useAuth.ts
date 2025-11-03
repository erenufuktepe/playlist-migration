import { useCallback, useEffect, useState } from "react";
import { storage } from "../lib/storage";
import { spotifyApi } from "../lib/spotify";
import { appleApi } from "../lib/apple";
import type { Platform } from "../types";

type Options = {
  platform: Platform;
};

export function useAuth({ platform }: Options) {
  const [authed, setAuthed] = useState<boolean>(() => storage.getAuth(platform));
  const [loading, setLoading] = useState(false);

  // detect redirect success: ?auth=success
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const auth = params.get("auth");
    const pending = storage.getPendingAuth();

    if (auth === "success" && pending === platform) {
      setAuthed(true);
      storage.setAuth(platform, true);
      storage.setPendingAuth(null);

      // clean URL params
      const url = new URL(window.location.href);
      url.searchParams.delete("auth");
      window.history.replaceState({}, "", url.toString());
    }
  }, [platform]);

  // on mount, try to confirm auth via /me (if available)
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        if (!authed) return;
        setLoading(true);
        if (platform === "spotify") {
          await spotifyApi.me();
        } else if (platform === "apple") {
          await appleApi.me();
        }
        // ok
      } catch {
        // token invalid/expired → clear
        if (active) {
          setAuthed(false);
          storage.setAuth(platform, false);
        }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [platform]);

  const beginAuth = useCallback(async () => {
    setLoading(true);
    try {
      storage.setPendingAuth(platform);
      const url =
        platform === "spotify"
          ? (await spotifyApi.getAuthorizationUrl()).authorization_url
          : (await appleApi.getAuthorizationUrl()).authorization_url;
      window.location.href = url; // redirect
    } catch (e) {
      storage.setPendingAuth(null);
      setLoading(false);
      throw e;
    }
  }, [platform]);

  const clearAuth = useCallback(() => {
    setAuthed(false);
    storage.setAuth(platform, false);
  }, [platform]);

  return { authed, loading, beginAuth, clearAuth };
}
