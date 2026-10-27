---
name: ofimatica
description: "Ofimatica integral: crear, editar y analizar Word .docx, PowerPoint .pptx y PDF (extraer texto y tablas, facturas, OCR, combinar, formularios, convertir entre formatos); hojas de calculo .xlsx .xlsm .csv .tsv (openpyxl, pandas, formulas, graficos, formato condicional, recalculo con LibreOffice, limpiar datos); Markdown .md (GFM, frontmatter, README, CHANGELOG, pandoc, conversion a HTML/PDF/DOCX); bovedas de Obsidian con su CLI (crear, leer, buscar notas, enlaces wiki, diarias); y CV profesional (estructura, logros cuantificables, optimizacion ATS, adaptacion a ofertas). Usar SIEMPRE que el usuario pida reportes, presentaciones, documentos descargables, exportar tablas, generar Excel desde datos, editar un .md, automatizar notas de Obsidian, o escribir, revisar u optimizar un CV, o mencione docx, pptx, pdf, xlsx, csv, openpyxl, markdown, frontmatter, pandoc, obsidian, cv, curriculum, resume o ATS, aunque no nombre la skill. NO usar para crear o editar skills ni su SKILL.md (usa skill-creator)."
license: Proprietary. LICENSE.txt has complete terms
---

# Ofimática integral — Word · PowerPoint · PDF · Excel · Markdown · Obsidian · CV

SUPER SKILL consolidada: absorbe a las antiguas skills `md`, `xlsx`, `obsidian` y `cv` (archivadas en `~/.agents/skills-archive/`). **Todo entregable de oficina es ahora una sección interna de esta skill** — ya no se "continúa con otra skill". Excepción de fronteras: para crear o editar skills y su `SKILL.md` se usa la skill `skill-creator`; los datos que van a una base de datos no son hoja de cálculo.

## Guía de dispatch — entregable → qué leer

Carga SOLO la referencia que la tarea pida (índice completo con triggers al final):

| El usuario pide... | Lee |
|---|---|
| Word: documento, informe, carta, `.docx` | `references/docx.md` |
| PowerPoint: presentación, slides, `.pptx` | `references/pptx.md` (crear desde cero: `references/pptxgenjs.md`; editar plantilla: `references/editing.md`) |
| PDF: leer/extraer/combinar/OCR/crear | `references/pdf.md` |
| PDF: formularios | `references/forms.md` |
| PDF: avanzado (pypdfium2, pdf-lib, troubleshooting) | `references/reference.md` |
| Hoja de cálculo: `.xlsx`, `.xlsm`, `.csv`, `.tsv`, fórmulas, gráficos, limpiar datos | `references/xlsx/guia-general.md` |
| openpyxl avanzado (un tema concreto: charts, estilos, filtros…) | tabla de `references/xlsx/` más abajo |
| Markdown: `.md`, README, CHANGELOG, frontmatter, sintaxis GFM, pandoc | `references/md/guia-general.md` |
| pandoc: convertir entre formatos, PDF sin LibreOffice, citas, filtros Lua, diagnóstico de conversión | `references/pandoc.md` |
| Obsidian: bóveda, notas, enlaces wiki, daily notes | `references/obsidian.md` |
| CV: currículum, resume, ATS, postulación | `references/cv/guia-general.md` |

**Combinaciones entre formatos** (flujos mixtos frecuentes):
- Tablas de un PDF → Excel: extraer con `pdfplumber` (`references/pdf.md`) y escribir con openpyxl (`references/xlsx/guia-general.md`); atajo por comando: ver Quick Reference.
- Datos → informe Word/PDF o slides: pandas/openpyxl para el análisis + `references/docx.md` / `references/pdf.md` / `references/pptx.md` para el entregable.
- CV → PDF/DOCX: flujo de redacción de `references/cv/guia-general.md` + generación del archivo final con la sección PDF/Word.
- `.md` → DOCX/PDF con plantilla: pandoc (`--reference-doc`) en `references/md/format-conversion.md`.
- Nota Obsidian ↔ `.md` suelto: mismo formato de texto; el CLI solo hace falta si la acción es sobre la bóveda viva (índices, propiedades, sync).

## Regla de Carpetas de Trabajo (OBLIGATORIA, todos los formatos)

**Trabaja SIEMPRE desde una carpeta temporal dedicada DENTRO del proyecto actual.** Nunca uses `%TEMP%`, `/tmp/` ni ninguna carpeta fuera del proyecto.

1. Crea una subcarpeta con timestamp para CADA tarea dentro de `.tmp/` en la raíz del proyecto:
   ```bash
   mkdir ".tmp\ofimatica-20260812-103000"        # Windows
   mkdir -p ".tmp/ofimatica-20260812-103000"     # Unix
   ```
