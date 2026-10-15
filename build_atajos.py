#!/usr/bin/env python3
"""Genera atajos.html: página de descarga de los Atajos de iPhone, uno por tarea.

Lee tasks.json y la carpeta atajos/ (salida de make_shortcuts.py --all).
Cada fila enlaza al archivo .shortcut servido desde la misma página publicada.
"""
import html, json, os, re, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
tasks = json.load(open(os.path.join(HERE, "tasks.json"), encoding="utf-8"))
existing = set(os.listdir(os.path.join(HERE, "atajos")))


def safe_name(name, task_id):
    return (re.sub(r"[^\w .,()-]+", "", name).strip()[:60] or task_id) + ".shortcut"


def cat(t):
    return (t.get("categories") or [{"label": "Tarea"}])[0]["label"]


rows = []
missing = []
for t in sorted(tasks, key=lambda t: (cat(t), t["name"])):
    fn = safe_name(t["name"], t["id"])
    if fn not in existing:
        missing.append(t["name"])
        continue
    href = "atajos/" + urllib.parse.quote(fn)
    rows.append(
        f'<li class="row" data-q="{html.escape((t["name"] + " " + cat(t)).lower())}">'
        f'<span><span class="cat">{html.escape(cat(t))}</span><div class="name">{html.escape(t["name"])}</div></span>'
        f'<a class="dl" href="{href}" download>Descargar atajo</a></li>'
    )

page = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#111418">
<title>Atajos de iPhone · 1Futuro</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap">
<style>
  :root {{
    color-scheme: dark;
    --ground: #111418; --surface: #1b2026; --surface-2: #242a32; --line: #333b45;
    --ink: #f2f1ec; --ink-muted: #9aa3ad; --accent: #ff8a1f; --accent-ink: #1a0e00; --accent-soft: rgba(255,138,31,0.14);
    --display: "Barlow Condensed", "Arial Narrow", Impact, sans-serif;
    --body: "Barlow", -apple-system, "Segoe UI", Roboto, sans-serif;
  }}
  @media (prefers-color-scheme: light) {{
    :root:not([data-theme="dark"]) {{
      color-scheme: light;
      --ground: #f5f3ee; --surface: #ffffff; --surface-2: #ece9e2; --line: #d9d4ca;
      --ink: #171a1e; --ink-muted: #5e6670; --accent: #e8730a; --accent-ink: #ffffff; --accent-soft: rgba(232,115,10,0.12);
    }}
  }}
  :root[data-theme="light"] {{
    color-scheme: light;
    --ground: #f5f3ee; --surface: #ffffff; --surface-2: #ece9e2; --line: #d9d4ca;
    --ink: #171a1e; --ink-muted: #5e6670; --accent: #e8730a; --accent-ink: #ffffff; --accent-soft: rgba(232,115,10,0.12);
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.4;
         padding-inline: 16px; padding-block: calc(env(safe-area-inset-top,0px) + 20px) calc(env(safe-area-inset-bottom,0px) + 32px); }}
  main {{ max-width: 520px; margin-inline: auto; display: grid; gap: 22px; }}
  .eyebrow {{ font-family: var(--display); font-weight: 600; font-size: 14px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-muted); }}
  h1 {{ margin: 0; font-family: var(--display); font-weight: 700; font-size: clamp(36px, 10vw, 50px); line-height: 0.95; text-wrap: balance; }}
  .how {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; color: var(--ink-muted); font-size: 15px; }}
  .how li {{ display: flex; gap: 10px; align-items: baseline; }}
  .how b {{ color: var(--accent); font-family: var(--display); font-size: 17px; min-width: 1.2em; }}
  .how em {{ color: var(--ink); font-style: normal; font-weight: 600; }}
  input[type=search] {{ width: 100%; font: inherit; font-size: 17px; padding: 12px 14px; border-radius: 12px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); }}
  input[type=search]:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 1px; }}
  .list {{ display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }}
  .row {{ display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 12px; background: var(--surface); border: 1px solid var(--line); }}
  .row .cat {{ font-size: 12px; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }}
  .row .name {{ font-family: var(--display); font-weight: 600; font-size: 21px; line-height: 1.05; }}
  .dl {{ font-family: var(--display); font-weight: 700; font-size: 14px; letter-spacing: 0.05em; text-transform: uppercase; background: var(--accent); color: var(--accent-ink); padding: 9px 12px; border-radius: 10px; text-decoration: none; white-space: nowrap; }}
  .dl:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
  .count {{ color: var(--ink-muted); font-size: 14px; }}
  .back {{ color: var(--accent); font-size: 15px; }}
  .hidden {{ display: none !important; }}
</style>
</head>
<body>
<main>
  <header style="display:grid;gap:8px">
    <div class="eyebrow">1Futuro · iPhone</div>
    <h1>Atajos por tarea</h1>
    <ol class="how">
      <li><b>1</b><span>Buscá la tarea y tocá <em>Descargar atajo</em>. Safari lo baja; tocá la descarga (flecha arriba a la derecha) y después <em>Añadir atajo</em>.</span></li>
      <li><b>2</b><span>Abrí la app <em>Atajos</em>, mantené presionado el atajo, <em>Detalles</em>, <em>Añadir a pantalla de inicio</em>, <em>Añadir</em>.</span></li>
      <li><b>3</b><span>El ícono con el nombre de la tarea abre Minute directo en ella. La primera vez iOS puede preguntar si permitís abrir Minute: elegí <em>Permitir siempre</em>.</span></li>
    </ol>
    <a class="back" href="./">Volver al lanzador</a>
  </header>
  <input type="search" id="q" placeholder="Buscar tarea o rubro" autocomplete="off" aria-label="Buscar tarea">
  <div class="count" id="count"></div>
  <ul class="list" id="list">
    {''.join(rows)}
  </ul>
</main>
<script>
  const q = document.getElementById("q"), rows = [...document.querySelectorAll(".row")], count = document.getElementById("count");
  const norm = s => s.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
  function render() {{
    const needle = norm(q.value.trim()); let n = 0;
    rows.forEach(r => {{ const show = !needle || norm(r.dataset.q).includes(needle); r.classList.toggle("hidden", !show); if (show) n++; }});
    count.textContent = n + " de " + rows.length + " tareas";
  }}
  q.addEventListener("input", render); render();
</script>
</body>
</html>
"""
open(os.path.join(HERE, "atajos.html"), "w", encoding="utf-8").write(page)
print(f"atajos.html: {len(rows)} atajos enlazados" + (f"; sin archivo: {missing}" if missing else ""))
