# AGENT.md — Guía para agentes de IA en este repositorio

> Cualquier agente (humano o IA) que trabaje en `spa-stat-group` DEBE leer este archivo antes de tocar nada.

## Misión del proyecto

Réplica **metodológica** de un paper estadístico: reimplementar sus métodos sobre datos distintos, con fines didácticos y de reproducibilidad. **No es un facsímil textual.** No se copia la redacción; se replican los procedimientos estadísticos y se escribe un análisis propio.

## Reglas no negociables (LEER PRIMERO)

1. **Métodos sí, texto no.** Reimplementar modelos/test/procesos está bien. Copiar párrafos del paper original, NO. Toda redacción debe ser original nuestra.
2. **Citar la fuente.** Cada vez que se mencione un método o resultado del paper original, debe ir la cita correspondiente ( registrarla en `docs/referencias.md`).
3. **Procedencia de datos.** Nada de datos "misteriosos". Todo dataset en `data/raw/` debe tener un `README` o nota de origen + licencia. Si se simulan: declarar semilla y distribución.
4. **Reproducibilidad.** Semillas aleatorias fijas (`set.seed`/`random_state`). Scripts ejecutables de principio a fin. Entorno declarado (`requirements.txt` / `renv.lock` / `environment.yml`).
5. **Transparencia de cambios.** Si un método se adaptó, documentar qué se cambió y por qué en `docs/metodologia-original.md` y en el commit.

## Stack (a confirmar con el grupo)

- _TBD — definir antes de empezar_: lenguaje (¿R? ¿Python?), paquetes, formato de paper (¿LaTeX? ¿Quarto? ¿Markdown?).
- Mientras no esté definido, **preguntar** al usuario antes de asumir.

## Fábrica de Papers — Arquitectura Multi-Paper

Este repo es una **fábrica de papers académicos**. La fórmula es:

```
PAPER = DATASET × MÉTODO × POBLACIÓN × ENFOQUE
```

### Estructura del repo (v3.0 multi-paper)

```
datasets/              → Catálogo de fuentes de datos
  catalog/catalog.yml  → Registro maestro (fuente, variables, licencia)
  <id>/raw/            → Datos crudos (inmutables)
  <id>/processed/      → Datos procesados (derivables)
  <id>/src/            → Scripts de preprocesamiento

methods/               → Biblioteca de métodos reusables
  METHODS.yml          → Registro de métodos (params, I/O, implementación)
  <method>/            → Un método = un directorio (código + tests)

papers/                → Un directorio por paper
  <paper_id>/
    paper_spec.yml     → Especificación del paper (dataset + métodos + población)
    src/               → Scripts de análisis (compone métodos de methods/)
    results/           → Outputs específicos del paper
    reports/           → Reportes de revisión
    draft_v1.md        → Borrador inicial
    draft_v2.0.md      → Borrador pulido
    paper.tex          → LaTeX generado
    paper.pdf          → PDF compilado

shared/                → Recursos compartidos
  templates/latex/     → Plantillas LaTeX
  templates/reports/   → Plantillas de reportes
  utils/               → Utilidades R/Python

scripts/               → Scripts de automatización
docs/                  → Documentación global
```

### Flujo agéntico completo

```
PLANIFICAR:
  data-catalog → ¿qué datasets hay?
  method-library → ¿qué métodos hay?
  paper-planning → ¿qué papers podemos generar?

EJECUTAR (un paper):
  paper-factory → dataset + métodos → paper completo

EJECUTAR (múltiples papers):
  paper-batch → paper-factory × N papers

SINTETIZAR:
  paper-diff → comparar variantes
  paper-meta → meta-análisis cross-paper

AUDITAR:
  reproducibility-audit → ¿todo es reproducible?
```

## Convenciones de commits

- Usar **conventional commits**: `feat:`, `fix:`, `docs:`, `data:`, `chore:`.
- Un commit por cambio lógico. Nunca commitear secretos ni datos sensibles.
- Mensajes en presente: `feat: agrega script de limpieza de outliers` (no "agregado").

## Convenciones de scripts en src/

- Prefijo numérico ordenado por etapa: `01_carga.py`, `02_limpieza.py`, ...
- Un `header` con: propósito, autor, fecha, semilla usada.
- Sin rutas absolutas: usar rutas relativas desde la raíz del repo.
- Outputs van a `results/` o `data/processed/`, nunca a `src/`.

## Flujo ante una nueva tarea

1. ¿Hay que tocar datos? → verificar procedencia y licencia.
2. ¿Hay que reimplementar un método? → Documentarlo en `docs/metodologia-original.md` primero.
3. ¿Está definido el stack? → si no, preguntar antes de escribir código.
4. Escribir script numerado, con semilla, reproducible.
5. Commitear con conventional commit.

## Gestión del remoto de GitHub

**`gh` CLI NO está instalado en el entorno actual.** Opciones para crear/conectar el remoto:

