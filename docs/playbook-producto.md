# 📋 Playbook Estratégico: Plataforma de Referencia y Calificación de Productos
**Fase 0: Maduración, Conceptualización y Definición del MVP**

Este documento sirve como hoja de ruta y lista de verificación (*checklist*) para asentar las bases del proyecto antes de escribir la primera línea de código. Su objetivo es mitigar riesgos, definir el enfoque estratégico y estructurar la propuesta de valor.

> **v1.1 (Paso 1 de la revisión de privacidad).** Correcciones estructurales al modelo de datos (sección 7) según el Playbook de Privacidad v2: relaciones hacia usuarios compatibles con la supresión, registro de consentimientos inmutable y escrito solo por el backend, comprobantes de compra privados, datos personales aislados del perfil público, protección anti-fraude a nivel de columnas y votos que sobreviven a la supresión. Las correcciones que dependen del RAT quedan marcadas como `[Paso 3]`.

> **v1.2 (Paso 3).** Alineado con el RAT v0.2 (`rat.yaml`) y las decisiones D-01 a D-06: solo mayores de 18, sin nombre real ni datos demográficos (se elimina `user_private`), consentimientos referenciados por finalidad del RAT, señales antifraude con la IP en HMAC rotativo, elección del usuario sobre sus reseñas al suprimir la cuenta, aviso de datos de salud en el formulario y salvaguardas para la síntesis con IA.

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
* [ ] **Revisión humana de baneos:** un baneo automático es una decisión con efecto significativo. El usuario recibe un aviso y puede pedir revisión humana antes de que el baneo sea definitivo.
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
* [ ] **Solo mayores de 18 (D-01):** el registro incluye una declaración obligatoria de mayoría de edad, y los Términos lo establecen. Es una declaración, no un consentimiento: no va en el registro de consentimientos.
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



## 6. Arquitectura de Interfaz (UX/UI) y Flujo de Datos

Estructura de las tres pantallas críticas del MVP. Este diseño dicta la lógica de los endpoints de la API y las consultas a la base de datos.

### 🔲 Vista Home (Búsqueda y Descubrimiento)
* [ ] **Buscador Central Predictivo:** Implementar una barra de búsqueda con autocompletado semántico (*as-you-type*) que muestre de forma inmediata: *Miniatura del producto, marca y nota promedio*.
* [ ] **Carrusel de productos mas votados**
* [ ] **Módulo de Tendencias y Actividad:** Diseñar un grid dinámico para productos populares y un feed en tiempo real de "Reseñas Recientes" para generar sensación de comunidad activa.
* [ ] **Impacto Técnico:** Requiere indexación de texto rápido (ej. Meilisearch, Elasticsearch o PostgreSQL Full-Text Search) y almacenamiento en caché de las listas de tendencias para evitar saturar la base de datos.

### 🔲 Vista Ficha de Producto (Lectura y Conversión)
* [ ] **Cabecera Multifactorial:** Mostrar la nota general desglosada mediante un gráfico visual (radar o barras) basado en los 3 o 4 criterios específicos de la categoría.
* [ ] **Bloque de Síntesis IA:** Diseñar un contenedor destacado de "Pros y Contras resumidos por IA" que extraiga los puntos más repetidos antes de que el usuario baje a leer todo el listado.
  * Al modelo se envía solo el texto de reseñas aprobadas, sin `username`, con redacción automática de nombres, correos, teléfonos y RUT (RAT T-07).
  * El proveedor de IA no entrena con estos datos y no los retiene; figura como encargado en el RAT.
  * El bloque se etiqueta como generado por IA, y el usuario puede excluir sus reseñas de la síntesis.
* [ ] **Módulo de Reseñas Filtrables:** Tarjetas de reseña que muestren claramente el avatar, rango del usuario, medalla de "Compra Verificada" y botón para votar si la reseña fue "Útil".
* [ ] **Sidebar de Monetización:** Caja flotante lateral (*Sticky Sidebar*) con los botones de redirección de compra ("Ver precio en...") configurados con enlaces de afiliación.
* [ ] **Impacto Técnico:** Esta vista debe renderizarse del lado del servidor (SSR con Next.js/Remix) e incluir metadatos JSON-LD (Schema.org) para garantizar el posicionamiento SEO de las calificaciones en Google.
  > ⚠️ **Decisión pendiente:** el estándar de ingeniería fija React + Vite + TanStack Router (SPA). El SEO de las fichas requiere HTML renderizado en el servidor o prerenderizado. Opciones: declarar peervibe como excepción documentada al estándar (SSR) o resolver el SEO con prerenderizado de las fichas manteniendo Vite.

