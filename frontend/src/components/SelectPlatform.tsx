import styles from "./SelectPlatform.module.css";
import { PLATFORMS, type Platform } from "../types";

type Props = {
  label: string;
  value: Platform | "";
  disabledOption?: Platform | null; // if set, disallow selecting the same
  onChange: (p: Platform | "") => void;
};

export default function SelectPlatform({ label, value, disabledOption, onChange }: Props) {
  return (
    <div className={styles.field}>
      <label className={styles.label}>{label}</label>
      <select
        className={styles.select}
        value={value}
        onChange={(e) => onChange((e.target.value || "") as Platform | "")}
      >
        <option value="">Select...</option>
        {PLATFORMS.map((p) => (
          <option key={p.id} value={p.id} disabled={disabledOption === p.id}>
            {p.label}
          </option>
        ))}
      </select>
    </div>
  );
}
