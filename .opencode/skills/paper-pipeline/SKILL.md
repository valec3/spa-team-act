---
name: paper-pipeline
description: >
  Orquestador maestro del flujo agentico completo de redaccion de papers.
  Coordina las 6 fases: structure → draft → revision (3 pases) → latex-generate
  → latex-compile. Cada fase es una skill independiente. El pipeline maneja
  gates de calidad, iteraciones correctivas, y trazabilidad completa.
  Trigger: Cuando el usuario pide ejecutar el pipeline completo, iniciar el flujo
  agentico, crear un paper de principio a fin, o coordinar multiples skills.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Iniciar el flujo completo de creacion de un paper
- Coordinar la ejecucion secuencial de todas las skills
- Gestionar gates de calidad entre fases
- Re-ejecutar fases especificas despues de correcciones
- Trazabilidad completa del proceso de redaccion
- "Crear el paper de principio a fin"

## The Full Agentic Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    PAPER PIPELINE (orquestador)                  │
│                                                                 │
│  INPUTS:                                                        │
│  • docs/metodologia-original.md  (metodo documentado)           │
│  • results/tables/*.csv          (outputs de analisis)          │
│  • results/figures/*.png         (figuras generadas)            │
│  • docs/referencias.md           (referencias maestras)         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [FASE 1] paper-structure                                       │
│     Define: tipo de paper, secciones, word count                │
│     Output: plan estructural                                    │
│     Gate: ¿estructura definida y aprobada?                      │
│                                                                 │
│  [FASE 2] paper-draft                                           │
│     Ensambla: primer borrador completo                          │
│     Output: paper/draft_v1.md                                   │
│     Gate: ¿draft cubre todas las secciones?                     │
│                                                                 │
│  [FASE 3] paper-revision (orquesta 3 sub-pases)                 │
│     │                                                           │
│     ├── [3.1] paper-review-consistency                          │
│     │   Output: consistency_report.md                           │
│     │   Gate: ¿cero issues bloqueantes?                         │
│     │                                                           │
│     ├── [3.2] paper-review-language                             │
│     │   ├── paper-ai-patterns (catalogo AI a evitar)            │
│     │   ├── paper-humanize (burstiness, vocabulario, voz)       │
│     │   Output: language_report.md                              │
│     │   Gate: ¿cero AI vocabulary + burstiness > 15?            │
│     │                                                           │
│     └── [3.3] paper-polish                                      │
│         Output: polish_report.md + draft_v2.0.md                │
│         Gate: ¿checklist pre-LaTeX completo?                    │
│                                                                 │
│  [FASE 4] paper-latex-generate                                  │
│     Genera: archivo .tex compilable                             │
│     Output: paper/replica_lima.tex                              │
│     Gate: ¿.tex compila sin errores?                            │
│                                                                 │
│  [FASE 5] paper-latex (compilacion)                             │
│     Compila: xelatex 2-pass                                     │
│     Output: paper/replica_lima.pdf                              │
│     Gate: ¿PDF generado sin warnings criticos?                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Critical Patterns

### Phase Execution Protocol

```
Para CADA fase:

1. VERIFICAR dependencias: ¿estan listos los inputs de la fase?
2. EJECUTAR skill: delegar en la skill especializada
3. EVALUAR gate: ¿el output cumple los criterios de calidad?
4. DECIDIR:
   - ¿PASA? → avanzar a siguiente fase
   - ¿NO PASA? → documentar issues → corregir → RE-EJECUTAR esta fase
5. REGISTRAR: guardar artefactos y metadata de la fase
```

### Gate Criteria por Fase

| Fase | Gate | Criterio | Accion si falla |
|------|------|----------|-----------------|
| F1: structure | Estructura definida | Tipo paper, secciones, word count decididos | Re-planificar |
| F2: draft | Draft completo | Todas las secciones, placeholders marcados | Completar secciones faltantes |
| F3.1: consistency | Cero bloqueantes | Sin errores numericos ni citas huerfanas | Corregir y re-ejecutar F3.1 |
| F3.2: language | Cero bloqueantes | Sin errores gramaticales graves | Corregir y re-ejecutar F3.2 |
| F3.3: polish | Checklist completo | Abstract alineado, titulo optimizado | Pulir y re-ejecutar F3.3 |
| F4: latex-generate | Compilacion OK | xelatex sin errores | Corregir .tex y re-ejecutar F4 |
| F5: latex-compile | PDF OK | PDF generado, sin warnings criticos | Corregir y re-ejecutar F5 |

### Pipeline State Tracking

```json
{
  "pipeline": "paper-pipeline",
  "paper": "replica_lima",
  "started": "2024-07-15T10:00:00",
  "phases": {
    "F1_structure": {
      "status": "completed",
      "started": "2024-07-15T10:00:00",
      "completed": "2024-07-15T10:15:00",
      "output": "plan_estructural.md",
      "gate": "passed"
    },
    "F2_draft": {
      "status": "completed",
      "started": "2024-07-15T10:15:00",
      "completed": "2024-07-15T12:00:00",
      "output": "paper/draft_v1.md",
      "gate": "passed"
    },
    "F3_revision": {
      "status": "in_progress",
      "sub_phases": {
        "F3.1_consistency": {
          "status": "completed",
          "issues_blocking": 0,
          "gate": "passed"
        },
        "F3.2_language": {
          "status": "in_progress",
          "issues_blocking": 2,
          "gate": "pending"
        },
        "F3.3_polish": {
          "status": "pending"
        }
      }
    },
    "F4_latex_generate": { "status": "pending" },
    "F5_latex_compile": { "status": "pending" }
  }
}
```

### Error Recovery

```
Si una fase falla:

1. NO avanzar a la siguiente fase
2. Documentar el error en el pipeline state
3. Aplicar correccion (manual o asistida)
4. Re-ejecutar la fase fallida
5. Verificar que la correccion no rompio fases anteriores
   (ej: cambiar un numero en Results → re-ejecutar F3.1 consistency)

DEPENDENCIAS:
- F2 depende de F1
- F3 depende de F2
- F3.2 depende de F3.1
- F3.3 depende de F3.2
- F4 depende de F3
- F5 depende de F4
```

### Artifacts Map

```
Antes del pipeline:
  docs/metodologia-original.md     ← INPUT
  results/tables/*.csv             ← INPUT
  results/figures/*.png            ← INPUT
  docs/referencias.md              ← INPUT

Durante/despues del pipeline:
  paper/draft_v1.md                ← F2 output
  paper/draft_v2.0.md              ← F3.3 output (final)
  results/reports/consistency_report.md  ← F3.1 output
  results/reports/language_report.md     ← F3.2 output
  results/reports/polish_report.md       ← F3.3 output
  results/reports/revision_report.md     ← F3 consolidated
  paper/replica_lima.tex           ← F4 output
  paper/replica_lima.pdf           ← F5 output
  .pipeline_state.json             ← trazabilidad
```

## Code Examples

### Pipeline Initiation

```markdown
# Iniciar el pipeline agentico:

## Inputs requeridos:
- [x] Metodologia documentada en docs/metodologia-original.md
- [x] Resultados en results/tables/ y results/figures/
- [x] Referencias en docs/referencias.md y .bib

## Pipeline a ejecutar:
F1 → F2 → F3.1 → F3.2 → F3.3 → F4 → F5

## Comando (conceptual):
> Ejecutar paper-pipeline para replica_lima

¿Confirmas? [y/n]
```

### Resume Pipeline

```markdown
# Reanudar pipeline desde fase especifica:

Pipeline state: F3.2 (language) failed — 2 issues bloqueantes
Issues corregidos: ✅ si
Re-ejecutar desde: F3.2 (no es necesario re-ejecutar F3.1)

> Reanudar paper-pipeline desde fase F3.2
```

### Complete Pipeline Execution Report

```markdown
# Pipeline Execution Report
## Paper: replica_lima
## Inicio: 2024-07-15 10:00 | Fin: 2024-07-15 16:30 | Duracion: 6h 30m

### Resumen
| Fase | Estado | Issues | Duracion |
|------|--------|--------|----------|
| F1: structure | ✅ PASS | 0 | 15m |
| F2: draft | ✅ PASS | 3[TODO] | 1h 45m |
| F3.1: consistency | ✅ PASS (2 iter) | 5 → 0 | 1h 20m |
| F3.2: language | ✅ PASS (1 iter) | 8 → 0 | 55m |
| F3.3: polish | ✅ PASS | 3 → 0 | 40m |
| F4: latex-generate | ✅ PASS | 1 → 0 | 25m |
| F5: latex-compile | ✅ PASS | 0 | 5m |

### Artefactos generados
- paper/draft_v1.md (12 KB, 5200 palabras)
- paper/draft_v2.0.md (13 KB, 5600 palabras)
- results/reports/consistency_report.md
- results/reports/language_report.md
- results/reports/polish_report.md
- paper/replica_lima.tex (18 KB)
- paper/replica_lima.pdf (450 KB, 8 paginas)

### Metricas finales
- Palabras: 5,600 (target: 4,000-6,000) ✅
- Readability: 8/10 (target: ≥7) ✅
- Issues bloqueantes finales: 0 ✅
- Compilacion: sin errores ✅
```

## Pipeline Integration

`paper-pipeline` es el **entry point** principal. No es llamado por otras skills — es el que LLAMA a todas las demas.

```
                    ★ paper-pipeline ★
                    (ENTRY POINT)
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
 paper-structure   paper-draft    paper-revision
                                     │
                         ┌───────────┼───────────┐
                         ▼           ▼           ▼
                    consistency   language     polish
                         │           │           │
                         └───────────┴───────────┘
                                     │
                                     ▼
                           paper-latex-generate
                                     │
                                     ▼
                               paper-latex
```

## Rules for This Project

1. **Ejecutar fases en orden.** No saltar fases sin justificacion explicita.
2. **Gate enforcement estricto.** Si una fase no pasa, NO avanzar.
3. **Trazabilidad completa.** Cada fase deja artefactos versionados.
4. **Re-ejecutar lo minimo necesario.** Si F3.1 falla, corregir y re-ejecutar F3.1 (no F1, F2).
5. **Pipeline state versionado.** Guardar .pipeline_state.json en el repo.
6. **Intervencion humana en gates.** El usuario decide si un gate "pasa" cuando hay ambiguedad.
