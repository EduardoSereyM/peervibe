# Playbook de Ingeniería v2 — Privacidad desde el Diseño (Ley 21.719)

Oct 2, 2026 · @Eduardo

> **v2.1.** Alineado con ENGINEERING_STANDARDS v6.1.0: la supresión admite eliminación o anonimización irreversible; el registro de consentimientos admite marcar la revocación; el inventario pasa a ser un RAT organizado por finalidad; el playbook deja de prescribir mecanismos técnicos.

## Alcance y uso

Este playbook es la línea base obligatoria de privacidad para **todo proyecto web** que desarrolle, sea propio o de clientes. Stack de referencia: Python/FastAPI, React o Angular, Supabase/PostgreSQL, Render y Vercel.

La v2 corrige cuatro contradicciones de la v1: soft delete vs supresión, `DELETE` duro vs `SET NULL`, hash vs anonimización y log inmutable vs derecho al olvido. También agrega gobernanza, derechos ARCO+, retención automática, anexos de riesgo y cumplimiento ejecutable en CI.

**Aviso:** este documento es una guía técnica, no asesoría legal. La Ley 21.719 entra en vigencia el 1 de diciembre de 2026. Los puntos marcados como *\[validar\]* deben revisarse con un abogado antes de comprometerse con un cliente.

**Formato: norma, no implementación.** Este documento define *qué* debe cumplirse y *por qué*, nunca *cómo*. Cada requisito sigue la estructura **Requisito → Por qué → Criterios de aceptación**. Los criterios son verificables e independientes del stack: valen igual para Supabase, PostgreSQL autogestionado, React o Angular.

**Relación con los otros documentos.** Este playbook define *qué* exige la ley a cada proyecto. *Cómo* se implementa en el stack lo define `ENGINEERING_STANDARDS` (en especial sus secciones DB, SEC y PRIV), y *qué* se construye lo define el playbook de producto de cada proyecto. Este documento no contiene código ni prescribe mecanismos técnicos: cualquier implementación es válida si cumple los criterios de aceptación. Si una regla del estándar impide cumplir un criterio, se corrige el estándar.

### Cómo usarlo

1. Al iniciar un proyecto, clasifícalo según la tabla de niveles de riesgo.
2. Aplica siempre los Módulos 0 a 4 y el 6. El Módulo 5 se activa según el nivel.
3. Traduce los criterios de aceptación de cada módulo en tests propios del proyecto (Módulo 6).
4. Antes de salir a producción, completa el checklist de go-live del final.

### Niveles de riesgo del proyecto

| Nivel | Cuándo aplica | Ejemplos | Módulos |
| --- | --- | --- | --- |
| N1 · Básico | Solo datos de contacto o cuenta; sin perfilamiento | Landing con formulario, blog, sitio corporativo | 0–4, 6 |
| N2 · Estándar | Cuentas de usuario, contenido generado por usuarios, pagos, analítica o marketing | SaaS, e-commerce, plataforma de reseñas | 0–4, 6 + 5.3 si usa IA sobre usuarios |
| N3 · Alto | Datos sensibles, menores de edad, perfilamiento o decisiones automatizadas con efecto relevante, o tratamiento masivo | Salud, opinión política, educación, biometría, scoring | 0–6 completo + evaluación de impacto |

Regla de oro: **ante la duda, sube un nivel**. Reclasificar un proyecto ya en producción cuesta mucho más que diseñarlo bien desde el inicio.

## Resumen para desarrolladores

Qué hay que construir, en una lista. Cada punto enlaza a su sección, donde están los criterios de aceptación. Para saber qué *verificar* antes de salir a producción, usa el checklist de go-live del final.

- Política de Privacidad y Política de Cookies publicadas y versionadas → 0.2, 0.3
- Banner de cookies con "Aceptar" y "Rechazar" iguales, y botón para reabrirlo → 1.3
- Ningún script de terceros carga antes del consentimiento → 1.2
- Registro inmutable de cada consentimiento → 2.1
- Formularios sin casillas premarcadas y con consentimientos separados → 1.4
- Solo pedir los datos que figuran en el inventario → 0.1, 1.4
- Página "Mi privacidad": descargar mis datos, borrar mi cuenta, preferencias → 1.5
- Supresión que elimina o anonimiza de forma irreversible los datos personales (no un flag); el contenido conservado se muestra como "Usuario privado" → 2.2
- Cola de solicitudes de derechos con alerta de plazos → 2.4
- Eliminación o anonimización automática de los datos al vencer su plazo → 2.5
- HTTPS forzado con HSTS y headers de seguridad → 3.1
- Seguridad a nivel de fila en todas las tablas → 3.2
- 2FA obligatorio y roles limitados en el panel de administración → 3.3
- Sin datos reales en desarrollo ni secretos en el repositorio → 3.4
- Log de auditoría y plantillas de aviso de brechas listas → 4.1, 4.3
- Si hay datos sensibles, menores o IA: aplicar el Módulo 5

## Módulo 0 · Gobernanza (antes de escribir código)

Ningún dato personal se recolecta sin una finalidad, una base de licitud y un plazo de retención documentados. La documentación de este módulo se versiona junto con el código del proyecto.

### 0.1 Registro de Actividades de Tratamiento (RAT)

**Requisito.** Cada proyecto mantiene un Registro de Actividades de Tratamiento (RAT) organizado **por finalidad**, no por campo. Cada tratamiento tiene un identificador estable, la finalidad en lenguaje claro, su base de licitud, las categorías de titulares y de datos, los sistemas donde viven esos datos, los encargados que los reciben, si salen de Chile, el plazo de retención y si requiere evaluación de impacto. Cada campo con datos personales se asocia a uno o más tratamientos.

