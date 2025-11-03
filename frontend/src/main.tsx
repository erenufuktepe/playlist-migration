import App from './App.tsx'
import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/theme.css";
import "./styles/index.css";
import { storage } from "./lib/storage";

const root = document.documentElement;
const theme = storage.getTheme();
if (theme === "light") root.classList.add("theme-light");

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
