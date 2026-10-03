# Registro de tratamiento (RAT) — peervibe

Fuente operativa del RAT (PRIV-006). Se mantiene al día con cada cambio de tratamiento. Plazos y bases los define el humano.

- **Estado:** RAT v0.2 — decisiones D-01 a D-06 confirmadas. Lo marcado «propuesta» requiere confirmación; lo marcado «[validar]» requiere revisión legal.
- **Referencias:** `docs/playbook-privacidad.md` y `docs/playbook-producto.md`.
- **Nivel de riesgo:** N2 (contenido generado por usuarios, cuentas, analítica e IA; ver datos sensibles incidentales en T-03).
- **Responsable:** persona natural. Pendiente: nombre legal y domicilio para la política de privacidad.
- **Canal de derechos:** correo `privacidad@[dominio]` · formulario `/privacidad/solicitud`.
- **Edad mínima:** 18 años (D-01); no se admiten menores.

## Decisiones del proyecto

| # | Decisión |
|---|---|
| D-01 | Edad mínima 18 años. |
| D-02 | No se pide el nombre real; la identidad pública es el `username`. |
| D-03 | No se recolectan rango de edad, país ni ciudad hasta que exista una finalidad concreta. |
| D-04 | Analítica sin cookies ni datos personales. |
| D-05 | Al suprimir la cuenta, el usuario elige si borrar sus reseñas o conservarlas como «Usuario privado». |
| D-06 | Responsable: persona natural. |

## Proveedores (encargados)

| Proveedor | Servicio | País / región | DPA |
|---|---|---|---|
| Supabase | Base de datos, autenticación y almacenamiento de archivos | [según región elegida; propuesta: São Paulo] | pendiente |
| Vercel | Hosting del frontend | EE.UU. / red global | pendiente |
| Render | Hosting del backend (FastAPI) | [según región elegida] | pendiente |
| Google | Inicio de sesión (OAuth) | EE.UU. | pendiente |
| Apple | Inicio de sesión (OAuth) | EE.UU. | pendiente |
| Proveedor de correo | Correos transaccionales y de marketing | TBD (el RAT proponía Resend, EE.UU.) | pendiente |
| Proveedor de IA | Síntesis de reseñas (LLM) | [por definir] | pendiente · condiciones: sin entrenamiento con datos del cliente, retención mínima |
| Proveedor de analítica | Analítica de uso | [por definir] | pendiente |
| Registro de errores / logs | Logs de aplicación (T-14) | TBD | pendiente |

La base de la transferencia internacional de cada proveedor (PRIV-008) queda por registrar antes de integrarlo.

## Tratamientos

### Cuenta y perfil

**T-01 · Cuenta y autenticación**
- Finalidad: crear y mantener la cuenta del usuario y permitirle iniciar sesión con Google o Apple.
- Base de licitud: contrato. Titulares: usuarios registrados.
- Datos: `auth.users.email` (contacto); identificador del proveedor OAuth (identificación).
- Sistemas: supabase_auth. Encargados: Supabase, Google, Apple. Transferencia internacional: sí.
- Retención: vida de la cuenta; inactiva 24 meses → aviso 30 días antes y supresión *(propuesta)*.
- Consentimiento: no requerido. EIPD: no.

**T-02 · Perfil público y reputación**
- Finalidad: mostrar el perfil público del usuario, su historial de reseñas, puntos y rango, para que la comunidad valore su criterio.
- Base de licitud: contrato. Titulares: usuarios registrados.
- Datos públicos: `user_profiles.username`, `avatar_url`, `reputation_points`, `user_rank`.
- Sistemas: user_profiles, supabase_storage. Encargados: Supabase. Transferencia internacional: sí.
- Retención: vida de la cuenta (supresión). Consentimiento: no requerido.
- Informar en: registro y política de privacidad (el usuario debe saber que su perfil es público). EIPD: no.

### Contenido y comunidad

**T-03 · Publicación de reseñas**
- Finalidad: publicar las reseñas, calificaciones y fotos de producto que el usuario escribe.
- Base de licitud: contrato. Titulares: usuarios registrados.
- Datos públicos: `reviews.pros / contras / commentary`; `ratings_breakdown / rating_final`; `reviews.user_id`; fotos del producto (Storage).
- Sistemas: reviews, supabase_storage. Encargados: Supabase. Transferencia internacional: sí.
- Retención: indefinida mientras la reseña esté publicada. Al suprimir la cuenta, el usuario elige borrar sus reseñas o conservarlas desvinculadas como «Usuario privado» (D-05).
- Consentimiento: no requerido.
- Riesgos: datos sensibles incidentales (en suplementos o cosmética el texto libre puede revelar condiciones de salud). Mitigación propuesta: aviso en el formulario de no incluir datos de salud ni de terceros, y criterio de moderación para editarlos o rechazarlos.
- EIPD: no **[validar]** si se lanza con categorías de salud (suplementos).

