# replica_lima

> **Tipo:** Réplica metodológica  
> **Paper original:** Alonso-Pastor, Olaya Acosta & Calmet (2025). Segregación educativa y desigualdad social en el Perú. REICE 23(1).  
> **Dataset:** CPV 2017 (INEI), 128 distritos del departamento de Lima  
> **Métodos:** PCA → Índice Socioeconómico (NSE), Moran I Global, LISA, scatterplot de Moran  
> **Parámetros:** Queen contiguity orden 1, 999 permutaciones Monte Carlo, α = 0.05  

## Objetivo

Replicar los métodos de análisis espacial del paper original (Moran Global, LISA)
con los mismos parámetros pero sobre datos distintos: el Censo de Población y
Vivienda 2017 para 128 distritos del departamento de Lima.

**No es una copia textual.** Se replican los MÉTODOS, no la redacción.

## Resultados principales

| Variable | I de Moran | Z | p (MC) |
|---|---|---|---|
| NSE (vía PCA) | 0.5296 | 9.45 | .000 |
| Pobreza 2013 | 0.5300 | 9.44 | .000 |
| ECE Lengua | 0.1063 | 2.01 | .042 |
| ECE Matemáticas | 0.1774 | 3.26 | .004 |

## Referencia original

Alonso-Pastor, A., Olaya Acosta, G. y Calmet, E. (2025). *Segregación educativa y desigualdad social en el Perú: Un análisis espacial en el nivel secundario.* REICE 23(1). https://doi.org/10.15366/reice2025.23.1.001
