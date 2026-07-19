#!/usr/bin/env python3
"""
new_paper.py — Scaffold de un nuevo paper.

Crea la estructura de directorios y archivos iniciales para un paper nuevo,
copiando templates de papers/_template/.

Uso:
    python scripts/new_paper.py <paper_id> [opciones]

Opciones:
    --type TYPE         Tipo de paper: replica, extension, comparison, meta (default: replica)
    --dataset ID        Dataset a usar
    --population DEPT   Departamento/poblacion
    --based-on PAPER    Paper base para variante (hereda metodos)

Ejemplos:
    python scripts/new_paper.py replica_arequipa --dataset cpv2017 --population Arequipa
    python scripts/new_paper.py replica_cusco --dataset cpv2017 --population Cusco --based-on replica_arequipa
    python scripts/new_paper.py cpv_vs_ece --type comparison --dataset cpv2017
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

PAPERS_DIR = Path("papers")
TEMPLATE_DIR = PAPERS_DIR / "_template"


def scaffold_paper(
    paper_id: str,
    paper_type: str,
    dataset: str | None,
    population: str | None,
    based_on: str | None,
) -> Path:
    """Crea la estructura inicial para un paper nuevo."""
    paper_dir = PAPERS_DIR / paper_id

    if paper_dir.exists():
        print(f"Error: El paper '{paper_id}' ya existe en {paper_dir}", file=sys.stderr)
        sys.exit(1)

    # Crear estructura de directorios
    dirs = [
        paper_dir,
        paper_dir / "src",
        paper_dir / "results" / "figures",
        paper_dir / "results" / "tables",
        paper_dir / "reports",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Copiar template si existe
    if TEMPLATE_DIR.exists():
        for item in TEMPLATE_DIR.iterdir():
            if item.is_file():
                shutil.copy2(item, paper_dir / item.name)

    # Generar paper_spec.yml
    spec = {
        "paper_id": paper_id,
        "title": f"[TITULO PENDIENTE] — Paper generado el {datetime.now():%Y-%m-%d}",
        "type": paper_type,
        "dataset": {"id": dataset} if dataset else {},
        "population": {"department": population} if population else {},
        "methods": [],
        "based_on": based_on,
        "template": {"base": str(TEMPLATE_DIR)},
        "pipeline": {"seed": 20240101},
        "created": datetime.now().isoformat(),
        "status": "scaffold",
    }

    # Si se basa en otro paper, heredar metodos
    if based_on:
        base_spec_path = PAPERS_DIR / based_on / "paper_spec.yml"
        if base_spec_path.exists():
            import yaml
            with open(base_spec_path) as f:
                base_spec = yaml.safe_load(f)
            spec["methods"] = base_spec.get("methods", [])
            spec["original_study"] = {"paper": based_on}
            print(f"  Metodos heredados de {based_on}: {len(spec['methods'])} metodos")

    # Guardar spec
    spec_path = paper_dir / "paper_spec.yml"
    try:
        import yaml
        with open(spec_path, "w", encoding="utf-8") as f:
            yaml.dump(spec, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except ImportError:
        # Fallback: escribir JSON si YAML no disponible
        import json
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

    # Generar README.md
    readme = f"""# {paper_id}

> Tipo: {paper_type} | Dataset: {dataset or 'N/A'} | Poblacion: {population or 'N/A'}
> Creado: {datetime.now():%Y-%m-%d %H:%M} | Estado: scaffold

## Pipeline

```
data → analysis → draft → revision → latex → pdf
```

## Como reproducir

```bash
# Ejecutar pipeline completo
cd papers/{paper_id}
Rscript src/analysis_pipeline.R
```

## Resultados

(Pendiente)
"""
    with open(paper_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    # Generar .gitkeep en directorios vacios
    for d in dirs:
        gitkeep = d / ".gitkeep"
        if not any(d.iterdir()):
            gitkeep.touch()

    return paper_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold de un nuevo paper")
    parser.add_argument("paper_id", help="ID del paper (snake_case)")
    parser.add_argument("--type", default="replica",
                        choices=["replica", "extension", "comparison", "meta", "methodological"],
                        help="Tipo de paper")
    parser.add_argument("--dataset", help="Dataset ID (del catalogo)")
    parser.add_argument("--population", help="Departamento o poblacion")
    parser.add_argument("--based-on", help="Paper base para variante")

    args = parser.parse_args()

    # Validar paper_id
    if not args.paper_id.replace("_", "").isalnum():
        print("Error: paper_id debe ser alfanumerico con underscores", file=sys.stderr)
        sys.exit(1)

    print(f"Creando paper: {args.paper_id}")
    print(f"  Tipo:       {args.type}")
    print(f"  Dataset:    {args.dataset or 'N/A'}")
    print(f"  Poblacion:  {args.population or 'N/A'}")
    if args.based_on:
        print(f"  Basado en:  {args.based_on}")

    paper_dir = scaffold_paper(
        args.paper_id, args.type, args.dataset, args.population, args.based_on
    )

    print(f"\n✅ Paper creado en: {paper_dir}")
    print(f"   Siguiente paso: editar {paper_dir}/paper_spec.yml")
    print(f"   Luego ejecutar: paper-factory para generar el paper")


if __name__ == "__main__":
    main()