### 🔲 Vista Formulario de Reseña (Captura y Reducción de Fricción)
* [ ] **Flujo Asistido (Stepper):** Dividir el formulario en 3 pasos rápidos:
  * *Paso 1:* Deslizadores o clics para las calificaciones por estrellas obligatorias.
  * *Paso 2:* Dos cajas de texto obligatorias y guiadas (*"¿Qué es lo que más te gustó?"* y *"¿Qué es lo que menos te gustó?"*). Incluyen un aviso visible: *"Tu reseña será pública. No incluyas datos de salud, tus datos personales ni los de otras personas."*
  * *Paso 3:* Zona de arrastre (*Drag & Drop*) opcional para subir fotos reales del producto o del ticket de compra. Al subir un comprobante aparece la casilla de consentimiento *"Usar mi comprobante para verificar la compra · se borra 30 días después de verificar"* (RAT T-04), con la recomendación de tapar los datos personales.
* [ ] **Impacto Técnico:** Integración con buckets de almacenamiento (AWS S3 o Supabase Storage) con un pipeline intermedio que optimice, comprima y redimensione las imágenes automáticamente en el backend.


## 7. Modelo de Datos Relacional (Base de Datos) `[P0]`

Diseño del esquema de base de datos relacional para PostgreSQL / Supabase. Garantiza integridad referencial, control anti-fraude, paridad idiomática (infraestructura en inglés, dominio en español), trazabilidad total y cumplimiento de la Ley 21.719 según el **Playbook de Privacidad v2**.

### 🔲 Principios del modelo `[P0]`
* [ ] **Minimización por diseño (D-02, D-03):** peervibe no recolecta nombre real, edad, país ni ciudad. Los únicos datos personales de la cuenta son el correo y el identificador del proveedor OAuth (en Supabase Auth) y el perfil público (`username`, avatar). Si en el futuro aparece una finalidad nueva, se agrega primero al RAT y luego al esquema.
* [ ] **El contenido apunta al perfil con `ON DELETE SET NULL`:** al suprimir una cuenta, las reseñas y los votos se conservan desvinculados y se muestran como **"Usuario privado"** (Playbook de Privacidad v2, 2.2).
* [ ] **Toda referencia a usuarios permite la supresión:** las columnas `created_by`, `updated_by`, `deleted_by` y cualquier otra relación hacia `auth.users` o `user_profiles` declaran `ON DELETE SET NULL` o `ON DELETE CASCADE`. Sin esta regla, el `ON DELETE` por defecto (`NO ACTION`) **impide eliminar a cualquier usuario que haya creado algo**.
* [ ] **Los campos que el usuario no debe controlar no se pueden escribir desde el cliente:** reputación, rango, estado de moderación, verificación y contadores se modifican solo desde el backend o mediante triggers.

### 🔲 Columnas Canónicas Obligatorias de Auditoría y Soft Delete `[P0]`
* [ ] **Campos de Trazabilidad:** toda tabla de contenido incluye `created_at`, `updated_at` (`TIMESTAMPTZ`), `created_by` y `updated_by` (`UUID`, con `ON DELETE SET NULL`).
* [ ] **Estrategia Soft Delete (Sección 14):** toda tabla de contenido incorpora `is_deleted`, `deleted_at` y `deleted_by` (este último con `ON DELETE SET NULL`). El soft delete sirve para moderación y papelera; **no** satisface una solicitud de supresión de datos personales.
* [ ] **Excepciones declaradas:** `consents` y `privacy_subjects` (registro probatorio append-only), `fraud_signals` (retención corta con borrado real) y `review_votes` (retirar un voto es un borrado legítimo).
* [ ] **Trigger de Actualización:** refresco automático de `updated_at` mediante un trigger `BEFORE UPDATE` enganchado a la función canónica `update_updated_at()`.

