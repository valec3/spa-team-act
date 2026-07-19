---
name: paper-planning
description: >
  Planificacion estrategica de la cartera de papers. Dado un conjunto de
  datasets y metodos disponibles, determina que papers se pueden generar,
  prioriza por valor cientifico, y genera un plan de publicacion.
  Formula: Papers = Datasets x Metodos x Poblaciones.
  Trigger: Cuando el usuario quiere planificar papers, decidir que papers
  escribir, priorizar la cartera de publicaciones, o explorar combinaciones
  posibles de datasets + metodos.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Planificar que papers se pueden escribir con los datos disponibles
- Priorizar papers por impacto, factibilidad y originalidad
- Generar una matriz Datasets × Metodos × Poblaciones
- Definir variantes de un paper (diferente poblacion, diferente metodo)
- Estimar esfuerzo y recursos por paper
- Mantener un roadmap de publicaciones del repositorio

## Critical Patterns

### Paper Generation Formula

```
PAPERS POSIBLES = DATASETS × METODOS × POBLACIONES × ENFOQUES

Ejemplo con 3 datasets, 4 metodos, 2 poblaciones:

Datasets:    [cpv2017, ece2019, poverty_map_2018]
Metodos:     [moran_global, lisa, pca, descriptive]
Poblaciones: [Lima (128 distritos), Nacional (1874 distritos)]
Enfoques:    [original, replica, comparacion]

Total combinaciones teoricas: 3 × 4 × 2 × 3 = 72
Combinaciones viables (con datos): ~12
Papers priorizados (esfuerzo razonable): 3-5
```

### Paper Type Taxonomy

```
TIPO 1: REPLICA
  Dataset: alternativo al original
  Metodo: identico al original
  Proposito: validar generalizabilidad
  Ejemplo: replica_lima (cpv2017 × moran+lisa × Lima)

TIPO 2: EXTENSION
  Dataset: mismo que original
  Metodo: original + nuevo metodo
  Proposito: extender el analisis
  Ejemplo: bivariate_moran (ece2019 × moran_bivariado × Nacional)

TIPO 3: COMPARACION
  Datasets: 2+ datasets
  Metodo: identico
  Proposito: comparar resultados entre fuentes
  Ejemplo: cpv_vs_ece (cpv2017 vs ece2019 × moran × Nacional)

TIPO 4: META-REPLICA
  Datasets: 3+ datasets
  Metodo: identico
  Proposito: sintesis de multiples replicas
  Ejemplo: meta_replica (3 datasets × moran × 3 departamentos)

TIPO 5: METODOLOGICO
  Dataset: cualquiera
  Metodo: comparacion de metodos
  Proposito: evaluar sensibilidad a elecciones metodologicas
  Ejemplo: queen_vs_knn (cpv2017 × moran[queen,knn] × Lima)
```

### Paper Planning Matrix

```
Matriz de factibilidad para cada paper candidato:

| ID | Dataset | Metodo | Poblacion | Tipo | Datos? | Metodo listo? | Novedad | Esfuerzo | Prioridad |
|----|---------|--------|-----------|------|--------|---------------|---------|----------|-----------|
| P1 | cpv2017 | moran+lisa | Lima | replica | ✅ | ✅ | Media | Bajo | ⭐⭐⭐ |
| P2 | cpv2017 | moran+lisa | Arequipa | replica | ✅ | ✅ | Alta | Bajo | ⭐⭐⭐ |
| P3 | cpv2017 | moran+lisa | Cusco | replica | ✅ | ✅ | Alta | Bajo | ⭐⭐⭐ |
| P4 | ece2019 | moran+lisa | Nacional | replica | ⚠️ | ✅ | Baja | Medio | ⭐⭐ |
| P5 | cpv2017 vs ece2019 | moran | Lima | comparacion | ✅ | ✅ | Alta | Medio | ⭐⭐⭐ |
| P6 | cpv2017 | moran[queen vs knn] | Lima | metodologico | ✅ | ❌ | Alta | Alto | ⭐ |
| P7 | 3 datasets | moran | 3 deptos | meta-replica | ⚠️ | ✅ | Muy alta | Alto | ⭐⭐ |
```

### Paper Prioritization Rubric

