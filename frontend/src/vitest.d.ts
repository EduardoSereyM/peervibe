import "vitest";
import type { AxeMatchers } from "vitest-axe/matchers";

declare module "vitest" {
  // Matchers de accesibilidad registrados en test-setup.ts (UI-009).
  interface Assertion<T = unknown> extends AxeMatchers {
    _axeBrand?: T;
  }
  interface AsymmetricMatchersContaining extends AxeMatchers {
    _axeBrand?: never;
  }
}
