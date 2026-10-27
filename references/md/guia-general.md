# Markdown — guía general (crear · analizar · editar · convertir)

> Este archivo absorbe el cuerpo de la antigua skill `md` (archivada el 2026-10-13 en `~/.agents/skills-archive/md`). La skill `ofimatica` lo mantiene íntegro; el índice de referencias detalladas está al final y también en el `SKILL.md` de la skill.

Escribe, analiza, edita y convierte archivos Markdown normales (documentos, notas, README, wikis, manuales).

**Alcance:** solo archivos `.md` de usuario. Para crear, modificar o evaluar `SKILL.md` de skills (opencode/Zed), usa la skill `skill-creator` — esta guía no genera `SKILL.md` ni estructura de skills. Si la tarea es en realidad un `.docx`, `.pdf`, `.xlsx` o `.pptx`, no estás en la sección equivocada: todo eso vive en esta misma skill `ofimatica` (ver dispatch del `SKILL.md`).

## Herramientas que necesita el agente

- `read`, `write`, `edit` — leer, crear y modificar los archivos `.md`
- `glob`, `grep` — localizar documentación en el proyecto
- `bash` — ejecutar las herramientas de conversión (pandoc, marked, etc.)
- `webfetch` — opcional: consultar la documentación de markdownguide.org si una referencia no alcanza

## Regla de Carpetas de Trabajo (OBLIGATORIA)

**Documentación del proyecto:** para tareas de creación de documentación **dentro del proyecto**, crea los `.md` en la ubicación que corresponda (`docs/`, `README.md`, etc.) — no uses carpeta temporal para documentación del proyecto.

**Conversiones o transformaciones temporales:** trabaja en una carpeta temporal **dentro del proyecto actual** (nunca en `AppData\Local\Temp` ni fuera del proyecto) y entrega el resultado al usuario. La carpeta **NO se elimina** al terminar:

```bash
set WORKDIR=.tmp\ofimatica-YYYYMMDD-HHMMSS
mkdir "%WORKDIR%" 2>nul
```

## Filosofía

Markdown es el lenguaje de marcado ligero más utilizado para documentación técnica. Fue creado por John Gruber en 2004 con el objetivo de ser legible en su formato fuente (sin necesidad de previsualización). Esta guía cubre las 6 capacidades:

1. **Crear** archivos `.md` bien estructurados y profesionales
2. **Leer/Analizar** archivos `.md` extrayendo su estructura y metadatos
3. **Editar/Transformar** archivos `.md` manteniendo consistencia
4. **Gestionar frontmatter** (metadatos YAML/TOML)
5. **Convertir** entre `.md` y otros formatos
6. **Usar la sintaxis correcta** según el estándar (CommonMark, GFM, Pandoc…)

## Workflow rápido

**Crear documentación:**
1. Definir frontmatter (YAML entre `---`) con al menos `title`.
2. Estructurar con un solo H1, jerarquía H2/H3 sin saltos, y TOC si hay más de 3 secciones.
3. Partir de una plantilla: ver `references/md/document-templates.md` (README, doc técnica, CHANGELOG) o las plantillas inline de más abajo.

**Analizar un .md existente:**
1. Leer el archivo completo con `read`.
2. Identificar frontmatter y extraer headings → TOC.
3. Detectar enlaces e imágenes y verificar consistencia de sintaxis.
4. Scripts Python: ver `references/md/analysis-and-editing.md`.

**Editar:**
1. Leer el archivo completo (contexto) → identificar secciones a cambiar.
2. Aplicar cada cambio con `edit` → releer el resultado final.
3. Opcional: convertir a HTML para previsualizar.

**Convertir formatos:**
1. Copiar el `.md` a la carpeta temporal `.tmp\ofimatica-<timestamp>\` del proyecto.
2. Ejecutar pandoc/marked → validar el output → entregar al usuario.
3. Comandos detallados: bloque de Conversión de más abajo y `references/md/format-conversion.md`.

## Cheatsheet mínima (lo más usado)

| Elemento | Sintaxis |
|----------|----------|
| Heading | `# Texto` (H1) … `###### Texto` (H6) |
| Párrafo | separar con una línea en blanco |
| Salto de línea | dos espacios al final de la línea + Enter |
| Negrita | `**texto**` |
| Cursiva | `*texto*` |
| Tachado | `~~texto~~` |
| Lista desordenada | `- Item` (subitems: 2–4 espacios) |
| Lista ordenada | `1. Item` |
| Enlace | `[texto](https://ejemplo.com)` |
| Imagen | `![alt](/ruta/imagen.png)` |
| Código inline | `` `codigo` `` |
| Bloque de código | `` ``` `` + lenguaje (`python`, `bash`…) |
| Blockquote | `> texto` |
| Línea horizontal | `---` |
| Tabla | `\| Col1 \| Col2 \|` con `:---`, `:---:`, `---:` |
| Task list | `- [ ] tarea` / `- [x] hecha` |
| Nota al pie | `[^1]` en el texto + `[^1]: texto` al final |
| Frontmatter | bloque YAML entre `---` al inicio del archivo |

**Reglas de oro:** espacio después de `#`; línea en blanco antes y después de headings, listas y bloques; un solo H1 por documento; no saltar niveles de heading; usar `*` (no `_`) dentro de palabras; rutas relativas para enlaces internos.

## Sintaxis avanzada (KaTeX · Mermaid · MDX)

- Matemáticas (KaTeX/MathJax): inline `$E=mc^2$` o bloque con `$$ ... $$`
- Diagramas: bloque de código con lenguaje `mermaid` (flujo, secuencia, Gantt, estados…)
- MDX: componentes JSX dentro del documento, p. ej. `<Componente prop={valor} />`

