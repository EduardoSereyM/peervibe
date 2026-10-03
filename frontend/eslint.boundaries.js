import boundaries from "eslint-plugin-boundaries";

// Archivo único de composición: el único de core que puede importar el index de los módulos.
export const COMPOSITION_FILE = "src/core/routes.tsx";

const BASE_TYPES = ["core", "shared", "generated"];

// ARQ-006 y ARQ-009. Se prueba en tooling/boundaries.test.ts, que exige que las violaciones fallen.
export const boundariesConfig = {
  plugins: { boundaries },
  settings: {
    // El resolver por defecto solo prueba extensiones .js: sin esto los imports .ts/.tsx no se
    // resuelven y la regla no detecta ninguna violación.
    "import/resolver": { node: { extensions: [".ts", ".tsx", ".js", ".jsx"] } },
    "boundaries/elements": [
      { type: "core", pattern: "src/core" },
      { type: "shared", pattern: "src/shared" },
      { type: "generated", pattern: "src/generated" },
      { type: "module", pattern: "src/modules/*", capture: ["moduleName"] },
    ],
  },
  rules: {
    "boundaries/dependencies": [
      2,
      {
        default: "disallow",
        policies: [
          { allow: { to: { module: { origin: "external" } } } },
          {
            from: { element: { type: "core" } },
            allow: { to: { element: { types: { anyOf: ["core", "generated"] } } } },
          },
          {
            from: { file: { path: COMPOSITION_FILE } },
            allow: { to: { element: { type: "module", fileInternalPath: "index.ts" } } },
          },
          {
            from: { element: { type: "shared" } },
            allow: { to: { element: { types: { anyOf: ["core", "shared", "generated"] } } } },
          },
          {
            from: { element: { type: "module" } },
            allow: [
              { to: { element: { types: { anyOf: BASE_TYPES } } } },
              { dependency: { relationship: { to: "internal" } } },
            ],
          },
        ],
      },
    ],
  },
};
