# 🏛️ Estándar de Ingeniería — Constitución para desarrollo con IA

> **Propietario:** Eduardo Serey M.
> **Versión del estándar:** 6.1.0 (ver Anexo D)
> **Alcance:** todo proyecto web del stack de oro (ARQ-001).
> **Documento único:** este archivo es el estándar completo. La IA y los humanos leen lo mismo.
> **Documentos complementarios:** el **Playbook de Privacidad** (qué exige la ley a todo proyecto) y el **playbook de producto** de cada proyecto (qué se construye). Ninguno repite las reglas de otro: este estándar define **cómo** se construye.

---

## ▶ Instrucción de arranque para la IA

Eres un socio de ingeniería senior. Este archivo es el estándar de ingeniería: lo lees completo al inicio de cada sesión y cumples todas sus reglas, sin excepciones.

- **MUST**: siempre. **NEVER**: nunca. **ASK**: detente, explica el impacto y espera aprobación explícita. **DEFAULT**: así, salvo un ADR aprobado.
- Si una tarea choca con una regla MUST o NEVER, detente e infórmalo; no busques un rodeo.
- Aplica las reglas sin corchetes en el título y solo las `[condicionales]` que el perfil `docs/PROJECT_PROFILE.yaml` activa. Si el proyecto no tiene perfil, ejecuta primero la **Fase 0 de arranque de proyecto**.
- Lee también el Playbook de Privacidad (qué exige la ley; la sección PRIV de este estándar define cómo se implementa) y el playbook de producto del proyecto (qué se construye).
- Ante conflicto entre reglas: PRIV > SEC > DB > resto. Si persiste: ASK. Si una regla de este estándar impide cumplir un criterio del Playbook de Privacidad, detente: ASK.
- Ante duda sobre una regla, relee su ID en este archivo; si la duda sigue, pregunta.
- Antes de trabajar, lee `docs/SYSTEM_STATE.md` y, antes de tocar el esquema, `docs/SCHEMA_MAP.md`, si existen (la Fase 0 los crea).
- Si una verificación (HOOK, CI, TEST o LINT) aún no existe en el proyecto, **no omitas la regla**: cúmplela por tu cuenta y marca el ítem como verificación manual en la Definición de Hecho.
- Nada está terminado hasta cumplir la Definición de Hecho del final.

---

## 0. Cómo usar este documento

### 0.1 Lectores

Este archivo es el **único documento del estándar**. La copia maestra vive en el repositorio del propietario; cada proyecto lleva una copia de solo lectura en su raíz (PRO-015). La IA lo lee completo al inicio de cada sesión, junto con `docs/PROJECT_PROFILE.yaml` y `docs/SYSTEM_STATE.md`; los humanos lo consultan, y cada regla trae su *Por qué*. Ante una duda de interpretación, la IA relee la regla por su ID; si sigue en duda, **pregunta**: nunca interpreta a su favor.

### 0.2 Anatomía de una regla

```markdown
#### XXX-000 · MUST · [condición] Título corto
**Regla:** Qué se exige, en una o dos frases imperativas y verificables.
**Por qué:** El riesgo o beneficio concreto.
**Detalle:** Opcional. Es parte de la regla y se cumple igual.
**Verifica:** TIPO · mecanismo concreto.
```

`XXX-000` es un marcador de ejemplo, no un ID real. `[condición]` es opcional: sin corchetes, la regla aplica siempre. El texto de **Regla** tiene un máximo de 280 caracteres, sin contar una tabla si la regla la necesita. Lo que no cabe va a **Detalle** si es una exigencia, que forma parte de la regla y se cumple igual, o a **Por qué** si es una explicación, que no es vinculante; quien edite el estándar respeta este límite.

### 0.3 Modalidades

Solo existen cuatro. No hay "debería": si una regla parece opcional, es DEFAULT.

| Modalidad | Significado para la IA | ¿Se puede desviar? |
|---|---|---|
| **MUST** | Hacerlo siempre. | No. Solo cambiando este estándar. |
| **NEVER** | No hacerlo nunca. | No. Solo cambiando este estándar. |
| **ASK** | Detenerse, explicar el impacto y esperar aprobación humana **explícita en la sesión**. | Sí, con OK explícito del humano para ese caso. |
| **DEFAULT** | Hacerlo así salvo decisión documentada. | Sí, **solo** con un ADR aprobado (`docs/ADR/`). |

### 0.4 Tipos de verificación

| Tipo | Quién verifica | Momento | Ejemplo |
|---|---|---|---|
| **HOOK** | El agente es bloqueado por un hook (ej. `PreToolUse` de Claude Code) | Antes de ejecutar la acción | `git push --force`, `supabase db push` |
| **CI** | El pipeline falla y bloquea el merge | En cada push/PR | Lockfile, Actions fijadas por SHA, cobertura |
| **TEST** | Un test específico falla | En cada push/PR | RLS, rate limit, envelope de respuesta |
| **LINT** | Análisis estático / regla custom | En pre-commit y CI | Imports entre módulos, `SET` sin `LOCAL` |
| **REVIEW** | Checklist de la Definición de Hecho (Sección 13) en el PR | Antes del merge | Minimización de PII |

Meta: ≥60 % de las reglas MUST/NEVER con verificación automática (HOOK, CI, TEST o LINT). Una regla sin verificación es una sugerencia.

### 0.5 Prefijos de dominio

| Prefijo | Dominio | Sección |
|---|---|---|
| `PRO` | Proceso de trabajo con IA (aprobaciones, git, operaciones) | 2 |
| `ARQ` | Arquitectura y estructura del código | 3 |
| `API` | Contratos HTTP | 4 |
| `DB` | Datos, migraciones, RLS | 5 |
| `SEC` | Seguridad | 6 |
| `PRIV` | Privacidad y protección de datos (Ley 21.719) | 7 |
| `UI` | Frontend, mobile, accesibilidad | 8 |
| `IA` | Modelos de IA dentro del producto | 9 |
| `QA` | Calidad y tests | 10 |
| `OPS` | Operación, entornos, incidentes | 11 |
| `NOM` | Convenciones de nombres | 12 |
| `DOC` | Documentación viva | 12 |

**Política de IDs:** un ID es permanente y **nunca se reutiliza**. Una regla retirada se marca `RETIRADA` en el Changelog; su número no vuelve a usarse.

### 0.6 Condiciones de aplicación (`[condición]`)

Las condiciones leen el archivo `docs/PROJECT_PROFILE.yaml` del proyecto. La condición va entre corchetes en el título de la regla. La IA aplica una regla condicional solo si el perfil la activa; una regla sin corchetes aplica siempre.

| Condición | Se cumple cuando |
|---|---|
| `[datos_personales]` | `datos_personales: true` |
| `[rut]` | `rut` es `hmac` o `hmac+cifrado` |
| `[llm]` | `llm: true` |
| `[pagos_webhooks]` | `pagos_webhooks: true` |
| `[uploads]` | `uploads: true` |

Además de las condiciones, el perfil contiene configuración que algunas reglas leen:

| Clave | Usada por | Valores |
|---|---|---|
| `mirror_exclusions` | ARQ-004 | Subconjunto de: `webhook`, `job`, `integracion_externa`, `og`, `health`, `admin_sin_ui` |
| `entorno_staging` | OPS-001 | `true` / `false` |
| `modulos_opcionales` | ARQ-018 | Subconjunto de `dashboard`, `notifications` |
| `llm_usos` | IA-006, IA-009, PRIV-019 | Subconjunto de `moderacion`, `resumen`, `recomendaciones`, `asistencia`, `otro` |
| `estandar` | PRO-015 | `version` de la copia del estándar |
| `perfiles_opcionales` | ARQ-015, ARQ-017, SEC-009 | Subconjunto de `bff`, `cache`, `realtime` (cada uno exige ADR) |

El perfil se valida contra el código (ARQ-017): declarar menos de lo que el código usa hace fallar el CI.

### 0.7 Precedencia ante conflicto

PRIV > SEC > DB > el resto. Una regla con condición específica prevalece sobre una general del mismo dominio. Si el conflicto persiste: **ASK**; la IA nunca lo resuelve por su cuenta.

Entre documentos: el Playbook de Privacidad define **qué** exige la ley y este estándar **cómo** se implementa. Si una regla de este estándar impide cumplir un criterio del playbook, es un defecto del estándar: **ASK** y se corrige el estándar. El playbook de producto nunca modifica una regla de este estándar; una excepción del proyecto se documenta en un ADR.

### 0.8 Principio de atemporalidad

Este documento no contiene versiones de librerías, nombres de archivos generados, fechas legales ni sintaxis de configuración: eso vive en los lockfiles y en los archivos del proyecto. Las reglas dicen **qué** lograr y **por qué**; el proyecto concreta **cómo**, en la versión vigente. Quien edite el estándar no introduce versiones ni fechas en las reglas.

### 0.9 Glosario mínimo

| Término | Definición |
|---|---|
| **PII** | Dato personal: cualquier información que identifica o hace identificable a una persona natural. |
| **Espejo** | Paridad funcional entre frontend y backend (ARQ-004). |
| **Módulo** | Unidad funcional autónoma con su propio backend y frontend (ARQ-006). |
| **ADR** | Architecture Decision Record: registro breve de una decisión técnica y sus consecuencias (`docs/ADR/`). |
| **DoD** | Definición de Hecho: checklist que toda entrega debe pasar (Sección 13). |
| **Perfil** | `docs/PROJECT_PROFILE.yaml`: declara qué características tiene el proyecto. |
| **Stack de oro** | El conjunto tecnológico fijo de la Sección 3. |

---

## 1. 🧭 Principios

Los principios no se verifican: orientan cuando ninguna regla cubre un caso.

1. **Concepto → arquitectura → código.** Si el razonamiento conceptual es débil, se detiene y se cuestiona antes de escribir código.
2. **Seguridad y privacidad por defecto.** Todo input es hostil hasta ser validado; todo dato personal se trata como ajeno y prestado.
3. **Fallar cerrado.** Ante un error, una duda o un estado inesperado, el sistema niega el acceso y no revela información. Nunca "deja pasar".
4. **Una sola fuente de verdad** para cada cosa: el esquema en las migraciones, los tipos en los modelos del backend, las reglas en este documento.
5. **Lo verificable manda.** Si algo importa, se automatiza su verificación; si no se puede verificar, se revisa en la DoD.
6. **El historial es intocable.** Nada se borra físicamente, salvo lo que la ley exige anonimizar (Sección 7).
7. **Explícito sobre implícito.** Sin magia, sin dependencias fantasma, sin "funciona pero nadie sabe por qué".
8. **Lo simple primero.** La complejidad adicional (caché, websockets, BFF) entra solo con un ADR que la justifique.
9. **Mobile first y accesible** por defecto, no como agregado final.
10. **Automatizar lo repetible.** Si una tarea se hará más de una vez, se evalúa convertirla en script, hook, test o skill.

---

## Fase 0 · Arranque de proyecto

Se ejecuta cuando el proyecto no tiene `docs/PROJECT_PROFILE.yaml`. Es un procedimiento, no un conjunto de reglas. Sigue PRO-001: la IA presenta el plan y **cada paso es ASK**: enumera lo que hará y espera aprobación antes de ejecutarlo. F0-1 solo pregunta y no necesita aprobación aparte; el lote opcional de F0-2 a F0-4 está al final de F0-4. Nada se inventa (PRO-002): lo que falte se pregunta.

### F0-1 · Preguntas de inicio

La IA las hace juntas y registra las respuestas.

| Pregunta | Clave del perfil | Efecto |
|---|---|---|
| ¿Cómo se llama y qué hace, en una frase? | `proyecto` | Título; la frase va al README y a `SYSTEM_STATE.md` |
| ¿Existe ya un repositorio git y su remoto? ¿Cuál es la URL y la rama principal? | — | Si no existe, `git init` (F0-2); el remoto lo crea el humano (F0-6) |
| ¿Trata datos de personas naturales? | `datos_personales` | Activa PRIV, módulos base (ARQ-018) y comentarios PII |
| ¿Pide el RUT? ¿Se muestra a alguien (el titular, otros usuarios, terceros)? | `rut` | No lo pide: `none` · Solo búsqueda o unicidad: `hmac` · Debe mostrarse: `hmac+cifrado` |
| ¿Integra modelos de IA? Si es así, ¿para qué (moderación, resumen o análisis, recomendaciones, asistencia, otro)? | `llm`, `llm_usos` | Activa la Sección 9 y PRIV-021; IA-009 exige evaluaciones por cada uso, y los usos que deciden sobre personas activan IA-006 y PRIV-019 |
| ¿Recibe webhooks (pagos, integraciones)? | `pagos_webhooks` | Activa API-012 y agrega `webhook` a `mirror_exclusions` (ARQ-004; agregar categorías es ASK: esta respuesta lo confirma) |
| ¿Los usuarios suben archivos? | `uploads` | Activa SEC-015 |
| ¿Hay usuarios reales, o una fecha prevista para tenerlos? | `entorno_staging` | Si es sí, staging obligatorio (OPS-001) |
| ¿Qué módulos opcionales necesita: `dashboard`, `notifications`, ambos o ninguno? | `modulos_opcionales` | ARQ-018 |
| ¿Necesita BFF, caché distribuida o tiempo real? | `perfiles_opcionales` | Cada uno exige un ADR (ARQ-015). Por defecto, ninguno |
| ¿Qué proveedores usará (IA, pagos o webhooks, notificaciones, registro de errores)? | — | Se registran en `PRIVACY_POLICY_NOTES.md` (PRIV-008) y nombran las variables de `.env.example`; los que falten quedan en `TBD` |
| ¿Cuáles son los colores de marca? | — | Tokens de diseño (UI-010); si aún no existen, tokens neutros provisionales y un ADR |
| ¿Qué roles existen? | — | Se registran en `SYSTEM_STATE.md` (SEC-004) |

**Sobre el RUT:** el valor por defecto es `hmac`, también para impedir duplicados (unicidad); `hmac+cifrado` solo si el humano lo pide. `hmac` no permite recuperar el valor: si más adelante hay que mostrarlo, hay que volver a pedírselo a los titulares.

### F0-2 · Perfil

Si no hay repositorio git, primero `git init` (rama `main`), un commit inicial vacío y la rama `chore/fase-0-arranque` (PRO-009): ahí van los commits de la Fase 0, uno por paso (PRO-008). Luego crear `docs/PROJECT_PROFILE.yaml` desde el Anexo A con las respuestas (incluidos `webhook` en `mirror_exclusions` si hay webhooks y `llm_usos` si hay IA) y registrar `estandar.version` (la de la cabecera del estándar presente). Modificarlo después es ASK (ARQ-017).

### F0-3 · Estructura

Crear `docs/` con los documentos base: `SYSTEM_STATE.md`, `SCHEMA_MAP.md` y el inventario de datos (con el encabezado «generado por `generate_docs` en F0-5; vacío hasta entonces», DB-020), `INCIDENT_RESPONSE.md` (PRIV-020), `PRIVACY_POLICY_NOTES.md` (si hay datos personales), `ADR/000-plantilla.md`, `README.md` (DOC-003) y `.env.example` con los nombres del Anexo C.1 y placeholders (SEC-016). Crear además `.gitignore` (secretos, dependencias, cachés, artefactos de build y archivos del sistema; nunca `.env.example`) y `CLAUDE.md`, con una línea que importa `ENGINEERING_STANDARDS.md` y la orden de ejecutar la Fase 0 si no hay perfil. El estándar se copia a la raíz del proyecto (si ya está, se deja) y queda de solo lectura (PRO-015). Los valores reales de entorno los entrega el humano. `backend/`, `frontend/` y `supabase/` **no se crean aquí**: los generadores de F0-4 esperan carpetas vacías o inexistentes, y el árbol se completa después (cada directorio vacío lleva un `.gitkeep`, porque git no versiona carpetas vacías). Lo demás (`.github/` y `.claude/`) nace en F0-5.

```text
proyecto/
├── ENGINEERING_STANDARDS.md      # copia de solo lectura (PRO-015)
├── README.md
├── CLAUDE.md
├── .gitignore
├── .env.example
├── .github/workflows/            # CI (Anexo B.5), creado en F0-5
├── .claude/                      # hooks del agente (Anexo B.6), creado en F0-5
├── docs/
│   ├── PROJECT_PROFILE.yaml
│   ├── SYSTEM_STATE.md
│   ├── SCHEMA_MAP.md             # generado
│   ├── INCIDENT_RESPONSE.md
│   ├── PRIVACY_POLICY_NOTES.md
│   └── ADR/
├── supabase/                     # F0-4, tras `supabase init`
│   ├── migrations/
│   └── seed.sql                  # solo datos sintéticos (DB-018)
├── backend/                      # F0-4
│   ├── app/
│   │   ├── core/
│   │   ├── shared/
│   │   └── modules/<modulo>/     # router, schemas, service, repository, models, dependencies
│   └── tests/
└── frontend/                     # F0-4, tras el scaffolding
    ├── src/
    │   ├── core/
    │   ├── shared/
    │   ├── generated/            # cliente generado (ARQ-010, ARQ-011)
    │   └── modules/<modulo>/     # views, components, hooks, api.ts, types.ts, index.ts
    └── e2e/
```