### 🔲 Supresión de cuenta (derecho al olvido)
* [ ] **El usuario elige qué pasa con sus reseñas (D-05):** antes de confirmar, se le pregunta si quiere borrar sus reseñas o conservarlas como "Usuario privado". Si elige borrarlas, se eliminan físicamente junto con sus fotos y los promedios de los productos se recalculan.
* [ ] **Flujo orquestado por el backend (FastAPI):** registrar la solicitud → reautenticar al usuario → aplicar su elección sobre las reseñas → borrar sus archivos en Storage (avatar, comprobantes) → dar de baja su correo en Resend → enviar el acuse → eliminar la identidad con la Admin API de Supabase Auth.
* [ ] **Efecto en cascada:** al eliminar `auth.users`, se eliminan `user_profiles` y `privacy_subjects` (`CASCADE`); las reseñas y los votos quedan con `user_id = NULL` (`SET NULL`) y el registro de consentimientos queda desvinculado, pero intacto.
* [ ] **Sin hashes del dato original:** no se sobrescriben valores con hashes de los datos originales, porque eso es seudonimización y no anonimización.

### 🔲 Tabla: `public.user_profiles` (Módulo `users`) — perfil público
* [ ] **Estructura Técnica:** solo contiene datos que el usuario acepta mostrar públicamente (`username`, `avatar_url`, reputación y rango). Es la tabla que alimenta el **Perfil de usuario público** (sección 5).
* [ ] **Anti-fraude:** el usuario solo puede editar `username` y `avatar_url`. La reputación, el rango y el baneo se gestionan desde el backend.

```sql
create table public.user_profiles (
  id                uuid         primary key references auth.users(id) on delete cascade,
  username          varchar(50)  unique not null,
  avatar_url        text         null,
  reputation_points int          not null default 0,
  user_rank         varchar(50)  not null default 'Novato',
  is_banned         boolean      not null default false,

  created_at    timestamptz  not null default now(),
  updated_at    timestamptz  not null default now(),
  created_by    uuid         null references auth.users(id) on delete set null,
  updated_by    uuid         null references auth.users(id) on delete set null,
  is_deleted    boolean      not null default false,
  deleted_at    timestamptz  null,
  deleted_by    uuid         null references auth.users(id) on delete set null
);

create trigger trg_user_profiles_updated_at before update on public.user_profiles
  for each row execute function update_updated_at();

alter table public.user_profiles enable row level security;

create policy "cualquiera ve perfiles públicos activos" on public.user_profiles
  for select using (is_deleted = false and is_banned = false);

create policy "usuarios crean su propio perfil" on public.user_profiles
  for insert with check (
    (select auth.uid()) = id
    and reputation_points = 0 and user_rank = 'Novato' and is_banned = false
  );

create policy "usuarios editan su propio perfil" on public.user_profiles
  for update using ((select auth.uid()) = id and is_deleted = false)
  with check ((select auth.uid()) = id);

-- El cliente solo puede modificar estas columnas
revoke update on public.user_profiles from anon, authenticated;
grant update (username, avatar_url) on public.user_profiles to authenticated;
```

### 🔲 Tablas: `public.privacy_subjects` y `public.consents` (Módulo `auth` / Privacidad)
* [ ] **Estructura Técnica:** registro probatorio de consentimientos (Playbook de Privacidad v2, 2.1). El log guarda un `subject_id` seudónimo en vez del `user_id`; al suprimir la cuenta se borra el mapeo y el log queda intacto, pero desvinculado de la persona.
* [ ] **Append-only:** cada otorgamiento o revocación es una fila nueva (`action`). No existen `UPDATE` ni `DELETE`.
* [ ] **Solo el backend inserta:** FastAPI registra el consentimiento con la fecha y hora del servidor y la IP truncada (IPv4 /24, IPv6 /48). El cliente no tiene política de inserción.
* [ ] **Por finalidad del RAT:** `purpose_id` referencia el ID del tratamiento en `rat.yaml` (hoy solo `T-04` verificación de compra y `T-11` promociones requieren consentimiento). La aceptación de Términos y del aviso de privacidad se registra con `purpose_id = 'terms'` o `'privacy_notice'`, como evidencia de la versión informada. La validez de los IDs se verifica en CI contra el RAT, no con un `CHECK` fijo en la base.

