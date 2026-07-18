# Metodología del paper original

> Documentar AQUÍ, con nuestras palabras, los métodos estadísticos del paper que vamos a replicar. No copiar el texto del original: resumir y reformular, citando la fuente.

## Referencia
Alonso-Pastor, A., Olaya Acosta, G. y Calmet, E. (2025). *Segregación educativa y desigualdad social en el Perú: Un análisis espacial en el nivel secundario.* REICE 23(1). https://doi.org/10.15366/reice2025.23.1.001

## Objetivo del estudio original
Investigar la segregación educativa socioeconómica en el Perú (nivel secundaria) mediante análisis espacial, estudiando la autocorrelación espacial (AE) entre el Índice Socioeconómico (ISE) y los resultados educativos de los estudiantes de 2do de secundaria en la ECE 2019, a nivel distrital.

## Datos originales
- **Fuente**: Evaluación Censal a Estudiantes (ECE) 2019, Perú (Oficina de Medición de la Calidad de los Aprendizajes, 2020). Evaluación censal más reciente disponible.
- **Población**: Estudiantes de 2do grado de secundaria.
- **N estudiantes**: 506.420.
- **N distritos con datos**: 1.781.
- **N distritos totales (capa SIG)**: 1.874 (capa vectorial del Instituto Geográfico Nacional, 2020).
- **Distritos excluidos**: 93
  - 92 etiquetados "Sin definir" (sin estudiantes / sin datos en ECE).
  - 1 isla en el lago Titicaca (Puno) sin vecinos espaciales → AE no calculable.

## Variables (promedios distritales, media aritmética sobre estudiantes)
1. **ISE** (Índice Socioeconómico): construido vía Análisis de Componentes Principales sobre: años de estudio de los padres, materiales de construcción de la vivienda, servicios básicos, activos y otros servicios del hogar. Variable estandarizada.
2. **Lengua y Literatura** (puntuación).
3. **Matemáticas** (puntuación).
4. **Ciencia y Tecnología** (puntuación).

## Método estadístico
### Matriz de pesos espaciales (W)
- **Tipo**: Queen contiguity (contigüidad tipo "reina" = comparten frontera o vértice).
- **Orden de contigüidad**: 1 (solo vecinos inmediatos).
- **Software original**: GeoDa (Anselin, 2021).
- **Variable de unión**: `UBIGEO` (código único distrital).
- **Estadísticas de vecindad** (de 1.874 obs.): mín=0, máx=19, media=5, mediana=6.
- **Estandarización**: el paper describe el Moran bajo estandarización por filas (S0 = n), aunque no lo dice explícitamente para W — lo asumimos así por la fórmula simplificada que presentan.

### Índice Global de Moran (I)
Fórmula (paper):
$$I = \frac{\sum_i \sum_j w_{ij} z_i z_j / S_0}{\sum_i z_i^2 / n}$$

donde:
- $z_i = x_i - \bar{x}$ (desviación de la media),
- $w_{ij}$ = elementos de W,
- $S_0 = \sum_i \sum_j w_{ij}$ (suma de todos los pesos),
- $n$ = número de observaciones.

Con W estandarizada por filas: $S_0 = n$, se simplifica a la pendiente de la regresión de $\sum_j w_{ij} z_j$ sobre $z_i$ (base del scatterplot de Moran).

**Inferencia**:
- Permutación de Monte Carlo: **999 repeticiones**.
- Significancia: **α = 0.05**.
- Reportan: I observado, E[I], media y desv. estándar de la permutación, Z-valor, pseudo p-valor, n permutaciones.

###scatterplot de Moran
- Eje X = variable $z$ (en desviaciones),
- Eje Y = retraso espacial $Wz$,
- Pendiente = I de Moran.
- 4 cuadrantes:
  - **AA** (Alto-Alto, sup. derecha): AE positiva.
  - **BB** (Bajo-Bajo, inf. izquierda): AE positiva.
  - **AB** (Alto-Bajo, inf. derecha): AE negativa.
  - **BA** (Bajo-Alto, sup. izquierda): AE negativa.