Referencia completa de comandos LaTeX, diagramas Mermaid y MDX: `references/md/advanced-syntax.md`.

## Frontmatter de documento

Frontmatter YAML para documentos (artículos, notas, posts). **No es el frontmatter de una skill** (`name`, `description`) — eso lo maneja `skill-creator`.

```yaml
---
title: "Título"
description: "Descripción"
author: "Autor"
date: 2026-06-29
version: 1.0.0
status: draft
tags: [tag1, tag2]
draft: false
---
```

Campos comunes: `title`, `description`, `author`, `date`, `version`, `status`, `language`, `tags`, `draft`, `slug`. Ver `references/md/frontmatter-guide.md` (incluye campos por framework: Jekyll, Hugo, **Obsidian**, MkDocs, Next.js).

## Plantillas rápidas (inline)

### README.md

````markdown
# Proyecto
> Descripción breve.

## Instalación
```bash
comando
```

## Uso
Ejemplo básico.

## Estructura
```
src/
├── componente/
└── utils/
```
````

### CHANGELOG.md

```markdown
# Changelog
## [1.1.0] - YYYY-MM-DD
### Added
- Nueva funcionalidad.
### Fixed
- Corrección de bug.
```

Plantillas completas (README estándar de GitHub, documentación técnica con TOC y CHANGELOG ampliado) más 8 buenas prácticas de creación: `references/md/document-templates.md`.

## Conversión entre formatos (pandoc)

```bash
# md → HTML
pandoc input.md -o output.html --standalone --toc

# md → PDF
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf

# md → DOCX
pandoc input.md -o output.docx --reference-doc=template.docx

# DOCX → md
pandoc input.docx -o output.md --wrap=preserve
```

Alternativas sin pandoc (marked para HTML; showdown + puppeteer para PDF) y el workflow de conversión paso a paso: `references/md/format-conversion.md`. Nota: para `.md → .docx` con plantilla Word o `.md → .pdf` con motor fino, coordina con las secciones Word/PDF de esta misma skill (`references/docx.md`, `references/pdf.md`).

## Buenas prácticas

1. Un solo H1 por documento.
2. Jerarquía consistente; no saltes niveles.
3. Líneas en blanco alrededor de headings, listas y code blocks.
4. Máximo 80-120 caracteres por línea.
5. Tabla de contenidos para docs >3 secciones.
6. Frontmatter en documentos formales.
7. Enlaces estilo referencia para docs largos.

Organización multiarchivo (`docs/`, nombres kebab-case, enlaces entre documentos): `references/md/docs-as-code.md`.

## Índice de referencias detalladas (con trigger de carga)

Carga el archivo SOLO cuando su trigger lo pida (rutas relativas a la carpeta de la skill `ofimatica`):

| Archivo | Contenido | Cuándo cargarlo (trigger) |
|---------|-----------|---------------------------|
| `references/md/basic-syntax.md` | Referencia completa de sintaxis básica: headings, párrafos, énfasis, listas, enlaces, imágenes, código, blockquotes, líneas horizontales, escaping, HTML en Markdown + cheat sheet | Duda con sintaxis básica o regla de formateo no cubierta en la cheatsheet de arriba |
| `references/md/extended-syntax.md` | Sintaxis extendida GFM: tablas, fenced code, footnotes, heading IDs, definition lists, task lists, emojis, tachado, highlight, sub/superíndice, auto-link, alertas GitHub, menciones/issues, citas abreviadas, sabores de Markdown | Tabla avanzada, footnote, ancla personalizada, alerta GFM o elemento extendido específico |
| `references/md/advanced-syntax.md` | Matemáticas KaTeX/MathJax (tabla de comandos LaTeX), diagramas Mermaid y MDX | Mermaid, KaTeX/math, MDX o cualquier sintaxis avanzada |
| `references/md/frontmatter-guide.md` | Frontmatter YAML/TOML: tipos de datos, campos por framework (Jekyll, Hugo, Obsidian, MkDocs, Next.js), extracción/actualización/validación, errores comunes | Crear o editar metadatos, o depurar un frontmatter que no parsea |
| `references/md/document-templates.md` | Plantillas listas para README, documentación técnica y CHANGELOG + 8 buenas prácticas | Crear un README, CHANGELOG o documentación técnica desde cero |
| `references/md/analysis-and-editing.md` | Scripts Python de análisis (headings, frontmatter, estadísticas), tabla de modificaciones, TOC manual, normalización y workflow de edición | Automatizar análisis, extraer estructura, normalizar sintaxis o planificar una edición grande |
| `references/md/docs-as-code.md` | Estructura de `docs/`, convenciones de nombres y reglas de enlaces entre documentos | Organizar documentación multiarchivo, o mover/enlazar .md entre carpetas |
| `references/md/format-conversion.md` | Conversiones .md ↔ HTML/PDF/DOCX con pandoc, marked y showdown/puppeteer + workflow | Convertir .md a otro formato o importar DOCX a Markdown |
| `references/md/markdown-hacks.md` | Trucos con HTML inline: centrado, color, subrayado, comentarios ocultos, imágenes con caption, videos, nuevas pestañas, listas en tablas, sangría, admoniciones | Algo que Markdown puro no soporta (alineación, colores, incrustados, comentarios) |

**Flujo de consulta recomendado:** cheatsheet de arriba → referencia mínima necesaria de la tabla → `webfetch` a markdownguide.org solo si la referencia no alcanza.
