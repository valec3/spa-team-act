---
name: paper-batch
description: >
  Generacion por lotes de multiples papers. Ejecuta paper-factory para
  varios papers en secuencia o paralelo, con tracking de progreso,
  manejo de errores, y reporte consolidado. Ideal para generar variantes
  departamentales o comparaciones sistematicas.
  Trigger: Cuando el usuario quiere generar multiples papers, ejecutar
  variantes en lote, procesar una cartera de papers, o automatizar la
  generacion de replicas para varios departamentos.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Generar replicas para todos los departamentos de Peru (25 papers)
- Ejecutar el plan de paper-planning en lote
- Procesar variantes de un paper con diferentes parametros
- Regenerar todos los papers despues de actualizar un metodo
- Generar reportes consolidados de multiples papers
- Nightly build: regenerar todos los papers cada noche

## Critical Patterns

### Batch Execution Modes

```
MODO SECUENCIAL (default):
  Paper 1 → Paper 2 → Paper 3 → ...
  Uso: debugging, papers dependientes entre si
  Ventaja: logs claros, un error no afecta a otros

MODO PARALELO (--parallel):
  Paper 1 ─┐
  Paper 2 ─┼→ simultaneo (si recursos lo permiten)
  Paper 3 ─┘
  Uso: papers independientes, servidor con multiples cores
  Ventaja: velocidad (3-4x mas rapido)

MODO CONTINUAR (--resume):
  Retoma desde el ultimo paper completado
  Uso: batch interrumpido por error o timeout
```

### Batch Configuration

```yaml
# papers/batch_config.yml
batch_id: "replicas_departamentales_2024"
mode: "sequential"
papers:
  - paper_id: replica_lima
    spec: papers/replica_lima/paper_spec.yml
    priority: 1
    depends_on: []

  - paper_id: replica_arequipa
    spec: papers/replica_arequipa/paper_spec.yml
    priority: 1
    depends_on: []

  - paper_id: replica_cusco
    spec: papers/replica_cusco/paper_spec.yml
    priority: 2
    depends_on: []

  - paper_id: meta_tres_deptos
    spec: papers/meta_tres_deptos/paper_spec.yml
    priority: 3
    depends_on: [replica_lima, replica_arequipa, replica_cusco]

on_error: "continue"     # continue | stop | skip
max_parallel: 4           # solo en modo parallel
notify_on_complete: true
```

### Batch Progress Tracking

```json
{
  "batch_id": "replicas_departamentales_2024",
  "started": "2024-07-18T08:00:00",
  "status": "in_progress",
  "papers": {
    "replica_lima": {
      "status": "completed",
      "started": "2024-07-18T08:00:00",
      "completed": "2024-07-18T10:30:00",
      "duration_minutes": 150,
      "phases_completed": 7,
      "issues_total": 5,
      "issues_resolved": 5,
      "output_pdf": "papers/replica_lima/paper.pdf"
    },
    "replica_arequipa": {
      "status": "in_progress",
      "started": "2024-07-18T10:30:00",
      "current_phase": "F3.4: Language",
      "progress_pct": 65
    },
    "replica_cusco": {
      "status": "pending"
    },
    "meta_tres_deptos": {
      "status": "blocked",
      "blocked_by": ["replica_cusco"]
    }
  },
  "progress": {
    "total": 4,
    "completed": 1,
    "in_progress": 1,
    "pending": 1,
    "blocked": 1,
    "failed": 0
  }
}
```

### Batch Summary Report

```markdown
# Batch Execution Report: replicas_departamentales_2024
## Inicio: 2024-07-18 08:00 | Fin: 2024-07-19 16:00 | Duracion: 2 dias

---

### Resumen
| Metrica | Valor |
|---------|-------|
| Total papers | 4 |
| Completados | 3 ✅ |
| Fallidos | 1 ❌ (replica_cusco: error en data-validation) |
| Tiempo total | 32h (secuencial) |
| PDFs generados | 3 |

---

### Detalle por Paper

| Paper | Estado | Paginas | Palabras | Issues | Tiempo |
|-------|--------|---------|----------|--------|--------|
| replica_lima | ✅ | 8 | 5,600 | 5→0 | 2h 30m |
| replica_arequipa | ✅ | 7 | 5,200 | 3→0 | 2h 15m |
| replica_cusco | ❌ | - | - | - | 15m |
| meta_tres_deptos | ⏳ | - | - | - | - |

---

### Errores
❌ replica_cusco: Data validation failed
   - UBIGEO mismatch: 116 distritos en datos, 118 en shapefile
   - Accion: verificar shapefile de Cusco, re-ejecutar

---

### Hallazgos Cross-Paper
| Variable | Lima | Arequipa | Cusco | Patron |
|----------|------|----------|-------|--------|
| I Moran NSE | 0.53 | 0.48 | N/A | Decrece con tamaño depto? |
| Clusters AA (%) | 21% | 16% | N/A | Consistente con urbanizacion |
```

## Code Examples

### Batch Execution Script (Conceptual)

```python
# scripts/batch_papers.py
def run_batch(batch_config_path):
    config = load_yaml(batch_config_path)
    batch_id = config["batch_id"]
    state = init_batch_state(batch_id, config["papers"])

    # Ordenar por prioridad y dependencias
    ordered = topological_sort(config["papers"])

    for paper in ordered:
        if paper["paper_id"] in state["completed"]:
            continue

        # Verificar dependencias
        deps_met = all(d in state["completed"] for d in paper.get("depends_on", []))
        if not deps_met:
            state["papers"][paper["paper_id"]]["status"] = "blocked"
            continue

        try:
            result = run_paper_factory(paper["spec"])
            state["papers"][paper["paper_id"]]["status"] = "completed"
            state["progress"]["completed"] += 1
        except Exception as e:
            state["papers"][paper["paper_id"]]["status"] = "failed"
            state["papers"][paper["paper_id"]]["error"] = str(e)
            state["progress"]["failed"] += 1

            if config["on_error"] == "stop":
                break
            # "continue" o "skip": seguir con el siguiente

        save_batch_state(batch_id, state)

    # Reporte final
    generate_batch_report(batch_id, state)
```

### Dependency-Aware Scheduling

```
PAPERS CON DEPENDENCIAS:

  replica_lima ─────┐
                     ├──→ meta_tres_deptos
  replica_arequipa ─┤
                     │
  replica_cusco ────┘

Scheduling:
  Fase 1 (paralelo): replica_lima, replica_arequipa, replica_cusco
  Fase 2 (secuencial, depende de Fase 1): meta_tres_deptos
```

## Pipeline Integration

```
paper-planning (plan de papers)
  │
  ▼
paper-batch (ejecuta MULTIPLES papers)
  │
  ├── paper-factory × N (uno por paper)
  │   ├── data-preprocessing + data-validation
  │   ├── method-library
  │   └── paper-pipeline
  │
  ▼
paper-meta (sintesis cross-paper, si aplica)
```

## Rules for This Project

1. **Spec-driven.** Cada paper en el batch tiene su paper_spec.yml.
2. **Dependencias explicitas.** Si paper B necesita paper A, declararlo en depends_on.
3. **Estado persistente.** batch_state.json permite retomar batches interrumpidos.
4. **No paper huerfano.** Todo paper generado por batch queda registrado en el plan.
5. **Limpiar entre papers.** El estado de un paper no contamina al siguiente (entornos aislados).
