import styles from "./AuthButton.module.css";
import { useAuth } from "../hooks/useAuth";
import type { Platform } from "../types";

export default function AuthButton({ platform }: { platform: Platform }) {
  const { authed, loading, beginAuth, clearAuth } = useAuth({ platform });

  return (
    <div className={styles.row}>
      <button className={styles.btn} onClick={() => (authed ? clearAuth() : beginAuth())} disabled={loading}>
        {loading ? "Connecting…" : authed ? "Disconnect" : `Connect ${platform === "spotify" ? "Spotify" : "Apple"}`}
      </button>
      <span className={`${styles.badge} ${authed ? styles.ok : styles.warn}`}>
        {authed ? "Authenticated" : "Not authenticated"}
      </span>
    </div>
  );
}
