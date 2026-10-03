# Estado del sistema — peervibe

Describe el sistema actual, no historial ni planes (DOC-001).

## Resumen

peervibe es una plataforma de referencia y calificación de productos con reseñas verificadas. Qué se construye: `docs/playbook-producto.md`. Cómo: `ENGINEERING_STANDARDS.md`. Qué exige la ley: `docs/playbook-privacidad.md`.

## Fase actual

Fase 0 de arranque, en la rama `chore/fase-0-arranque`. F0-1 (preguntas), F0-2 (perfil) y F0-3 (estructura y documentos base) están completas. F0-4 (scaffolding, esqueletos de módulos y migración inicial) va en 6 de 12 commits:

1. Proyecto Supabase local (`supabase/`), con TOTP, confirmación de correo, contraseña de al menos 12 caracteres y GRANTs explícitos.
2. Runtimes fijados: Python 3.14 y Node 24.
3. Manifiestos y lockfile con hashes del backend, con la configuración de pytest, mypy, ruff, vulture e import-linter.
4. Frontend (`frontend/`): Vite, React, Tailwind con tokens neutros, ESLint con boundaries y su test permanente, Vitest, Playwright y knip.
5. Núcleo del backend (`backend/app/core/` y `shared/`): configuración tipada (ARQ-016) con verificación de producción (SEC-019), sesión que opera como el usuario y modo anónimo (DB-012, DB-014, B.7), envelope de errores y `trace_id` (API-005), `/health` (OPS-004) y `create_app` sin documentación interactiva ni OpenAPI público. Sus tests, incluidos los de integración contra Supabase local, y los paquetes vacíos de `app/modules/` con un `service.py` vacío por módulo.
6. Esqueletos de los módulos base (`backend/app/modules/{auth,users,settings,admin,logs}/`): las capas de ARQ-008 sin lógica y un `APIRouter` vacío por módulo, registrado en `create_app` bajo `/api/v1` (API-001). `tests/test_estructura.py` comprueba por AST las capas, el registro de los routers y que ningún `service.py` importa la sesión de base de datos.

Aún no hay módulos con lógica, esquema de base de datos ni CI. Excepciones vigentes: `docs/ADR/002-braces-herramientas-de-compilacion.md` (aviso de `braces`) y la excepción temporal de knip (QA-015) en `frontend/knip.jsonc`, que se vacía al usarse cada dependencia.

Próxima tarea: commit 6 de F0-4, el árbol del frontend (`core/`, `shared/` y los esqueletos de los módulos base con su `index.ts`, providers, router y cliente generado vacío). Después, los commits 7 a 10 acordados; el caso de lectura del modo anónimo (DB-014) va en el commit 9, tras las migraciones.

Pendientes conocidos, fuera de 5a y 5b:

- Verificación de JWT y dependencia de usuario actual (SEC-001).
- CORS (SEC-012).
- Rate limit (SEC-018).
- Propagación del `trace_id` a los logs (API-013).
- Logs estructurados (OPS-005).

## Perfil

Ver `docs/PROJECT_PROFILE.yaml`: datos personales, IA solo para resumen de reseñas, uploads, staging, sin RUT, sin webhooks, sin módulos ni perfiles opcionales. Nivel de riesgo de privacidad: N2.

## Roles (SEC-004)

| Rol | Descripción |
|---|---|
| `user` | Usuario registrado; se asigna al registrarse. |
| `moderador` | Modera reseñas y comprobantes. |
| `admin` | Administra roles y la plataforma. |

## Módulos

Ninguno con lógica aún. Los módulos base (ARQ-018: `auth`, `users`, `settings`, `admin` y `logs`) existen como esqueletos del backend: `router.py` (un `APIRouter` vacío, registrado en `create_app` bajo `/api/v1`), `schemas.py`, `service.py`, `repository.py`, `models.py` y `dependencies.py` (ARQ-008), sin lógica ni endpoints. Los módulos de dominio y la contraparte del frontend se crean después.

## Proveedores

| Servicio | Proveedor |
|---|---|
| Base de datos, autenticación y almacenamiento | Supabase |
| Hosting del frontend | Vercel |
| Hosting del backend | Render |
| Inicio de sesión | Google, Apple |
| Correo transaccional y de novedades | TBD |
| IA (síntesis de reseñas) | TBD |
| Registro de errores | TBD |
| Analítica | TBD |

Región y base de la transferencia de cada uno: `docs/PRIVACY_POLICY_NOTES.md`.

## Decisiones pendientes

- Categoría semilla y las 3 variables de calificación (playbook de producto, próximos pasos 1 y 2).
- Árbol de categorías y subcategorías (próximo paso 4).
- SEO de las fichas: SPA con Open Graph (ARQ-014) o SSR/prerenderizado con ADR (próximo paso 5).
- Colores de marca: tokens neutros provisionales (`docs/ADR/001-tokens-neutros-provisionales.md`).
- Si editar una reseña aprobada la devuelve a `pending`.
- Ítems `[validar]` del RAT: ver `docs/PRIVACY_POLICY_NOTES.md`.

## Mejoras propuestas a los documentos maestros

Los documentos maestros (`ENGINEERING_STANDARDS.md` y `docs/playbook-privacidad.md`) no se editan desde este proyecto. Cuando se detecta una mejora o un error, se anota aquí con el ID de la regla y el motivo; el propietario decide el cambio en la copia maestra.

