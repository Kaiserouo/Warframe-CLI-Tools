import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

import App from "./App";

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App envSetting={{
      'is_github_page': (import.meta.env.VITE_APP_TYPE === 'github'),
    }} />
  </StrictMode>
);