2. Copia los inputs del usuario a esa carpeta. Todos los outputs intermedios (`unpacked/`, `page_1.pdf`, `merged.pdf`, `output.xlsx`, `recalc.json`, scripts temporales) van DENTRO.
3. **Por qué**: el usuario puede auditar todo lo generado (scripts, intermedios, outputs) sin salir del proyecto, las tareas paralelas no colisionan y nada se pierde en una carpeta temporal del sistema que luego se borra.
4. Entrega final: copia el output a la carpeta que indique el usuario, o muéstrale la ruta absoluta.
5. **NO borres la carpeta temporal** bajo ninguna circunstancia, ni siquiera preguntando: debe quedar intacta dentro del proyecto para revisión del usuario.
6. **Excepción Markdown**: la documentación del proyecto (README, `docs/`) se escribe en su ubicación final, no en carpeta temporal; solo las conversiones/transformationes temporales van a `.tmp/ofimatica-<timestamp>/`.

## Quick Reference

| Tarea | Comando |
|---|---|
| Leer `.docx` (texto) | `pandoc doc.docx -o out.md` (con cambios: `--track-changes=all`) |
| Leer `.pptx` (texto) | `python -m markitdown pres.pptx` |
| Miniaturas `.pptx` (visual) | `python scripts/thumbnail.py pres.pptx` |
| Leer `.pdf` (texto) | `pdftotext -layout doc.pdf -` |
| Extraer tablas de un `.pdf` (a Excel/CSV) | `pdfplumber` `page.extract_tables()` + `pandas` → ver `references/pdf.md` |
| Convertir DOCX ↔ PDF | `python scripts/convert.py entrada salida` |
| PDF → imágenes (QA) | `python scripts/render_images.py in.pdf out_dir/ [dpi]` |
| Validar `.docx` creado | `python scripts/office/validate.py doc.docx` |
| Aceptar cambios en `.docx` | `python scripts/accept_changes.py in.docx out.docx` |
| PPTX → imágenes (QA) | `soffice --headless --convert-to pdf pres.pptx && pdftoppm -jpeg -r 150 pres.pdf slide` |
| Recalcular fórmulas de `.xlsx` (OBLIGATORIO si usas fórmulas) | `python "<base-dir-skill>\scripts\recalc.py" output.xlsx 90` y verificar JSON (en Windows usa 60-90: el primer arranque de LibreOffice puede tardar) |
| Leer `.xlsx` rápido (pandas) | `python -c "import pandas as pd; print(pd.read_excel('f.xlsx').describe())"` |
| `.md` → HTML/PDF/DOCX | `pandoc input.md -o out.html --standalone` (más: `references/md/format-conversion.md`) |
| DOCX → `.md` | `pandoc input.docx -o output.md --wrap=preserve` |
| Obsidian: nota diaria / buscar | `obsidian daily:append content="- [ ] Tarea"` · `obsidian search query="texto" format=json` |

Los comandos `scripts/...` son relativos a la carpeta de la skill; ejecútalos con la **ruta absoluta** (el base dir anunciado al cargar la skill) si trabajas desde la carpeta temporal `.tmp/` del proyecto.

## Reglas innegociables por dominio

1. **Excel**: deja fórmulas en el archivo (`=SUM(...)`), NO valores hardcodeados calculados en Python. Si usaste fórmulas → `scripts/recalc.py` y cero errores de fórmula en la entrega (`#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`). Preserva el formato y convenciones de plantillas existentes; fuente profesional. Estándares de modelo financiero (colores azul/negro/verde/rojo, formatos de números): en `references/xlsx/guia-general.md`.
2. **Word/PPT**: QA visual obligatorio — generar → convertir a imágenes → inspeccionar → corregir → **reverificar**. No declares éxito sin al menos un ciclo corregir-y-verificar (para PPTX usa subagentes con ojos frescos, ver `references/pptx.md`).
3. **Markdown**: un solo H1; jerarquía sin saltos; TOC si >3 secciones; frente de documento con frontmatter. Nunca generes `SKILL.md` con esta guía (eso es `skill-creator`).
4. **Obsidian**: la app debe estar **en ejecución** para que el CLI funcione; requiere CLI habilitado en Ajustes.
5. **CV**: estructura ATS (sin gráficos, tablas ni barras de skills), logros cuantificables (acción + contexto + resultado), sin datos personales prohibidos; entrega SIEMPRE con nota final recomendando PDF con nombre `Nombre_Apellido_CV_Puesto.pdf`.

## Flujo de trabajo típico