```sql
create table public.privacy_subjects (
  user_id     uuid         primary key references auth.users(id) on delete cascade,
  subject_id  uuid         not null unique default gen_random_uuid(),
  created_at  timestamptz  not null default now()
);

alter table public.privacy_subjects enable row level security;
create policy "titular ve su sujeto" on public.privacy_subjects
  for select using ((select auth.uid()) = user_id);

create table public.consents (
  id               uuid         primary key default gen_random_uuid(),
  subject_id       uuid         null,  -- sin FK a propósito: se desvincula al suprimir
  session_id       uuid         null,  -- visitantes anónimos
  purpose_id       text         not null,  -- ID del RAT (T-04, T-11) o 'terms' / 'privacy_notice'
  document_version text         not null,
  action           text         not null check (action in ('granted', 'revoked')),
  source           text         not null,  -- banner | signup_form | account_settings
  ip_truncated     inet         null,
  user_agent       text         null,
  created_at       timestamptz  not null default now(),
  check (subject_id is not null or session_id is not null)
);

alter table public.consents enable row level security;

create policy "titular ve su historial de consentimientos" on public.consents
  for select using (
    subject_id in (
      select subject_id from public.privacy_subjects where user_id = (select auth.uid())
    )
  );
-- Sin políticas de insert, update ni delete: solo el backend escribe.

create or replace function public.forbid_mutation() returns trigger
language plpgsql as $$
begin
  if tg_op = 'DELETE' and current_setting('app.retention_purge', true) = 'on' then
    return old;
  end if;
  raise exception '% es append-only', tg_table_name;
end $$;

create trigger consents_append_only before update or delete on public.consents
  for each row execute function public.forbid_mutation();
```

### 🔲 Tabla: `public.products` (Módulo `products`)
* [ ] **Campos Core:** catálogo central indexado mediante el identificador único global `gtin` (EAN/UPC/ASIN) para mitigar duplicidades operativas.
* [ ] **Caché Asíncrona de Rendimiento (Sección 27.2):** `rating_avg` y `review_count` se almacenan precalculados. Queda prohibido computar agregaciones (`AVG()`) en el camino caliente de lectura de las fichas de producto.
* [ ] **Pendiente:** la tabla `public.categories` se referencia, pero aún no está definida (ver "Próximos Pasos Inmediatos", punto 4).

```sql
create table public.products (
  id            uuid         primary key default gen_random_uuid(),
  category_id   int          references public.categories(id) on delete restrict,
  name          varchar(255) not null,
  slug          varchar(255) unique not null,
  brand         varchar(100) not null,
  description   text         null,
  image_url     text         null,
  gtin          varchar(14)  unique not null,

  rating_avg    decimal(3,2) not null default 0.00,
  review_count  int          not null default 0,

  created_at    timestamptz  not null default now(),
  updated_at    timestamptz  not null default now(),
  created_by    uuid         null references auth.users(id) on delete set null,
  updated_by    uuid         null references auth.users(id) on delete set null,
  is_deleted    boolean      not null default false,
  deleted_at    timestamptz  null,
  deleted_by    uuid         null references auth.users(id) on delete set null
);

create trigger trg_products_updated_at before update on public.products
  for each row execute function update_updated_at();

alter table public.products enable row level security;
create policy "cualquiera ve productos activos" on public.products
  for select using (is_deleted = false);
```

### 🔲 Tabla: `public.reviews` (Módulo `reviews`)
* [ ] **Vínculos:** relación `SET NULL` hacia `user_profiles`. Ante una supresión, la reseña permanece y se muestra como **"Usuario privado"**, preservando la integridad analítica del catálogo.
* [ ] **Calificación Multifactorial Dinámica:** `ratings_breakdown` encapsula las evaluaciones en `JSONB`, aislando los cambios de criterios por subcategoría sin alterar el esquema.
* [ ] **Anti-fraude:** una reseña nace siempre `pending`, sin verificar y con 0 votos. El usuario solo puede editar su texto y sus calificaciones; `status`, `is_verified`, `helpful_votes` y `rating_final` se gestionan desde el backend o con triggers.
* [ ] **Comprobante de compra fuera de esta tabla:** la imagen de la boleta vive en `review_proofs`, que no es pública.
* [ ] **Decisión de producto pendiente:** si editar una reseña aprobada la devuelve a `pending`.

