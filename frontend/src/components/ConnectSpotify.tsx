import { useEffect, useMemo, useState } from "react";
import { spotify } from "../lib/spotify";
import styles from "./ConnectSpotify.module.css"; 

function useSpotifyAuth() {
  const [isAuthed, setAuthed] = useState(false);
  const authParam = useMemo(() => new URLSearchParams(window.location.search).get("auth"), []);

  useEffect(() => {
    if (authParam === "success") {
      setAuthed(true);
      const url = new URL(window.location.href);
      url.searchParams.delete("auth");
      window.history.replaceState({}, "", url.toString());
    }
  }, [authParam]);

  const connect = async () => {
    const { authorization_url } = await spotify.getAuthorizationUrl();
    console.log("Redirecting to Spotify authorization URL:", authorization_url);
    window.location.href = authorization_url;
  };

  return { isAuthed, connect };
}

export default function ConnectSpotify() {
  const { isAuthed, connect } = useSpotifyAuth();

  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <h3 className={styles.title}>1) Connect Spotify</h3>
        <p className={styles.muted}>Authorize the app to read your playlists and create one for you.</p>
      </div>
      <div className={styles.cardBody}>
        {isAuthed ? (
          <div className={styles.ok}>Connected ✔</div>
        ) : (
          <button className={styles.btn} onClick={connect}>Connect Spotify</button>
        )}
      </div>
    </div>
  );
}
