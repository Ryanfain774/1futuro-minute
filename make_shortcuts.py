#!/usr/bin/env python3
"""Genera Atajos de iOS firmados que abren Minute directo en una tarea.

Uso:
  python3 make_shortcuts.py <taskId> [<taskId> ...]
  python3 make_shortcuts.py --featured          # usa la lista FEATURED de index.html

Cada Atajo tiene una sola acción: "Abrir URL" con minute://record?taskId=<id>.
Se firma con `shortcuts sign --mode anyone` (macOS), así se puede enviar por
AirDrop, WhatsApp o mail y se importa con un toque en el iPhone.
Los archivos quedan en ./atajos/<nombre de la tarea>.shortcut
"""
import json, os, plistlib, re, subprocess, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "atajos")
TASKS = {t["id"]: t for t in json.load(open(os.path.join(HERE, "tasks.json"), encoding="utf-8"))}


def featured_ids():
    html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    block = re.search(r"const FEATURED = \[(.*?)\];", html, re.S).group(1)
    return re.findall(r'"([0-9a-f-]{36})"', block)


def build(task_id):
    task = TASKS.get(task_id)
    if not task:
        print(f"  ! {task_id}: no está en tasks.json, se omite")
        return
    name = task["name"]
    url = f"minute://record?taskId={task_id}"
    workflow = {
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowClientVersion": "2605.0.5",
        "WFWorkflowHasShortcutInputVariables": False,
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4282601983, "WFWorkflowIconGlyphNumber": 59511},
        "WFWorkflowImportQuestions": [],
        "WFWorkflowInputContentItemClasses": [],
        "WFWorkflowTypes": [],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowName": name,
        "WFWorkflowActions": [
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
                "WFWorkflowActionParameters": {
                    "UUID": str(uuid.uuid4()).upper(),
                    "WFInput": url,
                    "Show-WFInput": True,
                },
            }
        ],
    }
    os.makedirs(OUT, exist_ok=True)
    safe = re.sub(r"[^\w .,()-]+", "", name).strip()[:60] or task_id
    unsigned = os.path.join(OUT, f".{safe}.unsigned.shortcut")
    signed = os.path.join(OUT, f"{safe}.shortcut")
    with open(unsigned, "wb") as f:
        plistlib.dump(workflow, f, fmt=plistlib.FMT_BINARY)
    subprocess.run(["shortcuts", "sign", "--mode", "anyone", "--input", unsigned, "--output", signed], check=True)
    os.remove(unsigned)
    print(f"  ✓ {signed}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        ids = list(TASKS.keys())
    elif args == ["--featured"]:
        ids = featured_ids()
    else:
        ids = args
    if not ids:
        print(__doc__)
        sys.exit(1)
    print(f"Generando {len(ids)} atajo(s)…")
    for tid in ids:
        build(tid)
