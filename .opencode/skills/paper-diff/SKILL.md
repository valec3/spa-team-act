---
name: paper-diff
description: >
  Comparacion de versiones y variantes de papers. Detecta diferencias en
  numeros, texto, estructura y resultados entre dos papers. Util para
  tracking de cambios, comparacion de variantes departamentales, y
  verificacion de que una correccion no introdujo nuevos errores.
  Trigger: Cuando el usuario compara dos versiones de un paper, analiza
  diferencias entre variantes, verifica que correcciones son correctas,
  o necesita un diff semantico (no solo textual) entre papers.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Comparar dos versiones del mismo paper (v1.0 vs v2.0)
- Comparar variantes departamentales (Lima vs Arequipa)
- Verificar que una correccion no introdujo cambios no deseados
- Auditar diferencias entre el draft y el LaTeX compilado
- Comparar resultados entre dataset original y alternativo
- Tracking de cambios entre iteraciones de revision

## Critical Patterns

### Diff Dimensions

```
PAPER DIFF — 4 dimensiones de comparacion:

1. NUMERICA: estadisticos, N, p-valores, tamanos de efecto
2. TEXTUAL: redaccion, estructura de parrafos, wording
3. ESTRUCTURAL: secciones, subsecciones, orden
4. REFERENCIAL: citas agregadas, eliminadas, modificadas
```

### Diff Report Template

```markdown
# Paper Diff Report
## Paper A: replica_lima (v1.0) | Paper B: replica_lima (v2.0)
## Fecha: 2024-07-18

---

### Resumen de Cambios
- Cambios numericos: 3
- Cambios textuales: 12 parrafos
- Cambios estructurales: 1 (nueva subseccion)
- Cambios referenciales: 2 citas agregadas

---

### 1. Cambios Numericos

| Variable | Paper A (v1.0) | Paper B (v2.0) | Delta | ¿Esperado? |
|----------|---------------|---------------|-------|------------|
| I Moran NSE | 0.53 | 0.53 | 0.00 | ✅ Sin cambios |
| Z NSE | 9.45 | 9.45 | 0.00 | ✅ Sin cambios |
| N distritos | 128 | 130 | +2 | ⚠️ ¿Se agregaron distritos? |

---

### 2. Cambios Textuales

[PARRAFO MODIFICADO] Introduccion, parrafo 3:
A: "Sin embargo, persiste la falta de evidencia sobre..."
B: "No obstante, la evidencia a escala subnacional es limitada..."
→ Mejora de precision y vocabulario academico ✅

[NUEVO PARRAFO] Discusion, parrafo 5:
+ "Es importante senalar que los resultados de Lima Metropolitana..."
→ Agregada limitacion sobre heterogeneidad intra-departamental ✅

---

### 3. Cambios Estructurales

+ Subseccion 4.4: "Analisis de sensibilidad"
  - Verifica robustez cambiando matriz W (Queen → KNN)
  - Nueva tabla y figura asociadas

---

### 4. Cambios Referenciales

+ Cita agregada: \cite{bonal2020} en Introduccion
+ Cita agregada: \cite{anselin1996} en Metodo
- Sin citas eliminadas

---

### Verificacion de No-Regresion
[x] Correcciones de revision (v1.0 issues) aplicadas sin efectos secundarios
[x] Nuevos contenidos no contradicen contenido existente
[x] Numeros que no debian cambiar, no cambiaron
```

### Cross-Variant Diff (Lima vs Arequipa)

```markdown
# Cross-Variant Diff: Lima vs Arequipa

### Diferencias Estructurales
| Aspecto | Lima | Arequipa | Diferencia |
|---------|------|----------|------------|
| N distritos | 128 | 109 | -19 (Arequipa es mas chico) |
| Estructura | IMRaD | IMRaD | Identica ✅ |

### Diferencias en Resultados
| Variable | Lima | Arequipa | Delta | Interpretacion |
|----------|------|----------|-------|---------------|
| I Moran NSE | 0.53 | 0.48 | -0.05 | Menor autocorrelacion |
| Z NSE | 9.45 | 7.32 | -2.13 | Menor significancia |
| Clusters AA | 27 (21%) | 18 (16%) | -9 | Menos concentracion |
| Clusters BB | 22 (17%) | 25 (23%) | +3 | Mas dispersion |

### Hallazgos Cross-Variant
- Patron consistente: autocorrelacion positiva en ambas poblaciones
- Magnitud varia: departamentos mas pequenos → menor I de Moran
- Hipotesis: la heterogeneidad intra-departamental modera la autocorrelacion
```

### Automated Diff Script (Conceptual)

```python
def diff_papers(paper_a_path, paper_b_path, mode="full"):
    """Compara dos papers y genera reporte de diferencias."""
    a = load_paper(paper_a_path)
    b = load_paper(paper_b_path)

    report = {}

    # 1. Diff numerico
    report["numerical"] = diff_numbers(
        extract_numbers(a["draft"]),
        extract_numbers(b["draft"])
    )

    # 2. Diff textual
    report["textual"] = diff_text(
        a["draft"], b["draft"]
    )

    # 3. Diff estructural
    report["structural"] = diff_structure(
        a["sections"], b["sections"]
    )

    # 4. Diff referencial
    report["references"] = diff_references(
        a["cites"], b["cites"]
    )

    # 5. No-regresion check
    if mode == "revision":
        report["no_regression"] = verify_no_regression(a, b)

    return report
```

## Pipeline Integration

```
paper-factory (genera paper)
  │
  ├── paper-diff (compara versiones: v1.0 vs v2.0)
  ├── paper-diff (compara variantes: Lima vs Arequipa)
  │
  ▼
paper-meta (sintetiza hallazgos cross-paper)
```

## Rules for This Project

1. **Diff despues de cada revision.** Verificar que solo cambiaron las cosas que debian cambiar.
2. **Cross-variant diff estandar.** Toda familia de variantes genera un diff consolidado.
3. **No-regresion obligatorio.** Si un numero no debia cambiar, NO debe cambiar.
4. **Diff como artefacto.** Guardar en `papers/<id>/reports/diff_v1_v2.md`.
