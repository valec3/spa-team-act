# Spatial Autocorrelation of Multidimensional Socioeconomic Deprivation across Metropolitan Lima, Peru

> Maye Mamani, V.R.; Mulluni Candia, J.J.; Maquera, J.S.E.; Choque Zuniga, C.N.  
> Universidad Nacional del Altiplano — Facultad de Ingenieria Estadistica e Informatica, Puno, Peru

## About

This repository contains the data, code, and manuscript for the paper
**"Spatial Autocorrelation of Multidimensional Socioeconomic Deprivation across
Metropolitan Lima, Peru: Evidence from Census Data."**

We analyze spatial clustering of socioeconomic deprivation across 128 districts
of Metropolitan Lima using Peru's 2017 National Population and Housing Census
(CPV 2017). A composite Socioeconomic Level Index (SELI) is constructed via PCA
and analyzed with Global Moran's I and LISA statistics (Queen contiguity order 1,
999 Monte Carlo permutations).

## Results

| Variable | Moran's I | Z | p (MC) |
|---|---|---|---|
| SELI (PCA) | 0.5296 | 9.45 | .001 |
| Poverty 2013 | 0.5300 | 9.44 | .001 |
| ECE Mathematics | 0.1774 | 3.26 | .004 |
| ECE Language | 0.1063 | 2.01 | .050 |

**LISA clusters (SELI):** High-High 6.3% (central Lima), Low-Low 13.3% (periphery),
Not significant 79.7%.

→ Full paper: [`papers/spatial_poverty_lima/paper.pdf`](papers/spatial_poverty_lima/paper.pdf)

## Structure

```
├── code/                  Analysis scripts
│   ├── 01_carga.R         Load data, aggregate to district, PCA for SELI
│   ├── 02_moran.R         Global Moran's I + LISA + scatterplots + maps
│   └── METHODS.yml        Method registry
├── data/
│   ├── catalog.yml        Dataset catalog (sources, variables, licenses)
│   ├── raw/               Raw census data (cpv_27.dta, enc_27.dta)
│   ├── geo/               District shapefile (INEI 2023)
│   └── processed/         Derived data (shp_distrital.rds)
├── papers/
│   └── spatial_poverty_lima/
│       ├── paper.tex      LaTeX source (Springer format)
│       └── paper.pdf      Compiled PDF
├── docs/
│   └── referencias/       Reference PDFs + referencias.bib (22 entries)
├── results/
│   ├── figures/           Moran scatterplots + LISA maps (4 PNGs)
│   └── tables/            Global Moran's I results (CSV)
└── README.md
```

## Reproducibility

### Requirements

- **R** 4.4+ with packages: `sf`, `spdep`, `ggplot2`, `dplyr`, `haven`, `tidyr`, `psych`
- **LaTeX**: MiKTeX or TeX Live (for PDF compilation)
- **Data**: CPV 2017 census files from INEI (see `data/raw/README.md`)

### Quick start

```bash
# 1. Clone
git clone https://github.com/valec3/spa-team-act.git
cd spa-team-act

# 2. Download data from INEI and place in data/raw/
#    Required: cpv_27.dta, enc_27.dta
#    See: data/raw/README.md

# 3. Install R packages
Rscript -e "install.packages(c('sf','spdep','ggplot2','dplyr','haven','tidyr','psych'), repos='https://cran.r-project.org')"

# 4. Run analysis (~3 min)
Rscript code/01_carga.R    # Load + aggregate + PCA
Rscript code/02_moran.R    # Moran I + LISA + figures

# 5. Compile paper
cd papers/spatial_poverty_lima
pdflatex paper.tex
pdflatex paper.tex         # second pass for references
```

All paths are **relative** — the pipeline runs from any machine after cloning.

## Parameters

| Parameter | Value |
|---|---|
| Spatial weights | Queen contiguity, order 1, row-standardized |
| Monte Carlo permutations | 999 |
| Significance level | α = 0.05 |
| PCA rotation | Varimax |
| Component retention | Eigenvalue > 1.0 |
| Random seed | 20240101 |
| N (districts) | 128 (Department of Lima) |

## License

Code: MIT. Data: INEI public use with attribution. Text: CC-BY 4.0.
