---
name: paper-factory
description: >
  Fabrica de papers: toma un paper plan (dataset + metodo + poblacion) y
  ejecuta el pipeline completo para producir un paper terminado. Es la
  maquina que convierte datos en publicaciones. Orquesta las skills del
  pipeline agnostico (paper-structure → draft → revision → latex).
  Trigger: Cuando el usuario quiere generar un paper especifico desde cero,
  ejecutar "dataset X + metodo Y en poblacion Z", o producir un paper
  siguiendo el plan de paper-planning.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Generar un paper completo desde dataset + metodo + poblacion
- Ejecutar el pipeline para un paper especifico del plan
- Producir variantes de un paper (misma metodologia, diferente poblacion)
- Replicar un paper existente con datos nuevos
- Crear un paper de comparacion entre dos datasets

## Critical Patterns

### Factory Workflow

```
PAPER FACTORY = Orquestador por paper

INPUT:
  paper_spec:
    dataset: cpv2017
    methods: [pca_socioeconomic, moran_global, lisa]
    population: Lima (128 distritos)
    type: replica
    template: papers/_template/

PROCESS:
  ┌─────────────────────────────────────────────────┐
  │ FASE 0: SCAFFOLD                                │
  │   Crear papers/<paper_id>/ con estructura        │
  │   Copiar templates de papers/_template/          │
  │   Inicializar README.md del paper                │
  ├─────────────────────────────────────────────────┤
  │ FASE 1: DATA PREP                                │
  │   Ejecutar data-preprocessing para dataset       │
  │   Filtrar a la poblacion especifica              │
  │   Ejecutar data-validation                       │
  ├─────────────────────────────────────────────────┤
  │ FASE 2: ANALYSIS                                 │
  │   Cargar metodos de method-library               │
  │   Ejecutar pipeline de analisis                  │
  │   Guardar outputs en papers/<id>/results/        │
  ├─────────────────────────────────────────────────┤
  │ FASE 3: WRITING (paper-pipeline)                 │
  │   paper-structure → define estructura            │
  │   paper-draft → ensambla borrador                │
  │   paper-revision → consistency+language+polish   │
  │   paper-latex-generate → genera .tex             │
  │   paper-latex → compila PDF                      │
  └─────────────────────────────────────────────────┘

OUTPUT:
  papers/<paper_id>/
    ├── README.md
    ├── src/analysis_pipeline.R
    ├── results/figures/*.png
    ├── results/tables/*.csv
    ├── draft_v1.md
    ├── draft_v2.0.md
    ├── reports/consistency_report.md
    ├── reports/language_report.md
    ├── reports/polish_report.md
    ├── paper.tex
    └── paper.pdf
```

### Paper Specification (paper_spec.yml)

```yaml
# papers/replica_arequipa/paper_spec.yml
paper_id: replica_arequipa
title: "Segregación educativa y desigualdad espacial en Arequipa: Una réplica metodológica"
type: replica

dataset:
  id: cpv2017
  source: "datasets/cpv2017/processed/cpv2017_distrital.rds"

population:
  department: "Arequipa"
  n_districts: 109
  filter_expression: "DEPARTAMENTO == 'AREQUIPA'"

methods:
  - id: pca_socioeconomic
    params:
      rotation: "varimax"
      retention: "eigenvalue"
      eigenvalue_threshold: 1.0
      variables: ["avg_educacion", "avg_ingreso", "p_servicios"]

  - id: moran_global
    params:
      weight_type: "queen"
      order: 1
      nsim: 999
      alpha: 0.05

  - id: lisa
    params:
      nsim: 999
      alpha: 0.05
      adjustment: "none"

  - id: method_comparison
    params:
      original_paper: "papers/replica_lima"
      output_format: "latex"

original_study:
  paper: "papers/replica_lima"
  section: "docs/metodologia-original.md"

template:
  base: "papers/_template/"
  latex_template: "shared/templates/latex/replica_template.tex"

pipeline:
  seed: 20240101
  skip_validation: false
  auto_revision: true
```

### Scaffold Generation

El factory crea automaticamente la estructura del paper:

```
papers/<paper_id>/
├── README.md              # Metadata del paper (auto-generado)
├── paper_spec.yml         # Especificacion del paper
├── src/
│   └── analysis_pipeline.R  # Pipeline de analisis (compone metodos)
├── results/
│   ├── figures/           # Figuras generadas
│   └── tables/            # Tablas generadas
├── reports/               # Reportes de revision
├── draft_v1.md            # Primer borrador
├── draft_v2.0.md          # Borrador pulido
├── paper.tex              # LaTeX generado
└── paper.pdf              # PDF final
```

