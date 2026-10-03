import { boundariesConfig } from "./eslint.boundaries.js";
import tseslint from "typescript-eslint";

const MAX_COMPLEXITY = 10;
const MAX_DEPTH = 4;
const MAX_LINES_PER_FUNCTION = 60;

export default tseslint.config(
  { ignores: ["dist", "coverage", "src/generated", "node_modules"] },
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      // QA-013: complejidad acotada.
      complexity: ["error", MAX_COMPLEXITY],
      "max-depth": ["error", MAX_DEPTH],
      "max-lines-per-function": ["error", { max: MAX_LINES_PER_FUNCTION, skipComments: true }],
      // QA-014: sin marcadores de pendiente sin tarea ni tipos "any" para callar al compilador.
      "no-warning-comments": ["error", { terms: ["todo", "fixme", "xxx"], location: "anywhere" }],
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/ban-ts-comment": "error",
      "@typescript-eslint/no-non-null-assertion": "error",
      // SEC-011: nada de código construido dinámicamente.
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
    },
  },
  boundariesConfig,
  {
    files: ["*.js", "*.ts"],
    ...tseslint.configs.disableTypeChecked,
  },
);