**T-06 · Votos de utilidad**
- Finalidad: permitir que los usuarios marquen reseñas como útiles y ponderar el ranking.
- Base de licitud: contrato. Titulares: usuarios registrados.
- Datos (no públicos): `review_votes.user_id / vote_type`.
- Sistemas: review_votes. Encargados: Supabase. Transferencia internacional: sí.
- Retención: indefinida; al suprimir la cuenta el voto se conserva desvinculado, porque el usuario queda anonimizado (PRIV-011).
- Consentimiento: no requerido. EIPD: no.

**T-07 · Síntesis de reseñas con IA**
- Finalidad: generar el resumen de pros y contras de cada producto a partir de las reseñas publicadas.
- Base de licitud: interés legítimo **[validar]**. Titulares: autores de reseñas.
- Datos: texto de reseñas aprobadas, sin username ni identificadores.
- Sistemas: backend_ia. Encargados: proveedor de IA. Transferencia internacional: sí.
- Minimización: se envía solo el texto, con redacción automática de nombres, correos, teléfonos y RUT.
- Retención: sin retención en el proveedor; el resumen generado no contiene datos personales.
- Oposición: preferencia para excluir las propias reseñas de la síntesis.
- Consentimiento: no requerido. EIPD: no.

### Verificación y prevención de fraude

**T-04 · Verificación de compra**
- Finalidad: verificar que el usuario compró el producto para otorgar la medalla «Compra Verificada».
- Base de licitud: consentimiento. Titulares: usuarios registrados que suben un comprobante.
- Datos (no públicos): `review_proofs.storage_path` (imagen de boleta o caja; identificación y financiero incidental); `review_proofs.verification_status`.
- Sistemas: review_proofs, supabase_storage_privado. Encargados: Supabase. Transferencia internacional: sí.
- Retención: 30 días desde la verificación o el rechazo; se conserva solo el resultado (`reviews.is_verified`); acción: borrado de la imagen *(propuesta)*.
- Consentimiento requerido. Texto corto: «Usar mi comprobante para verificar la compra · Consentimiento · se borra 30 días después de verificar».
- Notas: recomendar al usuario tapar datos personales; evaluar recorte o desenfoque automático en el pipeline de imágenes. EIPD: no.

**T-05 · Prevención de fraude y moderación**
- Finalidad: detectar reseñas falsas, cuentas múltiples y abuso, y moderar el contenido.
- Base de licitud: interés legítimo **[validar]**. Titulares: usuarios registrados, visitantes.
- Datos: `ip_hmac` (HMAC de la IP con clave rotada cada 90 días; *propuesta*); user agent y patrones de actividad; `user_profiles.is_banned`.
- Sistemas: fraud_signals (por diseñar), user_profiles. Encargados: Supabase, Render. Transferencia internacional: sí.
- Retención: 90 días; al vencer, anonimización (DB-007).
- Decisiones automatizadas: sí — shadowban o bloqueo automático por señales de fraude. Salvaguarda: notificación al usuario y canal de revisión humana antes de un baneo definitivo.
- Consentimiento: no requerido. EIPD: no.

### Analítica y afiliación

**T-08 · Analítica de uso**
- Finalidad: medir el uso del sitio de forma agregada para mejorar el producto.
- Base de licitud: interés legítimo **[validar]** (procede solo si efectivamente no se tratan datos personales). Titulares: visitantes, usuarios registrados.
- Datos: eventos agregados (páginas vistas, referencias, dispositivo genérico) sin identificador persistente.
- Sistemas y encargados: proveedor de analítica. Transferencia internacional: [según proveedor].
- Retención: 24 meses (agregación). Consentimiento: no requerido.
- Condiciones: sin cookies ni almacenamiento local en el navegador; la IP no se almacena (si el proveedor la usa, solo de forma transitoria); sin identificadores entre sesiones ni cruce con la cuenta.
- Notas: D-04 confirmada. Si se incorpora cualquier herramienta con cookies de analítica o marketing, el tratamiento pasa a base consentimiento y se requiere banner. EIPD: no.

**T-09 · Afiliación (botón «Ver precio en…»)**
- Finalidad: redirigir a tiendas y medir los clics de salida para el modelo de comisiones.
- Base de licitud: interés legítimo **[validar]**. Titulares: visitantes, usuarios registrados.
- Datos: clic de salida (producto, tienda, fecha) SIN identificador de usuario (*propuesta*).
- Sistemas: outbound_clicks (por diseñar). Encargados: Supabase. Transferencia internacional: sí.
- Retención: 24 meses (agregación). Consentimiento: no requerido.
- Notas: si los clics se registran sin identificar al usuario, no hay datos personales. Las cookies de afiliado las instala la tienda en su propio dominio, bajo su propia política. EIPD: no.

### Comunicaciones

