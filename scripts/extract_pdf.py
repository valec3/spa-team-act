#!/usr/bin/env python3
"""
extract_pdf.py — Extraccion de texto, tablas y metadatos de archivos PDF.

Uso:
    python scripts/extract_pdf.py <pdf_path> [opciones]
    python scripts/extract_pdf.py --all [opciones]

Opciones:
    --tables          Extraer tablas como CSV
    --metadata        Extraer metadatos como JSON
    --metadata-only   Solo metadatos, sin texto
    --all             Procesar todos los PDFs en docs/original/
    --output-dir DIR  Directorio de salida (default: data/processed/)
    --section SEC     Extraer solo una seccion especifica
                      (ej: "metodologia", "resultados", "introduccion")

Ejemplos:
    python scripts/extract_pdf.py docs/original/paper.pdf
    python scripts/extract_pdf.py docs/original/paper.pdf --tables --metadata
    python scripts/extract_pdf.py --all --tables
    python scripts/extract_pdf.py docs/original/paper.pdf --section metodologia

Dependencias: pdfplumber, pypdf (ver scripts/requirements.txt)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convierte un nombre de archivo en un slug seguro."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def sanitize_filename(path: Path) -> str:
    """Genera un nombre base seguro para outputs desde el nombre del PDF."""
    return slugify(path.stem)


# ---------------------------------------------------------------------------
# Metadata extraction (pypdf)
# ---------------------------------------------------------------------------

def extract_metadata(pdf_path: Path) -> dict:
    """Extrae metadatos del PDF usando pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    meta = reader.metadata

    def safe_meta(attr: str) -> Optional[str]:
        val = getattr(meta, attr, None)
        return str(val) if val is not None else None

    return {
        "archivo": pdf_path.name,
        "titulo": safe_meta("title"),
        "autor": safe_meta("author"),
        "asunto": safe_meta("subject"),
        "fecha_creacion": safe_meta("creation_date"),
        "fecha_modificacion": safe_meta("modification_date"),
        "productor": safe_meta("producer"),
        "creador": safe_meta("creator"),
        "paginas": len(reader.pages),
        "extraido_en": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# Text extraction (pdfplumber)
# ---------------------------------------------------------------------------

def extract_text(pdf_path: Path) -> str:
    """Extrae todo el texto de un PDF pagina por pagina usando pdfplumber."""
    import pdfplumber

    pages_text: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                pages_text.append(f"--- Pagina {i} ---\n{text}")

    return "\n\n".join(pages_text)


# ---------------------------------------------------------------------------
# Table extraction (pdfplumber)
# ---------------------------------------------------------------------------

def extract_tables(pdf_path: Path, output_dir: Path) -> list[dict]:
    """Extrae todas las tablas de un PDF y las guarda como CSV."""
    import pdfplumber

    base = sanitize_filename(pdf_path)
    tables: list[dict] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_tables = page.extract_tables()
            for j, table in enumerate(page_tables):
                filename = output_dir / f"{base}_pagina{i}_tabla{j+1}.csv"
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(table)
                tables.append({
                    "pagina": i,
                    "tabla_num": j + 1,
                    "archivo": str(filename),
                    "filas": len(table),
                    "columnas": len(table[0]) if table else 0,
                })

    return tables


# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

# Patrones para detectar secciones comunes en papers academicos (espanol + ingles)
SECTION_PATTERNS: dict[str, list[str]] = {
    "introduccion": [
        r"introducci[oó]n",
        r"introduction",
    ],
    "metodologia": [
        r"metodolog[ií]a",
        r"m[eé]todos?",
        r"method(?:ology|s)?",
        r"material(?:es)? y m[eé]todos?",
        r"data and methods?",
    ],
    "resultados": [
        r"resultados",
        r"results",
        r"findings",
    ],
    "discusion": [
        r"discusi[oó]n",
        r"discussion",
        r"conclusion(?:es)?",
    ],
    "referencias": [
        r"referencias",
        r"bibliograf[ií]a",
        r"references",
        r"bibliography",
    ],
}

# Patrones que marcan el INICIO de la siguiente seccion (para delimitar el fin)
NEXT_SECTION_PATTERNS: list[str] = [
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:introducci[oó]n|introduction)",
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:metodolog[ií]a|m[eé]todos?|method(?:ology|s)?|material(?:es)? y m[eé]todos?)",
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:resultados|results|findings)",
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:discusi[oó]n|discussion|conclusion(?:es)?)",
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:referencias|bibliograf[ií]a|references|bibliography)",
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:anexos?|ap[eé]ndices?|appendix|appendices)",
]