### Factory Execution Report

```markdown
# Factory Execution Report: replica_arequipa
## Inicio: 2024-07-18 14:00 | Fin: 2024-07-18 18:30 | Duracion: 4h 30m

### Pipeline Status
| Fase | Estado | Tiempo | Issues |
|------|--------|--------|--------|
| 0: Scaffold | ✅ | 5m | 0 |
| 1: Data Prep | ✅ | 15m | 0 |
| 2: Analysis | ✅ | 25m | 0 |
| 3.1: Structure | ✅ | 10m | 0 |
| 3.2: Draft | ✅ | 45m | 2 [CITAR] |
| 3.3: Consistency | ✅ (2 iter) | 40m | 3→0 |
| 3.4: Language | ✅ | 30m | 5→0 |
| 3.5: Polish | ✅ | 20m | 1→0 |
| 3.6: LaTeX Gen | ✅ | 15m | 0 |
| 3.7: Compile | ✅ | 5m | 0 |

### Resultados Clave
- I de Moran NSE: 0.48 (Z = 7.32, p < .001)
- Clusters AA: 18 distritos (Arequipa Metropolitana)
- Comparacion con replica_lima: delta = -0.05 (consistente, menor magnitud)

### Artefactos
- papers/replica_arequipa/paper.pdf (8 paginas, 480 KB)
- papers/replica_arequipa/draft_v2.0.md (5,200 palabras)
```

## Code Examples

### Factory Entry Point (Conceptual)

```r
# paper_factory.R — Fabrica un paper desde su especificacion
run_paper_factory <- function(paper_spec_path) {
  spec <- yaml::read_yaml(paper_spec_path)
  paper_dir <- dirname(paper_spec_path)

  # FASE 0: Scaffold
  scaffold_paper(paper_dir, spec$template$base)

  # FASE 1: Data Prep
  data <- load_dataset(spec$dataset$id)
  data <- filter_population(data, spec$population)
  validate_data(data, spec$pipeline$skip_validation)

  # FASE 2: Analysis
  results <- run_analysis_pipeline(data, spec$methods, spec$pipeline$seed)
  save_results(results, file.path(paper_dir, "results"))

  # FASE 3: Writing (delega en paper-pipeline skills)
  write_paper(paper_dir, spec, results)

  # Generar reporte
  generate_factory_report(paper_dir, spec)
}
```

### Variant Generation

```r
# Generar variantes de un paper base cambiando solo la poblacion
generate_variants <- function(base_paper, departments) {
  base_spec <- yaml::read_yaml(file.path(base_paper, "paper_spec.yml"))

  for (dept in departments) {
    variant_spec <- base_spec
    variant_spec$paper_id <- paste0("replica_", tolower(dept))
    variant_spec$title <- gsub(
      base_spec$population$department, dept, base_spec$title
    )
    variant_spec$population$department <- dept
    variant_spec$population$n_districts <- count_districts(dept)

    # Guardar spec y ejecutar factory
    variant_dir <- file.path("papers", variant_spec$paper_id)
    dir.create(variant_dir, recursive = TRUE)
    yaml::write_yaml(variant_spec, file.path(variant_dir, "paper_spec.yml"))
    run_paper_factory(file.path(variant_dir, "paper_spec.yml"))
  }
}

# Uso: generar replicas para Arequipa, Cusco, La Libertad
generate_variants("papers/replica_lima", c("Arequipa", "Cusco", "La Libertad"))
```

## Pipeline Integration

```
paper-planning (plan de papers)
  │
  ▼
paper-factory (fabrica UN paper)
  │
  ├── data-preprocessing + data-validation
  ├── method-library (ejecuta metodos)
  ├── paper-pipeline (writing: draft→revision→latex)
  │
  ▼
paper-batch (fabrica MULTIPLES papers)
```

## Rules for This Project

1. **Cada paper tiene su spec.** paper_spec.yml es el contrato del paper.
2. **Reusa, no dupliques.** Codigo compartido en methods/, templates en shared/.
3. **Scaffold primero.** La estructura del paper se crea antes de escribir una linea.
4. **Factory idempotente.** Re-ejecutar el factory regenera outputs sin perder personalizacion.
5. **Un paper = un directorio.** Aislamiento total entre papers.