### Local Moran / LISA (Local Indicators of Spatial Association)
- Descomposición local del Moran I (Anselin, 1995, 1996).
- Permutación MC: **999 reps**, p<0.05.
- Mapeo de clústeres significativos en 4 categorías (AA, BB, AB, BA) + no significativo + sin vecinos + sin definir.
- Consideraciones sobre comparaciones múltiples:
  - Bonferroni: $\alpha_i = \alpha / m$ (conservador).
  - Sidák: $\alpha_i = 1 - (1-\alpha)^{1/m}$ (menos conservador, preferido por Anselin).

## Resultados clave del original (Cuadro 1)

| Variable | I Moran | E[I] | Media | D.E. | Z | pseudo p | Perms |
|---|---|---|---|---|---|---|---|
| ISE | 0.6584 | -0.0006 | -0.0007 | 0.0147 | 44.7365 | 0.001 | 999 |
| Lengua y Lit. | 0.5650 | -0.0005 | -0.0007 | 0.0136 | 13.5284 | 0.001 | 999 |
| Matemáticas | 0.5005 | -0.0005 | -0.0007 | 0.0137 | 13.3746 | 0.001 | 999 |
| Ciencia y Tec. | 0.5031 | -0.0005 | -0.0007 | 0.0135 | 13.3060 | 0.001 | 999 |

**Interpretación**: AE positiva fuerte para todas las variables, estadísticamente significativa (p=0.001, Z>>1.96). El ISE presenta la AE más alta (0.66), los logros académicos más moderada (~0.50-0.57).

## Distribución nacional de clústeres (Cuadro 3)

| Variable | AA | BB | AB | BA | No sig. |
|---|---|---|---|---|---|
| ISE | 274 | 316 | 18 | 10 | 1.161 |
| Lengua y Lit. | 255 | 242 | 20 | 18 | 1.244 |
| Matemáticas | 250 | 255 | 17 | 28 | 1.229 |
| Ciencia y Tec. | 244 | 226 | 22 | 27 | 1.260 |

**Total % (Cuadro 2)**: No sig. 61,95 % · AA 14,62 % · BB 16,86 % · BA 0,53 % · AB 0,96 % · Sin vecinos 0,11 % · Sin definir 4,96 %.

**Distribución geográfica** (iskey del paper):
- **AA** (alto-alto): costa — Callao, Ica, Lambayeque, Tacna, Lima, Arequipa, Moquegua.
- **BB** (bajo-bajo): selva (Loreto, Ucayali, San Martín, Amazonas) + sierra (Cajamarca, Huánuco).

## Stack elegido para la réplica (R)
- `sf` — lectura/manipulación de la capa vectorial distrital.
- `spdep` — Moran Global, Local Moran / LISA, matrices de pesos (Queen).
- `tmap` — mapas estáticos/interactivos (clúster LISA).
- `ggplot2` — scatterplot de Moran.
- `dplyr` — manipulación de datos distritales.
- `readr`/`haven`/`readxl` — lectura de la ECE u otra fuente.

## Qué adaptaremos y por qué
- **Datos distintos**: como ofreces el facsímil "cambiando los datos", necesitamos decidir qué datos usamos (ver `docs/decision-datos.md`).
- **Métodos idénticos**: reutilizamos exactamente Queen order 1, 999 perms, α=0.05, Moran Global+Local+LISA, scatterplot, mapas de clúster.
- **Software**: cambiamos GeoDa → R (`spdep`) para reproducibilidad vía script.
- **Posible ajuste**: si los datos disponibles no llegan a nivel estudiante, usaremos promedios distritales sintéticos respects la capa IGN.

## Limitaciones declaradas por el paper (a preservar en nuestra réplica)
1. > 50 % de distritos "no significativos" — limita el poder local del LISA.
2. Pocos distritos en AB/BA — dificulta análisis de AE negativa.
3. Datos previos al COVID-19 — no refleja efectos pandemic.
4. Heterogeneidad en calidad/cobertura de datos distritales.
5. Recomienda análisis departamental granular + Moran bivariado ISE × logros.