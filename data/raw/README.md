# Datos crudos — fuentes

## Archivos del Mapa de Pobreza INEI 2018

Estos archivos NO se versionan (demasiado grandes). Descargar manualmente desde:

### Fuente oficial: INEI — Mapa de Pobreza 2018
URL: https://www.inei.gob.pe/estadisticas/pobreza/

### Archivos necesarios para la réplica:
1. `cpv_27.dta` (1 GB) — Variables candidatas para modelos (muestra Censo 2017)
2. `enc_27.dta` (12 MB) — Variables internas y externas (encuesta 2017)

Ambos archivos cubren 128 distritos de Lima (departamento 15).

### Procedimiento
Colocar ambos archivos en esta carpeta (`data/raw/`) y ejecutar desde la raíz del repositorio:
```
Rscript src/01_carga.R
```
Seguido de:
```
Rscript src/02_moran.R
```

El pipeline usa rutas relativas — funciona desde cualquier máquina donde se clone el repo y se coloquen los datos en `data/raw/`.
