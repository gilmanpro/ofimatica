# pandoc — contexto experto de conversión

Referencia de la herramienta de conversión de markup multi-formato (fuente: pandoc.org y `pandoc --help`; verificada con **pandoc 3.12.1** en Windows, features `+server +lua`, Lua 5.4). Cargar solo cuando la tarea implique convertir entre formatos con pandoc, elegir motor de PDF, citas/filtros o diagnosticar una conversión fallida. Para conversiones simples `.md ↔ HTML/PDF/DOCX` la receta corta vive en `references/md/format-conversion.md`; esta referencia es el contexto que falta ahí.

**Índice**: 1 [Cuándo pandoc vs alternativas](#1-cuándo-pandoc-vs-alternativas) · 2 [Instalar y verificar](#2-instalar-y-verificar) · 3 [Matriz de formatos](#3-matriz-de-formatos) · 4 [Sintaxis y extensiones](#4-sintaxis-y-extensiones) · 5 [PDF](#5-pdf) · 6 [DOCX](#6-docx) · 7 [PPTX con pandoc](#7-pptx-con-pandoc) · 8 [Citas y bibliografía](#8-citas-y-bibliografía) · 9 [Matemáticas](#9-matemáticas) · 10 [Filtros y templates](#10-filtros-y-templates) · 11 [Notebooks y datos](#11-notebooks-y-datos) · 12 [Anti-patrones](#12-anti-patrones) · 13 [Troubleshooting](#13-troubleshooting)

## 1. Cuándo pandoc vs alternativas

Regla central: **pandoc convierte estructura semántica (headings, tablas, código, footnotes), no maquetación de página**. Si el criterio es fidelidad visual de Office, gana LibreOffice/Word; si es convertir contenido estructurado entre formatos de texto enriquecido, gana pandoc.

| Necesidad | Primaria | Fallback | Señal para cambiar de opción |
|---|---|---|---|
| `.md` → HTML/DOCX/EPUB/ODT con estructura | pandoc | marked (solo HTML) | pierde estilo propio de Word → docx-js o `references/editing.md` |
| `.md` → PDF | pandoc con `--pdf-engine=weasyprint` o TeX si existe | `python scripts/convert.py` (vía DOCX + LibreOffice) | falla el motor o fuentes rotas → convert.py |
| Leer `.docx` → texto/estructura | `pandoc doc.docx -o out.md --track-changes=all` | markitdown / unpack XML | solo necesitas texto crudo → markitdown |
| Editar plantilla Word existente | unpack/pack XML (`references/editing.md`) o docx-js | pandoc `--reference-doc` | el contenido ya vive en `.md` y solo cambia estilo → pandoc |
| Presentaciones con diseño controlado | pptxgenjs (`references/pptxgenjs.md`) | pandoc `-t pptx` | contenido estructurado + plantilla corporativa → pandoc |
| Convertir **PDF** | pdftotext/pdfplumber (`references/pdf.md`) | OCR | pandoc **no lee PDF** (ver anti-patrones) |
| OCR, combinación, formularios | scripts de esta skill | — | nunca pandoc: no es su dominio |

## 2. Instalar y verificar

```bash
pandoc --version                 # primero: ¿existe y qué versión?
# Windows: winget install --exact --id JohnMacFarlane.Pandoc   (o choco install pandoc, o el MSI de pandoc.org)
# macOS:   brew install pandoc
# Linux:   apt-get install pandoc / dnf install pandoc  (¡versiones de distro a menudo anticuadas!)
pandoc --list-input-formats      # fuente canónica de formatos EN tu versión
pandoc --list-output-formats
```

Caveats de instalación (pandoc.org/installing):

- **Una sola instalación**: combinar MSI + winget/choco deja dos binarios y PATH ambiguo; desinstala antes de cambiar de método.
- **Binarios estáticos oficiales** (MSI, zip, winget, conda por defecto) **no pueden usar filtros Lua que dependan de módulos C**: si necesitas esos filtros, instala por choco/brew/conda (paquetes integrados).
- **PDF por defecto usa LaTeX**: en Windows instala MiKTeX (`choco install miktex`), en macOS BasicTeX/TinyTeX, en Linux `texlive`; o evita TeX con `--pdf-engine` (sección 5).
- Distro Linux antigua → binario oficial tarball/deb de `github.com/jgm/pandoc/releases` en vez del paquete del sistema.

## 3. Matriz de formatos

Lo que importa en ofimática (el listado completo y canónico es `--list-input-formats`/`--list-output-formats` de tu versión):

- **Entradas**: Markdown (con extensiones), CommonMark, GFM, reStructuredText, AsciiDoc, Org-mode, HTML, LaTeX, **DOCX**, ODT, RTF, EPUB, **Jupyter `.ipynb`**, MediaWiki/Jira/DokuWiki, **CSV/TSV/Excel (como tablas)**, BibTeX/BibLaTeX/CSL JSON/CSL YAML.
- **Salidas**: HTML5 (+ chunked), **DOCX**, ODT, RTF, **EPUB 2/3**, **PDF** (vía motor), **PPTX**, reveal.js/Slidy/S5 (slides web), LaTeX/Beamer, Typst, DocBook, JATS, ICML (InDesign), man/roff, Vimdoc, ANSI, **JSON del AST** (`-t json`, base de filtros y custom readers/writers en Lua).
- Pandoc infiere entrada/salida por extensión; **sé explícito con `-f` y `-t`** cuando el formato de origen pueda confundirse (`.md` puede ser pandoc-markdown, commonmark o gfm).

Flujos típicos de esta skill: `.md → docx|pdf|html|epub`, `docx → md`, `ipynb → md`, `csv/xlsx → html|docx|latex`, `md → pptx`, `md → json → (filtro) → cualquier salida`.

## 4. Sintaxis y extensiones

```bash
pandoc -f markdown -t html5 entrada.md -o salida.html
pandoc -f gfm -t commonmark entrada.md -o salida.md          # normalizar a CommonMark estricto
pandoc entrada.md -t docx --reference-doc=plantilla.docx
pandoc entrada.md -o salida.html --standalone --toc --metadata title="Informe"
pandoc entrada.md -o out.docx --wrap=preserve --extract-media=.tmp/ofimatica-ts/media
```

- **Extensiones**: se suman/restan al formato (`-f markdown+grid_tables+fancy_lists-smart`). Las útiles a conocer: `pipe_tables` y `grid_tables` (tablas; la de pandoc acepta bloques dentro de celdas), `raw_attribute` (bloques/inline raw con `` ```{=docx} `` para inyectar OOXML o `` ```{=html} ``), `fenced_code_attributes` (clases de resaltado/lenguaje), `native_divs` y `bracketed_spans` (contenedores `::: {.clase}` para estilos y citas), `footnotes`, `emoji`, `smart` (comillas/guiones tipográficos), `tex_math_dollars` (matemáticas; activo por defecto), `raw_html` (apagar con `-raw_html` si quieres markdown puro).
- **Frontmatter YAML** de la cabecera se lee como metadata automáticamente (`title`, `author`, `date`, `bibliography`…); sobreescribe con `--metadata`/`-V` (variables de plantilla).
- `--wrap=none|preserve` cuando extraes contenido: el default `auto` parte líneas y rompe código/URLs largas.
- `--shift-heading-level-by=1` para re-jerarquizar sin reescribir; un solo H1 de la skill aplica igual al generar.

## 5. PDF

```bash
pandoc entrada.md -o salida.pdf                          # default: --pdf-engine=pdflatex (¿hay TeX?)
pandoc entrada.md -o salida.pdf --pdf-engine=xelatex -V mainfont="DejaVu Sans"   # Unicode/acentos
pandoc entrada.md -o salida.pdf --pdf-engine=weasyprint   # sin TeX: HTML+CSS (pip install weasyprint)
pandoc entrada.md -o salida.pdf --pdf-engine=wkhtmltopdf   # alternativa HTML clásica
python scripts/convert.py entrada.docx salida.pdf          # último recurso garantizado: LibreOffice
```

Motores soportados: `pdflatex`, `xelatex`, `lualatex`, `latexmk`, `tectonic`, `context`, `wkhtmltopdf`, `weasyprint`, `prince`, `pagedjs-cli`, `pdfroff`.

**Árbol de decisión**: ¿está TeX? → sí: `xelatex` con `-V mainfont` si hay tildes/ñ/emojis rotos (pdflatex con fuentes 8-bit es la causa nº 1 de caracteres raros) → no: `weasyprint` (en Windows puede fallar por Pango ausente: si falla, cae a `scripts/convert.py` vía DOCX+LibreOffice, que siempre está en esta skill). Variables útiles: `-V geometry:margin=2.5cm`, `-V documentclass=report`, `--toc`, `--number-sections`, `--pdf-engine-opt=--shell-escape`.

## 6. DOCX

```bash
pandoc doc.docx -o out.md --track-changes=all            # lectura: accept | reject | all
pandoc --print-default-data-file reference.docx > base.docx   # plantilla base de pandoc para editarla
pandoc entrada.md -o salida.docx --reference-doc=base.docx    # estilos de la plantilla
pandoc entrada.md -o salida.docx --toc                      # inserta campo TOC: abrir en Word y F9
```

- `--reference-doc` hereda estilos (Título, H1-H6, tabla, código) de esa plantilla: es el puente profesional entre `.md` y plantillas corporativas.
- El writer DOCX **pierde** lo que no vive en el AST: comentarios, campos (índice, números de página), headers/footers y ajustes de página. Conserva headings, listas, tablas, código, footnotes, imágenes y estilos de carácter.
- Imágenes: al leer usa `--extract-media=<carpeta temporal de la tarea>` para que bajen a un path auditable; al escribir, rutas relativas al cwd de la ejecución.
- Roundtrip `docx → md → docx` solo para contenido; para editar el archivo existente sin pérdidas → `references/editing.md` (unpack/pack) o docx-js.

## 7. PPTX con pandoc

```bash
pandoc charla.md -o slides.pptx --slide-level=2          # H2 abre diapositiva; H3/H4 son secciones dentro
pandoc charla.md -o slides.pptx --slide-level=1 --reference-doc=corporativa.pptx
pandoc charla.md -o slides.pptx --toc                     # diapositiva de índice
```

- Cada encabezado del nivel `--slide-level` inicia diapositiva; el contenido debajo (párrafos, listas, imágenes, tablas) va dentro de ella. Notas de hablante: bloques `::: notes`.
- Con `--reference-doc` hereda fondos/fuentes de una plantilla PPTX existente.
- **Cuándo NO**: cuando pidas composición libre (formas, textos posicionados, diagramas) o QA visual pixel-perfect → pptxgenjs (`references/pptxgenjs.md`) es la herramienta de esta skill; pandoc es "contenido estructurado → slides con plantilla".

## 8. Citas y bibliografía

```bash
pandoc informe.md --citeproc --bibliography refs.bib --csl apa.csl -o informe.docx
pandoc informe.md --citeproc --bibliography refs.yaml --metadata link-citations=true -o informe.html
```

- Sintaxis de cita: `[@doe99]`, `[@doe99, pp. 33-35]`, texto prefijo `[-@doe99]`; citeproc inserta la bibliografía al final (o en el div `::: {#refs}` si quieres posicionarla).
- Datos: BibTeX (`.bib`), BibLaTeX, CSL JSON, CSL YAML (RIS y EndNote XML solo como entrada). Estilos: cientos de CSL en citationstyles.org (`--csl estilo.csl`).
- Funciona en **todos** los formatos de salida (DOCX con notas al pie o autor-año según el CSL). `--bibliography` es repetible (varios ficheros).
- Sin `--citeproc` las claves quedan literales: es la señal de que falta la flag.

## 9. Matemáticas

```bash
pandoc nota.md -o nota.html --mathml        # sin dependencia de red (recomendado)
pandoc nota.md -o nota.html --katex         # o --mathjax (requiere CDN en el navegador)
pandoc nota.md -o nota.docx                 # DOCX: ecuaciones nativas de Word (OMML)
pandoc nota.md -o nota.pdf                  # con TeX: render LaTeX nativo
```

Origen en markdown: `$...$` y `$$...$$` (extensión `tex_math_dollars`, activa por defecto en pandoc markdown; en GFM/CommonMark puro hace falta `-f gfm+tex_math_dollars`). Destino según salida: MathML/KaTeX/MathJax en HTML, OMML nativo en Word, LaTeX en PDF, y unicode aproximado si no hay motor.

## 10. Filtros y templates

```bash
pandoc entrada.md --lua-filter=resaltar.lua -t html       # filtros en orden de aparición
pandoc entrada.md --template=mi-template.html -o out.html
pandoc --print-default-data-file templates/default.html   # volcar la plantilla base para personalizarla
```

- **Lua filters** (recomendados, Lua 5.4 embebido) recorren el AST: alteran/borran elementos por tipo o atributo. Documentación de estructura: `pandoc --print-default-data-file ...` y los ejemplos oficiales de pandoc.org.
- Ojo con el caveat de la sección 2: los binarios estáticos oficiales no cargan módulos Lua en C.
- `--filter` acepta ejecutables que lean/escriban JSON del AST (Python, etc.); se aplican en el orden en que se pasan — el orden importa.
- Variables por plantilla: `-V key=value` (p. ej. `-V fontsize=11pt`, `-V colorlinks=true` en LaTeX).

## 11. Notebooks y datos

```bash
pandoc nb.ipynb -t markdown -o nb.md          # celdas → markdown; outputs según tipo
pandoc nb.md -t ipynb -o nb.ipynb             # inversa (celdas de código = bloques con lenguaje)
pandoc datos.csv -t html -o tabla.html        # CSV/TSV/Excel entran como tablas
pandoc datos.xlsx -t docx -o tabla.docx
```

En `ipynb → md` las imágenes de outputs se embeben (data URI) o se extraen con `--extract-media`; los notebooks con outputs gigantes → revisar antes de entregar.

## 12. Anti-patrones

- **Ida y vuelta `docx → md → docx` para "cambiar una frase"** → pierdes comentarios, campos y headers/footers: edita el XML (`references/editing.md`) o docx-js; pandoc solo si el contenido de verdad vive en markdown.
- **Asumir LaTeX instalado (sobre todo en Windows)** → el default de PDF falla con `pdflatex not found`: verifica con `pandoc --version` + `--pdf-engine`, o cae a `scripts/convert.py`.
- **Usar pandoc sobre un PDF** → pandoc no tiene lector de PDF: sale `Unknown input format`. Usa `pdftotext`/pdfplumber (`references/pdf.md`).
- **Dejar `--wrap` por defecto al extraer de DOCX** → el código y las URLs largas se parten en líneas: `--wrap=preserve`.
- **`--mathjax` en entorno sin red** → fórmulas sin renderizar: `--mathml`.
- **Dos pandocs instalados** → el PATH elige uno y las versiones no cuadran: desinstala antes de cambiar de método.
- **Rutas de imagen fuera de la carpeta temporal** → entregables no auditables y rotos al mover: `--extract-media` dentro de `.tmp/ofimatica-<timestamp>/`.
- **Confundir pandoc con la herramienta de fidelidad visual** → pandoc re-mapea estilos; el QA visual de Office de esta skill (convertir → imágenes → inspeccionar) sigue siendo obligatorio después de toda conversión.

## 13. Troubleshooting

| Error / síntoma | Causa | Acción |
|---|---|---|
| `pdflatex not found` / `xelatex not found` | no hay TeX | `--pdf-engine=weasyprint` o `scripts/convert.py` (sección 5) |
| `Could not find data file …` o template no encontrado | `--template`/`--reference-doc` con ruta inexistente | volcar la base: `--print-default-data-file <archivo>` |
| Imágenes ausentes en DOCX/PDF | rutas relativas al cwd | `--extract-media` y ejecutar desde la carpeta de la tarea |
| Tablas salen como texto plano | salida sin tablas o extensión apagada | `-t html`/`-t docx`, o `-f markdown+pipe_tables+grid_tables` |
| Código con líneas partidas | `--wrap=auto` (default) | `--wrap=preserve` o `none` |
| HTML crudo desaparece o citas `[@x]` literales | extensiones off / falta `--citeproc` | `+raw_html` donde haga falta; añadir `--citeproc` |
| Filtros Lua fallan con módulos C | binario estático oficial | reinstalar por choco/brew/conda (sección 2) |
| TOC del DOCX sale vacío | campo de Word sin actualizar | abrir en Word y actualizar campos (F9) |
| Tildes/ñ/emojis rotos en PDF | pdflatex con fuentes 8-bit | `--pdf-engine=xelatex -V mainfont="…"` |
| `Unknown input format X` | extensión no soportada (p. ej. `pdf`) | `pandoc --list-input-formats`; para PDF: `references/pdf.md` |
| Salida con metadatos YAML de más | frontmatter convertido en cuerpo | `--metadata`/`-V` o `-t ...-yaml_metadata_block` |
