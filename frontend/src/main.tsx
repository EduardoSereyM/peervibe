import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

const rootElement = document.getElementById("root");
if (rootElement === null) {
  throw new Error("No se encontró el elemento #root");
}

createRoot(rootElement).render(
  <StrictMode>
    <main className="p-4">
      <h1 className="text-texto">peervibe</h1>
    </main>
  </StrictMode>,
);