| ID de regla | Documento | Mejora o error | Motivo |
|---|---|---|---|
| F0-3, PRIV-006, DB-019, B.3 | `ENGINEERING_STANDARDS.md` | Aclarar dónde vive el inventario de datos. | F0-3 lo lista como documento aparte y el árbol canónico no lo muestra; PRIV-006 y B.3 lo ubican dentro de `PRIVACY_POLICY_NOTES.md`. Aquí queda un encabezado en `SCHEMA_MAP.md` y otro en `PRIVACY_POLICY_NOTES.md` hasta que se decida. |
| ARQ-001, Anexo C.2 | `ENGINEERING_STANDARDS.md` | Revisar si el router del frontend debe ser TanStack Router o react-router. | El stack de oro ya usa TanStack Query y C.2 lista react-router. Se mantiene react-router por C.2; el propietario decide si conviene unificar con TanStack Router. |
| Anexo C.2, B.4, ARQ-006, ARQ-009 | `ENGINEERING_STANDARDS.md` | Indicar que `eslint-plugin-boundaries` con TypeScript exige configurar `"import/resolver"` con extensiones TypeScript (`.ts`, `.tsx`), sin instalar dependencias nuevas. Además, la v7 deprecó las reglas clásicas (`element-types`, `entry-point`, `external`), que sin opciones son no-ops: la regla vigente es `boundaries/dependencies`. | El resolver por defecto solo prueba extensiones `.js`: sin ese ajuste, los destinos de los imports quedan como elemento desconocido y la regla no detecta ninguna violación, aunque ESLint termine en verde. B.4 y las reglas LINT de ARQ-006 y ARQ-009 deberían nombrar la regla vigente y exigir un test que pruebe que las violaciones se detectan. |
| DB-014, Anexo B.7 | `ENGINEERING_STANDARDS.md` | Precisar cuándo se prueba el modo anónimo del helper de sesión. | B.7 pide probar que el modo anónimo solo ve lo que permiten las políticas de lectura pública, pero F0-4 termina con el test de DB-014 en verde y esas políticas y tablas llegan después. Aquí la parte sin tablas (rol `anon`, sin claims) se prueba en el commit 5a y la lectura pública en el commit 9, tras las migraciones. |
| API-005, API-013, B.5 | `ENGINEERING_STANDARDS.md` | Indicar en qué paso nacen el manejador global de errores y el `trace_id`. | API-005 y API-013 los exigen en todo endpoint, pero ni F0-4 ni B.5 los ubican en un paso. Aquí nacen en el commit 5a (envelope y `trace_id` en la respuesta); la propagación a los logs (OPS-005) queda pendiente y su test es verificación manual en la DoD. |
| B.1, ARQ-006, B.4 | `ENGINEERING_STANDARDS.md` | Exigir que el caso válido de cada comprobación demuestre que esta evaluó algo. | B.1 pide un caso válido y otro inválido, pero un comando que no ejecuta nada pasa el válido en vacío y hace fallar los inválidos por la razón equivocada. Aquí el caso válido de import-linter exige que el informe indique los contratos evaluados y cumplidos. |
| F0-4a, F0-4b, ARQ-006 | `ENGINEERING_STANDARDS.md` | Indicar cuándo se declaran los contratos de import-linter. | Los contratos nombran los módulos base antes de que existan, y `lint-imports` falla hasta que F0-4b los crea. Aquí se crean los paquetes vacíos de los módulos y un service.py vacío por módulo, porque el contrato de ARQ-008 los exige como módulos fuente, en el commit 5a para mantener el linter en verde. |
| SEC-019, ARQ-010, OPS-002 | `ENGINEERING_STANDARDS.md` | Indicar cómo obtiene el generador de cliente el OpenAPI cuando la documentación interactiva está desactivada. | create_app fija docs_url, redoc_url y openapi_url en None en todos los entornos (SEC-019 sin condicionar por entorno, OPS-002), pero ARQ-010 toma el OpenAPI como fuente de los tipos. Aquí el generador deberá obtenerlo con `app.openapi()` y no por HTTP. |
| PRO-008, B.6, PRO-010 | `ENGINEERING_STANDARDS.md` | Prohibir enlaces de sesión y otros metadatos del agente en los mensajes de commit, y bloquearlos con un hook. | Los trailers del agente publican un enlace de sesión en el historial de un repo público; PRO-008 solo fija el formato `tipo(scope): descripción` y B.6 no tiene un hook que lo impida. |
| ARQ-010, ARQ-011, QA-012 | `ENGINEERING_STANDARDS.md` | Indicar cómo tratar el código generado que no cumple el tsconfig estricto. | El cliente que genera `@hey-api/openapi-ts` con el cliente fetch incluido produce 12 errores de `tsc` con `exactOptionalPropertyTypes: true`; QA-012 exige type-check estricto y ARQ-011 prohíbe editar lo generado. Aquí se acota la supresión (`// @ts-nocheck`) a `src/generated` con la opción de salida del generador y un ADR (003). |
| ARQ-009, QA-015 | `ENGINEERING_STANDARDS.md` | Aclarar cuándo exige ARQ-009 los archivos `api.ts` y `types.ts`. | ARQ-009 los lista en todo módulo, pero un archivo vacío y sin uso lo marca `knip` (QA-015). Aquí se crean cuando el módulo los necesita (`api.ts`, si consume la API). |
| NOM-001, NOM-002 | `ENGINEERING_STANDARDS.md` | Indicar en qué idioma van las funciones de endpoint de los módulos base. | NOM-001 pone los módulos base en inglés y las «funciones de negocio» en español; sin precisión, un `operationId` `{módulo}_{función}` de un módulo base con la función en español mezclaría idiomas (NOM-002). Aquí los módulos base llevan funciones en inglés y los de dominio, en español. |