```sql
create table public.reviews (
  id                uuid         primary key default gen_random_uuid(),
  product_id        uuid         not null references public.products(id) on delete cascade,
  user_id           uuid         null references public.user_profiles(id) on delete set null,
  pros              text         not null,
  contras           text         not null,
  commentary        text         null,
  ratings_breakdown jsonb        not null,
  rating_final      decimal(3,2) not null,  -- calculado en backend o trigger, nunca por el cliente
  is_verified       boolean      not null default false,
  status            varchar(20)  not null default 'pending'
                    check (status in ('pending', 'approved', 'rejected')),
  helpful_votes     int          not null default 0,

  created_at    timestamptz  not null default now(),
  updated_at    timestamptz  not null default now(),
  created_by    uuid         null references auth.users(id) on delete set null,
  updated_by    uuid         null references auth.users(id) on delete set null,
  is_deleted    boolean      not null default false,
  deleted_at    timestamptz  null,
  deleted_by    uuid         null references auth.users(id) on delete set null
);

create index reviews_product_status_idx on public.reviews(product_id, status)
  where is_deleted = false;
create trigger trg_reviews_updated_at before update on public.reviews
  for each row execute function update_updated_at();

alter table public.reviews enable row level security;

create policy "cualquiera ve reseñas aprobadas" on public.reviews
  for select using (status = 'approved' and is_deleted = false);

create policy "autor ve sus reseñas" on public.reviews
  for select using ((select auth.uid()) = user_id and is_deleted = false);

create policy "usuarios crean reseñas pendientes" on public.reviews
  for insert with check (
    (select auth.uid()) = user_id
    and status = 'pending' and is_verified = false and helpful_votes = 0
  );

create policy "usuarios editan su propia reseña" on public.reviews
  for update using ((select auth.uid()) = user_id and is_deleted = false)
  with check ((select auth.uid()) = user_id);

-- El cliente solo puede modificar estas columnas
revoke update on public.reviews from anon, authenticated;
grant update (pros, contras, commentary, ratings_breakdown) on public.reviews to authenticated;
```

### 🔲 Tabla: `public.review_proofs` (Verificación de compra) — privada
* [ ] **Estructura Técnica:** el comprobante (boleta, caja del producto) puede contener nombre, RUT, dirección o dígitos de tarjeta. Se guarda en un **bucket privado** de Supabase Storage y solo lo ven su autor y el equipo de moderación (vía backend).
* [ ] **Nunca público:** la ficha de producto muestra solo la medalla "Compra Verificada" (`reviews.is_verified`), nunca la imagen.
* [ ] **Retención (RAT T-04):** la imagen se borra del bucket 30 días después de la verificación o el rechazo, mediante un job programado. Se conserva solo el resultado (`reviews.is_verified`) y el registro de la verificación.

```sql
create table public.review_proofs (
  id                  uuid         primary key default gen_random_uuid(),
  review_id           uuid         not null unique references public.reviews(id) on delete cascade,
  storage_path        text         not null,  -- bucket privado 'review-proofs'
  verification_status varchar(20)  not null default 'pending'
                      check (verification_status in ('pending', 'verified', 'rejected')),
  verified_at         timestamptz  null,
  verified_by         uuid         null references auth.users(id) on delete set null,

  created_at    timestamptz  not null default now(),
  updated_at    timestamptz  not null default now(),
  created_by    uuid         null references auth.users(id) on delete set null,
  updated_by    uuid         null references auth.users(id) on delete set null,
  is_deleted    boolean      not null default false,
  deleted_at    timestamptz  null,
  deleted_by    uuid         null references auth.users(id) on delete set null
);

create trigger trg_review_proofs_updated_at before update on public.review_proofs
  for each row execute function update_updated_at();

alter table public.review_proofs enable row level security;

create policy "autor ve su comprobante" on public.review_proofs
  for select using (
    review_id in (select id from public.reviews where user_id = (select auth.uid()))
  );

create policy "autor sube su comprobante" on public.review_proofs
  for insert with check (
    verification_status = 'pending'
    and review_id in (select id from public.reviews where user_id = (select auth.uid()))
  );
-- La verificación (update) la realiza solo el backend de moderación.
```