### F0-4 · Módulos base y migración inicial

**a · Scaffolding.** `supabase init`; manifiestos y lockfiles con hashes (npm y pip con pip-tools); la plantilla del frontend; el runtime fijado en `.python-version` y `.nvmrc` con la versión estable vigente que se detecte, confirmada por el humano. Luego se completa el árbol canónico de F0-3. Al terminar, auditoría manual de vulnerabilidades (`npm audit`, `pip-audit`): se detiene ante cualquier hallazgo alto o crítico, porque SEC-020 aún no tiene un CI que lo aplique.

**b · Esqueletos.** Los módulos de ARQ-018 con las capas de ARQ-008 y ARQ-009, sin lógica de negocio; la única funcionalidad real es `/health` (OPS-004). Exportación, baja y registro son la primera iteración posterior. En `core/`: la configuración tipada (ARQ-016) y la conexión que opera como el usuario (DB-012, contrato B.7).

**c · Migración inicial.** La función del trigger de `updated_at`, `user_roles` (estructura en SEC-004), `audit_logs` y, si hay datos personales, `consents`; una migración por cambio lógico (DB-002). También se crea el script del primer administrador (SEC-021); se ejecuta aparte, con aprobación explícita.

**Lote opcional F0-2 a F0-4.** Si el humano lo invoca por su identificador («aprueba el lote F0-2 a F0-4»), la IA ejecuta esos tres pasos de corrido, con estas condiciones:

1. Antes de empezar, resume el alcance exacto del lote (qué crea y dónde) y la **lista exacta de dependencias** que instalará, limitada a ARQ-001, al Anexo C.2 y a las herramientas que las reglas exigen (driver de base de datos, tests, linters y type-check, E2E y accesibilidad: QA-003, QA-006, QA-012, UI-009). Resume también los commits que propondrá (PRO-008). Espera confirmación: aprobar el lote aprueba esa lista y esos commits, y nada más (PRO-005).
2. Se detiene de inmediato ante cualquier error o advertencia.
3. No toca entornos remotos (`supabase db push`, despliegues) ni CI, hooks o infraestructura.
4. F0-4 incluye el test de aislamiento de DB-014 (B.7) y el lote termina con ese test en verde.
5. Al cerrar, informa qué creó y qué tests corrió, y espera confirmación antes de F0-5.

F0-5, F0-6, F0-7 y cualquier operación destructiva (PRO-007) siguen paso a paso.

### F0-5 · CI, comprobaciones y hooks

Crear el workflow de CI de B.5 en `.github/`, los hooks de B.6 en `.claude/` y en git, y las comprobaciones automáticas de B.1 a B.4 (tests, linters y revisiones de estructura, espejo, migraciones, rutas, OpenAPI y matriz de tests), cada una con su prueba. Toca CI e infraestructura: ASK (PRO-006).

### F0-6 · Pasos manuales del humano

La IA no configura las plataformas: entrega la lista exacta y espera confirmación.

- Crear el repositorio remoto y conectarlo como `origin` (PRO-010): sin él no hay push ni branch protection.
- Branch protection en `main` con los checks de CI como requeridos (PRO-010, OPS-003).
- Secretos en las plataformas (SEC-016).
- Proyectos de Supabase local, staging y producción según OPS-001.
- Actualizaciones automáticas de seguridad (SEC-020).
- Headers y rewrites en Vercel (SEC-010, ARQ-014).
- Segundo factor y protecciones de Supabase Auth (SEC-007, SEC-008).

### F0-7 · Verificación y cierre

Ejecutar las comprobaciones y el CI sobre el proyecto recién creado: todo en verde. Un commit por paso, propuesto con su mensaje y su lista de archivos (PRO-008), en la rama `chore/fase-0-arranque` (PRO-009). Cierre con el formato de PRO-012 y la Definición de Hecho (Sección 13).

---

## 2. PRO · Proceso de trabajo con IA

#### PRO-001 · MUST · Plan antes de ejecutar
**Regla:** Ante una tarea con más de un paso, enumerar los pasos y esperar aprobación antes de ejecutar el primero. Luego avanzar un paso a la vez. Única excepción: el lote F0-2 a F0-4 de la Fase 0, si el humano lo invoca por su identificador.
**Por qué:** Evita trabajo en la dirección equivocada y mantiene al humano en control de las decisiones.
**Detalle:** Fuera de ese lote, un paso a la vez, sin excepciones: la excepción no se extiende a otras fases ni tareas, ni la puede invocar la IA por su cuenta.
**Verifica:** REVIEW · el historial muestra el plan aprobado o, en la Fase 0, el lote invocado por el humano.

#### PRO-002 · NEVER · Inventar valores
**Regla:** Nunca inventar ni asumir valores de variables de entorno, credenciales, dominios, nombres de columnas o reglas de negocio. Si falta un dato, preguntar.
**Por qué:** Un valor supuesto produce código que parece funcionar y falla en producción, o expone datos.
**Verifica:** REVIEW

#### PRO-003 · MUST · Verificar existencia antes de crear
**Regla:** Antes de crear un módulo, tabla, componente compartido o endpoint, verificar que no exista ya, ni con otro nombre ni con funcionalidad equivalente (revisar `SYSTEM_STATE.md`, `SCHEMA_MAP.md` y el código).
**Por qué:** Los duplicados funcionales son la principal fuente de deuda técnica generada por IA.
**Verifica:** REVIEW

#### PRO-004 · NEVER · Inventar sintaxis de librerías
**Regla:** Nunca usar una API, parámetro o firma de librería sin haberla verificado en la documentación o en el código instalado. Ante duda, consultar la documentación de la versión instalada.
**Por qué:** Las alucinaciones de API compilan mal o, peor, compilan y hacen otra cosa.
**Verifica:** CI · type-check y tests

#### PRO-005 · ASK · Nuevas dependencias
**Regla:** Antes de instalar una dependencia nueva, justificar su necesidad, verificar que no exista ya una herramienta equivalente en el stack y esperar aprobación.
**Por qué:** Cada dependencia es superficie de ataque (supply chain) y mantenimiento futuro.
**Detalle:** En modo paso a paso, la aprobación cubre una lista de dependencias presentada de una vez, no cada paquete por separado; la que se aprueba al invocar el lote de la Fase 0 es un caso particular. Cualquier dependencia fuera de la lista aprobada, aunque sea del stack, vuelve a pedir aprobación.
**Verifica:** HOOK · bloquea `npm install`/`pip install` de paquetes nuevos sin aprobación · CI · diff del lockfile en el PR

#### PRO-006 · ASK · Cambios en infraestructura y CI
**Regla:** Antes de modificar workflows de CI, hooks del agente, configuración de despliegue (Vercel, Render), políticas de branch protection o settings del proyecto Supabase, explicar el cambio y esperar aprobación.
**Por qué:** Un cambio de infraestructura afecta a todo el sistema y a veces a la facturación.
**Detalle:** Los hooks del agente (`.claude/`) cuentan como infraestructura: una IA que pudiera editarlos podría desactivar sus propios controles.
**Verifica:** HOOK · bloquea escritura en `.github/`, `.claude/` y archivos de despliegue sin aprobación

#### PRO-007 · ASK · Operaciones destructivas o irreversibles
**Regla:** Antes de `DROP`, `ALTER COLUMN` que cambie tipo, eliminar una política RLS, `supabase db push`, `git push --force`, `git reset --hard` o eliminar ramas remotas: mostrar el impacto concreto y esperar aprobación explícita.
**Por qué:** Son irreversibles o exponen datos.
**Verifica:** HOOK · `PreToolUse` bloquea estos comandos sin aprobación

#### PRO-008 · MUST · Commits propuestos y atómicos
**Regla:** Proponer el mensaje de commit y la lista exacta de archivos incluidos, y esperar aprobación. Formato: `tipo(scope): descripción` con `tipo` ∈ {`feat`, `fix`, `refactor`, `test`, `docs`, `chore`}. Un commit = un cambio lógico.
**Por qué:** El historial es documentación; los commits mezclados impiden revertir con precisión.
**Verifica:** HOOK · valida el formato del mensaje (commit-msg) · REVIEW · lista de archivos

#### PRO-009 · MUST · Ramas con propósito único
**Regla:** Trabajar siempre en una rama `tipo/descripcion-corta` (mismos tipos de PRO-008), creada con aprobación. Una rama = una funcionalidad o corrección. Tras el merge, eliminar la rama local y reportar las ramas locales inactivas.
**Por qué:** Las ramas mezcladas o abandonadas generan conflictos y cambios "perdidos".
**Verifica:** CI · valida el nombre de la rama en el PR

#### PRO-010 · MUST · Push informado
**Regla:** Antes de cada push, mostrar la rama destino, los commits (con sus mensajes) y los archivos modificados, y esperar aprobación. Nunca push directo a `main`: se integra solo vía PR con checks en verde.
**Por qué:** El push es el punto de no retorno hacia el repositorio compartido.
**Verifica:** HOOK · bloquea push sin aprobación · CI · branch protection en `main`

#### PRO-011 · DEFAULT · Sin worktrees
**Regla:** No usar `git worktree`. Si se usa (con ADR o pedido explícito), todos los cambios deben quedar commiteados e integrados en la rama que el humano usa para probar antes de cerrar la sesión.
**Por qué:** Los cambios en un worktree olvidado parecen "perdidos" para el humano.
**Verifica:** HOOK · `Stop` ejecuta `git status` y alerta si hay cambios fuera de la rama activa

#### PRO-012 · MUST · Cierre de sesión verificable
**Regla:** Al terminar una tarea, reportar: qué cambió, dónde quedó (rama y commits), qué tests se ejecutaron con su resultado, y qué ítems de la DoD quedan pendientes.
**Por qué:** El humano debe poder retomar sin reconstruir lo ocurrido.
**Verifica:** HOOK · `Stop` exige el cierre si el repositorio cambió en la sesión

#### PRO-013 · MUST · Regla del Boy Scout, separada
**Regla:** Si al modificar un archivo se detecta una violación a este estándar, proponer su corrección en un commit independiente, antes o después del cambio principal, nunca mezclada con él.
**Por qué:** Mejora continua sin contaminar el diff de la funcionalidad.
**Verifica:** REVIEW

#### PRO-014 · MUST · Proponer automatizaciones
**Regla:** Cuando una tarea, revisión o checklist se repita en el proyecto, proponer convertirla en script, hook, test o skill, con un borrador listo para revisar (no solo la pregunta).
**Por qué:** Lo repetido a mano se olvida o se hace distinto cada vez.
**Verifica:** REVIEW

#### PRO-015 · MUST · El estándar es de solo lectura en los proyectos
**Regla:** La copia de este archivo dentro de un proyecto es de solo lectura. Un cambio al estándar se propone al propietario, se aplica solo en la copia maestra (con ID, versión y changelog) y luego se copia a los proyectos.
**Por qué:** Copias editadas por proyecto terminan en constituciones distintas; un solo origen mantiene alineados a todos los proyectos.
**Verifica:** HOOK · bloquea escrituras sobre el archivo dentro de un proyecto

---

## 3. ARQ · Arquitectura

#### ARQ-001 · MUST · Stack de oro
**Regla:** Stack fijo: SPA React + Vite + TypeScript, TanStack Query (servidor), Zustand (UI), Tailwind; backend FastAPI + Pydantic + SQLAlchemy async; Supabase (PostgreSQL, Auth, Storage); Vercel, Render y GitHub Actions. Versión estable vigente, fijada en los lockfiles.
**Por qué:** Un stack único permite reutilizar conocimiento y automatizaciones entre proyectos.
**Detalle:** Gestores de paquetes: npm para el frontend y pip con pip-tools (lockfile con hashes) para el backend, que son los que cubre el hook de PRO-005; cambiar de gestor exige un ADR y extender ese hook. El runtime (Python y Node) se declara en `.python-version` y `.nvmrc` (OPS-011).
**Verifica:** CI · revisión de estructura: los manifiestos de dependencias coinciden con el stack

#### ARQ-002 · ASK · Tecnología fuera del stack
**Regla:** Cualquier herramienta, servicio o librería que cubra una función ya cubierta por el stack de oro requiere aprobación y ADR.
**Por qué:** Dos herramientas para lo mismo duplican mantenimiento y confunden a la IA.
**Verifica:** REVIEW · ADR

#### ARQ-003 · MUST · Estructura del monorepo
**Regla:** Monorepo con `frontend/`, `backend/`, `supabase/`, `docs/` y `.github/`; en frontend y backend: `modules/` (dominio), `shared/` (reutilizable, sin negocio) y `core/` (infraestructura). El árbol canónico y los archivos base los define la Fase 0 de arranque.
**Por qué:** Una estructura predecible permite a la IA ubicar y crear código sin interpretar.
**Verifica:** CI · revisión de estructura

#### ARQ-004 · MUST · Arquitectura espejo
**Regla:** Toda funcionalidad del frontend con datos tiene contraparte en el backend y todo endpoint, una interfaz que lo consume. Un endpoint sin contraparte exige un marcador de exención con categoría habilitada en `mirror_exclusions`. Agregar marcadores o categorías: ASK.
**Por qué:** Evita lógica huérfana, endpoints muertos y reglas de negocio implementadas en un solo lado; el ASK impide que la IA se auto-exima para pasar el CI.
**Detalle:** Categorías cerradas: `webhook`, `job`, `integracion_externa`, `og`, `health`, `admin_sin_ui`. Cada categoría exige una condición verificable (Anexo B.2): por ejemplo, `health` solo puede ser `/health`. La paridad es funcional, no de nombres de carpetas. El marcador vive en la definición del endpoint (visible en el OpenAPI).
**Verifica:** CI · revisión del espejo · REVIEW · las exenciones nuevas que informa el PR

#### ARQ-005 · NEVER · Lógica de negocio en un solo lado
**Regla:** Nunca implementar una regla de negocio solo en el frontend. El frontend puede **replicar** validaciones para dar feedback inmediato, pero el backend siempre las ejecuta.
**Por qué:** El frontend es manipulable por el usuario.
**Verifica:** TEST · los tests de backend cubren cada regla de negocio

#### ARQ-006 · MUST · Independencia modular
**Regla:** Un módulo nunca importa desde el interior de otro. Lo común va a `shared/` con aprobación; lo casi igual se duplica y evoluciona aparte. Única excepción: el service de `dashboard` puede importar services de otros módulos, porque solo agrega datos.
**Por qué:** Módulos acoplados no se pueden modificar, testear ni eliminar de forma aislada.
**Detalle:** Direcciones permitidas: un módulo importa de `shared/` y de `core/`; `shared/` importa solo de `core/`; `core/` no importa de módulos ni de `shared/`, salvo el registro de los routers en el punto de composición de la aplicación. Los contratos de import-linter y las reglas de boundaries de ESLint reflejan esta tabla.
**Verifica:** LINT · reglas de boundaries (ESLint en frontend, import-linter en backend)

#### ARQ-007 · MUST · `shared/` y `core/` sin lógica de negocio
**Regla:** `shared/` contiene solo elementos reutilizables sin conocimiento de ningún dominio. `core/` contiene solo infraestructura global (configuración, seguridad, base de datos, providers, routing). Un componente que necesita lógica de un dominio vive en ese módulo.
**Por qué:** La lógica de negocio escondida en capas genéricas es invisible y se rompe en silencio.
**Verifica:** REVIEW

#### ARQ-008 · MUST · Capas del módulo backend
**Regla:** Cada módulo backend separa estas responsabilidades:

| Archivo | Responsabilidad | Prohibido |
|---|---|---|
| `router.py` | Endpoints, dependencias de auth, códigos HTTP | Lógica de negocio, queries |
| `schemas.py` | Modelos Pydantic de entrada y salida | Lógica |
| `service.py` | Reglas de negocio y orquestación | Queries directas a la DB |
| `repository.py` | Todo acceso a datos (queries) | Reglas de negocio |
| `models.py` | Modelos ORM que reflejan las migraciones | Lógica |
| `dependencies.py` | Dependencias inyectables del módulo | Lógica de negocio |

El repository expone métodos por caso de uso que devuelven justo lo necesario, con relaciones cargadas en la misma query; nunca CRUD genérico ni llamadas en bucle (DB-015).
**Por qué:** Cada cosa tiene un único lugar inequívoco, el service se testea sin base de datos y los métodos por caso de uso evitan el N+1.
**Verifica:** LINT · el service no importa la sesión de DB ni construye queries · CI · revisión de estructura · TEST · carga perezosa de relaciones configurada para fallar (DB-015)

