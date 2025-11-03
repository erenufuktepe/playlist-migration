// src/components/DestinationFields.tsx
import styles from "./DestinationFields.module.css";

export default function DestinationFields({
  value,
  onChange,
}: {
  value: { name: string; description: string };
  onChange: (v: { name: string; description: string }) => void;
}) {
  const { name, description } = value;

  return (
    <div className={styles.group}>
      <div className={styles.row}>
        <label>Destination name</label>
        <span className={styles.muted}>{name.length}/100</span>
      </div>
      <input
        className={styles.input}
        maxLength={100}
        value={name}
        onChange={(e) => onChange({ name: e.target.value, description })}
        placeholder="Playlist name"
      />
      <label>Description (optional)</label>
      <textarea
        className={styles.textarea}
        value={description}
        onChange={(e) => onChange({ name, description: e.target.value })}
        placeholder="Describe your playlist"
      />
    </div>
  );
}
