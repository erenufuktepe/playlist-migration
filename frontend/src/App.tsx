import { useEffect, useMemo, useRef, useState } from "react";
import styles from "./App.module.css";

import ThemeToggle from "./components/ThemeToggle";
import SideBox from "./components/SideBox";
import SelectPlatform from "./components/SelectPlatform";
import AuthButton from "./components/AuthButton";
import PlaylistSelect from "./components/PlaylistSelect";
import DestinationFields from "./components/DestinationFields";

import type { Platform } from "./types";
import { storage } from "./lib/storage";
import { spotifyApi, type Playlist as SpotifyPlaylist } from "./lib/spotify";
import { appleApi, type Playlist as ApplePlaylist } from "./lib/apple";

type AnyTrack = { id: string; name: string; artists: string[] };
type AnyPlaylist = { id: string; name: string; tracks: AnyTrack[] };

export default function App() {
  // ---- Platforms (persisted) ------------------------------------------------
  const [fromPlatform, setFromPlatform] = useState<Platform | "">(
    (storage.getFrom() as Platform | "") || ""
  );
  const [toPlatform, setToPlatform] = useState<Platform | "">(
    (storage.getTo() as Platform | "") || ""
  );

  useEffect(() => storage.setFrom(fromPlatform), [fromPlatform]);
  useEffect(() => storage.setTo(toPlatform), [toPlatform]);

  // mutual exclusion (can’t be the same)
  const fromDisabled = useMemo(() => (toPlatform ? toPlatform : null), [toPlatform]);
  const toDisabled = useMemo(() => (fromPlatform ? fromPlatform : null), [fromPlatform]);

  useEffect(() => {
    if (fromPlatform && toPlatform === fromPlatform) setToPlatform("");
  }, [fromPlatform]);
  useEffect(() => {
    if (toPlatform && fromPlatform === toPlatform) setFromPlatform("");
  }, [toPlatform]);

  // ---- Auth state badges (persisted by AuthButton/useAuth) ------------------
  const fromAuthed = fromPlatform ? storage.getAuth(fromPlatform) : false;
  const toAuthed = toPlatform ? storage.getAuth(toPlatform) : false;

  // ---- Source playlist selection (persisted) --------------------------------
  const [sourcePlaylistId, setSourcePlaylistId] = useState<string>(
    storage.getSourcePlaylistId()
  );
  useEffect(() => storage.setSourcePlaylistId(sourcePlaylistId), [sourcePlaylistId]);

  const [sourcePlaylist, setSourcePlaylist] = useState<AnyPlaylist | null>(null);

  // reset source when platform or auth changes
  useEffect(() => {
    setSourcePlaylistId("");
    storage.setSourcePlaylistId("");
    setSourcePlaylist(null);
  }, [fromPlatform, fromAuthed]);

  // fetch full playlist when an id is chosen
  useEffect(() => {
    let active = true;
    (async () => {
      if (!sourcePlaylistId || !fromPlatform) return;
      try {
        const pl =
          fromPlatform === "spotify"
            ? await spotifyApi.getPlaylist(sourcePlaylistId)
            : await appleApi.getPlaylist(sourcePlaylistId);
        if (active) setSourcePlaylist(pl as unknown as AnyPlaylist);
      } catch {
        if (active) setSourcePlaylist(null);
      }
    })();
    return () => {
      active = false;
    };
  }, [sourcePlaylistId, fromPlatform]);

  // ---- Destination inputs (controlled + persisted) --------------------------
  const [dest, setDest] = useState<{ name: string; description: string }>(
    storage.getDest()
  );
  useEffect(() => storage.setDest(dest), [dest]);

  // auto defaults derived from the selected source playlist
  const autoName = sourcePlaylist ? `Migrated — ${sourcePlaylist.name}` : "";
  const autoDesc = ""; // pass source description if your backend returns it
  const lastAutoNameRef = useRef<string>(autoName);
  const lastAutoDescRef = useRef<string>(autoDesc);

  // When source changes, update destination only if user hasn't customized
  useEffect(() => {
    const userKeptName =
      dest.name === lastAutoNameRef.current || dest.name === "" || dest.name === "Migrated — ";
    const userKeptDesc = dest.description === lastAutoDescRef.current;

    const next = {
      name: userKeptName ? autoName : dest.name,
      description: userKeptDesc ? autoDesc : dest.description,
    };

    setDest(next);
    storage.setDest(next);

    lastAutoNameRef.current = autoName;
    lastAutoDescRef.current = autoDesc;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourcePlaylist?.id]);

  // also keep whatever user had typed when changing destination platform
  useEffect(() => {
    setDest(storage.getDest());
  }, [toPlatform]);

  // ---- Migration ------------------------------------------------------------
  const [migrating, setMigrating] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const canMigrate =
    !!fromPlatform &&
    !!toPlatform &&
    fromPlatform !== toPlatform &&
    fromAuthed &&
    toAuthed &&
    !!sourcePlaylist &&
    !!dest.name &&
    !migrating;

  async function handleMigrate() {
    if (!canMigrate || !sourcePlaylist) return;
    setMigrating(true);
    setMessage(null);
    try {
      let newId = "";
      if (toPlatform === "spotify") {
        newId = await spotifyApi.createPlaylist({
          name: dest.name,
          description: dest.description,
          public: true,
        });
        await spotifyApi.addTracks(
          newId,
          sourcePlaylist.tracks.map((t) => t.id)
        );
      } else {
        // Apple branch (enable when your Apple backend routes are ready)
        newId = await appleApi.createPlaylist({
          name: dest.name,
          description: dest.description,
        });
        await appleApi.addTracks(
          newId,
          sourcePlaylist.tracks.map((t) => t.id)
        );
      }
      setMessage(`✅ Migrated ${sourcePlaylist.tracks.length} tracks to playlist ${newId}.`);
    } catch (e: any) {
      setMessage(e?.message ?? "Migration failed.");
    } finally {
      setMigrating(false);
    }
  }

  // ---- Render ---------------------------------------------------------------
  return (
    <div className={styles.wrap}>
      <div className={styles.top}>
        <h1 style={{ margin: 0 }}>Playlist Migration</h1>
        <ThemeToggle />
      </div>

      <div className={styles.grid}>
        {/* LEFT: migrate FROM */}
        <SideBox title="Migrate From" right={fromPlatform && fromAuthed ? <span>✅</span> : null}>
          <SelectPlatform
            label="Source platform"
            value={fromPlatform}
            disabledOption={fromDisabled as Platform | null}
            onChange={setFromPlatform}
          />
          {fromPlatform && <AuthButton platform={fromPlatform as Platform} />}

          {fromPlatform && fromAuthed && (
            <PlaylistSelect
              platform={fromPlatform as Platform}
              enabled={true}
              value={sourcePlaylistId}
              onPick={setSourcePlaylistId}
            />
          )}
        </SideBox>

        {/* RIGHT: migrate TO */}
        <SideBox title="Migrate To" right={toPlatform && toAuthed ? <span>✅</span> : null}>
          <SelectPlatform
            label="Destination platform"
            value={toPlatform}
            disabledOption={toDisabled as Platform | null}
            onChange={setToPlatform}
          />
          {toPlatform && <AuthButton platform={toPlatform as Platform} />}

          {/* Show destination inputs as soon as a destination platform is chosen */}
          {toPlatform && (
            <DestinationFields value={dest} onChange={setDest} />
          )}

          {!toAuthed && toPlatform && (
            <div style={{ marginTop: 8, color: "var(--muted)" }}>
              You must authenticate {toPlatform === "spotify" ? "Spotify" : "Apple Music"} to migrate.
            </div>
          )}
        </SideBox>
      </div>

      <div className={styles.migrateBar}>
        <button className={styles.migrateBtn} disabled={!canMigrate} onClick={handleMigrate}>
          {migrating ? "Migrating…" : "Migrate"}
        </button>
      </div>

      {message && (
        <div
          style={{
            marginTop: 12,
            textAlign: "center",
            color: message.startsWith("✅") ? "var(--ok)" : "var(--error)",
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
}