#### ARQ-009 · MUST · Estructura del módulo frontend
**Regla:** Cada módulo frontend tiene `views/`, `components/`, `hooks/`, `api.ts` (si consume API), `types.ts` (solo tipos exclusivos de UI) e `index.ts` como **único punto de entrada** del módulo.
**Por qué:** Un solo punto de entrada hace visible y controlable la superficie pública del módulo.
**Verifica:** LINT · imports solo vía `index.ts` · CI · revisión de estructura

#### ARQ-010 · MUST · Tipos de extremo a extremo
**Regla:** Los tipos de la API fluyen desde los modelos Pydantic → OpenAPI → código generado en el frontend (tipos, SDK y opciones de query). Si un tipo no existe en el código generado, se crea el modelo en el backend y se regenera; nunca se define a mano en el frontend.
**Por qué:** Una sola fuente de verdad para los contratos elimina desincronizaciones entre frontend y backend.
**Detalle:** Un único comando del proyecto, documentado en el README, exporta el OpenAPI del backend y regenera el cliente; el CI ejecuta ese mismo comando y falla si hay diferencias.
**Verifica:** CI · regenera el código y falla si hay diferencias con lo commiteado

#### ARQ-011 · NEVER · Editar o duplicar código generado
**Regla:** Nunca editar a mano el directorio de código generado ni duplicar en otro lugar lo que ya genera (tipos, funciones de API, query keys de endpoints).
**Por qué:** Se sobrescribe en cada regeneración y crea dos fuentes de verdad.
**Verifica:** CI · el diff del directorio generado solo puede venir del generador

#### ARQ-012 · MUST · I/O asíncrono
**Regla:** Todo I/O del backend (base de datos, HTTP externo, storage) es asíncrono y usa clientes async (sesión async del ORM, cliente HTTP async). Nunca una llamada bloqueante dentro de una función `async`.
**Por qué:** Una llamada bloqueante congela el event loop y degrada a todos los usuarios concurrentes.
**Verifica:** LINT · detección de llamadas bloqueantes en código async

#### ARQ-013 · MUST · Trabajo pesado fuera del request
**Regla:** Recálculos de agregados, envío masivo, generación de reportes y cualquier tarea que no sea necesaria para responder se ejecutan fuera del ciclo del request (tareas en segundo plano o jobs programados, ver OPS).
**Por qué:** El tiempo de respuesta percibido no debe depender de trabajo que el usuario no espera.
**Verifica:** REVIEW

#### ARQ-014 · DEFAULT · SPA pura con endpoint de Open Graph
**Regla:** El frontend es una SPA. Las vistas que deben compartirse en redes sociales se resuelven con un endpoint público del backend `/og/{recurso}/{id}` (fuera de `/api/v1/`) que devuelve metadatos Open Graph, con rewrites en Vercel para los crawlers.
**Por qué:** Da previsualización en redes sin introducir renderizado en servidor ni otro framework.
**Verifica:** TEST · el endpoint responde metadatos válidos

#### ARQ-015 · DEFAULT · Perfiles opcionales solo con ADR
**Regla:** BFF con cookies (`perfil:bff`), caché distribuida (`perfil:cache`) y tiempo real por websockets (`perfil:realtime`) no forman parte de la base. Se activan solo con un ADR aprobado y declarándolos en el perfil del proyecto.
**Por qué:** Cada uno agrega complejidad operativa que la mayoría de los proyectos no necesita.
**Verifica:** CI · revisión del perfil: si el código usa el mecanismo, el perfil debe declararlo

#### ARQ-016 · MUST · Configuración centralizada y tipada
**Regla:** Toda configuración del backend se lee en un único módulo de settings tipado (Pydantic Settings) que valida al arrancar. El frontend lee solo variables públicas por diseño. Si falta una variable requerida, la aplicación no arranca.
**Por qué:** Fallar al arrancar es mejor que fallar en producción con una configuración a medias (principio 3).
**Detalle:** Son requeridas las variables del grupo base (Supabase, bases de datos, CORS, proxies y límites). Las de cada funcionalidad (IA, webhooks, uploads, notificaciones, errores) se declaran desde el inicio, pero pasan a ser requeridas cuando existe el módulo que las usa; nunca se rellenan con valores falsos. Los nombres canónicos de las variables están en el Anexo C.1.
**Verifica:** TEST · arranque con variable faltante falla

#### ARQ-017 · MUST · Perfil coherente con el código
**Regla:** `docs/PROJECT_PROFILE.yaml` declara todo lo que el código usa; el CI falla ante un uso no declarado (SDK de LLM, subidas, webhooks, columnas PII, websockets, caché, cookies de sesión). Modificar el perfil: ASK.
**Por qué:** Si el perfil declara menos de lo que existe, las reglas que más importan se omiten en silencio justo cuando se necesitan.
**Detalle:** Señal → declaración: SDK de LLM → `llm`; Storage o subidas → `uploads`; marcador `webhook` → `pagos_webhooks`; columnas `pii:*` → `datos_personales`; websockets, caché o cookies de sesión → su perfil.
**Verifica:** CI · revisión del perfil

#### ARQ-018 · MUST · [datos_personales] Módulos base
**Regla:** Con datos personales existen los módulos base `auth`, `users` (exportación y baja de cuenta), `settings` (consentimientos), `admin` y `logs` (auditoría). `dashboard` y `notifications` solo si el perfil los declara en `modulos_opcionales`.
**Por qué:** La ley exige acceso, portabilidad, supresión, consentimiento y trazabilidad; tenerlos desde el inicio evita improvisarlos con datos reales.
**Detalle:** Sin datos personales, solo `auth` si el proyecto tiene inicio de sesión. `logs` es el visor de auditoría para administradores (PRIV-013); el logging técnico estructurado (OPS-005) no vive en ese módulo, sino en `core/`.
**Verifica:** CI · revisión de estructura

---

## 4. API · Contratos HTTP

#### API-001 · MUST · Prefijo y versionado
**Regla:** Toda la API REST vive bajo `/api/v1/`. En una versión solo hay cambios aditivos; un cambio que rompe contratos crea la versión siguiente y depreca la anterior con los headers `Deprecation` y `Sunset`. Todo cambio que rompe: ASK.
**Por qué:** Un frontend desplegado, una integración externa o una app en caché no se actualizan al mismo tiempo que el backend.
**Detalle:** La versión deprecada se mantiene durante un periodo declarado antes de retirarse.
**Verifica:** CI · comparación del OpenAPI contra la rama base: detecta cambios que rompen

#### API-002 · MUST · Forma de las rutas
**Regla:** Recursos en plural en colección y detalle (`/recursos/{id}`); kebab-case en rutas de varias palabras; namespace de módulo solo si el recurso vive en ese contexto (`/admin/users`). Acciones no-CRUD al final, con verbo en español (`/archivar`); nunca verbos en la ruta base.
**Por qué:** Una convención única y sin alternativas es la única que una IA puede cumplir sin interpretar.
**Detalle:** `/health` y `/og/{recurso}/{id}` viven fuera de `/api/v1/` y no son recursos en plural: la revisión de rutas los exceptúa (OPS-004, ARQ-014).
**Verifica:** LINT · revisión de rutas sobre el OpenAPI

#### API-003 · MUST · Semántica de los métodos HTTP
**Regla:** `GET` nunca modifica estado. `POST` crea o ejecuta una acción, `PUT` reemplaza, `PATCH` actualiza de forma parcial, `DELETE` elimina de forma lógica (DB-007).
**Por qué:** Cachés, proxies, reintentos automáticos y crawlers asumen esta semántica; violarla produce efectos no deseados.
**Verifica:** REVIEW

#### API-004 · MUST · Envelope de éxito
**Regla:** Toda respuesta exitosa con cuerpo es `{"data": ...}`. Las colecciones paginadas son `{"data": [...], "meta": {...}}` (API-010). `204` no tiene cuerpo. Nunca se devuelve un objeto suelto.
**Por qué:** El frontend siempre sabe dónde están los datos; los tipos generados son uniformes.
**Verifica:** TEST · test de contrato sobre todos los endpoints

#### API-005 · MUST · Envelope de error
**Regla:** Todo error es `{"error": {code, message, details?, trace_id}}`: `code` en UPPER_SNAKE_CASE (NOM-004), `message` en español legible, `details` solo en validación por campo. Nunca `str(exc)`, trazas, SQL ni detalles técnicos, en ningún entorno.
**Por qué:** Un formato único simplifica el manejo en el frontend; los detalles técnicos en respuestas son información para un atacante.
**Detalle:** Los errores de validación del framework se reformatean a este envelope mediante un manejador global.
**Verifica:** TEST · errores forzados (validación, 404, 500) cumplen el envelope y no contienen trazas

#### API-006 · MUST · Códigos HTTP
**Regla:** Se usan exclusivamente estos códigos, con este significado:

| Código | Cuándo |
|---|---|
| `200` | Éxito con cuerpo (`GET`, `PUT`, `PATCH`, acciones) |
| `201` | Recurso creado (`POST`) |
| `204` | Éxito sin cuerpo (`DELETE`) |
| `400` | Regla de negocio violada que no es de formato |
| `401` | Sin autenticación o token inválido |
| `403` | Autenticado, pero su rol no permite la acción |
| `404` | No existe, **o pertenece a otro usuario** (no revelar existencia) |
| `409` | Conflicto con el estado actual: duplicado, estado inválido, versión desactualizada (API-014) |
| `422` | Validación de formato de la entrada |
| `429` | Rate limit excedido |
| `500` | Error no controlado (mensaje genérico) |
| `503` | Dependencia caída o mantenimiento (usado por `/health`) |

**Por qué:** El código HTTP comunica qué pasó sin leer el cuerpo; su uso consistente habilita reintentos y manejo global de errores.
**Verifica:** TEST · los tests por endpoint verifican el código esperado (QA)

#### API-007 · MUST · Endpoints autodocumentados
**Regla:** Todo endpoint declara resumen, descripción de su regla de negocio, modelo de respuesta, código de éxito y las respuestas de error posibles.
**Por qué:** El OpenAPI es la fuente de los tipos del frontend (ARQ-010) y la documentación viva de la API.
**Verifica:** CI · revisión del OpenAPI: falla si falta algún elemento

#### API-008 · MUST · Validación estricta de entrada
**Regla:** Todo schema de entrada rechaza campos no declarados. Todo texto tiene largo máximo; emails, URLs y UUIDs usan tipos específicos; valores de un conjunto fijo usan enumeraciones; secretos y contraseñas usan un tipo que no se serializa ni se loguea.
**Por qué:** La validación en el borde es la primera barrera contra inyección de campos, payloads gigantes y datos corruptos.
**Verifica:** LINT · regla custom sobre los schemas de entrada

#### API-009 · NEVER · Exponer campos internos
**Regla:** Nunca devolver objetos ORM ni schemas que incluyan campos internos (`is_deleted`, `deleted_*`, `created_by`, hashes, HMAC, claves, IDs de proveedores). Toda respuesta usa un schema de salida explícito.
**Por qué:** Los campos internos filtran información de implementación y, a veces, datos personales.
**Verifica:** TEST · test de contrato con lista de campos prohibidos

#### API-010 · MUST · Paginación
**Regla:** Todo listado pagina con el componente compartido: offset por defecto (`page`, `limit` ≤ 100) y cursor para feeds, tablas grandes y auditoría (`cursor`, `limit`). El orden solo acepta campos de una lista permitida por endpoint. Campos de `meta`:

| Tipo | `meta` |
|---|---|
| Offset | `page`, `limit`, `total`, `total_pages`, `has_next`, `has_prev` |
| Cursor | `limit`, `next_cursor`, `has_next` |
**Por qué:** Un listado sin límite es un incidente de rendimiento esperando datos. Un campo de orden libre es un vector de inyección.
**Verifica:** TEST · `limit` mayor a 100 es rechazado; orden fuera de la lista es rechazado

#### API-011 · MUST · Idempotencia en operaciones con efectos
**Regla:** Todo `POST` con efectos externos o monetarios (pagos, emails, notificaciones, recursos facturables) acepta `Idempotency-Key`: la misma clave del mismo usuario, dentro de la ventana, devuelve la respuesta original sin repetir el efecto. Resto de los `POST`: DEFAULT.
**Por qué:** Redes móviles inestables y reintentos automáticos duplican operaciones; con dinero de por medio, eso es un incidente.
**Verifica:** TEST · dos requests con la misma clave producen un solo efecto

#### API-012 · MUST · [pagos_webhooks] Webhooks entrantes
**Regla:** Todo webhook: verifica la firma antes de leer el contenido; rechaza eventos fuera de la ventana de tiempo; deduplica por ID de evento; responde rápido y procesa en segundo plano; lleva el marcador `webhook` (ARQ-004).
**Por qué:** Un webhook es público por definición: sin firma cualquiera puede simular un pago; sin deduplicación, un reintento duplica la operación.
**Verifica:** TEST · firma inválida → rechazo; evento repetido → un solo efecto

#### API-013 · MUST · Trazabilidad por request
**Regla:** Cada request tiene un `trace_id`: se acepta el que envía el frontend si es válido o se genera uno nuevo. Se propaga a todos los logs de ese request y se incluye en toda respuesta de error y en el header de respuesta.
**Por qué:** Permite pasar de "el usuario vio un error" al log exacto en segundos, sin exponer detalles técnicos.
**Verifica:** TEST · el `trace_id` de la respuesta de error aparece en el log

#### API-014 · DEFAULT · Concurrencia optimista
**Regla:** La actualización de recursos que más de una persona puede editar incluye la versión (o el `updated_at`) que el cliente leyó. Si no coincide con la actual, se responde `409` y el frontend ofrece recargar.
**Por qué:** Sin esto, la última escritura pisa en silencio la anterior.
**Verifica:** TEST

---

## 5. DB · Datos, migraciones y RLS

#### DB-001 · MUST · Las migraciones son la única vía de cambio
**Regla:** El esquema cambia solo mediante archivos de migración versionados, creados con la CLI de Supabase. Nunca se cambia el esquema desde el dashboard. Una migración ya aplicada nunca se edita: se crea una nueva. Aplicar migraciones en un entorno remoto es **ASK** (PRO-007).
**Por qué:** Es la única forma de reproducir el esquema en cualquier entorno y de auditar su historia.
**Verifica:** CI · detecta ediciones en migraciones existentes y diferencias entre las migraciones y el esquema remoto

#### DB-002 · MUST · Una tabla nace completa
**Regla:** La migración que crea una tabla incluye, en el mismo archivo: columnas canónicas (DB-006), índices, trigger de `updated_at`, RLS habilitada con sus políticas (DB-009), GRANTs (DB-010) y comentarios de PII (DB-019). Una migración = un cambio lógico.
**Por qué:** Una tabla a medio crear (con RLS sin políticas o sin GRANTs) bloquea o expone datos en producción.
**Verifica:** LINT · revisión de migraciones sobre cada archivo nuevo

#### DB-003 · MUST · El esquema tiene una sola fuente
**Regla:** Las migraciones son la fuente de verdad del esquema. Los modelos del ORM lo reflejan y nunca lo definen: no se generan migraciones desde el ORM.
**Por qué:** Dos definiciones del mismo esquema divergen en silencio.
**Verifica:** CI · compara los modelos del ORM contra el esquema resultante de las migraciones

#### DB-004 · MUST · Cambios compatibles (expand/contract)
**Regla:** Toda migración es compatible con el código que está desplegado en ese momento. Renombrar o eliminar una columna o tabla se hace en fases: (1) agregar lo nuevo, (2) desplegar código que usa lo nuevo, (3) retirar lo viejo en una migración posterior.
**Por qué:** Frontend, backend y base de datos no se despliegan en el mismo instante; un cambio incompatible produce errores durante el despliegue.
**Verifica:** REVIEW

#### DB-005 · MUST · Índices sin bloquear
**Regla:** En tablas existentes con datos, los índices se crean sin bloquear escrituras (`CONCURRENTLY`), en una migración propia que no contenga otras sentencias. En tablas nuevas se usa un índice normal dentro de la migración de creación.
**Por qué:** Un índice bloqueante detiene las escrituras en producción; `CONCURRENTLY` no puede ejecutarse junto a otras sentencias en una misma transacción.
**Verifica:** LINT · revisión de migraciones

#### DB-006 · MUST · Columnas canónicas
**Regla:** Toda tabla de negocio tiene: `id` UUID generado por la DB; `created_at` y `updated_at` con zona horaria, no nulos y con default; `created_by` y `updated_by` no nulos; `is_deleted`, `deleted_at`, `deleted_by`. `updated_at` se mantiene por trigger. Excepciones: DB-007.
**Por qué:** Trazabilidad uniforme y soft delete en todas las tablas sin decisiones caso a caso.
**Detalle:** La función del trigger de `updated_at` se crea en la migración inicial del proyecto, antes que cualquier tabla. `created_by` y `updated_by` son UUID `NOT NULL`, sin `DEFAULT` y sin clave foránea hacia Auth: cuando actúa el sistema (triggers, jobs) se llena el UUID nulo (`00000000-0000-0000-0000-000000000000`) que devuelve `system_actor_id()`, nunca se deja vacío; así un camino de código que olvida el actor falla al insertar.
**Verifica:** LINT · revisión de migraciones

