---
name: pdf-extract
description: >
  Extraccion de texto, tablas y metadatos de archivos PDF usando Python. Utiliza
  pdfplumber para extraccion precisa de texto y tablas, PyPDF2 para metadatos,
  y soporta procesamiento por lotes de multiples PDFs.
  Trigger: Cuando el usuario necesita extraer texto de un PDF, convertir PDF a texto
  para analisis, extraer tablas de un paper, o procesar documentos PDF originales
  para estudiar su metodologia.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Extraer texto completo de un paper en PDF
- Extraer tablas de un PDF (datos tabulares)
- Obtener metadatos (autor, titulo, fecha) de un PDF
- Convertir PDF a texto plano para busqueda o analisis
- Procesar por lotes varios PDFs
- Extraer secciones especificas de un paper (metodologia, resultados)

## Critical Patterns

### Library Choice

| Biblioteca | Mejor para | Limitacion |
|-----------|------------|------------|
| `pdfplumber` | Texto + tablas con coordenadas | Mas lento que PyPDF2 |
| `PyPDF2` / `pypdf` | Metadatos, texto simple | Tablas pierden estructura |
| `camelot-py` | Tablas complejas | Solo tablas, no texto |
| `pdfminer.six` | Control fino del parsing | API mas compleja |

**Recomendacion para papers:** `pdfplumber` para texto + tablas. Si solo necesitas metadatos y texto basico, `pypdf`.

### File Locations

Los PDFs del paper original se almacenan en `docs/original/`. Los textos extraidos van a `data/processed/`.

```
docs/original/                 → PDFs fuente (inmutables)
  ├── alonso2025_segregacion.pdf
  └── ...
data/processed/                → Texto extraido (generado por scripts/extract_pdf.py)
  ├── alonso2025_texto.txt
  ├── alonso2025_metadatos.json
  └── ...
```

### Extraction Pipeline

```
1. Leer PDF con pdfplumber
2. Extraer metadatos (titulo, autores, fecha)
3. Extraer texto pagina por pagina
4. Detectar y extraer tablas
5. Guardar outputs:
   - texto_completo.txt (todo el texto)
   - metadatos.json (metadatos)
   - tablas/ (CSVs individuales por tabla)
```

## Code Examples

### Basic Text Extraction

```python
import pdfplumber

def extract_text(pdf_path: str, output_path: str) -> str:
    """Extrae todo el texto de un PDF pagina por pagina."""
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text.append(f"--- Pagina {i} ---\n{text}")

    result = "\n\n".join(full_text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    return result
```

### Metadata Extraction

```python
import json
from pypdf import PdfReader

def extract_metadata(pdf_path: str) -> dict:
    """Extrae metadatos del PDF."""
    reader = PdfReader(pdf_path)
    meta = reader.metadata
    return {
        "titulo": getattr(meta, "title", None),
        "autor": getattr(meta, "author", None),
        "fecha": getattr(meta, "creation_date", None),
        "paginas": len(reader.pages),
        "productor": getattr(meta, "producer", None),
    }
```

### Table Extraction

```python
def extract_tables(pdf_path: str, output_dir: str) -> list[dict]:
    """Extrae todas las tablas de un PDF y las guarda como CSV."""
    import csv
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_tables = page.extract_tables()
            for j, table in enumerate(page_tables):
                filename = f"{output_dir}/pagina{i}_tabla{j+1}.csv"
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(table)
                tables.append({
                    "pagina": i,
                    "tabla_num": j + 1,
                    "archivo": filename,
                    "filas": len(table),
                })
    return tables
```

### Selective Section Extraction

```python
import re

def extract_methodology_section(text: str) -> str | None:
    """Extrae la seccion de metodologia del texto completo."""
    patterns = [
        r"(?:Metodologia|Metodo|Methodology|Methods?|Material(?:es)? y m[ée]todos?)",
    ]
    for pattern in patterns:
        match = re.search(rf"({pattern}.*?)(?=\n(?:Resultados|Results|Discusi[oó]n|Discussion|\Z))",
                         text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1)
    return None
```

## Commands

```bash
# Extraer texto de un PDF
python scripts/extract_pdf.py docs/original/alonso2025_segregacion.pdf

# Extraer texto + tablas + metadatos
python scripts/extract_pdf.py docs/original/alonso2025_segregacion.pdf --tables --metadata

# Procesar todos los PDFs en docs/original/
python scripts/extract_pdf.py --all

# Extraer solo metadatos (sin texto)
python scripts/extract_pdf.py docs/original/alonso2025_segregacion.pdf --metadata-only
```

## Rules for This Project

1. **PDFs fuente en `docs/original/`.** Nunca modificar los PDFs originales.
2. **Outputs en `data/processed/`.** Todo texto extraido va ahi.
3. **Encoding UTF-8.** Siempre guardar con encoding explicito.
4. **Tablas verificadas.** Revisar manualmente que las tablas extraidas automaticamente conserven la estructura correcta.
5. **No incluir en git outputs derivables.** `data/processed/*.txt` en `.gitignore` si se puede regenerar.

## Dependencies

```
pdfplumber>=0.10.0
pypdf>=4.0.0
camelot-py[cv]>=0.11.0   # opcional, para tablas complejas
```

Ver `scripts/requirements.txt` para la lista completa.