1. Identifica el entregable → tabla de dispatch de arriba → lee la reference correspondiente (una sola).
2. Crea la carpeta temporal `.tmp/ofimatica-<timestamp>/` dentro del proyecto y copia los inputs.
3. Analiza el documento existente (pandoc / markitdown / thumbnail.py / pdfplumber / pandas) para entender plantillas, placeholders y estructura.
4. **Crear**: escribe el script (docx-js / pptxgenjs / openpyxl / pandoc) o el código Python y genera el archivo. **Editar**: desempaqueta → edita XML → empaqueta (`references/editing.md`) o modifica con openpyxl preservando estilo.
5. **QA (obligatorio)**: Word/PPT → convierte a PDF e inspecciona imágenes; Excel → `recalc.py` + JSON `status: success`; Markdown → releer y validar sintaxis/frontmatter; CV → checklist `references/cv/ats-formato.md`. Corrige y **reverifica**.
6. Entrega el output final. La carpeta temporal queda en el proyecto: no la borres.

## Índice de referencias con trigger de carga

### Base de la skill (Word/PPT/PDF)

| Archivo | Cuándo cargarlo |
|---|---|
| `references/docx.md` | Crear (docx-js) o editar Word; referencia XML |
| `references/pandoc.md` | Conversión entre formatos con pandoc: matriz, motores PDF, citas, filtros, troubleshooting |
| `references/pptx.md` | Crear presentaciones, diseño, QA visual |
| `references/pptxgenjs.md` | API completa pptxgenjs para crear PPTX desde cero |
| `references/editing.md` | Editar plantillas PPTX vía XML (unpack/pack) |
| `references/pdf.md` | Leer, extraer, crear, OCR y CLI de PDF |
| `references/forms.md` | Llenar/extraer formularios PDF |
| `references/reference.md` | PDF avanzado: pypdfium2, pdf-lib, troubleshooting |

### Hojas de cálculo — `references/xlsx/`

| Archivo | Cuándo cargarlo |
|---|---|
| `references/xlsx/guia-general.md` | SIEMPRE que el entregable sea xlsx/csv: flujos, requisitos, recetas, recálculo |
| `references/xlsx/charts.md` | Tipos de gráficos, ejes secundarios, chartsheets |
| `references/xlsx/formatting.md` | Formato condicional (reglas, data bars, icon sets) |
| `references/xlsx/optimized.md` | Modos read-only/write-only y paralelización (archivos grandes) |
| `references/xlsx/pandas.md` | Conversión DataFrame ↔ Worksheet |
| `references/xlsx/styles.md` | Colores aRGB, NamedStyle, celdas combinadas |
| `references/xlsx/filters.md` | Autofiltros, CustomFilter, ordenación |
| `references/xlsx/formulas.md` | Fórmulas de array, Tokenizer, traducción de fórmulas |
| `references/xlsx/tables.md` | Tablas de Excel formales |
| `references/xlsx/validation.md` | Validación de datos (listas desplegables, rangos) |
| `references/xlsx/images-comments.md` | Imágenes, comentarios, texto enriquecido |
| `references/xlsx/protection.md` | Protección de libro y hoja |
| `references/xlsx/print-setup.md` | Configuración de impresión |
| `references/xlsx/dates.md` | Fechas y horas |

### Markdown — `references/md/`

| Archivo | Cuándo cargarlo |
|---|---|
| `references/md/guia-general.md` | SIEMPRE que el entregable sea .md: workflows, cheatsheet, plantillas, conversiones |
| `references/md/basic-syntax.md` | Duda de sintaxis básica no cubierta por la cheatsheet |
| `references/md/extended-syntax.md` | Tablas avanzadas, footnotes, alertas GFM, heading IDs, sabores |
| `references/md/advanced-syntax.md` | KaTeX/MathJax, Mermaid, MDX |
| `references/md/frontmatter-guide.md` | Crear/editar/depurar frontmatter YAML/TOML |
| `references/md/document-templates.md` | Crear README, CHANGELOG o doc técnica desde cero |
| `references/md/analysis-and-editing.md` | Automatizar análisis, normalizar o planificar edición grande |
| `references/md/docs-as-code.md` | Organizar documentación multiarchivo (`docs/`, enlaces) |
| `references/md/format-conversion.md` | Convertir .md ↔ HTML/PDF/DOCX (pandoc, marked, showdown) |
| `references/md/markdown-hacks.md` | HTML inline: centrado, color, captions, embeds, admoniciones |

### Obsidian y CV

