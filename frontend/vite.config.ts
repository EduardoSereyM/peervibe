import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

const COVERAGE_MIN = 80;

export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-setup.ts"],
    include: ["src/**/*.test.{ts,tsx}", "tooling/**/*.test.ts"],
    // process.chdir (tooling/boundaries.test.ts) no está disponible en hilos.
    pool: "forks",
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/generated/**", "src/**/*.test.{ts,tsx}", "src/test-setup.ts", "src/main.tsx"],
      thresholds: {
        lines: COVERAGE_MIN,
        statements: COVERAGE_MIN,
        functions: COVERAGE_MIN,
        branches: COVERAGE_MIN,
      },
    },
  },
});
