# spa-stat-group

> Réplica metodológica: Alonso-Pastor, Olaya Acosta & Calmet (2025). *Segregación educativa y desigualdad social en el Perú.* REICE 23(1). https://doi.org/10.15366/reice2025.23.1.001

## ¿De qué se trata?

**Estudio de réplica metodológica.** Reimplementamos los métodos de análisis espacial del paper original (Moran Global, LISA, scatterplot de Moran) con los mismos parámetros — Queen contiguity orden 1, 999 permutaciones Monte Carlo, α = 0.05 — pero sobre **datos distintos**: el Mapa de Pobreza Distrital 2018 del INEI para 128 distritos del departamento de Lima.

**Esto NO es plagio ni copia textual.** Replicamos los MÉTODOS, no la redacción. Escribimos nuestro propio análisis citando siempre la fuente.

## Resultados principales

| Variable | I de Moran | Z | p (MC) |
|---|---|---|---|
| NSE (vía PCA) | 0.5296 | 9.45 | 0.000 |
| Pobreza 2013 | 0.5300 | 9.44 | 0.000 |
| ECE Lengua | 0.1063 | 2.01 | 0.042 |
| ECE Matemáticas | 0.1774 | 3.26 | 0.004 |

→ Documento completo: [`paper/replica_lima.pdf`](paper/replica_lima.pdf) (8 páginas, LaTeX)

## Estructura

```
spa-stat-group/
├── README.md
├── AGENT.md
├── .gitignore
├── data/
│   ├── raw/          ← cpv_27.dta + enc_27.dta (NO versionados, bajar de INEI)
│   │   └── README.md    Instrucciones de descarga
│   ├── geo/          ← Shapefile distrital INEI 2023 (1.891 distritos)
│   │   └── README.md
│   └── processed/    ← shp_distrital.rds (generado por 01_carga.R)
├── src/
│   ├── 01_carga.R    ← Carga datos, agrega a distrito, construye NSE vía PCA
│   └── 02_moran.R    ← Moran I Global + Local, LISA, scatterplots, mapas
├── results/
│   ├── figures/      ← 4 PNGs (scatterplots + mapas LISA)
│   └── tables/       ← cuadro1_moran_lima.csv
├── paper/
│   ├── replica_lima.tex
│   └── replica_lima.pdf
└── docs/
    ├── metodologia-original.md   ← Parámetros exactos del paper original
    ├── referencias.md
    ├── decision-datos.md         ← Opciones de datos evaluadas
    └── original/                 ← PDF + txt del paper original
```

## Stack

- **Lenguaje**: R 4.4+
- **Paquetes**: `sf`, `spdep`, `ggplot2`, `dplyr`, `haven`, `tidyr`
- **LaTeX**: XeLaTeX (MiKTeX)

## Cómo reproducir

```bash
# 1. Clonar el repo
git clone https://github.com/valec3/spa-team-act.git
cd spa-team-act

# 2. Descargar datos del INEI (ver data/raw/README.md)
#    Colocar cpv_27.dta y enc_27.dta en data/raw/

# 3. Instalar paquetes R (solo la primera vez)
Rscript -e "install.packages(c('sf','spdep','ggplot2','dplyr','haven','tidyr'), repos='https://cran.r-project.org')"

# 4. Ejecutar pipeline
Rscript src/01_carga.R    # ~2 min (carga 1 GB + PCA)
Rscript src/02_moran.R    # ~30 seg (Moran + LISA + mapas)

# 5. Compilar paper (opcional)
cd paper
xelatex replica_lima.tex
xelatex replica_lima.tex  # segunda pasada para referencias
```

Todas las rutas son **relativas** — el pipeline funciona desde cualquier máquina clonando el repo.

## Reglas no negociables

1. **Se replican MÉTODOS, nunca texto.** La redacción es original.
2. **Se cita la fuente** siempre que se mencionan sus métodos o resultados.
3. **Los datos son públicos** (INEI) y están documentados en `data/raw/README.md`.
4. **Reproducibilidad total**: scripts versionados, rutas relativas, parámetros declarados.
5. **Transparencia** sobre qué se replicó y qué se adaptó.

## Licencia

Código: MIT. Datos: según licencia INEI. Texto: CC-BY 4.0.