#### DB-007 · NEVER · Borrado físico
**Regla:** Nunca borrar filas físicamente: toda eliminación es lógica (`is_deleted`, `deleted_at`, `deleted_by`) y toda lectura filtra `is_deleted = false`. Recuperar eliminados solo desde admin. Únicas excepciones: `audit_logs` y `consents`.
**Por qué:** El historial es intocable (principio 6); el borrado físico destruye evidencia e integridad referencial.
**Detalle:** Cada excepción tiene su propio mecanismo: `audit_logs` se anonimiza por antigüedad (PRIV-014); `consents` se revoca con `revoked_at` (PRIV-005). Estas dos tablas tampoco llevan `updated_*` ni las columnas de borrado lógico (DB-006); la revisión de migraciones conoce la excepción. Una fila borrada lógicamente que contiene PII se anonimiza al vencer su plazo de retención (PRIV-006) mediante un job (OPS-009): nunca se conserva identificable indefinidamente.
**Verifica:** LINT · detecta borrados físicos fuera de las excepciones · TEST · un registro eliminado no aparece en lecturas

#### DB-008 · NEVER · Eliminar usuarios desde Auth
**Regla:** Nunca eliminar un usuario desde el dashboard de Supabase ni con la función de eliminación de la API de administración de Auth. La baja de cuenta ocurre solo mediante el flujo de anonimización (Sección 7).
**Por qué:** Las claves foráneas hacia los usuarios de Auth tienen borrado en cascada: eliminar el usuario borra físicamente todas sus filas relacionadas.
**Verifica:** LINT · detecta llamadas a la eliminación de usuarios de Auth

#### DB-009 · MUST · RLS completa en toda tabla expuesta
**Regla:** Toda tabla del esquema expuesto tiene RLS habilitada y una política por cada operación otorgada a `anon` o `authenticated` (DB-010). Nunca políticas de `delete` ni `all` (DB-007), ni RLS sin políticas.
**Por qué:** La clave publicable es pública: sin RLS, cualquiera puede leer la tabla directamente. RLS sin políticas bloquea el módulo completo.
**Detalle:** RLS y políticas nacen en la misma migración que crea la tabla (DB-002). Una tabla sin GRANTs para esos roles no es accesible desde la API de datos.
**Verifica:** TEST · suite de RLS: por tabla, anónimo, usuario ajeno y dueño obtienen exactamente lo que deben · LINT · revisión de migraciones

#### DB-010 · MUST · GRANTs explícitos
**Regla:** Toda tabla recibe en su migración los privilegios mínimos explícitos para los roles que la usan (`authenticated` y, solo si corresponde, `anon`). Nunca privilegios más amplios que las operaciones que el módulo necesita.
**Por qué:** Cuando el backend opera como el usuario (DB-012), sin el GRANT la query falla antes de evaluar RLS; con GRANTs amplios, un error en RLS expone más.
**Verifica:** TEST · suite de RLS · LINT · revisión de migraciones

#### DB-011 · MUST · RLS eficiente
**Regla:** En las políticas RLS, las funciones de contexto van envueltas en `select` (una evaluación por consulta) y toda columna usada tiene índice. Los roles se verifican con una función `security definer` en un esquema no expuesto, solo con roles activos.
**Por qué:** Evaluar funciones por fila y comparar sin índice multiplica los tiempos de consulta; un rol eliminado nunca debe conservar permisos.
**Detalle:** Las políticas de administración llaman a esa función y exigen además el segundo factor verificado (SEC-007), de modo que la base de datos lo impone aunque el backend falle. El segundo factor va dentro de la política de admin, no como política restrictiva global: los usuarios sin rol admin no se ven afectados.
**Verifica:** LINT · revisión de migraciones sobre las políticas · TEST · un admin degradado pierde acceso de inmediato

#### DB-012 · MUST · El backend opera como el usuario
**Regla:** Todo request autenticado ejecuta sus queries dentro de una transacción que fija el rol `authenticated` y los claims del usuario de forma **local a esa transacción**. Así, RLS se aplica también al backend.
**Por qué:** Con una conexión privilegiada, RLS no protege nada de lo que hace el backend; operar como el usuario da defensa en profundidad real.
**Detalle:** Cada tarea, concurrente o en segundo plano, abre su propia transacción: como el usuario si actúa en su nombre, o con la conexión privilegiada solo si es un job declarado (DB-013). El contrato del helper está en el Anexo B.7. Los endpoints de la lista pública (SEC-003) que consultan la base de datos usan su modo anónimo.
**Verifica:** TEST · una query del backend sin filtro por dueño igual devuelve solo filas propias

#### DB-013 · MUST · Conexión privilegiada acotada
**Regla:** La conexión que ignora RLS solo se usa en contextos declarados: jobs, scripts de arranque (SEC-021), webhooks firmados (API-012), anonimización, escritura de auditoría y registro de consentimientos. Nunca en endpoints de administración. Cada uso es explícito y queda auditado.
**Por qué:** Es la llave maestra; su uso debe ser excepcional, visible y trazable.
**Detalle:** Auditoría y consentimientos son evidencia: si el rol del usuario pudiera insertarlos, la API de datos permitiría fabricarlos (PRIV-005, PRIV-013). Los endpoints de administración operan como el usuario (DB-012), bajo las políticas RLS de admin (DB-011). Cada uso de la conexión privilegiada pasa por una dependencia explícita. En código de test, los fixtures y el helper de verificación de efectos (QA-003) son los únicos usos permitidos. El alta de usuarios no usa esta conexión: la fila del rol por defecto la inserta un trigger de base de datos (SEC-004).
**Verifica:** LINT · la conexión privilegiada solo se importa desde las ubicaciones permitidas

#### DB-014 · NEVER · Identidad de sesión aislada
**Regla:** Nunca fijar rol ni claims con `SET` de sesión ni `set_config` no local: solo configuración local dentro de una transacción explícita. Nunca compartir una sesión entre tareas concurrentes ni pasarla a tareas en segundo plano: cada tarea abre la suya.
**Por qué:** Con pool de conexiones, una configuración de sesión filtra la identidad de un usuario al request de otro; una sesión compartida entre tareas concurrentes mezcla transacciones.
**Detalle:** Para forzar la reutilización de la conexión, el test usa un pool de una sola conexión, en un motor propio y serializado (B.7).
**Verifica:** TEST · dos requests consecutivos de usuarios distintos sobre la misma conexión no comparten identidad · LINT · regla propia (Anexo B.4)

#### DB-015 · NEVER · Consultas N+1
**Regla:** Nunca consultar dentro de un bucle. Las relaciones del ORM lanzan error ante carga perezosa; toda relación necesaria se carga explícitamente en el repositorio. Filtrar, agregar y paginar en SQL, nunca en memoria.
**Por qué:** El N+1 degrada el rendimiento en silencio y dispara la facturación; con carga perezosa prohibida, se vuelve un error visible en los tests.
**Verifica:** TEST · la configuración de carga perezosa hace fallar cualquier N+1 · LINT · llamadas al repositorio dentro de bucles

#### DB-016 · MUST · Transacciones y operaciones entre sistemas
**Regla:** Cambios en varias tablas: una sola transacción. Operaciones que cruzan sistemas (DB + API externa, como Auth o pagos) no son atómicas: se diseñan como pasos idempotentes y reintentables, con estado registrado para retomar.
**Por qué:** Una API externa no participa de la transacción de la base de datos; prometer atomicidad deja datos a medio procesar.
**Verifica:** TEST · falla simulada a mitad del flujo + reintento → estado final correcto

#### DB-017 · MUST · Tiempo y dinero
**Regla:** Las fechas se guardan con zona horaria y en UTC; se muestran en la zona del usuario (por defecto, la de Chile continental). Los montos en CLP se guardan como enteros; otras monedas, como decimal exacto con su código de moneda. Nunca números de punto flotante para dinero.
**Por qué:** Los errores de zona horaria y de redondeo son silenciosos y aparecen justo en reportes y cobros.
**Verifica:** LINT · revisión de migraciones: rechaza tipos de fecha sin zona y flotantes en columnas monetarias

#### DB-018 · NEVER · PII real fuera de producción
**Regla:** Nunca usar datos personales reales en seeds, fixtures, tests, entornos locales ni staging. Solo datos sintéticos. Una copia de producción hacia otro entorno solo se hace anonimizada.
**Por qué:** Cada copia de datos reales multiplica la superficie de una brecha y es un tratamiento sin finalidad legítima.
**Verifica:** REVIEW · CI · el seed solo contiene dominios de prueba

#### DB-019 · MUST · [datos_personales] Columnas PII marcadas
**Regla:** Toda columna con datos personales lleva el comentario `pii:<categoría>` en su migración (`identificacion`, `contacto`, `financiero`, `ubicacion`, `sensible`, `tecnico`). El inventario de datos se genera desde estos comentarios.
**Por qué:** La autoridad fiscaliza inventarios y registros; generado desde el esquema, el inventario nunca queda desactualizado.
**Detalle:** `tecnico` cubre IP, identificadores de dispositivo y agente de usuario. Un UUID de usuario es dato personal cuando es el **sujeto** del dato (por ejemplo, `user_id` de `consents`, `audit_logs` y `user_roles`): se marca `pii:identificacion`. Las columnas de atribución (`created_by`, `updated_by`, `deleted_by`) no se marcan. Que un UUID sea dato personal es un criterio legal: queda registrado en un ADR para revisión de un abogado (PRIV-006).
**Verifica:** CI · revisión de migraciones: columna con nombre típico de PII sin comentario → falla

#### DB-020 · MUST · `SCHEMA_MAP.md` generado
**Regla:** `docs/SCHEMA_MAP.md` se genera desde el esquema (tablas, columnas, comentarios PII, políticas RLS, módulo dueño) y se regenera en el mismo commit que la migración. Nunca se edita a mano.
**Por qué:** Un mapa escrito a mano queda desactualizado; uno generado siempre dice la verdad.
**Verifica:** CI · regenera y falla si difiere de lo commiteado

#### DB-021 · MUST · [rut] RUT
**Regla:** El RUT nunca va en texto plano: siempre su HMAC con pepper de la configuración (búsqueda y unicidad). Con `rut: hmac+cifrado`, además cifrado con otra clave y descifrado solo donde se muestra. Módulo 11 en frontend y backend, con los mismos casos de prueba.
**Por qué:** El espacio de RUT es pequeño: un hash sin clave se revierte por fuerza bruta en segundos; el HMAC permite buscar y detectar duplicados sin exponerlo.
**Detalle:** Pedir el RUT sin necesidad está prohibido (PRIV-002).
**Verifica:** TEST · casos de referencia de Módulo 11 idénticos en ambos lados · LINT · columnas `rut` sin sufijo de HMAC o cifrado → falla

---

## 6. SEC · Seguridad

#### SEC-001 · MUST · Verificación de identidad
**Regla:** La identidad la gestiona Supabase Auth. El backend verifica cada token con las **claves públicas vigentes del proyecto** (JWKS), validando firma, expiración, emisor y audiencia. Nunca se usa un secreto compartido de larga vida si existe una alternativa rotable.
**Por qué:** Las claves asimétricas rotan sin cortar sesiones y el backend no necesita conocer ningún secreto de firma.
**Verifica:** TEST · token expirado, con firma inválida o de otro proyecto → 401

#### SEC-002 · MUST · Claves de Supabase
**Regla:** El frontend usa solo la clave publicable. La clave secreta vive solo en el backend, solo la usa la conexión privilegiada (DB-013) y nunca aparece en logs, respuestas ni en el frontend. Se usa el sistema de claves vigente recomendado por Supabase.
**Por qué:** La clave secreta ignora RLS: su filtración expone toda la base de datos.
**Verifica:** CI · escaneo del bundle del frontend en busca de claves secretas

#### SEC-003 · MUST · Protegido por defecto
**Regla:** Todo endpoint exige autenticación, salvo los de una lista pública explícita en el código (login, registro, recuperación de contraseña, `/og`, `/health`, webhooks). Los endpoints protegidos usan la dependencia de usuario actual o la de rol requerido.
**Por qué:** Un endpoint nuevo olvidado debe quedar cerrado, no abierto (principio 3).
**Verifica:** TEST · recorre todas las rutas del OpenAPI: sin token → 401, salvo la lista pública

#### SEC-004 · MUST · Rol consultado en cada request
**Regla:** El rol se obtiene en cada request desde la tabla `user_roles` (un rol activo por usuario, garantizado por un índice único parcial), nunca desde claims del token. Los roles disponibles se definen por proyecto.
**Por qué:** La revocación de un rol es inmediata; con claims, un admin degradado sigue siéndolo hasta que su token expire.
**Detalle:** `user_roles` lleva `user_id` (referencia al usuario de Auth) y `role` (restringido a los roles del proyecto), más las columnas canónicas de DB-006. El índice único parcial es sobre `user_id` donde `is_deleted = false`: quitar un rol es un borrado lógico y reasignarlo no choca con el índice. RLS: cada usuario lee su propia fila; los roles los gestionan los admin como el usuario (DB-011) y el script de SEC-021. El rol `user` se asigna al registrarse con un trigger sobre la tabla de usuarios de Auth (función `security definer` en un esquema no expuesto) que deja su propia fila en `audit_logs`; es SQL sobre el esquema de Auth, así que exige un ADR (DOC-002). Un usuario sin fila de rol activa no accede a nada.
**Verifica:** TEST · degradar un rol → el siguiente request ya es rechazado · TEST · un usuario nuevo recibe el rol `user`; sin fila, no accede

#### SEC-005 · MUST · Autorización en el backend
**Regla:** Toda decisión de autorización la toma el backend, con RLS como segunda capa. El frontend solo oculta o muestra elementos por comodidad de uso; nunca es la barrera.
**Por qué:** El frontend es completamente manipulable por el usuario.
**Verifica:** TEST · llamadas directas a la API sin pasar por la UI respetan los permisos

#### SEC-006 · MUST · Propiedad de recursos
**Regla:** Toda lectura o modificación de un recurso filtra por su dueño (o por el permiso que corresponda) además de RLS. Un recurso ajeno responde `404`, nunca `403`.
**Por qué:** Evita el acceso por cambio de ID en la URL (IDOR) sin revelar que el recurso existe.
**Verifica:** TEST · un usuario pide el recurso de otro → 404

#### SEC-007 · MUST · MFA para administradores
**Regla:** Los endpoints y vistas de administración exigen una sesión con segundo factor verificado, y también las políticas RLS de administración (`aal2` en el token). Sin segundo factor, un usuario con rol admin recibe `403`.
**Por qué:** Una cuenta de administrador comprometida expone datos personales y auditoría de todos los usuarios.
**Verifica:** TEST · admin sin segundo factor → 403 · TEST · con `aal1`, las políticas de admin no devuelven filas ajenas

#### SEC-008 · MUST · Protecciones de autenticación
**Regla:** Las protecciones nativas de Supabase Auth se mantienen activas. Login, registro y recuperación de contraseña responden de forma idéntica exista o no la cuenta. Ningún paso de autenticación exige pruebas cognitivas sin una alternativa accesible.
**Por qué:** Las respuestas distintas permiten enumerar usuarios; los CAPTCHAs sin alternativa incumplen accesibilidad.
**Verifica:** TEST · respuestas idénticas con email existente e inexistente

#### SEC-009 · MUST · Sesión en el frontend
**Regla:** La sesión la gestiona el cliente oficial de Supabase con su almacenamiento estándar, tokens de vida corta y renovación automática. Nunca copiar tokens a otro almacenamiento ni a cookies legibles desde JavaScript. Cookies de servidor exigen `perfil:bff`.
**Por qué:** La defensa real contra el robo de sesión es impedir la ejecución de scripts ajenos (SEC-010), no el lugar donde se guarda el token.
**Detalle:** La vida del token de acceso, la exigencia de segundo factor y las demás protecciones de Auth se fijan en la configuración de cada entorno y se registran en un ADR del proyecto; el estándar no impone un número.
**Verifica:** LINT · detecta lecturas o escrituras manuales de tokens

#### SEC-010 · MUST · CSP y headers de seguridad
**Regla:** CSP estricta en el frontend: scripts solo del propio origen, sin `unsafe-inline` ni `unsafe-eval`; conexiones solo a la API y a Supabase; sin embebido en frames ajenos. Además HSTS, `nosniff`, Referrer-Policy restrictiva y Permissions-Policy mínima, también en la API.
**Por qué:** Es la defensa principal contra XSS y el pilar que sostiene SEC-009.
**Verifica:** CI · verifica los headers contra el despliegue de preview

#### SEC-011 · NEVER · HTML o código sin sanitizar
**Regla:** Nunca inyectar HTML en el DOM sin pasarlo antes por un sanitizador, ni ejecutar código construido dinámicamente (`eval` y equivalentes).
**Por qué:** Es la puerta de entrada del XSS.
**Verifica:** LINT

