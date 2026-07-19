---
name: paper-results
description: >
  Redaccion de secciones de Resultados con rigor estadistico. v2.0 agrega:
  reporte de modelos complejos (mixtos, mediacion, SEM), estrategia de materiales
  suplementarios, anatomia de captions de figuras, vinculacion resultados-hipotesis,
  y manejo de resultados nulos/no significativos.
  Trigger: Cuando el usuario redacta resultados, reporta estadisticos, crea tablas
  de resultados, describe hallazgos de modelos complejos, prepara material
  suplementario, o escribe la seccion de Resultados.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Redactar la seccion de Resultados de un paper
- Reportar estadisticos en formato APA 7
- Describir resultados de modelos complejos (mixtos, SEM, mediacion)
- Crear tablas y figuras con captions profesionales
- Vincular resultados con hipotesis de investigacion
- Preparar material suplementario
- Reportar resultados nulos o no significativos con rigor

## Critical Patterns

### APA 7 Statistical Reporting

| Prueba | Formato APA | Ejemplo |
|--------|------------|---------|
| Moran's I | I = X.XX, Z = X.XX, p = .XXX | I = 0.53, Z = 9.45, p < .001 |
| t-test | t(gl) = X.XX, p = .XXX, d = X.XX | t(126) = 3.42, p = .001, d = 0.61 |
| ANOVA | F(gl1, gl2) = X.XX, p = .XXX, eta2 = .XX | F(3, 124) = 12.67, p < .001, eta2 = .23 |
| Chi-square | X^2(gl, N = XX) = X.XX, p = .XXX, V = .XX | X^2(2, N = 128) = 8.45, p = .015, V = .26 |
| Correlation | r(gl) = .XX, p = .XXX | r(126) = .67, p < .001 |
| Regression | b = X.XX, SE = X.XX, beta = .XX, t(gl) = X.XX, p = .XXX | b = 2.34, SE = 0.45, beta = .52, t(124) = 5.20, p < .001 |
| Mixed Model | b = X.XX, SE = X.XX, t = X.XX, p = .XXX | b = 0.34, SE = 0.12, t = 2.83, p = .005 |
| Mediation (indirect) | ab = X.XX, 95% CI [X.XX, X.XX] | ab = 0.23, 95% CI [0.08, 0.38] |
| SEM fit | X^2(gl) = X.XX, CFI = .XX, RMSEA = .XX | X^2(45) = 78.34, CFI = .95, RMSEA = .06 |

### Reporting Null/Non-Significant Results

```
NO hacer: "No se encontro diferencia significativa (p > .05)."
SI hacer: "La diferencia no fue estadisticamente significativa,
           t(126) = 1.23, p = .221, d = 0.15, IC 95% [-0.12, 0.42]."

Siempre incluir:
  - Estadistico de prueba (no solo el p-valor)
  - Tamano del efecto (d, r, eta2) con IC 95%
  - Interpretacion de la precision (ancho del IC)
```

### Figure Caption Anatomy

```
Figura X
[Titulo descriptivo en una frase — sin punto final si es titulo]
(panel A) [Descripcion del panel A]. (panel B) [Descripcion del panel B].
Las barras de error representan [±1 SE | IC 95% | IQR].
La linea punteada indica [referencia]. N = [tamano muestral].

Componentes obligatorios:
1. Label: "Figura X" (negrita en APA 7)
2. Titulo: una frase descriptiva en cursiva
3. Descripcion de paneles (si es multi-panel)
4. Unidades/barras de error
5. Abreviaturas definidas (si no estan en la nota general)
```

### Table Anatomy with APA 7 Notes

```
Tabla X
[Titulo descriptivo en cursiva]

[HEADER ROW]
[DATA ROWS]

Nota. [Nota general: explica abreviaturas, definiciones, fuente.]
[a] [Nota especifica para fila/columna a.]
[b] [Nota especifica para fila/columna b.]
*p < .05. **p < .01. ***p < .001. (two-tailed)

Reglas APA 7:
- Solo lineas horizontales (toprule, header-rule, bottomrule)
- Sin lineas verticales JAMAS
- Notas en este orden: General, Especifica (a, b, c...), Probabilidad (*)
```

### Results-Hypothesis Linking

