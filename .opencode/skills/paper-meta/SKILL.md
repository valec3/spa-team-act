---
name: paper-meta
description: >
  Sintesis y meta-analisis entre papers. Toma los resultados de multiples
  papers (variantes departamentales, replicas, comparaciones) y genera
  una sintesis de hallazgos, tablas comparativas cross-paper, y analisis
  de patrones. Identifica hallazgos robustos vs dependientes del dataset.
  Trigger: Cuando el usuario quiere sintetizar resultados de multiples papers,
  hacer meta-analisis de replicas, identificar patrones cross-dataset, o
  generar un paper de sintesis que integre hallazgos de varios estudios.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Sintetizar hallazgos de multiples replicas departamentales
- Comparar resultados entre diferentes datasets
- Identificar que hallazgos son robustos y cuales dependen del contexto
- Generar un paper de sintesis (meta-replica)
- Crear tablas comparativas cross-paper
- Analisis de sensibilidad: ¿cambian los resultados si cambio el dataset?

## Critical Patterns

### Meta-Analysis Workflow

```
INPUT: N papers con misma metodologia, diferentes poblaciones/datasets

PASO 1: EXTRACCION
  Para cada paper, extraer:
  - Estadisticos clave (I Moran, Z, p)
  - Parametros metodologicos (N, W, alpha)
  - Caracteristicas de la poblacion (tamano, urbanizacion, etc.)

PASO 2: COMPARACION
  Construir tabla cross-paper:
  - Variable dependiente: I de Moran
  - Variables moderadoras: N distritos, % urbano, tamano depto

PASO 3: SINTESIS
  - Hallazgos ROBUSTOS (consistentes en todos los papers)
  - Hallazgos CONTEXTUALES (varian segun poblacion)
  - Hallazgos CONTRADICTORIOS (direccion opuesta en distintos papers)

PASO 4: META-REGRESION (si N papers ≥ 5)
  - Relacion entre I Moran y caracteristicas poblacionales
  - ¿El tamano del departamento predice la magnitud de autocorrelacion?

OUTPUT: paper de sintesis + tablas cross-paper
```

### Cross-Paper Synthesis Table

```markdown
# Sintesis Cross-Paper: Replicas Departamentales

## Tabla 1: Resultados comparativos

| Departamento | N distritos | % Urbano | I Moran NSE | Z | p | Clusters AA (%) |
|-------------|------------|----------|-------------|---|---|-----------------|
| Lima | 128 | 89% | 0.53 | 9.45 | <.001 | 21.1% |
| Arequipa | 109 | 78% | 0.48 | 7.32 | <.001 | 16.5% |
| Cusco | 116 | 42% | 0.41 | 5.89 | <.001 | 12.1% |
| La Libertad | 83 | 65% | 0.45 | 6.12 | <.001 | 14.8% |
| Loreto | 53 | 35% | 0.38 | 4.21 | <.001 | 9.4% |

## Tabla 2: Correlaciones cross-paper

| Predictor | r con I Moran | p |
|-----------|--------------|---|
| N distritos | .72 | .017 |
| % Urbano | .85 | .002 |
| Densidad poblacional | .68 | .031 |

→ Interpretacion: Departamentos mas urbanos y con mas distritos tienden a
  mostrar mayor autocorrelacion espacial en indicadores socioeconomicos.
```

### Robustness Classification

```
HALLAZGOS ROBUSTOS (consistentes en ≥80% de los papers):
✅ Autocorrelacion espacial positiva del NSE en TODOS los departamentos
✅ Clusters AA concentrados en capitales departamentales
✅ I Moran NSE > I Moran variables educativas

HALLAZGOS CONTEXTUALES (varian segun contexto):
⚠️ Magnitud de I Moran: mayor en deptos mas urbanizados
⚠️ % clusters significativos: menor en deptos con menos distritos
⚠️ Variables educativas: mas autocorrelacion en deptos con mas cobertura ECE

HALLAZGOS CONTRADICTORIOS (direccion opuesta):
❌ (ninguno encontrado en esta familia de replicas)
```