**T-10 · Comunicaciones transaccionales**
- Finalidad: avisar sobre el estado de las reseñas, la verificación y la seguridad de la cuenta.
- Base de licitud: contrato. Titulares: usuarios registrados.
- Datos: `auth.users.email`. Sistemas: backend. Encargados: proveedor de correo (TBD). Transferencia internacional: sí.
- Retención: logs de envío 90 días (borrado). Consentimiento: no requerido. EIPD: no.

**T-11 · Novedades y promociones**
- Finalidad: enviar novedades de la plataforma, beneficios y cupones de marcas aliadas.
- Base de licitud: consentimiento. Titulares: usuarios registrados.
- Datos: `auth.users.email`. Sistemas: backend. Encargados: proveedor de correo (TBD). Transferencia internacional: sí.
- Retención: hasta la revocación (baja).
- Consentimiento requerido. Texto corto: «Recibir novedades y promociones · Consentimiento · hasta que te des de baja».
- Notas: los datos nunca se entregan a las marcas aliadas; los cupones se envían desde peervibe. EIPD: no.

### Obligaciones legales y seguridad

**T-12 · Atención de derechos**
- Finalidad: recibir, gestionar y responder solicitudes de acceso, rectificación, supresión, oposición, portabilidad y bloqueo.
- Base de licitud: obligación legal. Titulares: usuarios registrados, visitantes, terceros.
- Datos: `privacy_requests` (tipo, estado, fechas, correo de respuesta).
- Sistemas: privacy_requests. Encargados: Supabase, proveedor de correo (TBD). Transferencia internacional: sí.
- Retención: 3 años **[validar]**; el correo de respuesta se borra al cerrar. Consentimiento: no requerido. EIPD: no.

**T-13 · Registro de consentimientos**
- Finalidad: acreditar ante la Agencia qué consintió cada persona, cuándo y sobre qué versión.
- Base de licitud: obligación legal. Titulares: usuarios registrados, visitantes.
- Datos: `consents` (titular, finalidad y versión del documento, fecha, IP truncada, agente de usuario, `revoked_at`; PRIV-005).
- Sistemas: consents. Encargados: Supabase. Transferencia internacional: sí.
- Retención: vida de la relación + plazo de prescripción **[validar]**; al vencer, anonimización.
- Consentimiento: no requerido. EIPD: no.

**T-14 · Seguridad y auditoría**
- Finalidad: proteger la plataforma, detectar accesos indebidos y reconstruir incidentes.
- Base de licitud: interés legítimo **[validar]**. Titulares: usuarios registrados, administradores.
- Datos: `audit_logs` (actor, acción, IP truncada, fecha); logs de aplicación.
- Sistemas: audit_logs, logs_externos. Encargados: Supabase, Render, [servicio de logs por definir]. Transferencia internacional: sí.
- Retención: `audit_logs` 12 meses (plazo definido por el proyecto); al vencer, anonimización según PRIV-014. Logs de aplicación 90 días (borrado). Consentimiento: no requerido. EIPD: no.

### Fuera del MVP

**T-15 · Cuentas de marcas (B2B)**
- Finalidad: permitir a las marcas reclamar su perfil, responder reseñas y ver métricas agregadas.
- Base de licitud: contrato. Titulares: representantes de marcas.
- Datos: nombre, correo corporativo, empresa, cargo (contacto profesional).
- Sistemas: [por diseñar, fuera del MVP]. Encargados: Supabase, proveedor de correo (TBD). Transferencia internacional: sí.
- Retención: vigencia del contrato + 2 años **[validar]** (supresión).
- Restricción: las marcas solo reciben métricas agregadas; nunca datos personales de quienes reseñan. Consentimiento: no requerido. EIPD: no.

## Pendientes para el responsable

1. Bases de licitud «interés legítimo» por validar: T-05, T-07, T-08, T-09, T-14.
2. Plazos por validar: T-12 (3 años), T-13 (prescripción), T-15 (contrato + 2 años).
3. EIPD de T-03 si se lanzan categorías de salud (suplementos).
4. Valores «propuesta» por confirmar: retención de T-01 y T-04; `ip_hmac` de T-05; clic de salida de T-09.
5. Proveedores TBD: correo, IA, analítica, logs/errores; región de Supabase y Render; DPA de todos.
6. Nombre legal y domicilio del responsable; dominio del correo `privacidad@[dominio]`.
7. Se hicieron 5 ajustes para alinear con el estándar v6.1.0 (los mecanismos los define el estándar, no el `rat.yaml`; finalidades, bases y plazos se mantienen): T-01 (sin `user_private`), T-05 (anonimización en vez de borrado, DB-007), T-06 (voto desvinculado por anonimización, PRIV-011), T-13 (datos según PRIV-005; sin `subject_id` ni `privacy_subjects`; anonimización al vencer) y T-14 (`audit_logs`; anonimización según PRIV-014 con plazo de 12 meses definido por el proyecto).

## Inventario de datos

> Generado por `generate_docs` en F0-5; vacío hasta entonces (DB-019, PRIV-006).