| Criterio | Peso | Score 3 | Score 2 | Score 1 |
|----------|------|---------|---------|---------|
| Factibilidad (datos listos) | 30% | Datos validados | Datos disponibles, sin validar | Datos pendientes |
| Metodo disponible | 20% | Implementado y testeado | Implementado, sin tests | Requiere desarrollo |
| Novedad cientifica | 25% | No se ha hecho en esta poblacion | Extension de trabajo previo | Replica exacta |
| Esfuerzo estimado | 15% | <1 dia | 1-3 dias | >3 dias |
| Impacto potencial | 10% | Alta relevancia politica/social | Relevancia academica | Interes metodologico |

### Paper Plan Document

```markdown
# Paper Plan — spa-team-act
## Fecha: 2024-07-18

### Resumen
- Datasets disponibles: 4
- Metodos disponibles: 6
- Papers planificados: 5 activos, 3 en backlog

---

### Fase 1: Replicas departamentales (Prioridad: ALTA)

**P1: replica_lima** ✅ COMPLETADO
  Dataset: cpv2017 | Metodo: moran+lisa | Poblacion: Lima (128 distritos)
  Papers/replica_lima/

**P2: replica_arequipa** 🔄 EN PROGRESO
  Dataset: cpv2017 | Metodo: moran+lisa | Poblacion: Arequipa (109 distritos)
  Mismos metodos que P1, diferente poblacion. Reusa codigo.

**P3: replica_cusco** ⏳ PLANIFICADO
  Dataset: cpv2017 | Metodo: moran+lisa | Poblacion: Cusco (116 distritos)

---

### Fase 2: Comparaciones (Prioridad: MEDIA)

**P5: cpv_vs_ece_lima** ⏳ PLANIFICADO
  Datasets: cpv2017 + ece2019 | Metodo: moran | Poblacion: Lima
  Compara resultados entre dos fuentes de datos.

---

### Fase 3: Meta-analisis (Prioridad: BAJA)

**P7: meta_tres_departamentos** 🔮 BACKLOG
  Datasets: cpv2017 | Metodo: moran | Poblaciones: Lima + Arequipa + Cusco
  Requiere P1, P2, P3 completados primero.

---

### Métricas
- Papers completados: 1
- Papers en progreso: 1
- Papers planificados: 3
- Backlog: 3
- Eslabor estimado total: ~8 dias
```

## Code Examples

### Paper Generation Matrix (Conceptual)

```r
# Generar matriz de papers posibles
generate_paper_matrix <- function(datasets, methods, populations) {
  matrix <- expand.grid(
    dataset = names(datasets),
    method = names(methods),
    population = names(populations),
    stringsAsFactors = FALSE
  )

  matrix$feasible <- mapply(function(d, m, p) {
    # Verificar que la combinacion es viable
    has_data <- populations[[p]]$ubigeos %in% datasets[[d]]$ubigeos
    has_method <- methods[[m]]$status == "implemented"
    all(has_data) && has_method
  }, matrix$dataset, matrix$method, matrix$population)

  return(matrix[matrix$feasible, ])
}
```

### Prioritization Scoring

```r
score_paper <- function(paper) {
  factibilidad <- if (paper$data_status == "validated") 3
                 else if (paper$data_status == "available") 2
                 else 1

  metodo <- if (paper$method_ready) 3
            else if (paper$method_exists) 2
            else 1

  novedad <- if (paper$type == "extension") 3
             else if (paper$type == "comparison") 3
             else if (paper$type == "replica") 2
             else 1

  esfuerzo <- if (paper$effort_days <= 1) 3
              else if (paper$effort_days <= 3) 2
              else 1

  score <- factibilidad * 0.30 + metodo * 0.20 +
           novedad * 0.25 + esfuerzo * 0.15
  return(score)
}
```

## Pipeline Integration

```
data-catalog (datasets disponibles)
method-library (metodos disponibles)
  │
  ▼
paper-planning (matriz de papers posibles)
  │
  ├── paper_plan.md (documento de planificacion)
  │
  ▼
paper-factory (ejecuta papers planificados)
  │
  ▼
paper-batch (ejecuta multiples papers en lote)
```

## Rules for This Project

1. **Planificar antes de escribir.** Ningun paper se inicia sin estar en el plan.
2. **Priorizar por factibilidad.** Paper mas facil primero (genera momentum y reusa codigo).
3. **Maximo 3 papers activos.** Evitar dispersion. Completar antes de abrir mas.
4. **Reusa todo.** Paper 2 reusa metodos, codigo y templates de Paper 1.
5. **Plan versionado.** `papers/paper_plan.md` se actualiza con cada paper completado.
