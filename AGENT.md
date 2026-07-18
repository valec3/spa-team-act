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

## Estructura del repo (respetar)

```
data/raw/         → inmutable, no se edita a mano, se documenta
data/processed/   → solo generado por src/, no commitear si es derivable
src/              → numerado: 01_carga, 02_limpieza, 03_analisis, 04_figuras...
results/          → generado por src/, reproducible
paper/            → redacción propia (NO el texto del original)
docs/             → referencias, metodología original, notas
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

## Lo que NO se hace

- No se asume el stack sin confirmar.
- No se copia texto del paper original como "nuestra" redacción.
- No se commitean datos sin documentar su origen.
- No se borra `data/raw/` — es inmutable por definición.