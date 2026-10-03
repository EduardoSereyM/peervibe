# 📋 Playbook Estratégico: Plataforma de Referencia y Calificación de Productos
**Etapa: maduración, conceptualización y definición del MVP**

Este documento define **qué** se construye en peervibe: la idea, el producto y sus decisiones propias. **Cómo** se construye lo define `ENGINEERING_STANDARDS`, y **qué exige la ley**, el Playbook de Privacidad. Este documento no repite sus reglas; si necesita una excepción al estándar, se documenta en un ADR.

> **v1.3.** Alineado con ENGINEERING_STANDARDS v6.1.0 y el Playbook de Privacidad v2.1: el modelo de datos (sección 7) pasa a ser conceptual, sin SQL; la implementación la define el estándar.

---

## 1. Definición del Enfoque y Modelo de Datos

Antes de abrir la plataforma al público, se debe definir con precisión qué se va a calificar y cómo se estructurará la información para evitar el caos de datos.

### 🔲 Alcance Inicial (Vertical vs. Horizontal)
* [ ] **Definir el nicho de lanzamiento (Caballo de Troya):** Elegir una o dos categorías específicas de alta fricción de compra (ej. tecnología, cosmética, suplementos) en lugar de lanzar un catálogo generalista.
* [ ] **Establecer plan de escalabilidad:** Diseñar la arquitectura de la base de datos de forma flexible para que añadir nuevas categorías en el futuro no rompa el sistema.

### 🔲 Atributos de la Ficha de Producto
* [ ] **Identificadores universales:** Asegurar campos para códigos de barra/identificadores estándar (EAN, UPC, ASIN o ISBN) para evitar duplicados.
* [ ] **Criterios de evaluación multifactorial:** Definir de 3 a 4 variables de nota por categoría (ej. para tecnología: *Batería, Diseño, Relación Calidad/Precio*; para cosmética: *Eficacia, Textura, Duración*).

---

## 2. El Factor de Confianza (Anti-Fraude y Moderación)

El valor de un sitio de reseñas radica exclusivamente en la credibilidad de sus datos. Las reseñas falsas o compradas destruyen la plataforma.

### 🔲 Sistema de Verificación de Reseñas
* [ ] **Definir niveles de certeza:**
  * *Nivel 1 (Básico):* Usuario registrado opina de forma abierta.
  * *Nivel 2 (Verificado):* El usuario sube foto del ticket de compra, caja del producto o vincula su cuenta con un ecommerce.
* [ ] **Trazabilidad temporal:** Implementar el concepto de **Reseña Evolutiva** (permitir o incentivar al usuario a actualizar su opinión tras 1, 3 o 6 meses de uso).

### 🔲 Reglas de Moderación y Algoritmo de Confianza
* [ ] **Filtros automatizados (Shadowban/Spam):** Bloqueo de cuentas que publiquen múltiples reseñas con la misma IP en cortos periodos de tiempo. La IP nunca se almacena en claro: se guarda un HMAC con una clave que rota cada 90 días (RAT T-05; ver `fraud_signals` en la sección 7).
* [ ] **Baneos automáticos con salvaguardas:** aviso al usuario y revisión humana antes de un baneo definitivo (decisión automatizada: Playbook de Privacidad 5.3).
* [ ] **Algoritmo de ponderación:** El puntaje final del producto no debe ser un promedio simple. Debe pesar más la opinión de un usuario verificado y con historial que la de un usuario nuevo.

---

## 3. Estrategia de Incentivos y Comunidad (Gamificación)

Nadie escribe reseñas gratis de forma masiva a menos que haya un disparador psicológico, de estatus o económico.

### 🔲 Sistema de Reputación del Usuario
* [ ] **Roles y Medallas:** Crear rangos por categoría (ej. *"Cata-Cafés Experto"*, *"Tech-Guru"*).
* [ ] **Sistema de puntos por acción:**
  * +10 pts por reseña escrita.
  * +30 pts por subir foto real del producto.
  * +50 pts por reseña verificada con ticket.
  * +5 pts cuando otros usuarios marquen la reseña como "Útil".

### 🔲 Incentivos para el Usuario
* [ ] **Beneficios tangibles:** Alianzas con marcas del nicho para ofrecer muestras gratis o cupones de descuento a los usuarios con mayor reputación (sin comprometer la imparcialidad de sus notas).

---

## 4. Viabilidad Comercial y Monetización

Determinar cómo se sustentará la plataforma a largo plazo sin caer en el conflicto de interés (cobrar a marcas por alterar notas).

