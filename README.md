# Lanzador de tareas para Minute

Página de un toque para que cada empleado abra la app Minute directamente en su tarea,
sin buscarla entre las 154 del catálogo. Funciona porque la app registra el esquema
`minute://` y la ruta `record` acepta un `taskId`:

```
minute://record?taskId=<id de la tarea>
```

Verificado el 2026-10-08 con la app 1.29.0: con un ID válido abre la hoja de la tarea
con el botón "iniciar tarea"; con un ID inválido muestra "Esta tarea ya no está disponible".

## Archivos

- `index.html`: la página. Lleva el catálogo completo embebido y una lista `FEATURED`
  con las tareas del equipo. Editar el bloque "Configuración" al inicio del `<script>`.
- `tasks.json`: catálogo de tareas de la organización (id, nombre, rubro). Regenerar
  desde el Partner Portal o la API vendor (`GET /api/v1/vendor/tasks`) si cambia.
- `make_shortcuts.py`: genera Atajos de iOS firmados, uno por tarea.
- `atajos/`: salida de `make_shortcuts.py`.

## Configurar las tareas del equipo

En `index.html`:

```js
const COMPANY = "Nombre de la empresa";
const FEATURED = [
  "22d1338c-9a8e-45e1-8369-696ce314f8ae", // Montaje de amplificación o PA
];
const SHOW_ALL_TASKS = true; // false = solo "Mis tareas"
```

Los IDs están en `tasks.json`.

## Configurar cada teléfono con sus propias tareas

En el teléfono del empleado, abrir la página y tocar **"Configurar este teléfono"**
(abajo). Marcar las tareas de esa persona, escribir su nombre (opcional) y tocar
**Guardar**. La página recarga con un enlace del tipo `?t=f9cdf2b9,dce84d3e&n=Juan`:
la selección viaja en la URL, así que el ícono de pantalla de inicio la conserva.
Después: Safari → Compartir → "Agregar a pantalla de inicio" (iPhone) o
Chrome → ⋮ → "Agregar a pantalla principal" (Android).

Un teléfono configurado muestra solo sus tareas; el catálogo completo queda detrás
de "Ver todas las tareas". Los códigos de `t` son los primeros 8 caracteres del ID
de cada tarea (únicos en este catálogo).

Página publicada: https://ryanfain774.github.io/1futuro-minute/

## Publicar la página

Tiene que estar en una URL normal (https) que los teléfonos abran en Safari o Chrome.
No sirve dentro de un iframe ni como Artifact: los esquemas `minute://` se bloquean ahí.
Cualquier hosting estático sirve: GitHub Pages, Netlify, Vercel, Cloudflare Pages o un
servidor propio. Es un solo archivo, sin backend.

Cada empleado abre la URL una vez y la agrega a la pantalla de inicio
(Safari: Compartir → Agregar a pantalla de inicio; Chrome: menú ⋮ → Agregar a pantalla principal).

## Atajos de iOS (alternativa de un toque real)

```bash
python3 make_shortcuts.py --featured          # un atajo por tarea de FEATURED
python3 make_shortcuts.py <taskId> [<taskId>]  # tareas puntuales
```

Cada `.shortcut` se firma con `shortcuts sign --mode anyone`, así que se puede mandar
por AirDrop, WhatsApp o mail. En el iPhone: tocar el archivo → "Añadir atajo" → en la
app Atajos, mantener presionado → "Añadir a pantalla de inicio". Queda un ícono con el
nombre de la tarea que abre Minute directo en ella.

## Android (Samsung)

La página usa enlaces `intent://record?taskId=...#Intent;scheme=minute;package=com.bakerdata.minute;...;end`,
que Chrome abre directo en la app si está instalada y manda a Play Store si no.
Falta probarlo en un Samsung real.

## Requisitos del lado del empleado

La app Minute instalada y con sesión iniciada en la organización. El enlace solo
elige la tarea; el resto del flujo (soporte de cabeza, cámara, subida) sigue en Minute.
