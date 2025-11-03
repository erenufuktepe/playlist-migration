import styles from "./SideBox.module.css";
import { ReactNode } from "react";

export default function SideBox({
  title,
  right,
  children,
}: {
  title: string;
  right?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h3 className={styles.title}>{title}</h3>
        {right}
      </div>
      <div className={styles.body}>{children}</div>
    </div>
  );
}