**Por qué.** La Agencia fiscaliza tratamientos, no columnas *[validar artículos]*. Un mismo dato puede servir a varias finalidades con bases y plazos distintos: el correo se usa para la cuenta (contrato) y para el newsletter (consentimiento). Organizar por finalidad permite revocar una sin afectar las otras. El consentimiento, la política de privacidad, la evaluación de impacto y la retención dependen de este registro.

En este documento, "inventario" y "RAT" se usan como sinónimos.

**Criterios de aceptación**

- [ ] Cada tratamiento tiene un identificador estable, que no cambia aunque cambie la redacción de su finalidad.
- [ ] Ningún tratamiento carece de finalidad, base de licitud o plazo de retención.
- [ ] Todo campo con datos personales del modelo de datos está asociado al menos a un tratamiento.
- [ ] El RAT se puede contrastar de forma automática con el modelo de datos.
- [ ] Un campo o un tratamiento nuevo sin registro en el RAT impide el paso a producción.
- [ ] El RAT se revisa ante cada nuevo proveedor, nueva funcionalidad con datos personales o cambio de finalidad.

### 0.2 Bases de licitud

**Requisito.** Cada tratamiento declara una base de licitud. El consentimiento se usa solo cuando corresponde, no por defecto.

**Por qué.** Si el servicio no funciona sin el dato, la base es el contrato, no el consentimiento. Pedir consentimiento para algo que en realidad es obligatorio confunde al usuario y debilita tu posición legal.

| Base | Úsala para | No la uses para |
| --- | --- | --- |
| Contrato | Datos necesarios para prestar el servicio (cuenta, pedido, pago) | Marketing o analítica |
| Consentimiento | Marketing, cookies no esenciales, datos sensibles, menores | Datos sin los que el servicio no funciona |
| Obligación legal | Boletas, facturas, registros que exige la ley | Retenciones sin respaldo normativo |
| Interés legítimo *\[validar\]* | Seguridad, prevención de fraude, logs de auditoría | Perfilamiento comercial invasivo |

**Criterios de aceptación**

- [ ] Cada entrada del inventario tiene una base de licitud asignada.
- [ ] Ningún dato con base "contrato" se pide mediante una casilla de consentimiento.
- [ ] Todo tratamiento con base "consentimiento" tiene su registro correspondiente (ver 2.1).

### 0.3 Política de retención

**Requisito.** Todo dato personal tiene una fecha de vencimiento, y al vencer se elimina o se anonimiza de forma automática.

**Por qué.** Conservar datos sin finalidad vigente es un tratamiento ilícito y además amplía el impacto de cualquier brecha.

Plazos de referencia, a ajustar según el proyecto:

| Dato | Retención sugerida | Acción al vencer |
| --- | --- | --- |
| Cuenta inactiva | 24 meses sin login + aviso 30 días antes | Supresión (ver 2.2) |
| Registro de consentimientos | Vida de la relación + plazo de prescripción *\[validar\]* | Desvincular de la persona |
| Logs de aplicación con IP | 90 días | Eliminación o anonimización |
| Logs de auditoría de seguridad | 12 meses | Eliminación o agregación |
| Solicitudes de derechos | 3 años *\[validar\]* | Eliminación o anonimización |
| Documentos tributarios | Plazo legal tributario *\[validar\]* | Eliminación o anonimización |

**Criterios de aceptación**

- [ ] Cada plazo del inventario tiene un proceso automático que lo ejecuta.
- [ ] Existe evidencia (logs de ejecución) de que los procesos de retención corren con regularidad.
- [ ] La política de privacidad publica los plazos.
- [ ] Los plazos y demás parámetros normativos son configuración editable, no valores fijos en el código, para que un cambio regulatorio no exija un nuevo despliegue.

### 0.4 Encargados y transferencias internacionales

**Requisito.** Todo proveedor que procese datos personales por cuenta del proyecto (hosting, base de datos, correo, analítica, IA) está identificado, tiene un acuerdo de tratamiento de datos y, si procesa fuera de Chile, la transferencia está declarada.

**Por qué.** Respondes por lo que tus proveedores hacen con los datos. La mayoría del stack típico (Supabase, Vercel, Render, servicios de correo, APIs de IA) opera fuera de Chile.

**Criterios de aceptación**

- [ ] Existe un acuerdo de tratamiento de datos (DPA) archivado por cada encargado.
- [ ] Se eligió la región disponible más cercana para alojar los datos y la elección está documentada.
- [ ] La política de privacidad declara los países de destino y las garantías aplicadas *\[validar mecanismo con abogado\]*.
- [ ] Los proveedores de IA operan en planes sin entrenamiento con tus datos y con retención mínima.

### 0.5 Roles y canal de derechos

**Requisito.** Están definidos el responsable, el encargado y un canal único para ejercer derechos.

**Por qué.** Cuando desarrollas para un cliente, el cliente es el responsable y tú eres encargado. Si eso no queda por escrito, la responsabilidad queda ambigua ante la Agencia.

**Criterios de aceptación**

- [ ] El contrato con el cliente define los roles de responsable y encargado.
- [ ] Existe un canal de derechos (correo dedicado y formulario) que alimenta una cola única de solicitudes (ver 2.4).
- [ ] En proyectos N3 se evaluó designar un delegado de protección de datos, que forma parte del modelo de prevención de infracciones reconocido por la ley *\[validar\]*.

## Módulo 1 · Frontend y consentimiento

El frontend no decide nada: captura una acción afirmativa del usuario y la envía al backend, que es quien la registra y la hace valer.

### 1.1 Lógica de consentimiento centralizada

**Requisito.** La gestión del consentimiento (estado por categoría, versión de la política vigente, carga condicionada de scripts y envío al backend) vive en un único módulo reutilizable, independiente del framework de UI.

**Por qué.** Si cada proyecto o cada componente reimplementa la lógica, una corrección legal tiene que aplicarse N veces y alguna quedará sin aplicar.