### 🔲 Canales de Ingreso del MVP
* [ ] **Afiliación Inteligente:** Botón de "Comprar" redirigiendo a tiendas oficiales (Amazon, retailers locales) con tracking ID para comisiones.
* [ ] **Herramientas B2B para Marcas:** Espacio donde las marcas puedan responder a las críticas, reclamar el perfil de su producto de manera oficial y analizar métricas (sin poder borrar comentarios negativos).

---

## 5. Arquitectura del MVP (Producto Mínimo Viable)

Lista de funcionalidades mínimas requeridas para el lanzamiento de la primera versión web Beta.

### 🔲 Funcionalidades Core (Obligatorias para el Día 1)
* [ ] **Buscador predictivo:** Barra de búsqueda semántica de productos por nombre, marca o categoría.
* [ ] **Módulo de login/registro sencillo:** Autenticación fluida (Google/Apple) para reducir la fricción. El registro pide solo un `username`; no se solicita nombre real, edad, país ni ciudad (D-02, D-03).
* [ ] **Solo mayores de 18 (D-01):** el registro incluye una declaración obligatoria de mayoría de edad, y los Términos lo establecen. Se registra como declaración de mayoría de edad, según el estándar (PRIV-005).
* [ ] **Una sola casilla opcional en el registro:** "Recibir novedades y promociones" (RAT T-11), desmarcada por defecto. Los demás tratamientos de la cuenta se informan en un aviso breve, sin casilla.
* [ ] **Formulario de reseña estructurado:** Campos de Pros, Contras, Comentario libre y barras de selección de estrellas desglosadas.
* [ ] **Perfil de usuario público:** Historial de reseñas del usuario para validar su criterio frente a la comunidad.
* [ ] **Página de producto optimizada para SEO:** Estructura de metadatos (Schema.org de *Product Review*) para que Google indexe las calificaciones y aparezcan en los resultados de búsqueda globales.

---

## 🚀 Próximos Pasos Inmediatos
1. Seleccionar la **categoría semilla** (Nicho inicial).
2. Definir las 3 variables de calificación específicas para esa categoría.
3. Crear el prototipo visual (Wireframes) del flujo: *Buscar Producto -> Leer Reseña -> Escribir Reseña*.
4. Definir categorias y sub categorias de productos tal como lo haria un retail o supermercado por ejemplo para tener un orden semantico de productos desde el comienzo.
5. Decidir si el SEO de las fichas se resuelve dentro del estándar (SPA con endpoint de Open Graph, ARQ-014) o exige SSR/prerenderizado con un ADR.



## 6. Arquitectura de Interfaz (UX/UI) y Flujo de Datos

Estructura de las tres pantallas críticas del MVP. Este diseño dicta la lógica de los endpoints de la API y las consultas a la base de datos.

### 🔲 Vista Home (Búsqueda y Descubrimiento)
* [ ] **Buscador Central Predictivo:** Implementar una barra de búsqueda con autocompletado semántico (*as-you-type*) que muestre de forma inmediata: *Miniatura del producto, marca y nota promedio*.
* [ ] **Carrusel de productos mas votados**
* [ ] **Módulo de Tendencias y Actividad:** Diseñar un grid dinámico para productos populares y un feed en tiempo real de "Reseñas Recientes" para generar sensación de comunidad activa.
* [ ] **Impacto Técnico:** Requiere búsqueda de texto rápida (por defecto, PostgreSQL Full-Text Search, dentro del stack; otra tecnología exige aprobación según ARQ-002) y caché de las listas de tendencias (perfil opcional `cache`, con ADR según ARQ-015).

### 🔲 Vista Ficha de Producto (Lectura y Conversión)
* [ ] **Cabecera Multifactorial:** Mostrar la nota general desglosada mediante un gráfico visual (radar o barras) basado en los 3 o 4 criterios específicos de la categoría.
* [ ] **Bloque de Síntesis IA:** Diseñar un contenedor destacado de "Pros y Contras resumidos por IA" que extraiga los puntos más repetidos antes de que el usuario baje a leer todo el listado.
  * Entrada: solo el texto de reseñas aprobadas, sin `username` (RAT T-07). El bloque va etiquetado como IA y el usuario puede excluir sus reseñas de la síntesis.
* [ ] **Módulo de Reseñas Filtrables:** Tarjetas de reseña que muestren claramente el avatar, rango del usuario, medalla de "Compra Verificada" y botón para votar si la reseña fue "Útil".
* [ ] **Sidebar de Monetización:** Caja flotante lateral (*Sticky Sidebar*) con los botones de redirección de compra ("Ver precio en...") configurados con enlaces de afiliación.
* [ ] **Impacto Técnico:** Las calificaciones deben ser indexables por Google con metadatos JSON-LD (Schema.org de *Product Review*). El estándar fija por defecto una SPA con endpoint de Open Graph (ARQ-014); si eso no basta para el SEO de las fichas, SSR o prerenderizado se aprueban con un ADR. **Decisión pendiente** (Próximos pasos, punto 5).

