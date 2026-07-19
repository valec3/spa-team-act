#!/usr/bin/env python3
"""
batch_papers.py — Generacion por lotes de multiples papers.

Ejecuta paper-factory para una lista de papers (desde batch_config.yml),
con tracking de progreso, manejo de dependencias y reporte consolidado.

Uso:
    python scripts/batch_papers.py [batch_config.yml]
    python scripts/batch_papers.py --resume [batch_id]
    python scripts/batch_papers.py --status [batch_id]

Ejemplos:
    python scripts/batch_papers.py papers/batch_replicas.yml
    python scripts/batch_papers.py --resume replicas_departamentales_2024
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML no instalado. Ejecuta: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

STATE_DIR = Path("papers/.batch_state")


def load_batch_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_batch_state(config: dict) -> dict:
    batch_id = config["batch_id"]
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "batch_id": batch_id,
        "started": datetime.now().isoformat(),
        "status": "in_progress",
        "config_file": str(path),
        "papers": {},
        "progress": {"total": len(config["papers"]), "completed": 0,
                      "failed": 0, "pending": len(config["papers"]), "blocked": 0},
    }

    for paper in config["papers"]:
        state["papers"][paper["paper_id"]] = {
            "status": "pending",
            "spec": paper.get("spec", f"papers/{paper['paper_id']}/paper_spec.yml"),
            "priority": paper.get("priority", 1),
            "depends_on": paper.get("depends_on", []),
        }

    save_state(batch_id, state)
    return state


def load_state(batch_id: str) -> dict:
    state_file = STATE_DIR / f"{batch_id}.json"
    if not state_file.exists():
        print(f"Error: No hay estado para batch '{batch_id}'", file=sys.stderr)
        sys.exit(1)
    with open(state_file, encoding="utf-8") as f:
        return json.load(f)


def save_state(batch_id: str, state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_DIR / f"{batch_id}.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def is_ready(paper_state: dict, all_states: dict) -> bool:
    """Verifica si un paper esta listo (dependencias completadas)."""
    for dep in paper_state.get("depends_on", []):
        if dep not in all_states:
            return False
        if all_states[dep]["status"] != "completed":
            return False
    return True


def run_paper(paper_id: str, spec_path: str) -> bool:
    """Ejecuta paper-factory para un paper. Retorna True si OK."""
    print(f"\n{'='*60}")
    print(f"  Ejecutando: {paper_id}")
    print(f"{'='*60}")

    start = time.time()

    # Verificar que el spec existe
    if not Path(spec_path).exists():
        print(f"  ❌ Spec no encontrado: {spec_path}")
        return False

    # En el futuro, esto llamaria a paper-factory via R o Python
    # Por ahora, simulamos verificando la estructura
    paper_dir = Path(f"papers/{paper_id}")
    if not paper_dir.exists():
        print(f"  ❌ Directorio no existe: {paper_dir}")
        return False

    elapsed = time.time() - start
    print(f"  ✅ Completado en {elapsed:.1f}s")
    return True


def run_batch(config: dict, resume: bool = False) -> None:
    """Ejecuta el batch completo."""
    batch_id = config["batch_id"]
    mode = config.get("mode", "sequential")
    on_error = config.get("on_error", "continue")

    if resume:
        state = load_state(batch_id)
        print(f"Reanudando batch: {batch_id}")
    else:
        state = init_batch_state(config)
        print(f"Iniciando batch: {batch_id} ({state['progress']['total']} papers)")

    # Ordenar por prioridad
    papers_ordered = sorted(
        config["papers"],
        key=lambda p: (p.get("priority", 1), p["paper_id"])
    )

    for paper in papers_ordered:
        pid = paper["paper_id"]
        pstate = state["papers"][pid]

        # Saltar si ya completado
        if pstate["status"] == "completed":
            state["progress"]["completed"] += 1
            continue

        # Verificar dependencias
        if not is_ready(pstate, state["papers"]):
            pstate["status"] = "blocked"
            state["progress"]["blocked"] += 1
            print(f"  ⏳ {pid}: bloqueado (dependencias: {pstate['depends_on']})")
            continue

        # Ejecutar paper
        pstate["status"] = "in_progress"
        pstate["started"] = datetime.now().isoformat()
        save_state(batch_id, state)

        success = run_paper(pid, pstate["spec"])

        if success:
            pstate["status"] = "completed"
            pstate["completed"] = datetime.now().isoformat()
            state["progress"]["completed"] += 1
        else:
            pstate["status"] = "failed"
            state["progress"]["failed"] += 1
            if on_error == "stop":
                print("Batch detenido por error.")
                break

        state["progress"]["pending"] -= 1
        save_state(batch_id, state)

    # Reporte final
    state["status"] = "completed" if state["progress"]["failed"] == 0 else "partial"
    state["finished"] = datetime.now().isoformat()
    save_state(batch_id, state)

    print(f"\n{'='*60}")
    print(f"  BATCH COMPLETADO: {batch_id}")
    print(f"  Total: {state['progress']['total']} | OK: {state['progress']['completed']} | "
          f"Fail: {state['progress']['failed']} | Blocked: {state['progress']['blocked']}")
    print(f"{'='*60}")


def cmd_status(batch_id: str) -> None:
    """Muestra el estado actual de un batch."""
    state = load_state(batch_id)
    prog = state["progress"]
    print(f"Batch: {batch_id}")
    print(f"Estado: {state['status']}")
    print(f"Progreso: {prog['completed']}/{prog['total']} completados, "
          f"{prog['failed']} fallidos, {prog['blocked']} bloqueados")
    print()
    for pid, ps in state["papers"].items():
        icon = {"completed": "✅", "failed": "❌", "in_progress": "🔄",
                "pending": "⏳", "blocked": "🔒"}.get(ps["status"], "❓")
        print(f"  {icon} {pid}: {ps['status']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generacion por lotes de papers")
    parser.add_argument("config", nargs="?", help="Archivo batch_config.yml")
    parser.add_argument("--resume", help="Reanudar batch por ID")
    parser.add_argument("--status", help="Mostrar estado de un batch")
    args = parser.parse_args()

    if args.status:
        cmd_status(args.status)
        return

    if args.resume:
        state = load_state(args.resume)
        # Reconstruir config desde el state (simplificado)
        config = {"batch_id": args.resume, "papers": [], "mode": "sequential"}
        for pid, ps in state["papers"].items():
            config["papers"].append({
                "paper_id": pid,
                "spec": ps["spec"],
                "priority": ps["priority"],
                "depends_on": ps.get("depends_on", []),
            })
        run_batch(config, resume=True)
        return

    if not args.config:
        parser.error("Debe especificar archivo de configuracion o --resume/--status")

    config = load_batch_config(args.config)
    run_batch(config)


if __name__ == "__main__":
    path = None  # for state reconstruction
    main()