```
ESTRUCTURA POR HIPOTESIS:

H1: [enunciado de la hipotesis]
→ "Para evaluar H1, se calculo [prueba estadistica]. Los resultados
   mostraron que [hallazgo], [estadistico = X.XX, p = .XXX, efecto = .XX].
   Este resultado [apoya | no apoya | refuta] H1."

H2: [enunciado]
→ ...
```

### Replication Comparison Table (Enhanced)

```
Tabla X
Comparacion de resultados: Estudio original vs. Presente replica

Variable      | I Moran (Orig) | I Moran (Repl) | Delta   | % Cambio | Interpretacion
--------------|----------------|----------------|---------|----------|---------------
NSE / ISE     | 0.658          | 0.530          | -0.128  | -19.5%   | Atenuacion moderada
Lengua        | 0.565          | 0.106          | -0.459  | -81.2%   | Atenuacion severa
Matematicas   | 0.501          | 0.177          | -0.324  | -64.7%   | Atenuacion severa

Nota. Delta = I_replica - I_original. % Cambio = (Delta / I_original) * 100.
Todos los I son significativos (p < .05, 999 permutaciones MC) en ambos estudios.
```

## Code Examples

### Results Paragraph — Single Hypothesis

```latex
\subsection{Autocorrelacion espacial global}

La Tabla~\ref{tab:moran} presenta los indices de Moran global. Consistentemente
con H1 (presencia de autocorrelacion espacial positiva), todas las variables
mostraron I de Moran positivo y estadisticamente significativo ($p < .05$).
El NSE presento la autocorrelacion mas fuerte ($I = 0.53$, $Z = 9.45$,
$p < .001$), seguido por Pobreza 2013 ($I = 0.53$, $Z = 9.44$, $p < .001$).
Las variables de logro educativo mostraron asociaciones espaciales
considerablemente mas debiles: ECE Lengua ($I = 0.11$, $Z = 2.01$,
$p = .042$) y ECE Matematicas ($I = 0.18$, $Z = 3.26$, $p = .004$).
```

### Figure Description (No Interpretation)

```latex
La Figura~\ref{fig:lisa-nse} presenta el mapa de clusters LISA para el NSE.
Los distritos clasificados como Alto-Alto ($n = 27$, 21.1\%) se concentraron
en Lima Metropolitana, mientras que los Bajo-Bajo ($n = 22$, 17.2\%) se
ubicaron predominantemente en las provincias del norte y sur del departamento.
Los clusters Alto-Bajo ($n = 3$, 2.3\%) y Bajo-Alto ($n = 2$, 1.6\%) fueron
escasos. Los 74 distritos restantes (57.8\%) no mostraron asociacion espacial
local significativa ($p > .05$).
```

### Supplementary Materials Strategy

```markdown
## Que va al papel principal vs. suplementario

| Contenido | Principal | Suplementario |
|-----------|-----------|---------------|
| Descriptivos basicos | Si (Tabla 1) | - |
| Resultados H1-H3 | Si | - |
| Mapas LISA (variable principal) | Si (Figura 2) | - |
| Mapas LISA (resto de vars) | - | Si (Figuras S1-S3) |
| Scatterplots Moran (todos) | - | Si (Figuras S4-S7) |
| Tabla de correlaciones | Si | - |
| Analisis de sensibilidad | Mencion | Si (resultados completos) |
| Diagnostico de supuestos | - | Si |
| Codigo completo | - | Si (repositorio) |
```

## Pipeline Integration

`paper-results` alimenta a `paper-draft`. En `paper-review-consistency`, se audita que cada numero en esta seccion coincida con los outputs de `results/tables/` y `results/figures/`.

## Rules for This Project

1. **Nunca interpretar en Resultados.** Interpretacion → Discusion.
2. **APA 7 estricto.** p sin cero inicial, cursivas, efecto + IC.
3. **Resultados nulos se reportan completos.** Estadistico + efecto + IC.
4. **Cada tabla/figura: autonoma.** El lector debe entenderla sin leer el texto.
5. **Hipotesis-driven.** Cada resultado se vincula a una hipotesis.
6. **Suplementario estrategico.** Lo esencial al paper, lo auxiliar al supplement.
