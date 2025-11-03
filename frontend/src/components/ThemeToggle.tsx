import { useEffect, useState } from "react";
import styles from "./ThemeToggle.module.css";
import { storage, type Theme } from "../lib/storage";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => storage.getTheme());

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "light") {
      root.classList.add("theme-light");
    } else {
      root.classList.remove("theme-light");
    }
    storage.setTheme(theme);
  }, [theme]);

  return (
    <div className={styles.wrap}>
      <button
        className={styles.btn}
        onClick={() => setTheme(theme === "light" ? "dark" : "light")}
        aria-label="Toggle theme"
      >
        {theme === "light" ? "🌙 Dark" : "☀️ Light"}
      </button>
    </div>
  );
}