**Criterios de aceptación**

- [ ] Existe un único punto de verdad para el estado del consentimiento dentro de la aplicación.
- [ ] Ningún componente consulta ni modifica el consentimiento por fuera de ese módulo.
- [ ] Cambiar las categorías o la versión de la política requiere tocar un solo lugar.

### 1.2 Bloqueo preventivo de scripts

**Requisito.** Ningún servicio de terceros (analítica, marketing, mapas de calor, embeds de video, mapas o redes sociales) se carga ni almacena información en el dispositivo antes de un consentimiento afirmativo para su categoría.

**Por qué.** El consentimiento posterior no legitima un tratamiento que ya ocurrió. Un script que se carga "solo un momento" antes del banner ya transmitió datos.

**Criterios de aceptación**

- [ ] Al cargar el sitio sin interactuar con el banner, no se emite ninguna petición de red a dominios de terceros no esenciales.
- [ ] Sin consentimiento, no existen cookies ni almacenamiento local de terceros; solo la preferencia de consentimiento, que es esencial.
- [ ] Si se usan herramientas de Google, operan en modo de consentimiento denegado por defecto hasta la aceptación.
- [ ] Una política de seguridad de contenido (CSP) actúa como segunda barrera ante scripts no autorizados.
- [ ] Los contenidos embebidos de terceros muestran un marcador que se carga solo a petición del usuario.

### 1.3 Banner y panel granular

**Requisito.** El banner ofrece aceptar y rechazar con igual facilidad, permite elegir por categoría y puede reabrirse en cualquier momento.

**Por qué.** Un rechazo más difícil que la aceptación es un patrón oscuro e invalida el consentimiento.

**Criterios de aceptación**

- [ ] "Aceptar" y "Rechazar" tienen el mismo tamaño, estilo, color y nivel de jerarquía, y están en la misma vista.
- [ ] Existen categorías separadas: esenciales (siempre activas) y, como mínimo, analítica y marketing, desactivadas por defecto y con los proveedores listados.
- [ ] Cerrar el banner sin elegir equivale a rechazar.
- [ ] Desde cualquier página, el usuario puede reabrir sus preferencias y revocar en un máximo de dos clics.
- [ ] Si cambia la versión de la política, se vuelve a pedir el consentimiento.
- [ ] El banner es operable con teclado y lector de pantalla y cumple el contraste WCAG AA.

### 1.4 Formularios de captura de datos

**Requisito.** Los formularios piden solo los datos necesarios y obtienen consentimientos separados, nunca premarcados.

**Por qué.** El consentimiento debe ser libre, específico e inequívoco. Amarrar el marketing a los Términos y Condiciones lo invalida.

**Criterios de aceptación**

- [ ] Ninguna casilla de consentimiento viene marcada por defecto.
- [ ] La aceptación de los Términos y Condiciones y de la Política de Privacidad está separada de cualquier consentimiento opcional (marketing, perfilamiento).
- [ ] El envío del formulario no depende de aceptar los consentimientos opcionales.
- [ ] Cada casilla corresponde a una finalidad del RAT y muestra la finalidad, su base de licitud y su plazo de retención, con un enlace al documento completo que se abre sin perder lo escrito en el formulario.
- [ ] Todo campo del formulario figura en el inventario (0.1); si no tiene finalidad, se elimina.
- [ ] Junto al formulario hay un aviso breve con enlace a la política completa. Las finalidades basadas en contrato u obligación legal se informan ahí, sin casilla, porque no dependen del consentimiento.
- [ ] El backend vuelve a validar los consentimientos obligatorios y no confía solo en el cliente.

### 1.5 Autoservicio de privacidad

**Requisito.** Los usuarios con cuenta pueden gestionar su privacidad sin escribir a soporte.

**Por qué.** El autoservicio reduce a casi cero el costo de atender derechos y elimina el riesgo de incumplir plazos por carga operativa.

**Criterios de aceptación**

- [ ] Existe una sección de privacidad en la cuenta que permite descargar los datos, solicitar la supresión, gestionar las preferencias y ver el historial de consentimientos.
- [ ] Las acciones de esa sección generan el mismo registro que una solicitud por correo (ver 2.4).

## Módulo 2 · Backend y datos

Regla central: **la supresión elimina o anonimiza de forma irreversible los datos personales**, no se limita a marcarlos con un flag. El borrado lógico (soft delete) sirve para el contenido y la moderación, no para cumplir la supresión.

### 2.1 Registro de consentimientos

**Requisito.** Cada otorgamiento o revocación de un consentimiento queda registrado de forma inmutable, con evidencia suficiente para demostrarlo ante la Agencia.

**Por qué.** Debes poder probar quién consintió qué, cuándo y bajo qué versión del documento. Al mismo tiempo, el registro no puede convertirse en un obstáculo para el derecho de supresión: tras una supresión debe dejar de identificar a la persona sin perder su historial.

**Criterios de aceptación**

- [ ] Cada registro incluye: un identificador de la persona (o de la sesión, para visitantes), la finalidad (identificador del tratamiento en el RAT o, para cookies, la categoría), la versión exacta del texto informado, el origen (banner, formulario, configuración), la IP truncada, el navegador, la fecha y hora y, si corresponde, la fecha de revocación.
- [ ] La fecha y hora la genera el servidor; cualquier valor enviado por el cliente se ignora.
- [ ] Ningún registro se puede borrar ni alterar, y esa restricción la impone la base de datos, no solo la aplicación. Las únicas excepciones son marcar la revocación y el proceso automático de retención.
- [ ] Una revocación queda registrada con su fecha, sin borrar ni alterar los datos del otorgamiento, y detiene esa finalidad en todos los sistemas que el RAT le asocia, sin afectar las demás.
- [ ] La IP se trunca antes de almacenarse: IPv4 a /24 e IPv6 a /48.
- [ ] Los visitantes anónimos se registran con un identificador de sesión, que se vincula a la cuenta si después inician sesión.
- [ ] Solo el backend puede escribir en el registro; el cliente no tiene acceso directo.
- [ ] Tras una supresión, ningún registro permite identificar a la persona, y el historial permanece intacto.
- [ ] Se puede obtener el estado vigente de cada consentimiento de una persona o sesión.