### 🔲 Tabla: `public.review_votes` (Contramedida Estricta de Fraude)
* [ ] **Un voto por cuenta y reseña:** `UNIQUE (review_id, user_id)` impide a nivel de motor que una cuenta infle o sabotee las calificaciones.
* [ ] **Compatible con la supresión:** `user_id` usa `SET NULL`. Al suprimir una cuenta, sus votos se conservan anónimos y el contador `helpful_votes` sigue siendo consistente. (Con la clave primaria compuesta anterior, `user_id` no podía ser nulo y los votos desaparecían en cascada.)
* [ ] **Contador sincronizado:** un trigger sobre `review_votes` actualiza `reviews.helpful_votes` en cada inserción, cambio o eliminación.

```sql
create table public.review_votes (
  id          uuid         primary key default gen_random_uuid(),
  review_id   uuid         not null references public.reviews(id) on delete cascade,
  user_id     uuid         null references public.user_profiles(id) on delete set null,
  vote_type   varchar(10)  not null check (vote_type in ('upvote', 'downvote')),
  created_at  timestamptz  not null default now(),
  updated_at  timestamptz  not null default now(),
  unique (review_id, user_id)  -- los votos anónimos (user_id null) no colisionan entre sí
);

create trigger trg_review_votes_updated_at before update on public.review_votes
  for each row execute function update_updated_at();

alter table public.review_votes enable row level security;

create policy "usuarios ven sus propios votos" on public.review_votes
  for select using ((select auth.uid()) = user_id);
create policy "usuarios votan" on public.review_votes
  for insert with check ((select auth.uid()) = user_id);
create policy "usuarios cambian su voto" on public.review_votes
  for update using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "usuarios retiran su voto" on public.review_votes
  for delete using ((select auth.uid()) = user_id);
```

### 🔲 Índices de Rendimiento
* [ ] **`slug` y `gtin`** ya quedan indexados por sus restricciones `UNIQUE`; un índice compuesto adicional `(slug, gtin)` es redundante.
* [ ] **`reviews_product_status_idx`** (parcial, `WHERE is_deleted = false`) garantiza la carga rápida del feed de opiniones aprobadas.
* [ ] **Sin `CONCURRENTLY` en migraciones:** las migraciones de Supabase se ejecutan dentro de una transacción, y `CREATE INDEX CONCURRENTLY` falla en ese contexto. Úsalo solo en mantenciones manuales sobre tablas grandes en producción.

### 🔲 Tabla: `public.fraud_signals` (Antifraude) — sin acceso desde el cliente
* [ ] **Estructura Técnica:** eventos de riesgo (registro, publicación, voto) con la IP transformada en un HMAC calculado en FastAPI. La clave vive en variables de entorno y rota cada 90 días (`key_version`). Dentro de una misma ventana se puede detectar "misma IP, muchas cuentas"; después de rotar la clave, nadie puede reconstruir ni correlacionar la IP.
* [ ] **Retención (RAT T-05):** 90 días, con borrado físico mediante `pg_cron`.
* [ ] **Acceso:** RLS activado y sin políticas para `anon` ni `authenticated`; solo el backend lee y escribe.

```sql
create table public.fraud_signals (
  id           uuid         primary key default gen_random_uuid(),
  user_id      uuid         null references public.user_profiles(id) on delete set null,
  event_type   varchar(30)  not null check (event_type in ('signup', 'review', 'vote', 'proof_upload')),
  ip_hmac      text         not null,
  key_version  smallint     not null,
  user_agent   text         null,
  created_at   timestamptz  not null default now()
);

create index fraud_signals_ip_window_idx on public.fraud_signals(ip_hmac, key_version, created_at);

alter table public.fraud_signals enable row level security;
-- Sin políticas: el cliente no tiene acceso.

select cron.schedule('purge_fraud_signals', '0 4 * * *',
  $$ delete from public.fraud_signals where created_at < now() - interval '90 days' $$);
```

### 🔲 Trazabilidad con el RAT
* [ ] **Fuente de verdad:** `rat.yaml` (v0.2) define finalidades, bases, retenciones y encargados. Ningún campo con datos personales entra al esquema sin su tratamiento en el RAT.
* [ ] **Analítica (D-04):** herramienta sin cookies ni datos personales. Mientras peervibe no instale cookies no esenciales, no requiere banner de cookies *[validar]*; si se agrega cualquier pixel de marketing o analítica con cookies, el banner pasa a ser obligatorio.
* [ ] **Responsable (D-06):** persona natural. Evaluar la constitución de una SpA antes del lanzamiento público.
