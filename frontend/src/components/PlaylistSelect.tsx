import { useEffect, useState } from "react";
import styles from "./PlaylistSelect.module.css";
import type { Platform } from "../types";
import { spotifyApi, type SimplePlaylist as SpotifySimple } from "../lib/spotify";
import { appleApi, type SimplePlaylist as AppleSimple } from "../lib/apple";

type Props = {
  platform: Platform;
  enabled: boolean;                // only true when authenticated
  onPick: (id: string) => void;    // return selected playlist id
};

export default function PlaylistSelect({ platform, enabled, onPick }: Props) {
  const [list, setList] = useState<{ id: string; name: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [value, setValue] = useState("");

  useEffect(() => {
    let active = true;
    (async () => {
      if (!enabled) {
        setList([]);
        setValue("");
        return;
      }
      setLoading(true);
      try {
        const data =
          platform === "spotify"
            ? await spotifyApi.listPlaylists()
            : await appleApi.listPlaylists();

        if (!active) return;
        setList(data);
      } catch {
        if (active) setList([]);
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [platform, enabled]);

  useEffect(() => {
    if (value) onPick(value);
  }, [value]);

  return (
    <div className={styles.field}>
      <label className={styles.label}>Playlist</label>
      <div className={styles.row}>
        <select
          className={styles.select}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={!enabled || loading || list.length === 0}
        >
          <option value="">{loading ? "Loading…" : "Select a playlist…"}</option>
          {list.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        {!enabled && <span className={styles.muted}>Authenticate to load playlists</span>}
      </div>
    </div>
  );
}