### 2.2 Supresión (derecho al olvido)

**Requisito.** Ante una solicitud de supresión, los datos personales se eliminan o se anonimizan de forma irreversible en todos los sistemas, sin romper la integridad de los datos ni las métricas históricas del negocio.

**Por qué.** Un flag de "borrado" deja la información intacta y no cumple con la supresión. Al mismo tiempo, borrar en cascada el contenido destruiría promedios, reseñas y transacciones que el negocio necesita conservar. Eliminar y anonimizar de forma irreversible cumplen por igual: lo que importa es que ningún dato permita volver a identificar a la persona.

Estrategia según la situación:

| Situación | Estrategia | Mecanismo |
| --- | --- | --- |
| Caso general: la cuenta no tiene obligaciones legales pendientes | **Eliminación o anonimización irreversible** | La identidad de autenticación queda inutilizable y sin datos de la persona; sus datos personales se eliminan o se anonimizan; el contenido se conserva y se muestra como "Usuario privado" |
| Existen documentos con obligación legal de conservación (facturas, boletas) | **Bloqueo + conservación mínima** | Se conserva solo lo que exige la ley, con acceso restringido, y se elimina o anonimiza al vencer el plazo |
| El contenido libre puede identificar a la persona (reseñas, comentarios) | **Opción para el usuario** | Preguntar: "¿Borrar también mi contenido?". Si responde no, el contenido se muestra como "Usuario privado" |

Secuencia mínima que debe cubrir cualquier implementación:

1. Registrar la solicitud en la cola de derechos (ver 2.4).
2. Verificar la identidad del solicitante con una reautenticación, para evitar borrados desde una sesión robada.
3. Eliminar los archivos asociados (avatares, adjuntos) en el almacenamiento de archivos, no solo sus referencias.
4. Aplicar la decisión sobre el contenido libre (borrarlo o dejarlo sin autor).
5. Solicitar la baja o el borrado en los proveedores externos (correo, CRM, analítica).
6. Enviar el acuse de cierre **antes** de eliminar o anonimizar el correo de contacto.
7. Inutilizar la identidad de autenticación (revocar sesiones y desvincular el correo y los proveedores de inicio de sesión), eliminar o anonimizar los datos personales y desvincular el contenido.

**Criterios de aceptación**

- [ ] Los datos personales viven en estructuras separadas del contenido, de modo que suprimirlos no obligue a borrar el contenido.
- [ ] Al suprimir a una persona, el contenido que se conserva queda desvinculado y se muestra con la etiqueta genérica "Usuario privado", idéntica en todos los casos y sin ningún dato que permita reidentificar a la persona, sin errores de integridad referencial. Si el producto tiene perfiles privados voluntarios, su etiqueta visible debe ser la misma, para que no se pueda distinguir una cuenta suprimida de una privada.
- [ ] Tras la supresión, no es posible iniciar sesión con las credenciales anteriores ni con los proveedores de inicio de sesión vinculados, y la persona puede volver a registrarse como un usuario nuevo.
- [ ] Ningún valor de reemplazo deriva del dato original. Un hash del correo o del RUT es seudonimización reversible, no anonimización.
- [ ] Los archivos del usuario dejan de existir en el almacenamiento, no solo en la base de datos.
- [ ] Los proveedores externos recibieron la solicitud de baja y queda constancia de ello.
- [ ] La ventana de retención de los backups está declarada en la política de privacidad.
- [ ] Existe una lista de supresiones ejecutadas (sin datos personales) para volver a aplicarlas si alguna vez se restaura un backup.
- [ ] El flujo completo se probó de punta a punta antes de salir a producción.

### 2.3 Trazabilidad y borrado lógico (solo contenido)

**Requisito.** Las tablas de contenido con interacción de usuarios registran cuándo se crearon, modificaron y ocultaron sus filas, y quién lo hizo. El contenido marcado como borrado deja de ser visible de inmediato.

**Por qué.** El borrado lógico sirve para moderación, papelera recuperable y auditoría. **No** satisface una solicitud de supresión de datos personales (ver 2.2).

**Criterios de aceptación**

- [ ] Cada tabla de contenido registra: fecha de creación, fecha de modificación, si está borrada, cuándo y por quién.
- [ ] El filtro de contenido borrado se aplica en la capa de datos (por ejemplo, con políticas de seguridad a nivel de fila), no solo en las consultas de la aplicación, de modo que no pueda olvidarse.
- [ ] Los accesos con privilegios elevados que se saltan esas políticas también excluyen el contenido borrado.
- [ ] Las reglas de unicidad ignoran las filas borradas.
- [ ] El contenido borrado lógicamente que contiene datos personales deja de identificar a la persona al vencer su plazo de retención (eliminación o anonimización).
- [ ] La referencia a quién borró se mantiene válida aunque esa persona sea suprimida después.

### 2.4 Derechos de los titulares como funcionalidad

**Requisito.** Los derechos de acceso, rectificación, supresión, oposición, portabilidad y bloqueo temporal se atienden mediante funcionalidades del producto y una cola única con control de plazos.

