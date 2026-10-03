# 002 · Hallazgo de `braces` en herramientas de compilación

- **Estado:** aceptado
- **Reglas relacionadas:** SEC-020, PRO-005, PRO-006

## Contexto

`npm audit` del frontend reporta 4 hallazgos de severidad alta, todos del mismo origen: `braces` (agotamiento de pila por patrones anidados, GHSA-vfj7-8cjw-p6xm). Llega por `eslint-plugin-boundaries` → `@boundaries/elements` → `micromatch` → `braces`. El aviso cubre todas las versiones publicadas: no existe una versión corregida, así que un `override` no puede resolverlo. La única corrección que ofrece npm es bajar `eslint-plugin-boundaries` de 7.2.0 a 1.1.1, una degradación mayor que descartamos.

Los hallazgos de `js-yaml` que aparecían junto con este se resolvieron con un `override` a 4.3.2 en `frontend/package.json`.

## Decisión

Aceptar el riesgo de `braces` de forma temporal. Es una dependencia de desarrollo que solo procesa los patrones de la configuración de boundaries del propio repositorio, sin entrada de usuarios ni de terceros. `npm audit --omit=dev` (lo que llega a producción) da 0 hallazgos.

## Alternativas

- Degradar `eslint-plugin-boundaries` a 1.1.1: pierde funcionalidad y versiones de ESLint compatibles, para eliminar un riesgo que no afecta a producción.
- Quitar `eslint-plugin-boundaries`: deja sin verificación automática ARQ-006 y ARQ-009.
- Sustituirlo por otra herramienta: es una dependencia fuera de la lista aprobada (PRO-005) y de ARQ-002.

## Consecuencias

- El escaneo de vulnerabilidades del CI (SEC-020, F0-5) fallará con este hallazgo mientras no haya corrección. Cómo tratarlo en el CI es un cambio de infraestructura y requiere aprobación aparte (PRO-006). La excepción del CI debe limitarse al aviso GHSA-vfj7-8cjw-p6xm, sin cubrir ningún otro aviso ni paquete, y referenciar este ADR.
- Revisión activa: se reevalúa en cada actualización periódica de dependencias (OPS-011) y cuando se publique un `braces` corregido o un `micromatch` que no dependa de él. Si hay corrección, se retira la excepción del CI y este ADR se reemplaza por otro que lo referencia.
- Hasta entonces, el aviso queda registrado en `docs/SYSTEM_STATE.md`.

> Un ADR aceptado no se edita: se reemplaza por otro que lo referencia (DOC-002).
