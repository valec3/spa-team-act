---
name: method-library
description: >
  Biblioteca de metodos de analisis reusables. Cada metodo es un modulo
  independiente con parametros, inputs/outputs declarados, implementacion
  en R, tests, y documentacion. Permite componer analisis como
  "dataset + metodo → resultados".
  Trigger: Cuando el usuario define un nuevo metodo, busca metodos disponibles,
  compone un pipeline de analisis, o necesita documentar un procedimiento
  estadistico como modulo reusable.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Definir un nuevo metodo de analisis como modulo reusable
- Buscar metodos disponibles para un tipo de analisis
- Componer un pipeline: dataset X + metodo Y + metodo Z → resultados
- Documentar parametros, inputs y outputs de un metodo
- Versionar metodos (el metodo evoluciona, los papers referencian versiones)
- Testear metodos con datos sinteticos antes de usar datos reales

## Critical Patterns

### Method = Data → Results

```
El principio fundamental:

  dataset + method(params) → results

Un metodo es una funcion pura:
  - Mismos inputs + mismos parametros → mismos outputs (reproducible)
  - Sin efectos secundarios (no modifica datos globales)
  - Testeable con datos sinteticos
```

### Method Module Structure

```
methods/<method_name>/
├── README.md           # Documentacion del metodo
├── <method_name>.R     # Implementacion
├── tests/
│   └── test_<method>.R # Tests unitarios
└── examples/
    └── example.R       # Ejemplo de uso
```

### Method Registration (METHODS.yml)

```yaml
methods:
  - id: moran_global
    name: "Índice Global de Moran"
    category: "spatial_analysis"
    version: "1.0"

    # QUE hace
    description: >
      Calcula el I de Moran global. Soporta Queen/Rook/KNN.

    # COMO se configura
    parameters:
      - name: "weight_type"
        type: "enum[queen, rook, knn]"
        default: "queen"
      - name: "order"
        type: "integer"
        default: 1

    # QUE necesita
    inputs:
      - name: "sf_data"
        type: "sf"
        description: "Objeto sf con variable de interes"

    # QUE produce
    outputs:
      - name: "moran_I"
        type: "numeric"
      - name: "p_value"
        type: "numeric"

    # DONDE esta el codigo
    implementation: "methods/spatial_analysis/moran_global.R"
    tests: "methods/spatial_analysis/tests/test_moran_global.R"

    # QUE paquetes requiere
    dependencies:
      r_packages: ["spdep", "sf"]

    # EN QUE papers se ha usado
    used_in:
      - paper: "papers/replica_lima"
        params: {weight_type: "queen", order: 1, nsim: 999}
```

### Method Composition

```
Los metodos se pueden componer en pipelines:

PIPELINE: Analisis espacial completo
  data (sf object)
    → moran_global(weight_type="queen", nsim=999)
    → lisa(alpha=0.05)
    → spatial_clusters_map()

PIPELINE: Construccion de indice socioeconomico
  data (data.frame, variables socioeconomicas)
    → pca_socioeconomic(rotation="varimax")
    → descriptive_stats(format="apa")

PIPELINE: Replica completa
  dataset: cpv2017, poblacion: Lima, N=128
    → pca_socioeconomic(rotation="varimax")
    → moran_global(weight_type="queen", order=1)
    → lisa(alpha=0.05)
    → method_comparison()
    → export_for_paper(format="latex")
```

### Method Versioning

```
Los metodos evolucionan. Los papers deben referenciar la version exacta:

methods/spatial_analysis/moran_global.R
  v1.0 (2024-01): Queen/Rook, row-standardized, MC inference
  v1.1 (2024-07): +KNN, +Sidak adjustment, +parallel processing

Papers que usan v1.0:
  - papers/replica_lima (enero 2024)
Papers que usan v1.1:
  - papers/replica_arequipa (julio 2024)

Si un paper necesita v1.0 especificamente, usar git tag:
  git checkout methods/v1.0 -- methods/spatial_analysis/moran_global.R
```

### Method Testing with Synthetic Data

