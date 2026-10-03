import { defineConfig, devices } from "@playwright/test";

const MOBILE_WIDTH = 360;
const MOBILE_HEIGHT = 740;
const DEV_SERVER_URL = "http://localhost:5173";

// QA-006 y UI-003: E2E en viewport móvil (360 px) y de escritorio.
export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: DEV_SERVER_URL },
  projects: [
    {
      name: "movil",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: MOBILE_WIDTH, height: MOBILE_HEIGHT },
        // UI-004: emula un teléfono real, con interacción táctil.
        isMobile: true,
        hasTouch: true,
      },
    },
    { name: "escritorio", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: { command: "npm run dev", url: DEV_SERVER_URL, reuseExistingServer: true },
});