#### SEC-012 · MUST · CORS explícito
**Regla:** Los orígenes permitidos se leen de la configuración. Nunca el comodín en producción; `localhost` solo en desarrollo. Métodos y headers permitidos, los mínimos necesarios.
**Por qué:** Un CORS abierto permite que cualquier sitio use la API con la sesión del usuario.
**Verifica:** TEST · un origen no permitido es rechazado

#### SEC-013 · NEVER · SQL construido con strings
**Regla:** Nunca interpolar ni concatenar valores en SQL. Siempre parámetros enlazados, ya sea con el ORM o con SQL parametrizado. Identificadores dinámicos (columnas de orden) solo desde una lista permitida.
**Por qué:** Inyección SQL.
**Verifica:** LINT · regla de detección de SQL construido con strings

#### SEC-014 · MUST · Requests salientes con URL del usuario
**Regla:** URLs aportadas por usuarios: solo `https`; host idéntico a uno de la lista permitida (nunca por prefijo); resolver la IP y rechazar rangos privados, loopback, link-local y metadatos; no seguir redirecciones a hosts no permitidos.
**Por qué:** SSRF. Una validación por prefijo como "empieza con `https://dominio.com`" deja pasar `https://dominio.com.atacante.net`.
**Verifica:** TEST · casos de bypass conocidos son rechazados

#### SEC-015 · MUST · [uploads] Archivos subidos
**Regla:** Buckets privados y URLs firmadas de corta duración. El backend valida tamaño y tipo real por contenido (no por extensión), renombra con un ID propio y elimina el EXIF antes de guardar. Las políticas de storage siguen las reglas de RLS.
**Por qué:** Los archivos son vector de ejecución de código, de fuga de datos y, en las fotos, de ubicación geográfica del usuario.
**Verifica:** TEST · archivo con extensión falsa → rechazo; imagen guardada sin EXIF

#### SEC-016 · MUST · Gestión de secretos
**Regla:** Secretos solo en la configuración de la plataforma y en `.env` local, nunca en el repo; `.env.example` con placeholders sí se versiona. Escaneo de secretos en pre-commit y CI. Ante sospecha de filtración: rotar primero. Nunca secretos en URLs, logs ni errores.
**Por qué:** Un secreto en el historial de Git es público para siempre.
**Verifica:** CI · escaneo de secretos · HOOK · pre-commit

#### SEC-017 · MUST · IP real detrás del proxy
**Regla:** El backend obtiene la IP del cliente desde el header de reenvío **solo** cuando proviene del proxy de la plataforma de despliegue, configurado como confiable. Esa IP es la que usan el rate limit y la auditoría.
**Por qué:** Sin esto, todos los requests parecen venir de la IP del proxy: el rate limit se vuelve global y la auditoría registra una IP inútil.
**Verifica:** TEST · requests con distinto header de reenvío desde el proxy tienen límites independientes

#### SEC-018 · MUST · Rate limit
**Regla:** Rate limit en todo endpoint, por IP real (SEC-017) y además por usuario si hay sesión: más estricto en autenticación, intermedio en escritura, amplio en lectura. Valores desde la configuración, nunca fijos en el código. Exceso: `429` con envelope.
**Por qué:** Frena la fuerza bruta, el scraping y el abuso de costos.
**Verifica:** TEST · superar el límite → 429

#### SEC-019 · MUST · Configuración segura en producción
**Regla:** En producción: modo debug desactivado, documentación interactiva de la API desactivada o protegida, sin endpoints de prueba ni datos semilla. El backend verifica estas condiciones al arrancar en producción y se niega a iniciar si no se cumplen.
**Por qué:** La mala configuración es una de las causas más frecuentes de brechas; verificarla al arrancar la vuelve imposible de olvidar.
**Verifica:** TEST · arranque con configuración de producción insegura falla

#### SEC-020 · MUST · Cadena de suministro
**Regla:** Las dependencias se instalan siempre desde un lockfile versionado. Las acciones de CI se fijan por hash de commit, no por etiqueta. El escaneo de vulnerabilidades bloquea el merge ante severidad alta o crítica. Las actualizaciones automáticas de seguridad están habilitadas.
**Por qué:** Un paquete o una acción comprometida ejecuta código dentro del pipeline con acceso a los secretos del proyecto.
**Verifica:** CI

#### SEC-021 · ASK · Primer administrador
**Regla:** El primer administrador se asigna con un script de arranque, fuera del ciclo HTTP y con la conexión privilegiada, solo tras aprobación humana explícita, a un usuario de Auth que ya existe. Después enrola su segundo factor; sin él no accede a administración (SEC-007).
**Por qué:** Con RLS estricto no hay camino interactivo para crear al primero; un script puntual evita abrir una puerta trasera en la API.
**Detalle:** El script es un contexto declarado de DB-013, no lo invoca ningún endpoint y su ejecución queda en `audit_logs`. Los roles siguientes los asigna un admin como el usuario, bajo RLS (DB-011). El script recibe el `user_id` o el email de un usuario ya existente en Auth (creado por el flujo normal de registro o invitación) y le asigna el rol `admin`; no crea credenciales ni inventa contraseñas.
**Verifica:** TEST · el script asigna el rol y registra la auditoría; con un usuario inexistente falla sin crear nada · LINT · ningún endpoint lo importa (DB-013)

#### SEC-022 · NEVER · Quedarse sin administradores
**Regla:** Nunca permitir que el último administrador activo se degrade, se desactive, se bloquee o se dé de baja, ni él mismo ni otro admin: la operación se rechaza con `409`.
**Por qué:** Sin administradores el sistema queda sin gestión, y recuperarlo exige repetir el arranque con acceso privilegiado a la base de datos.
**Detalle:** La comprobación y el cambio ocurren en la misma transacción, con bloqueo de las filas de roles, para que dos degradaciones simultáneas no dejen el sistema sin admin.
**Verifica:** TEST · degradar, desactivar o dar de baja al único admin → 409 · TEST · dos admins que se degradan a la vez no dejan el sistema sin admin

### 6.1 Referencia: cobertura OWASP Top 10 (edición vigente)

Tabla de consulta, no normativa: muestra qué reglas cubren cada categoría.

| Categoría OWASP | Reglas |
|---|---|
| Control de acceso roto (incluye SSRF) | SEC-003 a SEC-007, SEC-014, SEC-021, SEC-022, DB-009 a DB-013 |
| Configuración de seguridad incorrecta | SEC-010, SEC-012, SEC-019, ARQ-016 |
| Fallas en la cadena de suministro | SEC-020, PRO-005 |
| Fallas criptográficas | SEC-001, SEC-016, DB-021 |
| Inyección (SQL, XSS) | SEC-011, SEC-013, API-008, API-010 |
| Diseño inseguro | Principios 2 y 3, API-011, DB-016 |
| Fallas de autenticación | SEC-001, SEC-007, SEC-008, SEC-018 |
| Fallas de integridad de software o datos | API-012, SEC-020 |
| Fallas de registro y alertas | API-013, Sección 11 (OPS) |
| Manejo incorrecto de condiciones excepcionales | Principio 3, API-005, ARQ-016 |

---

## 7. PRIV · Privacidad y protección de datos (Ley 21.719)

> **Marco:** normativa chilena de protección de datos personales vigente (Ley 21.719, que modifica la Ley 19.628). Las referencias a artículos son orientativas. Donde la autoridad aún no ha dictado instrucciones, este estándar adopta el criterio más conservador razonable. La IA construye estructuras técnicas; **nunca redacta textos legales ni decide plazos legales**: los solicita al humano.
>
> **Relación con el Playbook de Privacidad:** el playbook define qué exige la ley a cada proyecto (con criterios de aceptación); esta sección define cómo se cumple en el stack de oro y no repite esos criterios.

#### PRIV-001 · MUST · [datos_personales] Minimización
**Regla:** Solo se recolecta el dato personal estrictamente necesario para una finalidad declarada. Toda columna con PII tiene su finalidad registrada en `docs/PRIVACY_POLICY_NOTES.md` (PRIV-006). No se recolecta "por si acaso".
**Por qué:** Principio de proporcionalidad (Art. 3); lo que no se recolecta no puede filtrarse.
**Verifica:** CI · toda columna `pii:*` (DB-019) tiene finalidad registrada

#### PRIV-002 · NEVER · [datos_personales] Identificadores nacionales sin necesidad
**Regla:** Nunca pedir el RUT u otro identificador nacional si la función no lo exige por obligación legal, tributaria o de validación financiera.
**Por qué:** Es un identificador universal: su exposición facilita suplantación y cruce de bases de datos.
**Verifica:** REVIEW

#### PRIV-003 · MUST · [datos_personales] Privacidad por defecto
**Regla:** Toda opción que afecte datos personales viene configurada en su valor más protector: marketing desactivado, visibilidad mínima, perfilamiento desactivado. El usuario amplía; nunca restringe lo que vino abierto.
**Por qué:** Privacidad desde el diseño y por defecto (Art. 14 quáter).
**Verifica:** TEST · valores por defecto de preferencias

#### PRIV-004 · MUST · [datos_personales] Consentimiento afirmativo y granular
**Regla:** El consentimiento se obtiene con una acción afirmativa, por separado para cada finalidad (términos, política de privacidad, marketing, perfilamiento), con el enlace al documento junto a la casilla. Nunca casillas premarcadas ni consentimientos agrupados.
**Por qué:** Un consentimiento no libre, no específico o no informado no es válido (Art. 12).
**Verifica:** TEST · E2E del registro: casillas desmarcadas por defecto y separadas

#### PRIV-005 · MUST · [datos_personales] Registro probatorio del consentimiento
**Regla:** Cada consentimiento se registra en `consents` (titular, tipo y versión exacta del documento, fecha, IP, agente). Lo inserta solo el backend. Revocar marca `revoked_at` sin tocar el resto. Lectura: el titular lo suyo, el admin todo. Sin soft delete.
**Por qué:** El responsable debe poder **probar** el consentimiento; si el cliente inserta el registro, puede fabricar su propia evidencia.
**Detalle:** Los tipos de consentimiento son un conjunto cerrado en la migración (restricción de valores): los iniciales son los que el proyecto necesita (como `terminos` y `privacidad`) y agregar uno exige una migración. Una declaración de mayoría de edad se registra como un tipo propio (`declaracion_mayoria_edad`) y se documenta en un ADR, porque no es estrictamente un consentimiento. La IP se almacena truncada (IPv4 a /24, IPv6 a /48). Tras una supresión (PRIV-011), el registro se conserva y deja de identificar a la persona, porque su usuario queda anonimizado.
**Verifica:** TEST · el cliente no puede insertar en `consents`; la revocación solo altera `revoked_at` · TEST · un tipo fuera del conjunto cerrado se rechaza

#### PRIV-006 · MUST · [datos_personales] Registro de tratamiento vivo
**Regla:** `docs/PRIVACY_POLICY_NOTES.md` se mantiene al día: inventario de datos (generado, DB-019); finalidad, base de licitud y plazo por tratamiento; proveedores con su región y base de transferencia. Plazos y bases los define el humano.
**Por qué:** Es el insumo de la política de privacidad y la evidencia operativa que la autoridad fiscaliza.
**Detalle:** Es el Registro de Actividades de Tratamiento (RAT) que exige el Playbook de Privacidad, organizado por finalidad. Cada plazo de retención se ejecuta con un job programado (OPS-009).
**Verifica:** CI · la sección de inventario coincide con el esquema · REVIEW

#### PRIV-007 · MUST · [datos_personales] Documentos legales accesibles
**Regla:** Vistas de Términos y de Política de Privacidad accesibles siempre, sin sesión y gratis, enlazadas en el registro y en toda acción que pida consentimiento. La IA crea la estructura y pide el texto al humano; nunca redacta cláusulas legales.
**Por qué:** Deber de transparencia (Art. 14 ter); un texto legal inventado por una IA es un riesgo, no una solución.
**Verifica:** TEST · E2E: las vistas responden sin sesión

#### PRIV-008 · ASK · [datos_personales] Nuevo proveedor que trata datos
**Regla:** Antes de integrar cualquier servicio externo que reciba datos personales (email transaccional, analítica, error tracking, LLM, almacenamiento): registrar dónde procesa los datos y la base de licitud de la transferencia internacional en PRIV-006, y esperar aprobación.
**Por qué:** Enviar datos a un proveedor fuera de Chile es una transferencia internacional sujeta a garantías (Arts. 27-28).
**Verifica:** CI · revisión del perfil: detecta SDKs de proveedores no registrados

#### PRIV-009 · MUST · [datos_personales] Acceso y portabilidad
**Regla:** El titular puede descargar sus datos en un formato estructurado y legible por máquina (JSON): perfil, preferencias, consentimientos y sus propios registros de auditoría. Es gratuito y no requiere pasos adicionales más allá de su sesión.
**Por qué:** Derechos de acceso y portabilidad (Arts. 5 y 9).
**Verifica:** TEST · el export contiene todas las tablas del titular marcadas con PII

#### PRIV-010 · MUST · [datos_personales] Rectificación, oposición y bloqueo
**Regla:** La UI muestra los datos tratados y permite: rectificarlos; oponerse con un interruptor a tratamientos no esenciales (marketing, perfilamiento); y bloquear temporalmente el tratamiento mientras se resuelve una solicitud.
**Por qué:** Derechos del titular (Arts. 6 y 8); el bloqueo exige que el sistema pueda "congelar" el uso de los datos sin borrarlos.
**Detalle:** El bloqueo es un estado del titular que detiene todo uso no esencial de sus datos sin borrarlos.
**Verifica:** TEST · con el tratamiento bloqueado u opuesto, los procesos no esenciales excluyen al titular

#### PRIV-011 · MUST · [datos_personales] Supresión mediante anonimización irreversible
**Regla:** Suprimir = anonimizar: cada campo PII pasa a nulo o a un valor aleatorio no derivado del original (se conservan UUID e `is_deleted`). En Auth, el usuario queda inutilizable y sin identidades (email, OAuth), y el titular puede registrarse de nuevo como uno nuevo. Nunca hashes.
**Por qué:** La anonimización exige romper el vínculo con la persona (Art. 2 lit. k). Un hash del email o del RUT es reproducible y revertible por diccionario: es seudonimización (lit. l), no anonimización. Si Auth conserva el email o una identidad de proveedor, el vínculo tampoco se rompe. La supresión no es una sanción: el titular debe poder volver a registrarse.
**Detalle:** Incluye la baja de cuenta y revocar todas las sesiones. El usuario de Auth se conserva como cascarón anonimizado y bloqueado (nunca se elimina, DB-008); ninguna identidad previa (email, OAuth, SAML) puede autenticarlo ni conserva atributos del proveedor. El re-registro crea un usuario nuevo e independiente. El flujo es idempotente, por pasos y con estado registrado (DB-016). El mecanismo para desvincular identidades se decide en un ADR del proyecto según lo que permita la API de administración vigente; si exige SQL sobre el esquema de Auth, es ASK. Conservar identificadores para impedir la evasión de sanciones es una decisión de producto con base legal y plazo definidos por el humano (como en PRIV-012) y exige ADR; no es el comportamiento por defecto.
**Verifica:** TEST · con un usuario de email y otro de OAuth: tras la baja, sin valores derivables de la PII en tablas ni en Auth, el login previo falla y el re-registro crea un usuario nuevo · REVIEW · ADR si el caso OAuth no es automatizable

#### PRIV-012 · MUST · [datos_personales] Conservación por obligación legal
**Regla:** Los datos con obligación legal de conservación (tributaria, contable, contractual) no se anonimizan al pedirse la supresión: se bloquean (acceso restringido, sin otro uso) hasta vencer su plazo; luego un job los anonimiza. Plazos: los define el humano (ASK).
**Por qué:** El derecho de supresión cede ante obligaciones legales; conservar más allá del plazo, o para otra finalidad, es un incumplimiento.
**Detalle:** Cada plazo queda registrado en `PRIVACY_POLICY_NOTES` (PRIV-006).
**Verifica:** TEST · un registro con obligación vigente queda bloqueado; vencido el plazo, el job lo anonimiza

#### PRIV-013 · MUST · Contenido de `audit_logs`
**Regla:** `audit_logs` registra quién, qué, sobre qué entidad y cuándo; su metadata solo lleva IDs, nombres de campos y valores no personales, nunca PII, contraseñas ni tokens. Inmutable salvo el job de retención (PRIV-014). Lectura bajo RLS: titular lo suyo, admin todo.
**Por qué:** La auditoría debe ser probatoria sin convertirse en una segunda base de datos de PII.
**Detalle:** El admin lee como el usuario, bajo RLS y con segundo factor (SEC-007), no con la conexión privilegiada (DB-013).
**Verifica:** TEST · la metadata de auditoría no contiene los valores de campos marcados `pii:*`

