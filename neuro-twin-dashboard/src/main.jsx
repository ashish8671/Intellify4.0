import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";
import { DetectionProvider } from "./context/DetectionContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <DetectionProvider>
      <App />
    </DetectionProvider>
  </StrictMode>
);