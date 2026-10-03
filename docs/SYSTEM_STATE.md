# Estado del sistema — peervibe

Describe el sistema actual, no historial ni planes (DOC-001).

## Resumen

peervibe es una plataforma de referencia y calificación de productos con reseñas verificadas. Qué se construye: `docs/playbook-producto.md`. Cómo: `ENGINEERING_STANDARDS.md`. Qué exige la ley: `docs/playbook-privacidad.md`.

## Fase actual

Fase 0 de arranque, en la rama `chore/fase-0-arranque`. F0-1 (preguntas), F0-2 (perfil) y F0-3 (estructura y documentos base) están completas. No hay aún código de aplicación, esquema de base de datos ni CI.

Próxima tarea: F0-4 (scaffolding, esqueletos de módulos y migración inicial). Empieza presentando la lista exacta de dependencias y los commits propuestos, y espera aprobación antes de instalar nada (PRO-005).

## Perfil

Ver `docs/PROJECT_PROFILE.yaml`: datos personales, IA solo para resumen de reseñas, uploads, staging, sin RUT, sin webhooks, sin módulos ni perfiles opcionales. Nivel de riesgo de privacidad: N2.

## Roles (SEC-004)

| Rol | Descripción |
|---|---|
| `user` | Usuario registrado; se asigna al registrarse. |
| `moderador` | Modera reseñas y comprobantes. |
| `admin` | Administra roles y la plataforma. |

## Módulos

Ninguno aún. Los módulos base (ARQ-018) y los de dominio se crean en F0-4 y después.

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
| Anexo C.2, B.4, ARQ-006, ARQ-009 | `ENGINEERING_STANDARDS.md` | El Anexo C.2 no incluye el resolver de imports que `eslint-plugin-boundaries` necesita con TypeScript. Además, la v7 del plugin deprecó las reglas clásicas (`element-types`, `entry-point`, `external`), que sin opciones son no-ops: la regla vigente es `boundaries/dependencies`. | Sin resolver, el plugin no resuelve los destinos de los imports (quedan como elemento desconocido) y la regla no detecta ninguna violación, aunque ESLint termine en verde. B.4 y las reglas LINT de ARQ-006 y ARQ-009 deberían nombrar la regla vigente y exigir un test que pruebe que las violaciones se detectan. |