### 🔲 Vista Formulario de Reseña (Captura y Reducción de Fricción)
* [ ] **Flujo Asistido (Stepper):** Dividir el formulario en 3 pasos rápidos:
  * *Paso 1:* Deslizadores o clics para las calificaciones por estrellas obligatorias.
  * *Paso 2:* Dos cajas de texto obligatorias y guiadas (*"¿Qué es lo que más te gustó?"* y *"¿Qué es lo que menos te gustó?"*). Incluyen un aviso visible: *"Tu reseña será pública. No incluyas datos de salud, tus datos personales ni los de otras personas."*
  * *Paso 3:* Zona de arrastre (*Drag & Drop*) opcional para subir fotos reales del producto o del ticket de compra. Al subir un comprobante aparece la casilla de consentimiento *"Usar mi comprobante para verificar la compra · se borra 30 días después de verificar"* (RAT T-04), con la recomendación de tapar los datos personales.
* [ ] **Impacto Técnico:** Supabase Storage (perfil `uploads`, SEC-015) con un pipeline en el backend que optimice, comprima y redimensione las imágenes automáticamente.


## 7. Modelo de Datos (conceptual) `[P0]`

Qué entidades necesita peervibe y qué reglas **propias del producto** tienen. Las columnas canónicas, el borrado lógico, la RLS, los GRANTs, las migraciones y la supresión los define `ENGINEERING_STANDARDS`; los requisitos legales, el Playbook de Privacidad. Esta sección no los repite.

### 🔲 Entidades

| Entidad | Contenido | Reglas propias de peervibe |
|---|---|---|
| `user_profiles` | `username`, avatar, puntos de reputación, rango, baneo | Perfil público: visible para cualquiera mientras esté activo y no baneado. El usuario solo edita `username` y avatar; reputación, rango y baneo los gestiona el backend. |
| `products` | Nombre, `slug`, marca, descripción, imagen, `gtin` (EAN/UPC/ASIN, único), categoría | `rating_avg` y `review_count` se guardan precalculados: nunca se calculan promedios en la lectura de una ficha. |
| `categories` | Árbol de categorías y subcategorías | **Pendiente de definir** (Próximos pasos, punto 4). |
| `reviews` | Pros, contras, comentario, `ratings_breakdown` (JSONB por criterio de la categoría), `rating_final`, `is_verified`, estado (`pending`, `approved`, `rejected`), `helpful_votes` | Nace `pending`, sin verificar y con 0 votos. El usuario edita solo el texto y las calificaciones; `rating_final`, el estado, la verificación y los votos los gestiona el backend. Solo las `approved` son públicas. **Pendiente:** si editar una reseña aprobada la devuelve a `pending`. |
| `review_proofs` | Imagen del comprobante (bucket privado) y estado de la verificación | Nunca es pública: la ficha muestra solo la medalla "Compra Verificada". La ven el autor y la moderación. La imagen se borra 30 días después de verificar o rechazar (RAT T-04). |
| `review_votes` | Voto útil o no útil | Un voto por cuenta y reseña. `helpful_votes` se mantiene sincronizado con los votos. |
| `fraud_signals` | Tipo de evento, HMAC de la IP con versión de clave, agente de usuario | Sin acceso desde el cliente. La IP nunca se guarda en claro: HMAC con clave que rota cada 90 días; retención de 90 días (RAT T-05). |

### 🔲 Privacidad del proyecto

Decisiones propias de peervibe. El detalle de finalidades, bases y plazos vive en el RAT (`docs/privacy/rat.yaml`, que en la Fase 0 del estándar pasa a `docs/PRIVACY_POLICY_NOTES.md`, PRIV-006).

| # | Decisión |
|---|---|
| D-01 | Solo mayores de 18 años. |
| D-02 | No se pide el nombre real: la identidad pública es el `username`. |
| D-03 | No se recolectan rango de edad, país ni ciudad hasta que exista una finalidad concreta. |
| D-04 | Analítica sin cookies ni datos personales; mientras no haya cookies no esenciales, no se requiere banner de cookies *[validar]*. |
| D-05 | Al suprimir la cuenta, el usuario elige borrar sus reseñas o conservarlas como "Usuario privado". |
| D-06 | Responsable: persona natural. Evaluar la constitución de una SpA antes del lanzamiento público. |

Perfil del proyecto para la Fase 0 del estándar (`docs/PROJECT_PROFILE.yaml`): `datos_personales: true` · `rut: none` · `llm: true` (`llm_usos: resumen`) · `uploads: true` · `pagos_webhooks: false`. Nivel de riesgo según el Playbook de Privacidad: **N2**.
