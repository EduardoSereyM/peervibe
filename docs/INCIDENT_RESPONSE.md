# Respuesta a incidentes de datos — peervibe

Procedimiento exigido por PRIV-020. Notificar a la autoridad o a los titulares lo decide el humano, sin dilaciones indebidas. Los campos `TBD` los completa el responsable antes del lanzamiento.

## 1. Responsables

| Función | Persona | Contacto |
|---|---|---|
| Responsable del tratamiento (persona natural, D-06) | TBD (nombre legal) | TBD |
| Quien decide la notificación | El responsable | TBD |
| Respaldo | TBD | TBD |

## 2. Contención

1. Aislar el origen (revocar credenciales o claves expuestas, desactivar la cuenta o el servicio afectado).
2. Preservar evidencia (logs de aplicación y `audit_logs`) antes de limpiar nada.
3. Rotar secretos potencialmente comprometidos.
4. Registrar la hora de detección y cada acción tomada.

## 3. Criterios de notificación

Se notifica a la autoridad y a los titulares cuando la vulneración afecta datos personales y puede causar daño a los titulares. La decisión y su fundamento quedan en el registro del incidente. Criterios finos: TBD, a validar legalmente.

## 4. Plantilla de aviso a la autoridad

- Naturaleza de la vulneración y fecha de detección.
- Categorías y número aproximado de titulares y de datos afectados.
- Consecuencias probables.
- Medidas adoptadas o propuestas.
- Contacto del responsable.

## 5. Plantilla de aviso a los titulares

- Qué ocurrió, en lenguaje claro.
- Qué datos suyos están afectados.
- Qué hemos hecho y qué puede hacer la persona para protegerse.
- Canal de contacto (`privacidad@[dominio]`).

## 6. Registro por incidente

| Campo | Contenido |
|---|---|
| Identificador y fecha | |
| Detección (cómo y cuándo) | |
| Alcance | |
| Datos afectados | |
| Medidas adoptadas | |
| Decisión de notificar (y fundamento) | |

## 7. Simulacro

Al menos uno al año. Registro de simulacros: ninguno aún.
