---
name: paper-citation
description: >
  Gestion de citas y referencias bibliograficas en formato APA 7. Cubre la creacion
  de entradas BibTeX con DOIs, el mantenimiento de docs/referencias.md, el formateo
  de citas en texto y la verificacion de que todas las citas tienen su referencia.
  Trigger: Cuando el usuario gestiona referencias, crea archivos .bib, formatea citas,
  busca DOIs, o necesita verificar la bibliografia de un paper.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Crear o mantener `referencias.bib`
- Formatear una referencia en APA 7
- Agregar una entrada BibTeX con DOI
- Verificar que todas las citas en el texto estan en la bibliografia
- Mantener `docs/referencias.md` actualizado
- Convertir una referencia manual a formato BibTeX

## Critical Patterns

### BibTeX Entry Template (APA 7 fields)

```bibtex
@article{autor2024titulo,
  author    = {Apellido, Nombre and Apellido, Nombre},
  title     = {Titulo completo del articulo en oracion: Subtítulo si lo hay},
  journal   = {Nombre Completo de la Revista},
  volume    = {XX},
  number    = {X},
  pages     = {XX--XX},
  year      = {2024},
  doi       = {10.XXXX/XXXXX},
  url       = {https://doi.org/10.XXXX/XXXXX},
  publisher = {Editorial},
  abstract  = {Breve descripcion para referencia interna}
}
```

### Entry Types by Source

| Fuente | Type | Campos requeridos |
|--------|------|-------------------|
| Articulo de revista | `@article` | author, title, journal, year, doi |
| Libro | `@book` | author, title, publisher, year |
| Capitulo de libro | `@incollection` | author, title, booktitle, publisher, year |
| Tesis | `@phdthesis` / `@mastersthesis` | author, title, school, year |
| Informe tecnico | `@techreport` | author, title, institution, year |
| Pagina web | `@misc` | author, title, year, url, urldate |
| Dataset | `@misc` | author, title, year, publisher, doi |

### Finding DOIs

```
1. Crossref API: https://api.crossref.org/works?query=TITLE+AUTHORS
2. Buscar titulo en Google Scholar → citar → formato BibTeX
3. doi.org → pegar titulo completo
```

### In-Text Citation (APA 7)

| Caso | Formato | Ejemplo |
|------|---------|---------|
| 1 autor | Apellido (Año) | Anselin (1995) |
| 2 autores | Apellido y Apellido (Año) | Alonso-Pastor y Olaya (2025) |
| 3+ autores | Apellido et al. (Año) | Alonso-Pastor et al. (2025) |
| Cita parentetica | (Apellido, Año) | (Anselin, 1995) |
| Cita narrativa | Apellido (Año) afirma... | Anselin (1995) afirma... |
| Multiples fuentes | (Apellido1, Año; Apellido2, Año) | (Anselin, 1995; Moran, 1950) |

### APA 7 Reference Format by Type

**Articulo de revista:**
```
Apellido, N. y Apellido, N. (Año). Titulo del articulo. Nombre de la Revista, Volumen(Numero), paginas. https://doi.org/XXXX
```

**Libro:**
```
Apellido, N. (Año). Titulo del libro (X.ª ed.). Editorial.
```

**Capitulo de libro:**
```
Apellido, N. (Año). Titulo del capitulo. En N. Apellido (Ed.), Titulo del libro (pp. XX-XX). Editorial.
```

### references.md Maintenance

`docs/referencias.md` debe mantenerse como registro MAESTRO:

```markdown
# Referencias bibliograficas

> Registro maestro de todas las fuentes citadas. Cada entrada incluye
> el BibTeX key, DOI, y nota de relevancia para el proyecto.

## Fuentes primarias (paper original)
- **alonso2025segregacion**: Alonso-Pastor, Olaya Acosta & Calmet (2025)
  - DOI: 10.15366/reice2025.23.1.001
  - Relevancia: Paper original que estamos replicando

## Metodologicas
- **anselin1995local**: Anselin (1995) Local Indicators of Spatial Association
  - DOI: 10.1111/j.1538-4632.1995.tb00338.x
  - Relevancia: Fundamento del LISA que usamos

## Datos
- **inei2018mapa**: INEI (2018) Mapa de Pobreza Distrital
  - URL: https://www.inei.gob.pe/...
  - Relevancia: Fuente de datos de nuestra replica
```

## Code Examples

### BibTeX File Structure

```bibtex
% === referencias.bib ===
% Fuentes primarias (paper original y su metodologia)
% ----------------------------------------------------

@article{alonso2025segregacion,
  author    = {Alonso-Pastor, Alberto and Olaya Acosta, Gerardo and Calmet, Enrique},
  title     = {Segregacion educativa y desigualdad social en el Peru: Un analisis espacial en el nivel secundario},
  journal   = {REICE. Revista Iberoamericana sobre Calidad, Eficacia y Cambio en Educacion},
  volume    = {23},
  number    = {1},
  year      = {2025},
  doi       = {10.15366/reice2025.23.1.001}
}

@article{anselin1995local,
  author    = {Anselin, Luc},
  title     = {Local Indicators of Spatial Association—LISA},
  journal   = {Geographical Analysis},
  volume    = {27},
  number    = {2},
  pages     = {93--115},
  year      = {1995},
  doi       = {10.1111/j.1538-4632.1995.tb00338.x}
}
```

## Rules for This Project

1. **DOI obligatorio.** Toda referencia debe tener DOI. Si no tiene, verificar que la fuente sea confiable.
2. **references.md es el maestro.** Cualquier fuente nueva se registra PRIMERO en `docs/referencias.md`, despues en el `.bib`.
3. **APA 7 para todo.** Incluso si el paper original usa otro formato, nuestras citas van en APA 7.
4. **Verificacion cruzada.** Antes de compilar, verificar que cada `\cite{}` tiene su `@article{}` en el `.bib`.
5. **URLs funcionales.** Si una referencia tiene URL en lugar de DOI, verificar que la URL este viva.

## Commands

```bash
# Verificar que todas las citas tienen entrada en el .bib
rg "\\\\cite\{" paper/replica_lima.tex --only-matching | sort -u

# Buscar DOI via Crossref API
curl -s "https://api.crossref.org/works?query=TITULO+AUTOR&rows=1" | python -m json.tool

# Generar .bib desde DOI
curl -sLH "Accept: text/bibliography; style=bibtex" "https://doi.org/10.15366/reice2025.23.1.001"
```