```r
# methods/spatial_analysis/tests/test_moran_global.R
library(testthat)
library(sf)

test_that("moran_global returns expected structure", {
  # Crear datos sinteticos con autocorrelacion conocida
  set.seed(20240101)
  n <- 100
  coords <- expand.grid(x = 1:10, y = 1:10)
  sf_data <- st_as_sf(coords, coords = c("x", "y"))
  sf_data$var <- rnorm(n)

  # Ejecutar metodo
  result <- moran_global(sf_data, "var", weight_type = "queen")

  # Verificar estructura del output
  expect_type(result$I, "double")
  expect_true(result$I >= -1 && result$I <= 1)
  expect_type(result$p_value, "double")
  expect_true(result$p_value >= 0 && result$p_value <= 1)
})
```

### Method Discovery

```
"¿Que metodos hay para analisis espacial?"
→ METHODS.yml: filter(category == "spatial_analysis")

"¿Que metodos usan el paquete spdep?"
→ METHODS.yml: filter(dependencies.r_packages contains "spdep")

"¿Que metodos se han usado en papers/replica_lima?"
→ METHODS.yml: filter(used_in[*].paper == "papers/replica_lima")

"¿Que metodos no se han usado en ningun paper?"
→ METHODS.yml: filter(used_in == [])
```

## Code Examples

### Implementing a New Method

```r
# methods/mi_metodo/mi_metodo.R
# =============================================================================
# mi_metodo.R — [Descripcion breve]
# Version: 1.0 | Categoria: [categoria]
# Autor: [nombre] | Fecha: [YYYY-MM-DD]
# =============================================================================
# Parametros:
#   param1 (type, default): descripcion
#   param2 (type, default): descripcion
# Inputs:
#   input1 (type): descripcion
# Outputs:
#   output1 (type): descripcion
# Dependencias: pkg1, pkg2
# Tests: tests/test_mi_metodo.R
# =============================================================================

mi_metodo <- function(data, variable, param1 = "default", param2 = 0.05) {
  # 1. Validar inputs
  stopifnot(is.data.frame(data))
  stopifnot(variable %in% names(data))

  # 2. Ejecutar analisis
  set.seed(20240101)  # Semilla fija para reproducibilidad
  result <- analisis_core(data[[variable]], param1, param2)

  # 3. Formatear outputs
  list(
    statistic = result$stat,
    p_value = result$p,
    n = nrow(data),
    params = list(param1 = param1, param2 = param2)
  )
}
```

### Composing a Paper Pipeline

```r
# papers/replica_lima/src/analysis_pipeline.R
# Compone metodos de la biblioteca para este paper especifico

source("methods/pca/pca_socioeconomic.R")
source("methods/spatial_analysis/moran_global.R")
source("methods/spatial_analysis/lisa.R")
source("methods/descriptive/descriptive_stats.R")

# 1. Cargar datos preparados
data <- readRDS("datasets/cpv2017/processed/cpv2017_distrital.rds")

# 2. Construir NSE
nse_result <- pca_socioeconomic(
  data,
  variables = c("avg_educacion", "avg_ingreso", "p_servicios"),
  rotation = "varimax"
)
data$idx_nse <- nse_result$index

# 3. Moran Global
moran_result <- moran_global(
  data,
  variable = "idx_nse",
  weight_type = "queen",
  order = 1,
  nsim = 999,
  alpha = 0.05
)

# 4. LISA
lisa_result <- lisa(data, variable = "idx_nse", alpha = 0.05)

# 5. Exportar resultados
saveRDS(list(nse = nse_result, moran = moran_result, lisa = lisa_result),
        "papers/replica_lima/results/analysis_results.rds")
```

## Pipeline Integration

```
method-library define metodos reusables
  │
  ├──→ paper-planning (que metodos aplicar a que datasets)
  ├──→ paper-factory (dataset + metodo → resultados → paper)
  └──→ reproducibility-audit (verifica que metodos son reproducibles)
```

## Rules for This Project

1. **Un metodo = un directorio.** Codigo, tests y ejemplos en el mismo lugar.
2. **Parametros explicitos.** Todo parametro tiene tipo, default y descripcion en METHODS.yml.
3. **Testeable con datos sinteticos.** Cada metodo debe poder ejecutarse sin datos reales.
4. **Versionado.** Los metodos evolucionan; los papers referencian versiones con git tags.
5. **Outputs estandar.** Cada metodo devuelve una lista nombrada con tipos documentados.
6. **No reinventar.** Antes de crear un metodo nuevo, verificar que no existe en la biblioteca.
