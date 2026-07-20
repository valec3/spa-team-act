---
name: paper-revision
description: >
  Orquestador de revision de papers academicos. v2.0 coordina sub-skills
  especializadas: delega auditoria numerica a paper-review-consistency,
  revision de lenguaje a paper-review-language, y consolida todo en un
  reporte unificado de revision. Es el "control tower" del ciclo de revision.
  Trigger: Cuando el usuario pide revisar un draft, auditar calidad, preparar
  pre-submission, o ejecutar el ciclo completo de revision del pipeline agentico.
  NOTA: Esta skill ORQUESTA. Para tareas especificas, usa las sub-skills.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Coordinar una revision completa de paper (orquestador)
- Ejecutar el ciclo: consistency → language → polish
- Consolidar hallazgos de multiples revisores
- Decidir si un draft esta listo para LaTeX o necesita otra iteracion
- Preparar revision pre-submission con todas las verificaciones
- Generar reporte de revision unificado

## Revision Pipeline (Agentic Flow)

```
paper-revision (ORQUESTADOR)
│
├── [PASE 1] paper-review-consistency
│   ├── Auditoria numerica (texto vs outputs)
│   ├── Cross-references (figuras, tablas, ecuaciones, citas)
│   ├── Variable name consistency
│   └── Output: consistency_report.md + draft v1.1
│
├── [PASE 2] paper-review-language
│   ├── Tono academico y formalidad
│   ├── Claridad y concision
│   ├── Gramatica y ortografia
│   ├── Transiciones y fluidez entre parrafos
│   ├── ★ ANTI-AI HUMANIZACION (paper-humanize + paper-ai-patterns) ★
│   │   ├── Zero AI vocabulary (delve, tapestry, moreover, robust...)
│   │   ├── Burstiness check (rango > 15 palabras entre oraciones)
│   │   ├── Voice injection (preguntas retoricas, posicionamiento personal)
│   │   └── Citation naturalization (narrativas, no solo parenteticas)
│   └── Output: language_report.md + draft v1.2
│
└── [PASE 3] paper-polish
    ├── Alineacion Abstract-Conclusiones
    ├── Flow global entre secciones
    ├── Optimizacion de keywords y titulo
    ├── Readability final
    └── Output: polish_report.md + draft v2.0 (FINAL)
```

## Critical Patterns

### Gate Decision: ¿Iterar o avanzar?

Despues de cada pase, el orquestador evalua:

```
paper-review-consistency termina →
  ¿Issues bloqueantes > 0? → CORREGIR → re-ejecutar consistency
  ¿Issues bloqueantes = 0? → AVANZAR a language

paper-review-language termina →
  ¿Issues bloqueantes > 0? → CORREGIR → re-ejecutar language
  ¿Issues bloqueantes = 0? → AVANZAR a polish

paper-polish termina →
  ¿Readability score ≥ aceptable? → AVANZAR a LaTeX
  ¿Readability score < aceptable? → REVISAR secciones problematicas
```

### Unified Revision Report

El orquestador consolida los reportes de todas las sub-skills:

```markdown
# Revision Report: [Titulo del paper]
## Fecha: [YYYY-MM-DD] | Pipeline: consistency → language → polish
## Version del draft: v1.0 → v2.0

---

## Resumen Ejecutivo
- Pase 1 (Consistency): X issues (Y bloqueantes, Z sugerencias)
- Pase 2 (Language): X issues (Y bloqueantes, Z sugerencias)
- Pase 3 (Polish): X issues (Y bloqueantes, Z sugerencias)
- Estado final: [APROBADO para LaTeX | REQUIERE correcciones]
- Readability: [score] / [escala]

---

## Pase 1: Auditoria de Consistencia

### Issues Bloqueantes
1. [Seccion] [Descripcion] → [Correccion aplicada]
   - Archivo: [path]
   - Linea: [N]

### Issues Resueltos
- [X] [Issue] — Corregido en commit [hash]

---

## Pase 2: Revision de Lenguaje

[...mismo formato...]

---

## Pase 3: Pulido Final

[...mismo formato...]

---

## Metricas de Calidad
| Metrica | Inicial (v1.0) | Final (v2.0) | Target |
|---------|---------------|---------------|--------|
| Errores numericos | 5 | 0 | 0 |
| Citas huerfanas | 3 | 0 | 0 |
| Terminos inconsistentes | 2 | 0 | 0 |
| Oraciones >30 palabras | 12 | 3 | <5 |
| Voz pasiva % | 45% | 20% | <25% |

---

## Checklist Pre-LaTeX
- [ ] Cero issues bloqueantes en los 3 pases
- [ ] Todas las citas tienen entrada en .bib
- [ ] Todas las figuras referenciadas existen en disco
- [ ] Numeros en texto = numeros en tablas = numeros en outputs
- [ ] Terminologia consistente en todo el documento
- [ ] Abstract alineado con Conclusiones
```