**Por qué.** El plazo de respuesta es de 30 días corridos, prorrogables una sola vez por otros 30, y el bloqueo temporal se resuelve en 2 días hábiles ([fuente](https://alayiatrust.com/blog/plazos-ley-21719)). Cumplir esos plazos de memoria no escala.

| Derecho | Cómo se atiende | Automatizable |
| --- | --- | --- |
| Acceso | Descarga de los datos en formato legible | Total |
| Rectificación | Edición desde la cuenta; para datos no editables, una solicitud | Mayoritaria |
| Supresión | Flujo de 2.2 | Total, salvo excepciones legales |
| Oposición | Preferencias granulares de marketing y perfilamiento | Total |
| Portabilidad | Exportación en formato estructurado y reutilizable, generada a partir del inventario | Total |
| Bloqueo temporal | Interrupción inmediata del tratamiento no esencial de esa persona | Total, con alerta el mismo día |

**Criterios de aceptación**

- [ ] Toda solicitud, sin importar su canal, queda registrada con su tipo, su estado, la fecha de recepción y la fecha de vencimiento.
- [ ] Una alerta automática avisa de las solicitudes a menos de 5 días de vencer y de cualquier bloqueo sin resolver.
- [ ] La exportación de datos incluye todo lo que declara el inventario, sin omisiones.
- [ ] Un bloqueo activo detiene efectivamente los procesos no esenciales sobre esa persona (marketing, perfilamiento, IA).
- [ ] La respuesta y su fecha quedan registradas.

### 2.5 Retención automática

**Requisito.** Cada plazo de retención del inventario se ejecuta mediante un proceso programado, sin intervención manual.

**Por qué.** Una política de retención que depende de que alguien se acuerde no se cumple.

**Criterios de aceptación**

- [ ] Existe un proceso programado por cada regla de retención del inventario.
- [ ] Las cuentas inactivas reciben un aviso antes de suprimirse y luego pasan por el mismo flujo de 2.2.
- [ ] Cada ejecución deja un registro (cuántos elementos procesó y cuándo).
- [ ] Un fallo del proceso genera una alerta.

## Módulo 3 · Seguridad (DevSecOps)

La implementación concreta de estos controles en el stack la define el estándar de ingeniería; aquí se fija el resultado exigible.

La ley exige medidas de seguridad apropiadas al riesgo. En la práctica, cada control de este módulo debe ser verificable de forma automática o quedar documentado.

### 3.1 Cifrado

**Requisito.** Los datos personales viajan y se almacenan cifrados, y los secretos de autenticación nunca se guardan en forma recuperable.

**Por qué.** El cifrado es la diferencia entre una brecha con datos legibles y una sin impacto real para las personas.

**Criterios de aceptación**

- [ ] Todo el tráfico, incluidos los subdominios de API, usa HTTPS obligatorio con HSTS, y solo se aceptan TLS 1.2 y 1.3.
- [ ] El almacenamiento de la base de datos y de los archivos está cifrado en reposo.
- [ ] Los campos de alto riesgo (RUT, datos de salud, tokens de terceros) tienen una capa de cifrado adicional a nivel de campo.
- [ ] Las contraseñas se almacenan con un algoritmo de hashing robusto (por ejemplo, argon2id) o se delegan en un proveedor de autenticación que lo garantice.
- [ ] Los tokens de API se almacenan hasheados y se muestran una sola vez.
- [ ] El sitio envía los headers de seguridad básicos: CSP, protección contra detección de tipo MIME, política de referer y política de permisos.

### 3.2 Mínimo privilegio en la capa de datos

**Requisito.** Cada usuario accede solo a sus propios datos, y esa regla se aplica en la base de datos, no solo en la aplicación.

**Por qué.** Un error en el backend o una API expuesta por defecto no debe bastar para filtrar datos de otros usuarios.

**Criterios de aceptación**

- [ ] Todas las tablas expuestas por una API tienen seguridad a nivel de fila activada, sin excepciones.
- [ ] Un usuario autenticado no puede leer, modificar ni borrar filas de otro usuario.
- [ ] Las credenciales con privilegios totales nunca llegan al frontend ni a un repositorio; viven solo en las variables de entorno del servidor.
- [ ] Los datos de alto riesgo y las tablas internas están en un espacio no expuesto por la API pública.
- [ ] Las funciones que se ejecutan con privilegios elevados están protegidas contra la manipulación de su contexto de ejecución.
- [ ] Antes de cada release se ejecuta un análisis de seguridad de la base de datos y no quedan alertas críticas.

### 3.3 Backoffice y accesos internos

**Requisito.** El acceso interno a datos de usuarios exige un segundo factor de autenticación, se limita por rol y queda registrado.

**Por qué.** Las credenciales del personal son el vector de ataque más común, y el abuso interno también es una brecha.

**Criterios de aceptación**

- [ ] Todo rol con acceso a datos de usuarios exige MFA, y esa exigencia se verifica en la capa de datos, no solo en la pantalla de login.
- [ ] Existen roles diferenciados (por ejemplo: soporte de solo lectura, moderador, administrador y superadministrador).
- [ ] Solo el rol de mayor privilegio puede exportar datos de forma masiva, y cada exportación queda en el log de auditoría.
- [ ] Los datos personales aparecen enmascarados por defecto en el backoffice, y revelarlos es una acción registrada.
- [ ] Los accesos elevados se revisan cada trimestre mediante un reporte automático.

### 3.4 Secretos, entornos y dependencias

**Requisito.** Los secretos están protegidos, los entornos no productivos no contienen datos reales y las dependencias se monitorean.

**Por qué.** Una base de staging con datos reales y peor protegida es una brecha esperando ocurrir.

**Criterios de aceptación**

- [ ] Los entornos de desarrollo y staging usan datos sintéticos, nunca copias de producción.
- [ ] Existe un escaneo automático de secretos antes de cada commit y en CI.
- [ ] Las dependencias vulnerables se detectan automáticamente y bloquean el paso a producción si son críticas.
- [ ] Las claves se rotan ante la salida de un colaborador o ante una sospecha de exposición.

### 3.5 Backups

**Requisito.** Existen backups funcionales, cifrados y con una retención declarada.

**Por qué.** Un backup que nunca se ha restaurado no es un backup, y uno sin retención definida contradice la política de supresión.

**Criterios de aceptación**

- [ ] Los backups de producción están activos y se ha probado una restauración en el último trimestre.
- [ ] La retención de los backups está declarada en la política de privacidad.
- [ ] Los backups que salen del proveedor principal van cifrados a un almacenamiento privado con su propia retención.

## Módulo 4 · Incidentes y monitoreo

Ante una brecha, la ley exige notificar a la Agencia por los medios más expeditos y sin dilaciones indebidas. No fija un plazo en horas, a diferencia del RGPD ([fuente](https://www.dmcia.cl/insights/ley-21719-proteccion-datos-empresas)). Como estándar interno, este playbook fija **72 horas** desde la detección: llegar antes es fácil de defender, y llegar tarde no.

### 4.1 Log de auditoría

**Requisito.** Los eventos críticos de seguridad y privacidad quedan registrados de forma inmutable, con una copia fuera del alcance de la aplicación.

**Por qué.** Sin registro no se puede reconstruir qué pasó en un incidente. Y si un atacante puede borrarlo, el registro no sirve.

**Criterios de aceptación**

- [ ] Se registran como mínimo: inicios de sesión fallidos y exitosos de roles elevados, cambios de rol y de MFA, exportaciones, revelaciones de datos personales en el backoffice, ejecuciones de supresión y cambios de versión de los documentos legales.
- [ ] El registro no se puede modificar ni borrar desde la aplicación.
- [ ] Existe una copia en un servicio externo al que la aplicación solo puede escribir, sin leer ni borrar.
- [ ] Los logs no contienen datos personales innecesarios: se registran identificadores, no correos, cuerpos completos de requests ni tokens.
- [ ] Existen alertas automáticas ante patrones anómalos: logins fallidos repetidos, exportaciones masivas, cambios de rol fuera de horario y picos de accesos denegados.

### 4.2 Respuesta a brechas

**Requisito.** Existe un procedimiento documentado y ensayado para contener, evaluar y notificar una brecha.

**Por qué.** En medio de un incidente no hay tiempo para pensar el proceso. Lo que no está escrito y ensayado, se improvisa mal.

El procedimiento debe cubrir, en orden:

1. **Contener**: rotar claves, revocar sesiones y cerrar el vector de ataque.
2. **Registrar**: abrir el incidente con la hora de detección. El reloj interno de 72 horas empieza aquí.
3. **Evaluar**: qué datos se afectaron, cuántas personas, si incluye categorías especiales y cuál es el riesgo para ellas.
4. **Notificar a la Agencia** si existe un riesgo razonable para los derechos de los titulares.
5. **Comunicar a los titulares** cuando corresponda según la tabla siguiente.
6. **Cerrar**: análisis de causa raíz, medidas adoptadas y cambios a este playbook.

| La brecha afecta | Agencia | Titulares |
| --- | --- | --- |
| Datos personales con riesgo razonable | Sí | Según la evaluación |
| Datos sensibles | Sí | **Sí, obligatorio** |
| Datos de menores de 14 años | Sí | **Sí, obligatorio** |
| Datos económicos, financieros, bancarios o comerciales | Sí | **Sí, obligatorio** |

La comunicación a los titulares es obligatoria cuando la brecha involucra datos sensibles, de menores de 14 años o económico-financieros ([fuente](https://idonea.cl/ley-proteccion-datos-personales-chile-guia/)). Si el proyecto o el cliente es un operador regulado por la Ley 21.663 Marco de Ciberseguridad, la misma brecha puede requerir también un reporte a la ANCI *\[validar\]*.

**Criterios de aceptación**

- [ ] El procedimiento está escrito, tiene responsables asignados y es accesible sin depender de los sistemas afectados.
- [ ] Cada incidente queda registrado con su hora de detección, su evaluación y las notificaciones enviadas.
- [ ] Se realiza un simulacro anual en un entorno de prueba y se mide el tiempo de respuesta.

### 4.3 Notificación preparada

**Requisito.** Las comunicaciones de una brecha están preparadas antes de que ocurra y pueden enviarse de forma masiva y controlada.

**Por qué.** Redactar bajo presión produce mensajes confusos y retrasos que la ley sanciona.

**Criterios de aceptación**

- [ ] Existen plantillas preaprobadas para la Agencia, para los titulares y para el aviso de cambio de credenciales.
- [ ] La comunicación a los titulares explica en lenguaje claro qué pasó, qué datos se afectaron, qué medidas se tomaron, qué debe hacer la persona y cómo contactar al responsable.
- [ ] El envío masivo permite una simulación previa (cuántos destinatarios, una muestra del mensaje) y requiere una confirmación explícita antes de enviar.

## Módulo 5 · Anexos de riesgo (se activan por nivel)

Estos anexos se suman a los Módulos 0 a 4; no los reemplazan. Un proyecto N3 aplica todos los que correspondan y, además, realiza una evaluación de impacto antes de construir.

### 5.1 Datos sensibles

Incluye: salud física y mental, opiniones políticas, creencias religiosas, origen étnico, vida y orientación sexual, datos biométricos y afiliación sindical.

**Requisito.** Los datos sensibles se tratan con consentimiento expreso y específico, aislados del resto, con acceso mínimo y con una evaluación de impacto previa.

**Por qué.** Su exposición puede causar discriminación o daño grave, y una brecha que los involucre obliga a notificar a cada persona afectada.

**Criterios de aceptación**

- [ ] El consentimiento para datos sensibles es una casilla específica, separada de los Términos, que nombra el dato y la finalidad.
- [ ] Los datos sensibles se almacenan separados del resto de los datos personales y con cifrado adicional a nivel de campo.
- [ ] Pueden eliminarse o bloquearse sin afectar al resto de la cuenta.
- [ ] Cuando el producto lo permite, el dato sensible se desvincula de la identidad. En una encuesta de opinión, por ejemplo, el registro de que alguien participó está separado de su respuesta.
- [ ] No se publican estadísticas de grupos de menos de 10 personas, porque permitirían reidentificar a alguien.
- [ ] Ningún rol de soporte accede a datos sensibles; solo el rol de mayor privilegio, con MFA y registro de cada acceso.
- [ ] Existe una evaluación de impacto documentada antes de construir, con los riesgos, las medidas y el riesgo residual *\[validar el formato que exija la Agencia\]*.

### 5.2 Menores de edad

La ley distingue entre niños (menores de 14 años) y adolescentes (de 14 a 17), y exige atender a su interés superior y a su autonomía progresiva ([fuente](https://holarumi.app/blog/ley-21719-psicologos-datos-de-pacientes)). Para los menores de 14 se requiere el consentimiento de los padres o representantes ([fuente](https://lawwwing.com/cumplimiento-legal-chile/)).

| Edad declarada | Tratamiento | Datos sensibles |
| --- | --- | --- |
| Menor de 14 | Consentimiento parental verificable | Consentimiento parental |
| 14 a 15 | Consentimiento propio *\[validar\]* | Consentimiento parental *\[validar\]* |
| 16 a 17 | Consentimiento propio | Consentimiento propio *\[validar\]* |
| 18 o más | Flujo normal | Flujo normal (5.1) |

**Requisito.** El producto conoce la edad del usuario, obtiene el consentimiento que corresponde según la tabla y aplica la máxima privacidad por defecto a las cuentas de menores.

**Por qué.** Tratar datos de un menor sin el consentimiento adecuado invalida todo el tratamiento, y una brecha con datos de menores de 14 obliga a notificar a cada afectado.

**Criterios de aceptación**

- [ ] El registro pide la fecha de nacimiento sin sugerir una edad mínima, para no incentivar que la persona mienta.
- [ ] El consentimiento parental se verifica (por ejemplo, con confirmación al correo del adulto) y queda en el registro de consentimientos con referencia al adulto que consintió.
- [ ] Las cuentas de menores no tienen perfil público, marketing, perfilamiento ni publicidad personalizada.
- [ ] Si el producto no está dirigido a menores, los Términos lo declaran y el registro de menores de 14 está bloqueado.
- [ ] Si el producto atiende situaciones de riesgo (salud mental, violencia, crisis), existe un protocolo de derivación a servicios de emergencia que funciona **sin** esperar el consentimiento parental, revisado por un abogado antes de lanzar.

### 5.3 IA y decisiones automatizadas

Aplica a cualquier proyecto que use modelos de IA sobre datos de usuarios: moderación, scoring, recomendaciones o resúmenes.

**Requisito.** El uso de IA sobre datos personales es transparente, minimizado, revisable por un humano cuando afecta a la persona y respeta la oposición del usuario.

**Por qué.** Una decisión automatizada que afecta a una persona sin explicación ni revisión posible expone al proyecto a reclamos y sanciones, y enviar datos personales a un proveedor de IA es una transferencia más.

**Criterios de aceptación**

- [ ] La política de privacidad informa qué decisiones toma o asiste la IA y con qué datos.
- [ ] El contenido generado por IA está etiquetado cuando el usuario podría confundirlo con contenido humano.
- [ ] Si una decisión automatizada afecta a la persona de forma significativa (bloqueo de cuenta, rechazo, puntaje), existe un canal para pedir revisión humana y una explicación de la lógica aplicada *\[validar alcance\]*.
- [ ] Los datos personales se redactan o se reemplazan por marcadores antes de enviarse al modelo, salvo que la finalidad lo impida.
- [ ] Los proveedores de IA no entrenan con tus datos, tienen retención mínima y figuran como encargados en el inventario.
- [ ] Los prompts y las respuestas se guardan solo si es imprescindible, con redacción aplicada y una retención corta (por ejemplo, 30 días).
- [ ] El usuario puede oponerse al perfilamiento por IA, y esa preferencia se respeta en todos los procesos.

## Módulo 6 · Verificación automática

Cómo se implementa cada verificación (hooks, CI, tests) lo define el estándar de ingeniería.

Una regla que no rompe el build tarde o temprano se deja de cumplir. Este módulo define **qué** debe verificarse de forma automática en cada proyecto; cada proyecto elige con qué herramientas hacerlo según su stack.

### 6.1 Principio

**Requisito.** Todo criterio de aceptación de los Módulos 1 a 5 que pueda verificarse con una máquina se convierte en un test o en un check del pipeline de integración continua. Los que no pueden automatizarse se revisan en el checklist de go-live.

**Por qué.** Los colaboradores y los agentes de IA cometen los mismos errores que cualquiera. Un check automático los detecta antes de producción, sin depender de que alguien se acuerde de revisar.

### 6.2 Verificaciones mínimas obligatorias

| Qué se verifica | Tipo de verificación | Requisito |
| --- | --- | --- |
| Todas las tablas expuestas tienen seguridad a nivel de fila | Test de base de datos | 3.2 |
| El registro de consentimientos rechaza modificaciones y borrados | Test de base de datos | 2.1 |
| Las relaciones hacia usuarios permiten la supresión sin romper la integridad | Test de base de datos | 2.2 |
| Un usuario no puede acceder a datos de otro | Test de integración | 3.2 |
| Sin consentimiento no hay peticiones a terceros ni cookies de seguimiento | Test end-to-end en navegador | 1.2 |
| Ninguna casilla de consentimiento viene premarcada | Análisis estático del código | 1.4 |
| Todo campo con datos personales figura en el inventario | Script que compara el esquema con el inventario | 0.1 |
| El flujo de supresión elimina datos, archivos e identidad | Test de integración | 2.2 |
| La exportación de datos incluye todo lo que declara el inventario | Test de integración | 2.4 |
| No hay secretos en el repositorio | Escaneo de secretos | 3.4 |
| No hay dependencias con vulnerabilidades críticas | Auditoría de dependencias | 3.4 |

**Criterios de aceptación**

- [ ] Cada verificación de la tabla existe en el proyecto o tiene una justificación documentada de por qué no aplica.
- [ ] Un fallo en cualquiera de ellas bloquea el paso a producción.
- [ ] Las verificaciones corren en cada pull request, no solo antes del release.

### 6.3 Automatizaciones con IA recomendadas

No son obligatorias, pero reducen el costo de cumplir:

- **Revisión de cambios**: un agente contrasta cada pull request con este playbook (campos nuevos sin inventario, scripts de terceros, datos personales en logs) y deja comentarios.
- **Borrador de la política de privacidad**: generado a partir del inventario y revisado por un abogado. Cuando cambia el inventario, se genera el diff de la política y se incrementa su versión.
- **Clasificación de solicitudes de derechos**: los correos del canal de privacidad se clasifican por tipo de derecho, se registran en la cola y se propone una respuesta para aprobación humana.
- **Monitoreo regulatorio**: un resumen semanal de novedades de la Agencia (reglamentos, guías, sanciones) con su impacto en este playbook.
- **Reglas para agentes de desarrollo**: este playbook se referencia en las instrucciones de los agentes de IA del proyecto, para que lo apliquen al generar código.

## Checklist de go-live

Ningún proyecto sale a producción con una casilla abierta, salvo que esté documentada como riesgo aceptado. El detalle de cada punto está en los criterios de aceptación de su módulo.

**Gobernanza**

- [ ] Nivel de riesgo asignado (N1, N2 o N3)
- [ ] Inventario de tratamientos completo y verificado automáticamente
- [ ] Acuerdos de tratamiento de datos de todos los encargados archivados y regiones elegidas
- [ ] Política de privacidad publicada y versionada, con bases de licitud, retención, transferencias y canal de derechos
- [ ] Si desarrollas para un cliente: tu rol de encargado está definido en el contrato

**Frontend**

- [ ] Lógica de consentimiento centralizada; banner con opciones simétricas; revocación en dos clics
- [ ] Verificado que sin consentimiento no hay peticiones a terceros ni cookies de seguimiento
- [ ] Formularios con consentimientos separados y sin casillas premarcadas
- [ ] Sección de privacidad en la cuenta con exportación, supresión y preferencias

**Backend y datos**

- [ ] Registro de consentimientos inmutable, verificado por test
- [ ] Flujo de supresión probado de punta a punta, incluidos archivos y proveedores externos
- [ ] Procesos de retención automáticos activos y con alertas
- [ ] Alertas de vencimiento de solicitudes de derechos funcionando

**Seguridad**

- [ ] Seguridad a nivel de fila en todas las tablas expuestas; análisis de seguridad sin alertas críticas
- [ ] MFA obligatorio para roles internos; datos personales enmascarados en el backoffice
- [ ] Headers de seguridad y HSTS verificados
- [ ] Restauración de backup probada al menos una vez

**Incidentes**

- [ ] Log de auditoría con copia externa de solo escritura
- [ ] Procedimiento de brechas escrito y plantillas de notificación preaprobadas

**Solo N3**

- [ ] Evaluación de impacto completada
- [ ] Datos sensibles aislados y con cifrado adicional
- [ ] Flujo de menores y consentimiento parental probado (si aplica)
- [ ] Revisión legal específica antes de lanzar

## Cambios v1 → v2

| Tema | v1 | v2 |
| --- | --- | --- |
| Formato | Mezcla de norma y código | Solo norma: Requisito → Por qué → Criterios de aceptación; la implementación la define el estándar de ingeniería |
| Supresión | Soft delete y DELETE prohibido, pero dependía de SET NULL | Eliminación o anonimización irreversible de los datos personales, con estrategia según la situación; el soft delete queda solo para contenido |
| Anonimización | Hash del dato original | Valores sin relación con el original; el hash es solo seudonimización |
| Registro de consentimientos | Identidad directa, sin retención definida | Inmutable, por finalidad del RAT y con retención; deja de identificar a la persona tras la supresión |
| IP | Último octeto | IPv4 /24 e IPv6 /48 |
| Derechos | Solo supresión | Los seis derechos, con plazos y alertas |
| Brechas | Notificar a los usuarios en cualquier caso | Agencia según riesgo; titulares en los tres casos obligatorios; objetivo interno de 72 horas |
| Alcance | Genérico | Niveles de riesgo y anexos para datos sensibles, menores e IA |
| Ejecución | Checklist manual | Verificaciones automáticas mínimas obligatorias |

## Fuentes

- **Fuente primaria:** [Ley 21.719 — texto oficial, Biblioteca del Congreso Nacional](https://www.bcn.cl/leychile/navegar?idNorma=1209272)
- [Plazos de la Ley 21.719 — Alaiya Trust](https://alayiatrust.com/blog/plazos-ley-21719)
- [Guía Ley 21.719 — Idónea](https://idonea.cl/ley-proteccion-datos-personales-chile-guia/)
- [Ley 21.719 para empresas — DMCIA](https://www.dmcia.cl/insights/ley-21719-proteccion-datos-empresas)
- [Cumplimiento legal web en Chile — Lawwwing](https://lawwwing.com/cumplimiento-legal-chile/)
- [Ley 21.719 y datos de pacientes — Rumi](https://holarumi.app/blog/ley-21719-psicologos-datos-de-pacientes)

Las demás son fuentes secundarias. Ante cualquier discrepancia prevalece el texto oficial. Antes de comprometer plazos con un cliente, contrasta los puntos *\[validar\]* con el texto oficial en la Biblioteca del Congreso Nacional y con un abogado.