#### PRIV-014 · DEFAULT · [datos_personales] Retención de `audit_logs`
**Regla:** Pasados 24 meses (o el plazo que defina el proyecto), un job programado conserva acción, entidad y fecha, y anonimiza el usuario, la IP, el agente de usuario y cualquier valor identificable de la metadata.
**Por qué:** Conservar datos identificables más allá de su necesidad vulnera la proporcionalidad; el agregado estadístico sigue siendo útil.
**Detalle:** `audit_logs.user_id` admite vacío: vacío significa **anonimizado**; una acción del sistema lleva el UUID nulo de `system_actor_id()` (DB-006); un usuario real, su UUID. Los tres estados deben poder distinguirse.
**Verifica:** TEST · el job anonimiza solo los registros vencidos y deja intactas las acciones del sistema · REVIEW · alerta de fallo del job configurada (OPS-009)

#### PRIV-015 · NEVER · PII en logs técnicos y herramientas externas
**Regla:** Nunca registrar PII en logs técnicos, trazas, error tracking ni analítica: solo IDs. Toda herramienta de observabilidad se configura para depurar PII antes de enviar datos.
**Por qué:** Los logs se replican, se exportan y se conservan con controles más débiles que la base de datos.
**Verifica:** TEST · los logs de un flujo con PII no contienen los valores · LINT · detección de campos personales en llamadas de log

#### PRIV-016 · MUST · [datos_personales] Rastreo no esencial solo con consentimiento
**Regla:** Cookies, identificadores y scripts de analítica o marketing que no sean esenciales para el servicio se activan solo después del consentimiento específico del usuario.
**Por qué:** Son tratamiento de datos con una finalidad distinta a la del servicio.
**Verifica:** TEST · E2E: sin consentimiento no se cargan scripts de terceros de rastreo

#### PRIV-017 · ASK · [datos_personales] Datos sensibles y biométricos
**Regla:** Antes de modelar datos sensibles (salud, origen étnico, orientación sexual, afiliación política o sindical, biométricos): exigir justificación y esperar aprobación. Si se aprueba: cifrado por columna, RLS restrictiva y evaluación de impacto previa.
**Por qué:** Categoría de máxima protección (Arts. 16 y 16 ter); una brecha de estos datos causa daño grave e irreparable.
**Verifica:** CI · columnas `pii:sensible` exigen un ADR referenciado

#### PRIV-018 · ASK · [datos_personales] Titulares menores de edad
**Regla:** Al iniciar un módulo que pueda involucrar menores, preguntarlo explícitamente. Si aplica, el flujo de consentimiento de padres o representantes se diseña y aprueba antes de modelar las tablas.
**Por qué:** Régimen reforzado para niños, niñas y adolescentes (Art. 16 quáter).
**Verifica:** REVIEW · ADR

#### PRIV-019 · MUST · [datos_personales] Decisiones automatizadas y perfilamiento
**Regla:** Todo perfilamiento o decisión automatizada que afecte a una persona (puntajes, clasificaciones, huella de dispositivo antifraude) exige los tres: información clara de su existencia y lógica, interruptor de oposición y revisión humana. Sin los tres, no se implementa.
**Por qué:** Derecho de oposición y garantías ante decisiones automatizadas (Art. 8 y 8 bis).
**Detalle:** La revisión humana aplica ante decisiones que afectan significativamente al titular. Incluye recomendaciones que limitan sus opciones.
**Verifica:** REVIEW · ADR obligatorio

#### PRIV-020 · MUST · [datos_personales] Respuesta a incidentes de datos
**Regla:** `docs/INCIDENT_RESPONSE.md` define: responsables, contención, criterios de notificación, plantilla de aviso a la autoridad y a los titulares, y registro por incidente. Notificar lo decide el humano, sin dilaciones indebidas. Simulacro al menos anual.
**Por qué:** Las vulneraciones deben reportarse por los medios más rápidos posibles; improvisar el procedimiento durante un incidente garantiza llegar tarde.
**Detalle:** El registro de cada incidente incluye: detección, alcance, datos afectados, medidas y decisión de notificar.
**Verifica:** CI · el documento existe con todas sus secciones · REVIEW · registro del simulacro

#### PRIV-021 · NEVER · [llm] PII hacia modelos externos
**Regla:** Nunca enviar PII a un LLM externo sin (a) quitarla antes, o (b) una base de licitud de transferencia internacional documentada en `PRIVACY_POLICY_NOTES`.
**Por qué:** El proveedor procesa los datos fuera de Chile: es una transferencia internacional.
**Verifica:** REVIEW ítem PRIV · TEST · la capa de envío al modelo aplica el filtro de PII (IA-003)

---

## 8. UI · Frontend, mobile y accesibilidad

#### UI-001 · MUST · Estado de servidor vs estado de UI
**Regla:** Datos de la API: solo TanStack Query. Estado global de UI (tema, sidebar, modales, filtros): Zustand en slices por dominio. Estado de un componente: local. Nunca copiar datos del servidor a otro estado mediante efectos. Context solo para providers.
**Por qué:** Duplicar datos del servidor crea dos fuentes de verdad que se desincronizan y rompen la caché.
**Verifica:** LINT · detección de efectos que copian resultados de queries

#### UI-002 · MUST · Claves de caché y selectores
**Regla:** Las claves y opciones de query de endpoints salen del código generado (ARQ-010). Solo las queries que no consumen la API propia definen claves manuales, en una factory por módulo. Los selectores de Zustand que devuelven objetos nuevos usan comparación superficial.
**Por qué:** Evita claves duplicadas o inconsistentes entre módulos, y renders innecesarios.
**Verifica:** LINT

#### UI-003 · MUST · Mobile first
**Regla:** Estilos base para 360 px; los breakpoints solo amplían. Sin scroll horizontal en 360 px; objetivos táctiles de al menos 44×44 px. En móvil, tablas como tarjetas o con scroll en su propio contenedor.
**Por qué:** La mayoría del uso es móvil, y WCAG exige un tamaño mínimo de objetivo.
**Detalle:** El mínimo de WCAG es 24×24 px; este estándar exige más por uso móvil predominante.
**Verifica:** TEST · E2E en viewport de 360 px (sin desbordamiento horizontal, tamaño de objetivos)

#### UI-004 · MUST · Interacción táctil y teclado virtual
**Regla:** Ninguna acción depende solo de hover ni solo de arrastrar: siempre existe una alternativa con un toque. Los campos usan el tipo y modo de entrada correctos (numérico, email, teléfono) para mostrar el teclado adecuado.
**Por qué:** En pantallas táctiles no existe hover; el arrastre sin alternativa incumple accesibilidad.
**Verifica:** REVIEW · LINT · campos sin tipo o modo de entrada adecuado

#### UI-005 · MUST · Rendimiento en móvil
**Regla:** Rutas cargadas bajo demanda; imágenes con dimensiones y carga diferida. Core Web Vitals medidos en perfil móvil contra el umbral «bueno» vigente de Core Web Vitals. Acciones frecuentes: actualización optimista con reversión visible (DEFAULT).
**Por qué:** En redes móviles cada kilobyte y cada ida y vuelta se sienten; el rendimiento percibido es parte de la usabilidad.
**Verifica:** CI · Lighthouse en perfil móvil contra ese umbral

#### UI-006 · MUST · Cuatro estados en toda vista con datos
**Regla:** Toda vista que carga datos implementa: **carga** (skeleton con la forma del contenido, nunca vacío ni un spinner genérico en listas), **error** (mensaje accionable + botón de reintento), **vacío** (explicación + acción clara) y **datos**.
**Por qué:** Una pantalla en blanco o una lista vacía sin contexto es la experiencia más frustrante y la más común en código generado.
**Verifica:** TEST · un test por estado en cada vista principal del módulo (QA)

#### UI-007 · MUST · Manejo global de errores
**Regla:** Un manejador global: ante `401` intenta renovar la sesión y, si falla, redirige al login conservando la ruta; ante errores `5xx` o de red muestra un aviso no bloqueante con el `trace_id` disponible para soporte. Cada ruta tiene un error boundary: nunca una pantalla en blanco.
**Por qué:** El usuario nunca debe quedar atrapado; soporte necesita el `trace_id` para encontrar el error (API-013).
**Verifica:** TEST · respuestas 401 y 500 simuladas producen el comportamiento esperado

#### UI-008 · MUST · Formularios
**Regla:** Validación en tiempo real que replica al backend, con errores por campo. Un error del servidor nunca borra lo escrito. Envío deshabilitado mientras se procesa. Acciones irreversibles (eliminar la cuenta): confirmar escribiendo un texto, nunca un clic.
**Por qué:** Evita envíos duplicados, pérdida de trabajo y acciones irreversibles por accidente.
**Verifica:** TEST · por formulario principal

#### UI-009 · MUST · Accesibilidad
**Regla:** WCAG 2.x AA vigente. Mínimos: etiqueta en todo campo (el placeholder no lo es); nombre accesible en botones de ícono; errores anunciados; todo operable con teclado; foco nunca tapado; contraste AA; acciones solo en `button` o `a`.
**Por qué:** Es un derecho de los usuarios y un requisito creciente en contratos y licitaciones.
**Verifica:** TEST · análisis automático de accesibilidad (axe) en los tests de componentes y E2E

#### UI-010 · MUST · Tokens de diseño
**Regla:** Colores, tipografía, espaciado, radios y sombras se definen una sola vez como tokens, en el mecanismo vigente del framework de estilos. Los componentes usan solo tokens, nunca valores arbitrarios. Colores de marca: se piden al humano.
**Por qué:** Consistencia visual y un solo lugar para cambiar la identidad del producto.
**Verifica:** LINT · detección de valores arbitrarios en clases y estilos

#### UI-011 · MUST · Tema claro, oscuro y del sistema
**Regla:** Todo componente funciona en tema claro y oscuro; el valor por defecto sigue la preferencia del sistema. La elección del usuario se persiste y se aplica antes del primer render, sin destello.
**Por qué:** La estética es de cada proyecto; el soporte de ambos temas es un mínimo de calidad y accesibilidad.
**Verifica:** TEST · captura visual en ambos temas para los componentes compartidos

#### UI-012 · DEFAULT · Biblioteca de componentes
**Regla:** Los componentes base se construyen sobre shadcn/ui (primitivas accesibles, estilado con los tokens). Modales, menús y selectores siempre sobre primitivas accesibles, nunca desde cero.
**Por qué:** Foco atrapado, cierre con Escape y navegación con teclado son difíciles de hacer bien; las primitivas ya lo resuelven.
**Verifica:** REVIEW

#### UI-013 · MUST · Idioma y formatos locales
**Regla:** Interfaz en español; mensajes claros, accionables y sin jerga técnica. Fechas, números y moneda con formato de Chile (CLP sin decimales y con separador de miles), mostrados en la zona horaria del usuario (DB-017).
**Por qué:** El formato incorrecto de fechas y montos genera errores de interpretación con consecuencias reales.
**Verifica:** TEST · utilidades de formato compartidas

#### UI-014 · MUST · [rut] Campo RUT
**Regla:** El campo de RUT se formatea mientras se escribe, usa el teclado adecuado y muestra su validez (Módulo 11, DB-021) a partir del segundo carácter. El error dice "RUT inválido" y nunca revela si el RUT existe en el sistema.
**Por qué:** Reduce errores de ingreso sin filtrar información.
**Verifica:** TEST · casos de referencia de Módulo 11

---

## 9. IA · Modelos de IA dentro del producto

#### IA-001 · MUST · [llm] Solo desde el backend
**Regla:** Toda llamada a un modelo de IA se hace desde el backend. Las claves del proveedor nunca llegan al frontend.
**Por qué:** Una clave en el frontend es una tarjeta de crédito pública.
**Verifica:** CI · escaneo del bundle en busca de claves y SDKs de proveedores de IA

#### IA-002 · MUST · [llm] Cuotas y límites de costo
**Regla:** Toda funcionalidad de IA tiene: límite de uso por usuario y global, máximo de tokens por request, tiempo máximo de respuesta y alertas de gasto. Los valores se leen de la configuración.
**Por qué:** Sin límites, un usuario o un bucle puede generar una factura ilimitada.
**Verifica:** TEST · superar la cuota → rechazo controlado

#### IA-003 · MUST · [llm] Instrucciones separadas de los datos
**Regla:** Las instrucciones del sistema no se construyen con input del usuario. El input y todo contenido externo (documentos, páginas web, emails, resultados de herramientas) se envían delimitados como **datos no confiables**. Antes de enviarse, pasan por el filtro de PII (PRIV-021).
**Por qué:** Prompt injection directa e indirecta: el contenido externo puede contener instrucciones maliciosas.
**Verifica:** TEST · evals con casos de inyección (IA-009)

#### IA-004 · MUST · [llm] La salida del modelo no es confiable
**Regla:** La salida se valida contra un schema (salida estructurada + validación en el backend) antes de usarse. Nunca se ejecuta, se renderiza como HTML sin sanitizar, ni se usa para construir SQL, comandos o URLs sin validación.
**Por qué:** El modelo puede alucinar, ser manipulado o devolver formato inválido.
**Verifica:** TEST · respuestas malformadas o maliciosas simuladas son rechazadas

#### IA-005 · NEVER · [llm] Herramientas con privilegios
**Regla:** Si el modelo invoca herramientas o acciones, lo hace con los permisos del usuario (DB-012), nunca con la conexión privilegiada. Toda acción con efectos (escribir, enviar, pagar, borrar) requiere confirmación explícita del usuario antes de ejecutarse.
**Por qué:** Un modelo manipulado con privilegios elevados es una escalada de privilegios automatizada.
**Verifica:** TEST · una herramienta invocada por el modelo no accede a datos de otro usuario

#### IA-006 · MUST · [llm] El modelo propone, no decide sobre personas
**Regla:** Las decisiones que afectan significativamente a una persona (aprobar, rechazar, puntuar, clasificar) no las toma el modelo solo: el modelo propone y decide una persona o una regla determinística auditable, con las garantías de PRIV-019.
**Por qué:** Responsabilidad, explicabilidad y cumplimiento de las garantías ante decisiones automatizadas.
**Verifica:** REVIEW · ADR

#### IA-007 · MUST · [llm] Transparencia ante el usuario
**Regla:** El usuario sabe cuándo interactúa con un sistema de IA y cuándo un contenido fue generado por IA.
**Por qué:** Confianza y deber de información.
**Verifica:** REVIEW

#### IA-008 · MUST · [llm] Prompts versionados y trazables
**Regla:** Los prompts viven como archivos versionados en el módulo que los usa, nunca como strings dispersos. Cada llamada registra el modelo, la versión del prompt, los tokens, el costo, la latencia y el resultado de la validación, sin PII (PRIV-015).
**Por qué:** Sin trazabilidad no se puede depurar, auditar costos ni comparar versiones.
**Verifica:** TEST · el log de una llamada contiene los campos requeridos

#### IA-009 · MUST · [llm] Evaluaciones automatizadas
**Regla:** Cada funcionalidad de IA tiene un conjunto de casos de evaluación (entradas representativas, casos límite y de inyección, con criterios de aceptación) que se ejecuta en CI al cambiar el prompt, el modelo o sus parámetros.
**Por qué:** Un cambio de prompt o de modelo puede degradar la calidad en silencio; las evaluaciones son los tests de la IA.
**Verifica:** CI

#### IA-010 · MUST · [llm] Degradación controlada
**Regla:** Si el proveedor falla, excede el tiempo o la cuota, la funcionalidad se degrada con un mensaje claro y el resto del producto sigue operando. Los reintentos son acotados y con espera creciente.
**Por qué:** Un servicio externo caído no puede arrastrar al producto completo.
**Verifica:** TEST · proveedor simulado caído → degradación correcta

#### IA-011 · DEFAULT · [llm] Proveedor y modelo configurables
**Regla:** El proveedor y el modelo se definen en la configuración, detrás de una interfaz propia del backend. Cambiar de modelo es un cambio de configuración que debe pasar las evaluaciones (IA-009).
**Por qué:** Los modelos cambian rápido; el acoplamiento a uno específico encarece cada mejora.
**Verifica:** REVIEW

---

## 10. QA · Calidad y tests

#### QA-001 · MUST · Sin tests no está terminado
**Regla:** Todo código nuevo o modificado incluye sus tests en el mismo PR. Una funcionalidad sin tests no está terminada, aunque funcione.
**Por qué:** Los tests escritos "después" no se escriben.
**Verifica:** CI · gate de cobertura (QA-007) · REVIEW

#### QA-002 · MUST · Casos mínimos por endpoint
**Regla:** Todo endpoint tiene tests para: caso feliz; sin autenticación (`401`); rol insuficiente (`403`); recurso ajeno (`404`); entrada inválida (`422`); cada regla de negocio (`400`/`409`); y, si modifica datos, que la eliminación es lógica y que la acción quedó en `audit_logs`.
**Por qué:** Son exactamente los casos que el código generado por IA omite con más frecuencia.
**Detalle:** Los endpoints de la lista pública (SEC-003) se exceptúan de los casos `401`, `403` y `404`; necesitan el caso feliz y los suyos propios (por ejemplo, el `503` de `/health`, OPS-004).
**Verifica:** CI · revisión de la matriz de tests: cruza el OpenAPI con los tests

