#!/usr/bin/env python3
"""
catalog_datasets.py — Utilidad de catalogo de datasets.

Uso:
    python scripts/catalog_datasets.py list              # Listar todos
    python scripts/catalog_datasets.py show <id>          # Mostrar detalle
    python scripts/catalog_datasets.py search <query>     # Buscar
    python scripts/catalog_datasets.py validate           # Validar integridad

Ejemplos:
    python scripts/catalog_datasets.py list
    python scripts/catalog_datasets.py show cpv2017
    python scripts/catalog_datasets.py search "pobreza distrital"
    python scripts/catalog_datasets.py validate
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML no instalado. Ejecuta: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

CATALOG_PATH = Path("datasets/catalog/catalog.yml")


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        print(f"Error: Catalogo no encontrado en {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_list(catalog: dict) -> None:
    """Lista todos los datasets con info resumida."""
    print(f"{'ID':<25} {'Nombre':<50} {'N':<8} {'Año':<6} {'Usado en'}")
    print("-" * 110)
    for ds in catalog["datasets"]:
        n = ds["geography"].get("n_units", "?")
        year = ds["temporal"].get("year", "?")
        used = ", ".join(ds.get("used_in", [])) or "(sin usar)"
        print(f"{ds['id']:<25} {ds['name']:<50} {str(n):<8} {str(year):<6} {used}")


def cmd_show(catalog: dict, dataset_id: str) -> None:
    """Muestra metadata completa de un dataset."""
    ds = next((d for d in catalog["datasets"] if d["id"] == dataset_id), None)
    if ds is None:
        print(f"Dataset '{dataset_id}' no encontrado.", file=sys.stderr)
        sys.exit(1)

    print(f"=== {ds['name']} ===")
    print(f"ID:           {ds['id']}")
    print(f"Fuente:       {ds['source']}")
    print(f"URL:          {ds.get('url', 'N/A')}")
    print(f"Licencia:     {ds.get('license', 'N/A')}")
    print(f"Formato:      {ds.get('format', 'N/A')}")
    print(f"Archivos:     {', '.join(ds.get('files', []))}")
    print()
    print("--- Geografia ---")
    geo = ds.get("geography", {})
    print(f"  Nivel:      {geo.get('level', '?')}")
    print(f"  Cobertura:  {geo.get('coverage', '?')}")
    print(f"  N unidades: {geo.get('n_units', '?')}")
    print()
    print("--- Temporal ---")
    temp = ds.get("temporal", {})
    print(f"  Año:        {temp.get('year', '?')}")
    print(f"  Tipo:       {temp.get('type', '?')}")
    print()
    print("--- Variables ---")
    for cat in ds.get("variables", []):
        print(f"  [{cat['category']}] {', '.join(cat['names'])}")
    print()
    print("--- Calidad ---")
    qual = ds.get("quality", {})
    print(f"  Completitud:    {qual.get('completeness', '?')}")
    print(f"  Missing data:   {qual.get('missing_data', '?')}")
    print(f"  Known issues:   {qual.get('known_issues', '?')}")
    print()
    print(f"Papers que lo usan: {', '.join(ds.get('used_in', [])) or '(ninguno)'}")
    if ds.get("notes"):
        print(f"Notas: {ds['notes']}")


def cmd_search(catalog: dict, query: str) -> None:
    """Busca datasets por nombre, fuente, variables, o geografia."""
    query_lower = query.lower()
    results = []
    for ds in catalog["datasets"]:
        score = 0
        # Buscar en nombre
        if query_lower in ds["name"].lower():
            score += 3
        # Buscar en fuente
        if query_lower in ds.get("source", "").lower():
            score += 2
        # Buscar en variables
        for cat in ds.get("variables", []):
            for var in cat["names"]:
                if query_lower in var.lower():
                    score += 2
            if query_lower in cat["category"].lower():
                score += 1
        # Buscar en geografia
        geo = ds.get("geography", {})
        if query_lower in geo.get("level", "").lower():
            score += 1
        if query_lower in geo.get("coverage", "").lower():
            score += 1

        if score > 0:
            results.append((score, ds))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        print(f"No se encontraron datasets para '{query}'.")
        return

    print(f"Resultados para '{query}':")
    for score, ds in results:
        print(f"  [{score}] {ds['id']}: {ds['name']}")


def cmd_validate(catalog: dict) -> None:
    """Valida integridad del catalogo."""
    issues = []

    # 1. IDs duplicados
    ids = [ds["id"] for ds in catalog["datasets"]]
    if len(ids) != len(set(ids)):
        issues.append("[ERROR] IDs duplicados en el catalogo")

    # 2. IDs sin directorio
    for ds in catalog["datasets"]:
        ds_dir = Path(f"datasets/{ds['id']}")
        if not ds_dir.exists():
            issues.append(f"[WARN] Directorio no encontrado: datasets/{ds['id']}")

    # 3. Campos requeridos
    required = ["id", "name", "source", "geography", "temporal", "variables"]
    for ds in catalog["datasets"]:
        for field in required:
            if field not in ds:
                issues.append(f"[ERROR] {ds.get('id', '?')}: falta campo '{field}'")

    if not issues:
        print("✅ Catalogo valido. Sin issues.")
    else:
        print(f"Issues encontrados: {len(issues)}")
        for issue in issues:
            print(f"  {issue}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Utilidad de catalogo de datasets")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Listar todos los datasets")
    show_p = sub.add_parser("show", help="Mostrar detalle de un dataset")
    show_p.add_argument("id", help="ID del dataset")
    search_p = sub.add_parser("search", help="Buscar datasets")
    search_p.add_argument("query", help="Termino de busqueda")
    sub.add_parser("validate", help="Validar integridad del catalogo")

    args = parser.parse_args()
    catalog = load_catalog()

    if args.command == "list":
        cmd_list(catalog)
    elif args.command == "show":
        cmd_show(catalog, args.id)
    elif args.command == "search":
        cmd_search(catalog, args.query)
    elif args.command == "validate":
        cmd_validate(catalog)


if __name__ == "__main__":
    main()
