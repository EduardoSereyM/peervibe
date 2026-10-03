import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { ESLint } from "eslint";
import tseslint from "typescript-eslint";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { boundariesConfig, COMPOSITION_FILE } from "../eslint.boundaries.js";

// B.1: si una actualización del plugin vuelve no-ops las reglas, las violaciones dejan de fallar
// y este test lo detecta. Cada caso escribe una mini copia de `src/` y la lintea con la config real.
const RULE_ID = "boundaries/dependencies";

type Files = Record<string, string>;

const BASE: Files = {
  "src/core/util.ts": "export const c = 1;",
  "src/shared/util.ts": "export const s = 1;",
  "src/shared/otro.ts": "export const o = 1;",
  "src/modules/a/index.ts": "export const a = 1;",
  "src/modules/a/interno.ts": "export const interno = 1;",
  "src/modules/b/index.ts": "export const b = 1;",
};

const VIOLACIONES: [string, string, string][] = [
  ["un módulo importa de otro módulo", "src/modules/b/cruce.ts", 'import { a } from "../a/index"; export const x = a;'],
  ["se importa un archivo interno de un módulo desde fuera", COMPOSITION_FILE, 'import { interno } from "../modules/a/interno"; export const x = interno;'],
  ["core importa de shared", "src/core/hacia_shared.ts", 'import { s } from "../shared/util"; export const x = s;'],
  ["un archivo de core que no es el de composición importa el index de un módulo", "src/core/otro_archivo.ts", 'import { a } from "../modules/a"; export const x = a;'],
  ["shared importa de un módulo", "src/shared/hacia_modulo.ts", 'import { a } from "../modules/a"; export const x = a;'],
];

const PERMITIDOS: [string, string, string][] = [
  ["un módulo importa de core y de shared", "src/modules/a/ok.ts", 'import { c } from "../../core/util"; import { s } from "../../shared/util"; export const x = c + s;'],
  ["un módulo importa un archivo interno propio", "src/modules/a/ok_interno.ts", 'import { interno } from "./interno"; export const x = interno;'],
  ["shared importa otro archivo de shared", "src/shared/ok.ts", 'import { o } from "./otro"; export const x = o;'],
  ["core importa otro archivo de core", "src/core/ok.ts", 'import { c } from "./util"; export const x = c;'],
  ["el archivo de composición importa el index de un módulo", COMPOSITION_FILE, 'import { a } from "../modules/a"; export const x = a;'],
];

let raiz = "";
const cwdOriginal = process.cwd();

beforeAll(() => {
  raiz = mkdtempSync(join(tmpdir(), "boundaries-"));
  process.chdir(raiz);
});

afterAll(() => {
  process.chdir(cwdOriginal);
  rmSync(raiz, { recursive: true, force: true });
});

async function erroresDeBoundaries(archivo: string, contenido: string): Promise<string[]> {
  const files: Files = { ...BASE, [archivo]: contenido };
  for (const [ruta, texto] of Object.entries(files)) {
    mkdirSync(dirname(join(raiz, ruta)), { recursive: true });
    writeFileSync(join(raiz, ruta), texto);
  }
  const eslint = new ESLint({
    cwd: raiz,
    overrideConfigFile: true,
    overrideConfig: [
      { files: ["**/*.ts", "**/*.tsx"], languageOptions: { parser: tseslint.parser } },
      boundariesConfig,
    ],
  });
  const resultados = await eslint.lintFiles([archivo]);
  return resultados
    .flatMap((r) => r.messages)
    .filter((m) => m.ruleId === RULE_ID)
    .map((m) => m.message);
}

describe("boundaries (ARQ-006, ARQ-009)", () => {
  it.each(VIOLACIONES)("rechaza: %s", async (_caso, archivo, contenido) => {
    const errores = await erroresDeBoundaries(archivo, contenido);
    expect(errores.length).toBeGreaterThan(0);
  });

  it.each(PERMITIDOS)("permite: %s", async (_caso, archivo, contenido) => {
    const errores = await erroresDeBoundaries(archivo, contenido);
    expect(errores).toEqual([]);
  });
});