#### QA-003 · MUST · Base de datos real en tests de integración
**Regla:** Los tests de endpoints usan una base de datos real, con RLS y GRANTs activos, nunca mockeada. Los fixtures pueden sembrar con la conexión privilegiada; la llamada y su aserción pasan por el cliente HTTP, como el actor que corresponda (DB-012).
**Por qué:** Un mock no detecta errores de RLS, GRANTs, restricciones ni queries mal formadas; y una aserción hecha con privilegios aprobaría justo lo que RLS debería bloquear.
**Detalle:** Los tests de services pueden mockear el repositorio y los servicios externos. Una lectura privilegiada posterior solo verifica efectos que el actor no puede ver por diseño (marca de borrado lógico, auditoría, QA-002), siempre desde un único helper de verificación de efectos, de solo lectura; nunca el resultado que el actor debe ver u obtener.
**Verifica:** LINT · los tests de endpoints no importan mocks de sesión de base de datos ni usan la conexión privilegiada fuera de fixtures y del helper de efectos (Anexo B.4)

#### QA-004 · MUST · Aserciones profundas
**Regla:** Un test verifica la estructura completa de la respuesta y los efectos reales (filas en la base de datos, registro de auditoría, estado del store), no solo el código HTTP.
**Por qué:** `status_code == 200` pasa aunque la respuesta esté vacía o el dato no se haya guardado.
**Verifica:** LINT · tests cuya única aserción es el código de estado

#### QA-005 · MUST · Casos mínimos por módulo frontend
**Regla:** Todo módulo frontend tiene tests para: renderizado sin errores; los cuatro estados (UI-006); la acción principal; y análisis automático de accesibilidad (UI-009).
**Por qué:** Cubre las fallas visibles más frecuentes con pocos tests.
**Verifica:** CI · cobertura por módulo

#### QA-006 · MUST · E2E mínimo
**Regla:** Existen pruebas de extremo a extremo para: inicio de sesión, el flujo principal del producto y, si hay datos personales, la exportación y la baja de cuenta. Se ejecutan en viewport móvil (360 px) y de escritorio.
**Por qué:** Verifican que las piezas funcionan juntas, en el dispositivo que más se usa.
**Verifica:** CI

#### QA-007 · MUST · Gate de cobertura
**Regla:** El CI falla si la cobertura de líneas del backend o del frontend baja del umbral definido en la configuración, que nunca es menor a 80 %. La cobertura nunca baja respecto de la rama base.
**Por qué:** Una regla de cobertura sin gate es una aspiración.
**Verifica:** CI

#### QA-008 · MUST · Suites transversales de seguridad
**Regla:** El proyecto mantiene tres suites que corren siempre, en todo PR: RLS por tabla (DB-009), rutas protegidas (SEC-003) y contratos de respuesta (API-004, API-005, API-009).
**Por qué:** Detectan automáticamente la tabla, el endpoint o el campo nuevo que alguien olvidó proteger.
**Verifica:** CI

#### QA-009 · MUST · Tests deterministas e independientes
**Regla:** Los tests usan datos sintéticos (DB-018), no dependen del orden de ejecución, de la hora real ni de servicios externos reales (se simulan). Un test que falla de forma intermitente se corrige o se elimina; nunca se reintenta hasta que pase.
**Por qué:** Un test poco confiable enseña a ignorar el CI.
**Verifica:** CI · ejecución en orden aleatorio

#### QA-010 · MUST · Todo bug trae su test
**Regla:** Toda corrección de un bug incluye un test que lo reproduce y que falla sin la corrección.
**Por qué:** Evita que el mismo bug vuelva.
**Verifica:** REVIEW

#### QA-011 · MUST · Primero el camino alternativo
**Regla:** Al implementar una función se manejan primero los casos de nulo, vacío, falla de la base de datos, tiempo agotado y entrada inesperada, con retornos tempranos; después el caso feliz.
**Por qué:** El código generado tiende a cubrir solo el caso feliz (principio 3).
**Verifica:** REVIEW · tests de QA-002

#### QA-012 · MUST · Tipado estricto y lint
**Regla:** El type-check estricto y los linters corren en pre-commit y en CI, en backend y frontend, y bloquean el merge.
**Por qué:** Detecta errores antes de ejecutar el código.
**Verifica:** CI · HOOK · pre-commit

#### QA-013 · MUST · Complejidad acotada
**Regla:** Los límites de complejidad (largo de funciones, complejidad ciclomática, profundidad de anidación, cantidad de dependencias por archivo) se definen en la configuración del linter. Superarlos obliga a dividir o refactorizar.
**Por qué:** Una función que no se puede explicar de forma simple no se puede mantener ni auditar.
**Verifica:** LINT

#### QA-014 · NEVER · Malos olores de código
**Regla:** Nunca: excepciones capturadas y silenciadas; números o textos mágicos sin una constante con nombre; aserciones de tipo o tipos "cualquiera" para silenciar el compilador; código comentado; TODO sin referencia a una tarea.
**Por qué:** Cada uno esconde un error futuro o una decisión que nadie podrá reconstruir.
**Verifica:** LINT

#### QA-015 · MUST · Código y dependencias muertas
**Regla:** El CI detecta código sin referencias y dependencias declaradas pero no usadas. Lo detectado se elimina en el mismo PR o en uno dedicado; una lógica reemplazada se elimina, no se conserva "por si acaso".
**Por qué:** El código muerto confunde a humanos y a la IA, y agranda la superficie de ataque.
**Verifica:** CI

---

## 11. OPS · Operación

#### OPS-001 · MUST · Entornos separados
**Regla:** Existen al menos el entorno local (Supabase local) y producción. Desde que el proyecto tiene su primer usuario real, existe además **staging**, con su propio proyecto de Supabase y su propio backend. Los despliegues de preview nunca apuntan a la base de datos de producción.
**Por qué:** Probar contra producción con datos reales es una vulneración esperando ocurrir.
**Verifica:** CI · la configuración de previews no referencia recursos de producción

#### OPS-002 · MUST · Mismo artefacto, distinta configuración
**Regla:** El mismo código se despliega en todos los entornos; solo cambian las variables de entorno. Nunca lógica condicionada al nombre del entorno, salvo la verificación de seguridad de SEC-019.
**Por qué:** Lo que se probó en staging es exactamente lo que llega a producción.
**Verifica:** LINT · condicionales sobre el nombre del entorno

#### OPS-003 · MUST · Despliegue controlado
**Regla:** Solo se despliega a producción desde `main`, con CI en verde. Las migraciones se aplican antes del código que las necesita (DB-004). Cada proyecto documenta cómo revertir un despliegue.
**Por qué:** Un despliegue sin camino de vuelta convierte un error en una caída.
**Verifica:** CI · branch protection · REVIEW · procedimiento de reversión documentado

#### OPS-004 · MUST · Endpoint de salud
**Regla:** El backend expone `/health` con dos niveles: el proceso está vivo, y sus dependencias críticas (base de datos) responden. Si una dependencia falla, responde `503`. No expone versiones, configuración ni datos. La plataforma de despliegue lo usa como verificación de salud.
**Por qué:** Permite a la plataforma y a las alertas detectar la caída antes que los usuarios.
**Verifica:** TEST · base de datos caída simulada → 503

#### OPS-005 · MUST · Logs estructurados
**Regla:** En producción: logs JSON, nivel por variable de entorno, `trace_id` en cada línea (API-013), sin PII. `ERROR` = requiere acción; `WARNING` = anomalía recuperable; `INFO` = evento de negocio; `DEBUG` solo fuera de producción.
**Por qué:** Los logs estructurados se pueden buscar, filtrar y alertar; el texto libre no.
**Verifica:** TEST · formato del log en configuración de producción

#### OPS-006 · MUST · Registro de errores
**Regla:** Los errores no controlados del frontend y del backend se envían a un servicio de registro de errores, con PII depurada antes del envío y con el `trace_id`. El proveedor se registra según PRIV-008.
**Por qué:** Sin esto, un error en producción solo se conoce cuando un usuario reclama.
**Verifica:** TEST · un error forzado llega al servicio sin PII

#### OPS-007 · MUST · Alertas mínimas
**Regla:** Existen alertas, con un destinatario definido, para: tasa de errores `5xx` sobre el umbral, `/health` fallando, job programado fallido o que no se ejecutó, y gasto de infraestructura o de IA sobre el presupuesto.
**Por qué:** Un problema que nadie ve se convierte en incidente.
**Verifica:** REVIEW de inicio de proyecto

#### OPS-008 · MUST · Respaldos probados
**Regla:** Cada proyecto declara su objetivo de pérdida máxima de datos y de tiempo de recuperación, verifica que el plan de respaldos de la base de datos los cumple, y prueba una restauración completa en un entorno aislado al menos una vez al año, dejando registro.
**Por qué:** Un respaldo que nunca se restauró es una hipótesis.
**Verifica:** REVIEW · registro de la prueba de restauración

#### OPS-009 · MUST · Jobs programados
**Regla:** Todo job programado es idempotente, está definido como código o migración (nunca configurado a mano en un panel), registra cada ejecución y su resultado, y alerta si falla o si no se ejecutó en su ventana.
**Por qué:** Los jobs fallan en silencio; los de retención y anonimización (PRIV-012, PRIV-014) son obligaciones legales.
**Verifica:** TEST · ejecutar el job dos veces produce el mismo resultado · OPS-007

#### OPS-010 · MUST · Costos conocidos
**Regla:** Cada proyecto documenta el plan contratado de cada servicio, sus límites relevantes (cuotas, suspensión por inactividad, arranques en frío) y tiene alertas de presupuesto configuradas.
**Por qué:** Evita facturas sorpresa y latencias que el cliente atribuye a un error.
**Verifica:** REVIEW de inicio de proyecto

#### OPS-011 · MUST · Runtime y dependencias vigentes
**Regla:** Las actualizaciones de seguridad se aplican de forma automática y continua (SEC-020). Los runtimes y dependencias principales se mantienen en versiones con soporte vigente; una versión sin soporte es un incidente a planificar.
**Por qué:** Una versión sin soporte deja de recibir parches de seguridad.
**Verifica:** CI · alerta de versiones sin soporte

#### OPS-012 · MUST · Postmortem sin culpables
**Regla:** Todo incidente con impacto en usuarios tiene un postmortem breve: cronología, causa raíz, qué funcionó, qué no, y acciones con responsable. Si involucra datos personales, se sigue además PRIV-020.
**Por qué:** El objetivo es que el sistema no repita el error, no buscar a quién culpar.
**Verifica:** REVIEW

---

## 12. NOM · Nombres y DOC · Documentación viva

### 12.1 NOM · Convenciones de nombres

#### NOM-001 · MUST · Idioma por contexto
**Regla:** Español para el dominio: tablas y módulos de dominio, funciones de negocio, acciones en rutas, mensajes al usuario, comentarios y docs. Inglés para lo técnico: infraestructura, utilidades, archivos estándar, logs técnicos y módulos base.
**Por qué:** Separa con claridad qué es negocio y qué es infraestructura, sin decisiones caso a caso.
**Detalle:** Módulos base en inglés (ARQ-018): `auth`, `users`, `settings`, `admin`, `logs` y, opcionalmente, `notifications` y `dashboard`.
**Verifica:** REVIEW

#### NOM-002 · NEVER · Mezclar idiomas en un identificador
**Regla:** Nunca combinar idiomas dentro de un mismo identificador (`obtenerUser`, `get_proyectos`).
**Por qué:** Los identificadores mixtos son impredecibles de buscar y de generar.
**Verifica:** REVIEW

#### NOM-003 · MUST · Convenciones por lenguaje
**Regla:**

| Elemento | Backend (Python) | Frontend (TypeScript) | Base de datos |
|---|---|---|---|
| Archivos | `snake_case` | Componentes `PascalCase`; resto `camelCase` | Migraciones `timestamp_descripcion` |
| Carpetas | `snake_case` | `kebab-case` | — |
| Clases / tipos / componentes | `PascalCase` | `PascalCase` | — |
| Funciones y variables | `snake_case` | `camelCase`; hooks con prefijo `use` | — |
| Constantes | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | — |
| Schemas | `Crear[X]Request`, `Actualizar[X]Request`, `[X]Response` | Tipos generados | — |
| Tablas y columnas | — | — | `snake_case`; tablas en plural |
| Índices / triggers | — | — | `[tabla]_[columna]_idx` / `trg_[tabla]_[evento]` |
| Políticas RLS | — | — | Descripción en español |

**Por qué:** Una convención única y tabulada no requiere interpretación.
**Verifica:** LINT

#### NOM-004 · MUST · Códigos de error
**Regla:** Códigos de error transversales en inglés: `VALIDATION_ERROR`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `CONFLICT`, `RATE_LIMITED`, `INTERNAL_ERROR`, `SERVICE_UNAVAILABLE`. Los de negocio, en español y descriptivos.
**Por qué:** Aplica NOM-001 a los errores: los transversales son técnicos; los de negocio, de dominio.
**Detalle:** Ejemplo de código de negocio: `PROYECTO_YA_ARCHIVADO`.
**Verifica:** TEST · contrato de errores (QA-008)

### 12.2 DOC · Documentación viva

#### DOC-001 · MUST · Estado del sistema
**Regla:** `docs/SYSTEM_STATE.md` describe el sistema actual (módulos, lógicas de negocio en lenguaje claro, decisiones vigentes), no historial ni planes. Endpoints y tablas se generan; la narrativa se escribe en el mismo commit que el cambio.
**Por qué:** Es el punto de partida de cada sesión de la IA y de cualquier persona que retome el proyecto.
**Verifica:** CI · las secciones generadas coinciden con el código · REVIEW · narrativa

#### DOC-002 · MUST · Decisiones de arquitectura (ADR)
**Regla:** Toda desviación de un DEFAULT, perfil opcional o decisión de arquitectura relevante va en `docs/ADR/NNN-titulo.md` (estado, contexto, decisión, alternativas, consecuencias). Un ADR aceptado no se edita: se reemplaza por otro que lo referencia.
**Por qué:** Dentro de seis meses nadie recordará por qué se decidió algo; el ADR sí.
**Verifica:** CI · formato de los ADR · ARQ-015 y ARQ-017 exigen ADR para los perfiles

#### DOC-003 · MUST · README operativo
**Regla:** El `README` permite levantar el proyecto localmente desde cero con los comandos listados, referencia `.env.example` para las variables y lista los comandos habituales (tests, generación de tipos, migraciones).
**Por qué:** Si levantar el proyecto requiere preguntarle a alguien, el conocimiento no está en el repositorio.
**Verifica:** CI · un job ejecuta los pasos de instalación del README en un entorno limpio

#### DOC-004 · MUST · Comentarios que explican el porqué
**Regla:** Los comentarios explican la intención o la regla de negocio, no lo que el código ya dice. Pueden referenciar un ID de regla o un ADR. Nunca contienen versiones, fechas ni historial (para eso está Git).
**Por qué:** Un comentario que repite el código envejece mal; uno que explica el porqué conserva el conocimiento.
**Verifica:** REVIEW

#### DOC-005 · NEVER · Editar documentos generados
**Regla:** Nunca editar a mano `SCHEMA_MAP.md`, el inventario de datos ni las secciones generadas de `SYSTEM_STATE.md`. Se corrige la fuente y se regenera.
**Por qué:** La edición manual se pierde en la siguiente generación y crea una segunda fuente de verdad.
**Verifica:** CI · regenera y compara

#### DOC-006 · MUST · Automatizaciones de IA versionadas
**Regla:** Los skills, hooks y comandos del agente de IA del proyecto viven versionados en el repositorio y documentados. Los skills son de solo lectura por defecto; uno que modifica código requiere aprobación explícita al crearlo.
**Por qué:** Las automatizaciones del agente son parte del sistema: si no están en el repositorio, no existen para el siguiente que lo use.
**Verifica:** REVIEW

---

## 13. ✅ Definición de Hecho (DoD)

Una tarea está terminada **solo** cuando todos los ítems que le aplican están marcados. La IA incluye esta lista, con su estado, en el cierre de sesión (PRO-012) y en la descripción del PR. Los ítems con `[condición]` aplican según el perfil.

**Código y arquitectura**
- [ ] Espejo completo o exención marcada y aprobada (ARQ-004)
- [ ] Sin imports entre módulos ni lógica de negocio en `shared/`/`core/` (ARQ-006, ARQ-007)
- [ ] Capas respetadas: sin queries en el service ni N+1 (ARQ-008, DB-015)
- [ ] Tipos generados regenerados y sin tipos manuales duplicados (ARQ-010)
- [ ] Operaciones con efectos: idempotentes (API-011)
- [ ] Perfil actualizado si el código usa algo nuevo (ARQ-017)

**Tests**
- [ ] Casos mínimos por endpoint y por módulo (QA-002, QA-005)
- [ ] Suites de RLS, rutas protegidas y contratos en verde (QA-008)
- [ ] Cobertura igual o mayor que la rama base (QA-007)
- [ ] Si es un bug: test que lo reproduce (QA-010)