| Archivo | Cuándo cargarlo |
|---|---|
| `references/obsidian.md` | Cualquier operación sobre bóveda Obsidian (CLI completo) |
| `references/cv/guia-general.md` | SIEMPRE que el entregable sea un CV: flujo de 11 pasos, reglas, formato |
| `references/cv/estructura.md` | Definir el orden de secciones según perfil |
| `references/cv/formatos.md` | Elegir entre cronológico/funcional/combinado |
| `references/cv/plantilla.md` | Plantilla base para redactar el CV |
| `references/cv/redaccion.md` | Redactar perfil, logros, competencias (ejemplos) |
| `references/cv/ats-formato.md` | Optimizar keywords + checklist antes de entregar |
| `references/cv/errores-faq.md` | Errores comunes, mantenimiento y dudas |

**Regla de profundidad**: el `SKILL.md` es el único punto de entrada; no sigas cadenas de referencias dentro de referencias salvo la guia-general de tu dominio → su tabla (máximo 2 saltos y solo dentro del mismo dominio).

## Estructura de la skill

```
ofimatica/
├── SKILL.md               # este archivo (dispatch + reglas por dominio)
├── package.json           # docx-js (npm) para crear Word
├── requirements.txt       # librerías Python (docx/pptx/pdf/xlsx)
├── references/
│   ├── docx.md · pptx.md · pptxgenjs.md · editing.md        # Word/PPT
│   ├── pandoc.md                                             # contexto pandoc multi-formato
│   ├── pdf.md · forms.md · reference.md                     # PDF
│   ├── obsidian.md                                          # Obsidian CLI
│   ├── xlsx/   guia-general.md + 13 refs avanzadas de openpyxl
│   ├── md/     guia-general.md + 9 refs de sintaxis/plantillas/conversión
│   └── cv/     guia-general.md + 6 refs de redacción/ATS
├── scripts/               # Python compartido
│   ├── convert.py · render_images.py · thumbnail.py · add_slide.py
│   ├── accept_changes.py · comment.py · fill_*.py · extract_*.py · check_*.py
│   ├── recalc.py          # recálculo de fórmulas xlsx vía LibreOffice
│   └── office/            # unpack.py, pack.py, validate.py, soffice.py (entorno LibreOffice multi-OS)
├── evals/evals.json       # 8 evals: 5 xlsx + 3 cv (skill_name: ofimatica)
└── examples/              # ejemplos funcionales
```

## Dependencias

**Python** (`pip install -r requirements.txt`): pypdf, pdfplumber, pymupdf, reportlab, fpdf2, pdfminer.six, pdfquery, pytesseract, pdf2image, pillow, **pandas, openpyxl, lxml** (Excel), markitdown[pptx], pywin32 (Word COM, solo Windows).

**Node.js**: `npm install -g docx` (Word), `npm install -g pptxgenjs` (PowerPoint).

**Sistema**: LibreOffice (`soffice`) para conversión/render y **recálculo de fórmulas xlsx** (instalar en Windows: `winget install TheDocumentFoundation.LibreOffice`; `scripts/recalc.py`, `thumbnail.py`, `accept_changes.py` y `convert.py` usan `scripts/office/soffice.py` para garantizar entorno de ejecución — perfil escribible en Windows y shim AF_UNIX en sandboxes Linux); Poppler (`pdftotext`, `pdftoppm`); Tesseract (OCR); **pandoc** (lectura `.docx` y conversiones Markdown; instalar: `winget install --exact --id JohnMacFarlane.Pandoc`, verificar `pandoc --version`, contexto completo en `references/pandoc.md`); **Obsidian** con CLI habilitado (solo bóvedas Obsidian); Microsoft Word opcional (conversión de máxima fidelidad vía COM).

## Nota de seguridad (exenciones del auditor estático)

`auditar_seguridad.py` de `skill-creator` bloquea sin exenciones con 2 falsos positivos preexistentes, ambos documentación legítima y no operativa:

- `references/docx.md` (~línea 548) · OCULTO/alta: un comentario HTML de ejemplo que explica dónde van los marcadores de comentario en el XML de Word (OOXML), no una directiva oculta para el agente → eximir con `--allow "Comment markers are direct children"`.
- `references/pptxgenjs.md` (~línea 38) · GRADUAL/alta: un comentario JS que documenta una limitación de la API (el knob correcto es charSpacing; la alternativa no surte efecto), no manipulación entre conversaciones → eximir con `--allow "charSpacing, not letterSpacing"`.

Los warnings restantes (bajos/medios) son prosa de documentación: URLs de ejemplo en tablas/ejemplos de Markdown y notas de instalación pip en docs y mensajes de error de `scripts/convert.py`/`render_images.py` — aceptados sin exención (no bloquean en perfil estándar).

