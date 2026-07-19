---
name: paper-review-consistency
description: >
  Auditoria de consistencia numerica, referencial y terminologica del paper.
  Verifica que cada numero en el texto coincida con los outputs, que cada
  figura/tabla referenciada exista, que las citas tengan su entrada .bib,
  y que la terminologia sea uniforme a lo largo del documento.
  Trigger: Cuando el usuario necesita auditar numeros, verificar cross-references,
  validar consistencia de variables entre secciones, o el pipeline agentico
  ejecuta el pase 1 de revision (orquestado por paper-revision).
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Auditar que numeros en texto coinciden con outputs de scripts
- Verificar que figuras y tablas referenciadas existen en disco
- Validar que cada \cite{} tiene entrada en el .bib
- Detectar variables nombradas inconsistentemente entre secciones
- Comprobar que N reportados son consistentes en todo el paper
- Ejecutar el Pase 1 del pipeline de revision (orquestado por paper-revision)

## Critical Patterns

### Audit Categories

```
AUDITORIA DE CONSISTENCIA — 5 dimensiones:

1. NUMERICA: numeros en texto vs resultados en outputs vs tablas
2. REFERENCIAL: citas en texto vs entradas en .bib
3. VISUAL: figuras y tablas referenciadas vs archivos en disco
4. TERMINOLOGICA: nombres de variables consistentes entre secciones
5. ESTRUCTURAL: N reportados, criterios inclusion, numeracion de secciones
```

### Numerical Audit Protocol

```
Para CADA numero en el draft:

1. Identificar: "I = 0.53" en seccion Resultados
2. Localizar fuente: results/tables/cuadro1_moran_lima.csv, fila "NSE", columna "I"
3. Comparar:
   - ¿Valor identico? (0.530 vs 0.53 → SI, redondeo aceptable)
   - ¿Decimales correctos? (APA 7: 2 decimales para I)
   - ¿Signo correcto? (positivo/negativo)
4. Si NO coincide → ISSUE BLOQUEANTE
```

### Audit Report Format

```markdown
# Consistency Audit Report
## Draft: paper/draft_v1.md
## Fecha: [YYYY-MM-DD]

### Resumen
- Total numeros auditados: [N]
- Coincidencias: [N]
- Discrepancias: [N]
- Citas huerfanas: [N]
- Figuras faltantes: [N]
- Issues terminologicos: [N]

---

### 1. Auditoria Numerica

| # | Ubicacion | Valor en texto | Valor en output | Archivo fuente | Estado |
|---|-----------|---------------|-----------------|----------------|--------|
| 1 | Results, para 2 | "I = 0.53" | 0.5296 | cuadro1_moran_lima.csv:L3 | OK |
| 2 | Results, para 3 | "Z = 9.45" | 9.448 | cuadro1_moran_lima.csv:L3 | OK |
| 3 | Abstract | "N = 128" | 128 | 01_carga.R:L15 | OK |
| 4 | Methods, para 1 | "999 permutaciones" | 999 | 02_moran.R:L8 | OK |

---

### 2. Cross-Reference Audit

| Tipo | Label en texto | ¿Existe en disco/bib? | Estado |
|------|---------------|----------------------|--------|
| Figura | fig:moran-nse | results/figures/moran_scatter_nse.png | OK |
| Tabla | tab:moran | - (inline en LaTeX) | OK |
| Cita | anselin1995local | referencias.bib:L12 | OK |
| Cita | alonso2025segregacion | referencias.bib:L5 | OK |

---

### 3. Variable Name Consistency

| Variable | Intro | Methods | Results | Discussion | ¿Consistente? |
|----------|-------|---------|---------|------------|---------------|
| NSE | "NSE" | "NSE (via PCA)" | "NSE" | "indice socioeconomico" | ❌ "NSE" vs "indice socioeconomico" |

---

### 4. Issues Report

🔴 BLOQUEANTE: Abstract dice "N = 130" pero Methods dice "N = 128"
   → Corregir Abstract a "N = 128"

🟠 MAYOR: "NSE" vs "indice socioeconomico" usado inconsistentemente
   → Estandarizar a "NSE" con definicion en primera aparicion

🟡 MENOR: Discussion refiere a "Tabla 2" pero es "Tabla 1"
   → Corregir referencia

---

### Checklist Final
- [ ] Cero discrepancias numericas
- [ ] Cero citas huerfanas
- [ ] Cero figuras/tablas faltantes
- [ ] Terminologia consistente en todo el documento
- [ ] N consistente en Abstract, Methods, Results
```