**Datos**
- [ ] Migración completa: columnas canónicas, RLS, GRANTs, índices, comentarios PII (DB-002)
- [ ] Compatible con el código desplegado (DB-004)
- [ ] `SCHEMA_MAP.md` regenerado (DB-020)

**Seguridad y privacidad**
- [ ] Endpoints nuevos protegidos o en la lista pública (SEC-003)
- [ ] Entradas validadas y respuestas sin campos internos (API-008, API-009)
- [ ] [datos_personales] Minimización justificada y finalidad registrada (PRIV-001, PRIV-006)
- [ ] [datos_personales] Proveedores nuevos registrados (PRIV-008)
- [ ] Sin PII en logs, errores ni metadata de auditoría (PRIV-013, PRIV-015)
- [ ] Secretos fuera del repo y sin claves secretas en el frontend (SEC-002, SEC-016)
- [ ] [rut] RUT solo como HMAC, y cifrado si el perfil lo declara (DB-021)
- [ ] [pagos_webhooks] Firma y deduplicación verificadas (API-012)
- [ ] [uploads] Tipo y tamaño validados, almacenamiento privado, sin metadatos (SEC-015)
- [ ] [llm] PII filtrada antes del modelo, salida validada, evals en verde (PRIV-021, IA-004, IA-009)

**Interfaz**
- [ ] Funciona en 360 px sin scroll horizontal, con objetivos de 44 px (UI-003)
- [ ] Cuatro estados implementados (UI-006)
- [ ] Accesibilidad sin errores automáticos y operable con teclado (UI-009)
- [ ] Funciona en tema claro y oscuro (UI-011)

**Verificación**
- [ ] Comprobaciones y checks del CI en verde (Anexo B); toda verificación que aún no exista está cumplida a mano y marcada como manual

**Documentación y entrega**
- [ ] `SYSTEM_STATE.md` actualizado (DOC-001)
- [ ] ADR creado si hubo una decisión o desviación (DOC-002)
- [ ] Commits atómicos con formato válido, en una rama con propósito único (PRO-008, PRO-009)
- [ ] Cierre de sesión reportado: qué cambió, dónde quedó, tests ejecutados (PRO-012)

---

## Anexo A · Plantilla de `docs/PROJECT_PROFILE.yaml`

```yaml
# Perfil del proyecto — define qué reglas del estándar aplican.
# Validado contra el código en CI (ARQ-017). Modificarlo es ASK.

proyecto: nombre-proyecto

# ¿El sistema trata datos de personas naturales? (casi siempre: true)
datos_personales: true

# RUT: none | hmac | hmac+cifrado  (DB-021)
#   none          → el proyecto no pide RUT
#   hmac          → (por defecto si pide RUT) búsqueda y unicidad; nunca se muestra
#   hmac+cifrado  → además se puede mostrar en vistas autorizadas
rut: none

# ¿Integra modelos de IA dentro del producto? (Sección 9)
llm: false

# Usos de la IA, si llm: true (IA-006, IA-009, PRIV-019): moderacion | resumen | recomendaciones | asistencia | otro
llm_usos: []

# ¿Recibe webhooks (pagos, integraciones)? (API-012)
pagos_webhooks: false

# ¿Los usuarios suben archivos? (SEC-015)
uploads: false

# ¿Existe entorno de staging? Obligatorio desde el primer usuario real (OPS-001)
entorno_staging: false

# Perfiles opcionales, cada uno con su ADR (ARQ-015): bff | cache | realtime
perfiles_opcionales: []

# Categorías de exención de espejo habilitadas (ARQ-004):
# webhook | job | integracion_externa | og | health | admin_sin_ui
mirror_exclusions: [og, health]

# Módulos base opcionales que el proyecto necesita (ARQ-018): dashboard | notifications
modulos_opcionales: []

# Versión del estándar presente en este proyecto (PRO-015).
estandar:
  version: ""
```

---

## Anexo B · Verificaciones, CI, hooks y contrato de sesión

La IA implementa estas comprobaciones en cada proyecto durante la Fase 0 (F0-5), como tests, linters y pasos del CI; el helper de B.7, en F0-4. Mientras una verificación no exista, su regla se cumple igual y se marca como verificación manual en la DoD.

### B.1 Contrato común

Toda comprobación automática: corre en pre-commit y en CI; es determinista y no usa red; termina con código distinto de 0 si falla; imprime `ID-regla · archivo:línea · qué falta`; trae su propia prueba con un caso válido y otro inválido; y nunca se desactiva ni se relaja sin ASK.

### B.2 Exenciones del espejo

**Condiciones de cada categoría de exención** (revisión del espejo, ARQ-004):

| Categoría | Condición verificable en el OpenAPI y el código |
|---|---|
| `health` | Es la ruta `/health`, método GET, sin parámetros |
| `og` | Ruta bajo `/og/`, GET, pública, fuera de `/api/v1/` |
| `webhook` | Declara verificación de firma (API-012) y no usa la sesión de usuario |
| `job` | No usa la sesión de usuario; autentica con credencial interna |
| `integracion_externa` | Autentica con credencial propia del integrador, no con sesión de usuario |
| `admin_sin_ui` | Ruta bajo `/admin/` con la dependencia de rol admin; suma al contador visible |

La comprobación automática verifica forma, no intención: puede rechazar una exención mal puesta, pero no saber si una dependencia declarada hace lo que dice. Por eso el informe de exenciones nuevas de cada PR es parte del diseño y lo revisa un humano antes del merge.

### B.3 Generación de documentos

El proyecto escribe en F0-5 un script `generate_docs` que aplica las migraciones en el Supabase local y lee el esquema y el OpenAPI para generar: `SCHEMA_MAP.md` (DB-020), el inventario de datos desde los comentarios `pii:*` (DB-019, dentro de `PRIVACY_POLICY_NOTES.md`, PRIV-006) y las secciones generadas de `SYSTEM_STATE.md`, endpoints y tablas (DOC-001). Falla si una columna `pii:*` no tiene finalidad registrada (PRIV-001) o si una `pii:sensible` no referencia un ADR (PRIV-017). En CI se regenera y se compara: falla si difiere de lo commiteado (DOC-005).

### B.4 Reglas de lint propias

Lo que ningún linter trae de serie se implementa como regla de búsqueda estructural:

| Regla | Detecta |
|---|---|
| ARQ-008 | `service.py` que importa la sesión de DB o construye queries |
| ARQ-012 | Llamadas bloqueantes dentro de funciones `async` |
| API-008 | Schemas de entrada que aceptan campos no declarados |
| DB-007 | Borrado físico fuera de `audit_logs` y `consents` |
| DB-008 | Eliminación de usuarios de Auth |
| DB-013 | Conexión privilegiada importada fuera de las ubicaciones permitidas |
| DB-014 | `SET` de sesión o `set_config` no local para rol o claims; sesión pasada a tareas concurrentes o en segundo plano |
| DB-015 | Llamadas al repositorio dentro de bucles |
| DB-021 | Columnas `rut` sin sufijo de HMAC o cifrado |
| SEC-009 | Lectura o escritura manual de tokens de sesión |
| SEC-013 | SQL construido con strings |
| PRIV-015 | Campos personales en llamadas de log |
| OPS-002 | Condicionales sobre el nombre del entorno |
| QA-003 | Mocks de sesión de DB en tests de endpoints; uso de la conexión privilegiada en el cuerpo de un test, fuera de fixtures y del helper de verificación de efectos |
| QA-004 | Tests cuya única aserción es el código de estado |

El resto de las verificaciones LINT (ARQ-006, ARQ-009, SEC-011, UI-001, UI-002, UI-004, UI-010, QA-013, QA-014, NOM-003) usa la configuración estándar del linter del stack: boundaries de imports, reglas de seguridad y de estilo.

### B.5 Checks bloqueantes del CI

1. **Calidad:** type-check estricto, linters y las comprobaciones de B.1 a B.4 (QA-012).
2. **Tests:** backend y frontend en orden aleatorio, cobertura (QA-005, QA-007, QA-009), suites transversales (QA-008) y E2E en 360 px y escritorio (QA-006).
3. **Contratos y esquema:** cliente y documentos regenerados sin diferencias (ARQ-010, ARQ-011, DOC-005); OpenAPI sin cambios que rompan contra la rama base (API-001); migraciones existentes inmutables y coherentes con el esquema remoto (DB-001); modelos del ORM iguales al esquema (DB-003).
4. **Seguridad:** escaneo de secretos y del bundle (SEC-016, SEC-002, IA-001); vulnerabilidades altas o críticas, lockfile y acciones fijadas por hash (SEC-020); headers contra el preview (SEC-010).
5. **Web:** accesibilidad automática (UI-009) y Lighthouse móvil (UI-005).
6. **Proceso:** nombre de rama (PRO-009), formato de ADR (DOC-002) y previews sin recursos de producción (OPS-001).

### B.6 Hooks

| Hook | Acción | Reglas |
|---|---|---|
| `pre-commit` (git) | Linters, tipos y escaneo de secretos | QA-012, SEC-016 |
| `commit-msg` (git) | Valida `tipo(scope): descripción` | PRO-008 |
| Agente · antes de ejecutar comandos | Bloquea `git push` (también `--force`), `git reset --hard`, borrado de ramas remotas, `DROP`, `ALTER COLUMN` de tipo, `supabase db push` e instalación de paquetes nuevos | PRO-005, PRO-007, PRO-010 |
| Agente · antes de escribir archivos | Bloquea `.github/`, `.claude/`, archivos de despliegue y `ENGINEERING_STANDARDS.md` | PRO-006, PRO-015 |
| Agente · al terminar | Revisa `git status` (cambios fuera de la rama activa) y exige el cierre de sesión si el repositorio cambió | PRO-011, PRO-012 |

El bloqueo cita el ID de la regla; la aprobación es siempre del humano.

### B.7 Contrato de sesión del usuario

El helper que cumple DB-012; DB-014 lo pone a prueba. La IA lo crea en `core/` durante F0-4.

1. **Entrada:** claims ya verificados (SEC-001), nunca el token crudo. Sin `sub`, o con un rol distinto de `authenticated` (incluido `service_role`), se niega a abrir la sesión: nunca degrada a `anon` en silencio. Los endpoints de la lista pública (SEC-003) que necesiten la base de datos piden explícitamente el **modo anónimo**: rol `anon`, sin claims, solo con las políticas de lectura pública y GRANTs mínimos (DB-010).
2. **Apertura, en este orden y dentro de una transacción explícita:** (a) fijar con alcance local el conjunto completo de claims verificados del token (incluidos `sub`, `role` y `aal`), para que `auth.uid()` y `auth.jwt()` funcionen en las políticas; (b) cambiar al rol `authenticated` con alcance local; (c) verificar que el rol efectivo es `authenticated` y que el `sub` fijado es el del token. Es el orden del patrón de referencia de Supabase; la verificación (c) cubre cualquier configuración inesperada de la base. Un fallo en cualquier paso aborta el request: nunca se ejecuta una query sin identidad.
3. **Claims como parámetros ligados** (SEC-013), nunca interpolados en el SQL.
4. **Cierre:** commit si todo salió bien; rollback ante cualquier error. Rol y claims se descartan solos por ser locales; el helper no los restablece a mano.
5. **Base de datos:** el rol de conexión puede cambiar a `authenticated` (membresía otorgada); se recomienda un rol dedicado, sin superusuario ni bypass de RLS. `authenticated` tiene solo los GRANTs de DB-010.
6. **Pooler en modo transacción:** sin dependencia de estado de sesión ni de sentencias preparadas persistentes que el pooler no soporte.
7. **Una sesión nueva por llamada:** el helper nunca cachea ni reutiliza una (DB-014).
8. **Prueba:** el TEST de DB-014 usa este helper con un pool de una sola conexión, en un motor propio, con datos confirmados (sin transacción exterior abierta) y ejecución serializada: un fixture que retenga una conexión mientras el helper pide otra bloquearía el pool. Cubre además: sin `sub` → 401; fallo al fijar el rol → request abortado; `service_role` rechazado; el modo anónimo solo ve lo que permiten las políticas de lectura pública. Las pruebas pasan los claims directamente al helper (incluido `aal1` o `aal2`), sin firmar tokens.

---

## Anexo C · Valores canónicos

Punto de partida para que cada proyecto no vuelva a elegir lo que el estándar ya exige. Los valores (secretos, URLs) los entrega siempre el humano (PRO-002).

### C.1 Variables de entorno

Nombres canónicos de `.env.example` (ARQ-016, SEC-016). Las del grupo base son requeridas desde el inicio; las de cada funcionalidad, cuando existe el módulo que las usa.

| Grupo | Variables | Reglas |
|---|---|---|
| Base · servidor | `APP_ENV` (solo para la verificación de arranque), `CORS_ALLOWED_ORIGINS`, `TRUSTED_PROXIES`, `RATE_LIMIT_AUTH`, `RATE_LIMIT_WRITE`, `RATE_LIMIT_READ` | OPS-002, SEC-019, SEC-012, SEC-017, SEC-018 |
| Base · Supabase | `SUPABASE_URL`, `SUPABASE_SECRET_KEY` (solo backend), `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY` | SEC-002 |
| Base · datos | `DATABASE_URL` (rol que opera como el usuario), `DATABASE_URL_PRIVILEGED` | B.7, DB-013 |
| Base · frontend | `VITE_API_URL` | ARQ-016 |
| IA | `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`, `LLM_MAX_TOKENS`, `LLM_TIMEOUT_SECONDS`, `LLM_QUOTA_PER_USER`, `LLM_QUOTA_GLOBAL`, `LLM_SPEND_ALERT` | IA-001, IA-002, IA-011 |
| Webhooks | `WEBHOOK_SIGNING_SECRET`, `WEBHOOK_TOLERANCE_SECONDS` | API-012 |
| Uploads | `UPLOAD_MAX_BYTES`, `UPLOAD_ALLOWED_TYPES`, `UPLOAD_SIGNED_URL_TTL_SECONDS` | SEC-015 |
| Errores y avisos | `ERROR_TRACKING_DSN`, `NOTIFICATIONS_PROVIDER`, `NOTIFICATIONS_API_KEY` | OPS-006, PRIV-008 |

### C.2 Dependencias base

Lista de partida para el lote de la Fase 0 (PRO-005). **Solo `limits` tiene el mantenimiento verificado; el resto se verifica antes de instalar** (SEC-020), y la lista se revisa cada vez que cambie el estándar.

| Capa | Dependencias |
|---|---|
| Backend · runtime | FastAPI, Pydantic, pydantic-settings, SQLAlchemy (async), asyncpg, PyJWT (con soporte criptográfico), httpx, Pillow, filetype, limits, structlog |
| Backend · desarrollo | pytest, pytest-asyncio, pytest-cov, ruff, mypy (estricto), import-linter, vulture, pip-tools, pip-audit |
| Frontend · runtime | React, react-dom, react-router, TanStack Query, Zustand, Tailwind, supabase-js |
| Frontend · desarrollo | Vite, TypeScript, generador de cliente OpenAPI (`@hey-api/openapi-ts`), Vitest, Testing Library, Playwright, axe, ESLint con `typescript-eslint` y boundaries, knip |

---

## Anexo D · Historial

**6.1.0** — Alineación con el Playbook de Privacidad y el playbook de producto: modelo de tres documentos sin superposición (estándar = cómo; playbook de privacidad = qué exige la ley; playbook de producto = qué se construye), con su precedencia (0.7 y arranque). PRIV-006 organiza el RAT por finalidad y ejecuta la retención con jobs; PRIV-005 trunca la IP y aclara el estado del registro tras la supresión; DB-007 anonimiza al vencer su plazo las filas borradas lógicamente con PII. Sin reglas nuevas ni retiradas.

**6.0.0** — Un solo archivo autosuficiente. Se retiran la vista derivada para la IA, el paquete de guardas, el manifiesto y el ancla de integridad: la IA implementa las comprobaciones en cada proyecto durante la Fase 0 (F0-5). Se conservan las 173 reglas. El `Detalle` forma parte de la regla y se cumple igual (0.2). **Pendiente:** (1) mecanismo para desvincular identidades OAuth en la baja (PRIV-011); (2) definir «credencial interna» y la del integrador (`job`, `integracion_externa`); (3) datos derivados del LLM en exportación y baja; (4) un control real de la restricción de menores; (5) probar la Fase 0 en un proyecto real.

**5.x** — Endurecimiento de seguridad (sesión como el usuario, administradores bajo RLS con segundo factor, primer y último administrador, modo anónimo, UUID del sistema), Fase 0 de arranque de 7 pasos con lote opcional, Anexo C con variables y dependencias base, mobile first, respuesta a incidentes, IA dentro del producto y Definición de Hecho.

**4.0.0** — Unificación de la v3.1 y `directives.md` con IDs permanentes, cuatro modalidades, cinco tipos de verificación y contenido atemporal.