- **Opción A — Instalar `gh`**: `winget install --id GitHub.cli` (Windows) y autenticar con `gh auth login`, luego `gh repo create spa-stat-group --source=. --private --push`.
- **Opción B — Manual**: crear el repo vacío en github.com, copiar la URL y:
  ```bash
  git remote add origin https://github.com/<usuario>/spa-stat-group.git
  git branch -M main
  git push -u origin main
  ```

## Antes de cerrar una sesión

- Guardar en memoria (engram/persistencia) decisiones tomadas: stack elegido, paper seleccionado, semillas, paquetes.
- Avisar al usuario qué falta y cuál es el siguiente paso.

## Pipeline Agéntico de Redacción

Este repositorio implementa un **flujo agéntico completo** para crear papers académicos.
El pipeline coordina 13 skills en 5 fases con gates de calidad.

```
F1: paper-structure     → define estructura y word count
F2: paper-draft         → ensambla primer borrador (draft_v1.md)
F3: paper-revision      → orquesta 3 sub-pases de revisión:
  F3.1: paper-review-consistency → auditoría numérica y cross-refs
  F3.2: paper-review-language    → tono académico y claridad
  F3.3: paper-polish             → pulido final (draft_v2.0.md)
F4: paper-latex-generate → genera paper/replica_lima.tex
F5: paper-latex          → compila con xelatex → paper/replica_lima.pdf
```

**Entrada**: `docs/metodologia-original.md` + `results/` + `docs/referencias.md`
**Salida**: `paper/replica_lima.pdf` compilado y revisado

### Cómo ejecutar el pipeline

Decir "ejecutá el pipeline" o "creá el paper de principio a fin" dispara `paper-pipeline`,
que orquesta todo el flujo secuencialmente con gates de calidad entre fases.

## Skills disponibles (OpenCode)

Las skills son instrucciones especializadas que guían al agente en tareas específicas.
Se cargan automáticamente cuando el contexto coincide.

## Skills del proyecto (`.opencode/skills/`) — 23 skills

### Pipeline de Redacción (1 paper)

| Fase | Skill | Trigger |
|------|-------|---------|
| F1 | `paper-structure` v2.0 | Estructurar paper, definir secciones, word count |
| F2 | `paper-draft` | Ensamblar primer borrador desde outputs |
| F3 | `paper-revision` v2.0 | Orquestar ciclo de revisión (→ 3 sub-pases) |
| F3.1 | `paper-review-consistency` | Auditar números, citas, cross-refs |
| F3.2 | `paper-review-language` | Revisar tono académico, gramática, claridad |
| F3.3 | `paper-polish` | Pulir fluidez, alinear Abstract-Conclusiones |
| F4 | `paper-latex-generate` | Generar archivo .tex desde draft pulido |
| F5 | `paper-latex` | Compilar LaTeX con XeLaTeX |

### Gestión de Datos

| Skill | Trigger |
|-------|---------|
| `data-catalog` | Registrar/buscar datasets en catalog.yml |
| `data-preprocessing` | Pipeline load→clean→transform→validate→output |
| `data-validation` | Controles de calidad, missing, outliers, rangos |

### Métodos Reusables

| Skill | Trigger |
|-------|---------|
| `method-library` | Definir/buscar métodos, componer pipelines |

### Fábrica de Papers (multi-paper)

| Skill | Trigger |
|-------|---------|
| `paper-planning` | Planificar cartera: datasets × métodos × poblaciones |
| `paper-factory` | Generar UN paper desde dataset + método |
| `paper-batch` | Generar MÚLTIPLES papers en lote |
| `paper-diff` | Comparar versiones/variantes de papers |
| `paper-meta` | Sintetizar hallazgos cross-paper |

### Soporte

| Skill | Trigger |
|-------|---------|
| `paper-methodology` v2.0 | Documentar métodos, justificar diseño |
| `paper-results` v2.0 | Redactar resultados, APA 7 |
| `paper-citation` | Gestionar citas, BibTeX, DOIs |
| `pdf-extract` | Extraer texto/tablas de PDFs |
| `reproducibility-audit` | Auditoría completa de reproducibilidad |
| `paper-pipeline` | **ENTRY POINT** — Orquestar flujo completo |

### Skills globales (`~/.config/opencode/skills/`)

| Skill | Descripción |
|-------|-------------|
| `go-testing` | Testing Go + Bubbletea TUI |
| `branch-pr` | Creación de PRs |
| `issue-creation` | Creación de issues |
| `judgment-day` | Review adversarial paralelo |
| `skill-creator` | Creación de nuevas skills |

## Python scripts

```bash
# Extraer texto de PDFs
python scripts/extract_pdf.py docs/original/paper.pdf --tables --metadata

# Instalar dependencias
pip install -r scripts/requirements.txt
```

## Lo que NO se hace

- No se asume el stack sin confirmar.
- No se copia texto del paper original como "nuestra" redacción.
- No se commitean datos sin documentar su origen.
- No se borra `data/raw/` — es inmutable por definición.