### Cross-Reference Matrix

Para verificar que TODO lo referenciado existe:

| Lo que se referencia | Donde se busca | Que verificar |
|---------------------|----------------|---------------|
| `\ref{fig:X}` | `results/figures/*.png` | Archivo existe |
| `\ref{tab:X}` | En el .tex (tabular o input) | Tabla definida |
| `\cite{X}` | `paper/referencias.bib` | Entrada @article{X} existe |
| `\ref{eq:X}` | En el .tex (equation) | Ecuacion definida |
| `\ref{sec:X}` | En el .tex (section) | Seccion definida |
| "Figura 1" vs `\ref{fig:moran}` | Orden de aparicion | Numero coincide |

### Common Consistency Errors

| Error | Causa tipica | Correccion |
|-------|-------------|------------|
| N en Abstract ≠ N en Methods | Se actualizo Methods pero no Abstract | Sincronizar |
| "Tabla 2" en texto, pero es Tabla 1 | Se inserto tabla nueva cambiando orden | Actualizar refs |
| I = 0.53 en texto, 0.5296 en tabla | Redondeo no consistente | Usar mismo formato |
| Cita `\cite{inei2018}` sin entrada .bib | Se cito de memoria | Agregar entrada |
| "Nivel Socioeconomico" → "NSE" → "ISE" | Cambio de nombre sin estandarizar | Elegir uno y usar siempre |

## Code Examples

### Automated Audit Script (Conceptual)

```python
# pseudo-codigo del flujo de auditoria
def audit_consistency(draft_path, outputs_dir, bib_path):
    report = ConsistencyReport()

    # 1. Extraer todos los numeros del draft
    numbers_in_text = extract_numbers(draft_path)

    # 2. Para cada numero, buscar en outputs
    for num in numbers_in_text:
        match = find_in_outputs(num, outputs_dir)
        report.add_numerical_check(num, match)

    # 3. Extraer todas las citas
    cites = extract_cites(draft_path)
    bib_entries = extract_bib_entries(bib_path)
    orphans = cites - bib_entries
    report.add_cite_orphans(orphans)

    # 4. Extraer referencias a figuras/tablas
    fig_refs = extract_figure_refs(draft_path)
    for ref in fig_refs:
        exists = check_file_exists(ref)
        report.add_visual_check(ref, exists)

    # 5. Verificar consistencia de variables
    var_names = extract_variable_names(draft_path)
    inconsistencies = find_name_variations(var_names)
    report.add_terminology_issues(inconsistencies)

    return report
```

### Manual Audit Checklist

```
□ Abrir draft. Para CADA numero (estadistico, N, porcentaje, p-valor):
  □ Localizar el output fuente
  □ Verificar que coinciden (valor, formato, decimales)
  □ Marcar OK o ISSUE

□ Abrir draft. Extraer todos los \cite{key}.
  □ Para cada key, verificar que existe en referencias.bib
  □ Marcar huerfanas

□ Abrir draft. Extraer todos los \ref{fig:X} y \ref{tab:X}.
  □ Verificar que label existe en el documento
  □ Verificar que archivo de figura existe (si aplica)

□ Abrir draft. Buscar todas las variantes de cada variable:
  □ "NSE", "nivel socioeconomico", "indice socioeconomico", "ISE"
  □ Estandarizar a UNA variante
```

## Pipeline Integration

```
paper-draft (produce draft_v1.md)
  │
  ▼
paper-revision (orquesta)
  │
  ├── ★ paper-review-consistency (PASE 1) ★
  │   ├── Audit: numeros, citas, figuras, terminologia
  │   └── Output: consistency_report.md
  │
  ├── paper-review-language (PASE 2)
  └── paper-polish (PASE 3)
```

## Rules for This Project

1. **Auditar TODO numero.** Sin excepcion. Si un numero esta en el texto, debe trazarse a un output.
2. **Cero tolerancia a discrepancias.** Un solo numero incorrecto es BLOQUEANTE.
3. **Outputs fuente como verdad.** Si el texto dice X y el output dice Y, el output es la verdad.
4. **Orden de severidad.** Numerico > Referencial > Terminologico.
5. **Reporte versionado.** Guardar consistency_report.md en results/reports/.
