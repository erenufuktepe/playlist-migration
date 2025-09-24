import { useEffect, useState } from 'react';

type Provider = 'spotify' | 'apple';

export default function App() {
  // Theme
  const [dark, setDark] = useState(true);
  useEffect(() => {
    const saved = localStorage.getItem('theme');
    const isDark = saved ? saved === 'dark' : true;
    setDark(isDark);
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  }, []);
  const toggleTheme = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.setAttribute('data-theme', next ? 'dark' : 'light');
    localStorage.setItem('theme', next ? 'dark' : 'light');
  };

  // Providers (keep sides mutually exclusive)
  const [left, setLeft] = useState<Provider>('spotify');
  const [right, setRight] = useState<Provider>('apple');

  useEffect(() => {
    if (left === right) setRight(left === 'spotify' ? 'apple' : 'spotify');
  }, [left]);
  useEffect(() => {
    if (right === left) setLeft(right === 'spotify' ? 'apple' : 'spotify');
  }, [right]);

  return (
    <>
      {/* Top nav */}
      <nav className="nav">
        <div className="container nav-inner">
          <span className="brand">Playlist Migration</span>
          <button className="toggle" onClick={toggleTheme} aria-label="Toggle dark mode">
            {dark ? 'Light' : 'Dark'}
          </button>
        </div>
      </nav>

      {/* Main content */}
      <main className="container main">
        <div className="grid">
          {/* From */}
          <section className="panel" aria-labelledby="from-title">
            <div className="panel-head">
              <div>
                <h2 id="from-title" className="h2">From</h2>
                <p className="sub">Select the source application</p>
              </div>
              <ProviderSelect value={left} onChange={setLeft} />
            </div>

            <div className="placeholder">
              {left === 'spotify'
                ? 'Spotify source area (auth state, playlist picker, etc.)'
                : 'Apple Music source area (auth state, playlist picker, etc.)'}
            </div>
          </section>

          {/* To */}
          <section className="panel" aria-labelledby="to-title">
            <div className="panel-head">
              <div>
                <h2 id="to-title" className="h2">To</h2>
                <p className="sub">Select the destination application</p>
              </div>
              <ProviderSelect value={right} onChange={setRight} />
            </div>

            <div className="placeholder">
              {right === 'spotify'
                ? 'Spotify destination area (create playlist, options, etc.)'
                : 'Apple Music destination area (create playlist, options, etc.)'}
            </div>
          </section>
        </div>
      </main>
    </>
  );
}

function ProviderSelect({
  value,
  onChange,
}: {
  value: Provider;
  onChange: (p: Provider) => void;
}) {
  return (
    <label className="select" aria-label="Select provider">
      <select
        className="select-el"
        value={value}
        onChange={(e) => onChange(e.target.value as Provider)}
      >
        <option value="spotify">Spotify</option>
        <option value="apple">Apple Music</option>
      </select>
    </label>
  );
}