### Meta-Regression (si N ≥ 5)

```r
# Meta-regression: ¿que predice la magnitud de autocorrelacion?
meta_data <- data.frame(
  departamento = c("Lima", "Arequipa", "Cusco", "La Libertad", "Loreto"),
  i_moran = c(0.53, 0.48, 0.41, 0.45, 0.38),
  n_distritos = c(128, 109, 116, 83, 53),
  pct_urbano = c(89, 78, 42, 65, 35),
  densidad = c(320, 45, 22, 68, 6)
)

model <- lm(i_moran ~ n_distritos + pct_urbano, data = meta_data)
summary(model)
# Resultado esperado: pct_urbano como predictor significativo de I Moran
```

### Meta Paper Structure

```
Para generar un paper de sintesis:

1. Introduction
   - Proposito: sintetizar hallazgos de N replicas departamentales
   - Pregunta: ¿que factores moderan la autocorrelacion espacial?

2. Methods
   - Descripcion de los N estudios incluidos
   - Criterios de inclusion (misma metodologia, diferente poblacion)
   - Metodo de sintesis (comparacion descriptiva, meta-regresion)

3. Results
   - Tabla 1: Resultados comparativos (cross-paper)
   - Tabla 2: Correlaciones con predictores contextuales
   - Figura 1: Forest plot de I Moran por departamento

4. Discussion
   - Hallazgos robustos vs contextuales
   - Implicaciones para generalizabilidad
   - Recomendaciones para futuras replicas
```

## Code Examples

### Cross-Paper Data Extraction

```r
# Extraer resultados clave de todos los papers en un directorio
extract_cross_paper_data <- function(papers_dir) {
  papers <- list.dirs(papers_dir, recursive = FALSE)

  results <- map_dfr(papers, function(p) {
    spec <- yaml::read_yaml(file.path(p, "paper_spec.yml"))
    output <- readRDS(file.path(p, "results", "analysis_results.rds"))

    tibble(
      paper_id = spec$paper_id,
      departamento = spec$population$department,
      n_distritos = spec$population$n_districts,
      i_moran_nse = output$moran$I,
      z_moran_nse = output$moran$Z,
      p_moran_nse = output$moran$p_value,
      n_clusters_aa = sum(output$lisa$cluster == "AA"),
      pct_clusters_aa = n_clusters_aa / spec$population$n_districts * 100
    )
  })

  return(results)
}
```

### Forest Plot Generation

```r
# Forest plot de I Moran por departamento
library(ggplot2)

ggplot(cross_paper_data, aes(x = i_moran_nse, y = reorder(departamento, i_moran_nse))) +
  geom_point(size = 3, color = "steelblue") +
  geom_errorbarh(aes(xmin = i_moran_nse - 1.96 * se, xmax = i_moran_nse + 1.96 * se),
                 height = 0.2) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  labs(
    title = "I de Moran del NSE por departamento",
    subtitle = paste0("N = ", nrow(cross_paper_data), " departamentos"),
    x = "I de Moran (IC 95%)",
    y = ""
  ) +
  theme_minimal()
```

## Pipeline Integration

```
paper-batch (genera N papers)
  │
  ▼
paper-diff (compara pares de papers)
  │
  ▼
paper-meta (sintetiza TODOS los papers)
  │
  ▼
paper-factory (genera paper de sintesis)
```

## Rules for This Project

1. **Meta-analisis requiere N ≥ 3 papers.** Menos que eso es comparacion, no sintesis.
2. **Misma metodologia.** Solo comparar papers que usan metodos identicos.
3. **Documentar heterogeneidad.** No solo reportar promedios; mostrar variacion.
4. **Forest plot obligatorio.** Visualizar I Moran (o estadistico principal) para todos los papers.
5. **Paper de sintesis como output final.** La meta-sintesis puede ser un paper en si mismo.
