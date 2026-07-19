# spatial_poverty_lima

> **Tipo:** Paper original  
> **Autores:** Maye Mamani, V.R.; Mulluni Cándia, J.J.; Maquera, J.S.E.; Choque Zuñiga, C.N.  
> **Afiliación:** Universidad Nacional del Altiplano, Facultad de Ingeniería Estadística e Informática, Puno, Perú  
> **Dataset:** CPV 2017 (INEI), 128 distritos de Lima Metropolitana  
> **Métodos:** PCA → Socioeconomic Level Index (SELI), Moran I Global, LISA  
> **Parámetros:** Queen contiguity orden 1, 999 Monte Carlo permutations, α = 0.05  
> **Idioma:** Inglés  
> **Formato:** Springer LaTeX  

## Objetivo

Investigar la distribución espacial y los patrones de clustering de la privación
socioeconómica multidimensional en los 128 distritos de Lima Metropolitana usando
el Censo 2017. A diferencia de la réplica, este es un paper original que:

- Construye un índice compuesto vía PCA (educación, ingreso, servicios, vivienda)
- Compara patrones espaciales con literatura internacional (Colombia, Turquía, Indonesia)
- Propone implicaciones de política territorial para Lima Metropolitana

## Resultados principales

| Variable | I de Moran | Z | p (MC) |
|---|---|---|---|
| SELI (PCA) | 0.5296 | 9.45 | .001 |
| Total poverty 2018 | 0.5300 | 9.44 | .001 |

Clusters LISA: High-High 21.1%, Low-Low 17.2%, No significativo 57.8%

## Referencias clave

- Anselin (1995) — LISA methodology
- Alonso-Pastor et al. (2025) — Spatial analysis in Peru
- González Bula et al. (2025) — Multidimensional poverty in Colombia
- Tatli et al. (2025) — Subjective poverty in Turkey