def extract_section(text: str, section_name: str) -> str | None:
    """Extrae una seccion especifica del texto completo."""
    key = section_name.lower().strip()
    patterns = SECTION_PATTERNS.get(key)
    if not patterns:
        # Intentar busqueda directa
        patterns = [re.escape(key)]

    # Buscar la seccion
    for pattern in patterns:
        start_match = re.search(
            rf"(?:^|\n)\s*(?:\d+\.?\s+)?(?:{pattern})[:\s]*(?:\n|\r\n?)",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        if not start_match:
            continue

        start_pos = start_match.start()

        # Buscar el inicio de la siguiente seccion
        end_match = re.search(
            "|".join(NEXT_SECTION_PATTERNS),
            text[start_pos + len(start_match.group()):],
            re.IGNORECASE | re.MULTILINE,
        )
        if end_match:
            end_pos = start_pos + len(start_match.group()) + end_match.start()
        else:
            end_pos = len(text)

        return text[start_pos:end_pos].strip()

    return None


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def find_all_pdfs(source_dir: Path) -> list[Path]:
    """Encuentra todos los PDFs en docs/original/."""
    return sorted(source_dir.glob("*.pdf"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extrae texto, tablas y metadatos de PDFs academicos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/extract_pdf.py docs/original/paper.pdf
  python scripts/extract_pdf.py docs/original/paper.pdf --tables --metadata
  python scripts/extract_pdf.py --all --tables
  python scripts/extract_pdf.py docs/original/paper.pdf --section metodologia
        """,
    )

    parser.add_argument(
        "pdf_path",
        nargs="?",
        type=Path,
        help="Ruta al archivo PDF",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Procesar todos los PDFs en docs/original/",
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="Extraer tablas como CSV",
    )
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="Extraer metadatos como JSON",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Solo extraer metadatos (sin texto)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directorio de salida (default: data/processed/)",
    )
    parser.add_argument(
        "--section",
        type=str,
        default=None,
        help="Extraer solo una seccion especifica (ej: metodologia, resultados)",
    )

    args = parser.parse_args()

    # Validar argumentos
    if not args.all and args.pdf_path is None:
        parser.error("Debe especificar un PDF o usar --all")
    if args.all and args.pdf_path is not None:
        parser.error("No puede especificar un PDF y --all al mismo tiempo")
    if args.metadata_only and args.section is not None:
        parser.error("--metadata-only y --section son mutuamente excluyentes")

    # Determinar PDFs a procesar
    source_dir = Path("docs/original")
    if args.all:
        pdfs = find_all_pdfs(source_dir)
        if not pdfs:
            print(f"No se encontraron PDFs en {source_dir}/", file=sys.stderr)
            sys.exit(1)
        print(f"Procesando {len(pdfs)} PDFs en {source_dir}/")
    else:
        pdf_path = args.pdf_path
        if not pdf_path.exists():
            print(f"Error: No se encontro el archivo {pdf_path}", file=sys.stderr)
            sys.exit(1)
        pdfs = [pdf_path]

    # Procesar cada PDF
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdfs:
        base = sanitize_filename(pdf_path)
        print(f"\n--- {pdf_path.name} ---")

        # Metadatos
        if args.metadata or args.metadata_only:
            try:
                meta = extract_metadata(pdf_path)
                meta_path = output_dir / f"{base}_metadatos.json"
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)
                print(f"  Metadatos: {meta_path}")
                print(f"    Titulo: {meta['titulo']}")
                print(f"    Paginas: {meta['paginas']}")
            except Exception as e:
                print(f"  Error extrayendo metadatos: {e}", file=sys.stderr)

        if args.metadata_only:
            continue

        # Texto
        try:
            text = extract_text(pdf_path)

            if args.section:
                section_text = extract_section(text, args.section)
                if section_text:
                    text_path = output_dir / f"{base}_{slugify(args.section)}.txt"
                    with open(text_path, "w", encoding="utf-8") as f:
                        f.write(section_text)
                    lines = section_text.count("\n") + 1
                    print(f"  Seccion '{args.section}': {text_path} ({lines} lineas)")
                else:
                    print(f"  No se encontro la seccion '{args.section}'")
            else:
                text_path = output_dir / f"{base}_texto.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text)
                chars = len(text)
                lines = text.count("\n") + 1
                words = len(text.split())
                print(f"  Texto: {text_path}")
                print(f"    {chars:,} caracteres, {words:,} palabras, {lines:,} lineas")
        except Exception as e:
            print(f"  Error extrayendo texto: {e}", file=sys.stderr)

        # Tablas
        if args.tables:
            try:
                tables_dir = output_dir / f"{base}_tablas"
                tables = extract_tables(pdf_path, tables_dir)
                print(f"  Tablas extraidas: {len(tables)}")
                for t in tables:
                    print(f"    Pag {t['pagina']}, tabla {t['tabla_num']}: "
                          f"{t['filas']} filas x {t['columnas']} cols -> {t['archivo']}")
            except Exception as e:
                print(f"  Error extrayendo tablas: {e}", file=sys.stderr)

    print("\nListo.")


if __name__ == "__main__":
    main()