### Severity Classification

| Nivel | Icono | Criterio | Accion |
|-------|-------|----------|--------|
| BLOQUEANTE | 🔴 | Error numerico, cita falsa, contradiccion | Corregir antes de avanzar |
| MAYOR | 🟠 | Inconsistencia terminologica, falta de claridad | Corregir en esta iteracion |
| MENOR | 🟡 | Sugerencia de estilo, redundancia | Corregir si hay tiempo |
| SUGERENCIA | 🔵 | Mejora opcional | Considerar |

### Delegation Rules

| Trigger en el draft | Delegar a |
|--------------------|-----------|
| "el I de Moran fue 0.53" pero en tabla dice 0.58 | paper-review-consistency |
| "se encontro una diferencia" → voz pasiva excesiva | paper-review-language |
| Parrafo de 6 oraciones sin transiciones | paper-review-language |
| Abstract dice "N = 200" y Metodo dice "N = 128" | paper-review-consistency |
| "en el presente estudio se procedio a realizar" → redundante | paper-polish |
| Titulo no contiene la variable dependiente | paper-polish |
| "delve into", "moreover", "robust" → AI vocabulary | paper-humanize |
| Oraciones uniformes (todas ~22 palabras) → baja burstiness | paper-humanize |
| Sin preguntas retoricas ni voz personal en Discussion | paper-humanize |

## Code Examples

### Revision Trigger Script

```bash
#!/bin/bash
# revision.sh — Ejecuta el ciclo completo de revision y genera reporte unificado

DRAFT="paper/draft_v1.md"
echo "=== PAPER REVISION PIPELINE ==="

echo "[1/3] Auditoria de consistencia..."
# llama a paper-review-consistency
echo "→ consistency_report.md generado"

echo "[2/3] Revision de lenguaje..."
# llama a paper-review-language
echo "→ language_report.md generado"

echo "[3/3] Pulido final..."
# llama a paper-polish
echo "→ polish_report.md generado"

echo "=== REPORTE UNIFICADO ==="
cat consistency_report.md language_report.md polish_report.md > revision_report.md
echo "→ revision_report.md generado"
```

## Pipeline Integration

`paper-revision` es el CORAZON del ciclo de calidad. Es llamado por `paper-pipeline` despues de `paper-draft` y antes de `paper-latex-generate`.

```
paper-draft → paper-revision (orquesta 3 sub-pases) → paper-latex-generate
                  │
                  ├── paper-review-consistency
                  ├── paper-review-language
                  └── paper-polish
```

## Rules for This Project

1. **No corregir durante la revision.** La revision IDENTIFICA issues. La correccion es un paso separado.
2. **Issues bloqueantes primero.** No se avanza a language si hay errores numericos.
3. **Cada pase genera su reporte.** El orquestador consolida, pero las sub-skills son autonomas.
4. **Gate decision explicita.** Despues de cada pase, decidir: ¿iterar o avanzar?
5. **Reporte unificado como artefacto.** El reporte final se versiona junto con el paper.
6. **Dos pares de ojos logicos.** El pipeline ejecuta 3 perspectivas de revision distintas.

## Commands

```bash
# Iniciar ciclo completo de revision
# (esto es conceptual — paper-pipeline lo orquesta)
echo "Ciclo: consistency → language → polish"

# Verificar que los 3 reportes existen
ls results/reports/consistency_report.md \
   results/reports/language_report.md \
   results/reports/polish_report.md

# Contar issues por severidad
rg "🔴 BLOQUEANTE" results/reports/revision_report.md | wc -l
rg "🟠 MAYOR" results/reports/revision_report.md | wc -l
```
