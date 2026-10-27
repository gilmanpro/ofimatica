# PDF — Documentos PDF

Procesamiento completo: leer, extraer, crear, manipular, OCR, formularios y conversión. Regla de carpetas de trabajo y dependencias: ver `SKILL.md`.

## Conversión PDF ↔ DOCX

Usa `scripts/convert.py` para convertir en ambas direcciones. El orden de prioridad es Word (COM), LibreOffice (soffice) y, como fallback, PyMuPDF + python-docx (con OCR para PDFs escaneados).

```bash
# PDF -> DOCX editable
python scripts/convert.py documento.pdf documento.docx

# DOCX -> PDF
python scripts/convert.py documento.docx documento.pdf

# Forzar motor
python scripts/convert.py documento.pdf documento.docx --engine manual
```

## Librerías principales (resumen)

| Librería | Para qué | Instalar |
|----------|----------|----------|
| **pypdf** | Unir, dividir, rotar, metadatos, texto básico | `pip install pypdf` |
| **pdfplumber** | Texto con layout y tablas | `pip install pdfplumber` |
| **PyMuPDF (fitz)** | Extracción avanzada, imágenes, PDF→imágenes, muy rápido | `pip install pymupdf` |
| **pdfminer.six / PDFQuery** | Datos estructurados de documentos complejos | `pip install pdfminer.six pdfquery` |
| **FPDF2** | Crear PDFs ligeros: textos, imágenes, encabezados/pies | `pip install fpdf2` |
| **ReportLab** | Creación avanzada: diseños complejos, gráficos vectoriales | `pip install reportlab` |

## Lectura y manipulación

### pypdf - Basic Operations

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction (to Excel)
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
    # Variante a CSV: mismo DataFrame, sin necesitar motor Excel (openpyxl solo aplica a to_excel)
    combined_df.to_csv("extracted_tables.csv", index=False)
```

### PyMuPDF (fitz) - Extracción avanzada y rápida

```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")

# Texto por bloques (con posiciones)
for page in doc:
    blocks = [b[4] for b in page.get_text("blocks") if b[6] == 0]
    print("\n".join(b.strip() for b in blocks if b.strip()))

# Extraer imágenes
for i, page in enumerate(doc):
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha < 4:  # PNG/RGB sin canal alfa
            pix.save(f"page{i+1}_img{xref}.png")

# Páginas a imágenes (render)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(f"page_{i+1}.png")
```

### pdfminer.six / PDFQuery - Datos estructurados

PDFQuery permite seleccionar elementos con selectores tipo CSS sobre el layout del PDF:

```python
from pdfquery import PDFQuery

pdf = PDFQuery("document.pdf")
pdf.load()

# Extraer líneas de texto horizontales
lines = pdf.extract(["LTTextLineHorizontal"])
for line in lines:
    print(line.text, line.layout.x0, line.layout.y0)  # texto + coordenadas

# Seleccionar por posición: elementos en la mitad superior
top = pdf.pq("LTTextLineHorizontal:in_bbox('0, 400, 612, 792')")
print(top.text())

# Guardar/recargar árbol parseado
pdf.save_tree("tree.xml")
```

Con pdfminer.six directamente (más bajo nivel, útil para documentos complejos):

```python
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

# Texto plano
text = extract_text("document.pdf")

# Estructura: páginas → contenedores → líneas
for page_layout in extract_pages("document.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(element.get_text())
        elif isinstance(element, LTFigure):
            print("figura:", element)
```

## Creación de PDFs

### FPDF2 - Creación ligera

FPDF2 es simple y directo para documentos con texto, imágenes, encabezados y pies de página:

```python
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 10)
        self.cell(0, 10, "Mi Informe", align="C", new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)

# Texto
pdf.cell(0, 10, "Hola mundo", new_x="LMARGIN", new_y="NEXT")
pdf.multi_cell(0, 8, "Párrafo largo que se envuelve automáticamente...")

# Imagen
pdf.image("logo.png", x=10, y=20, w=40)

# Encabezados/pies personalizados con add_font para Unicode
pdf.add_font("DejaVu", "", "DejaVuSans.ttf")
pdf.set_font("DejaVu", size=10)
pdf.cell(0, 10, "Texto con acentos: á é í ó ú ñ")

pdf.output("out.pdf")
```

**Reglas fpdf2:**
- Las fuentes base (helvetica, courier, times) **no soportan Unicode** — para acentos/emojis usa `add_font()` con una TTF (ej. DejaVu)
- El orden de construcción importa: `set_font` antes de cada `cell`/`multi_cell`
- Con `new_x`/`new_y` (fpdf2 ≥ 2.7) se controla el flujo; las versiones antiguas usaban `ln=1`
- Subíndices/superíndices Unicode (₀, ²) NO existen en las fuentes base — usa `set_font_size` manual o markup donde aplique

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Datos estructurados | PDFQuery | `pdf.extract(["LTTextLineHorizontal"])` |
| Extracción rápida/imágenes | PyMuPDF | `page.get_text("blocks")`, `get_images()` |
| Create PDFs (simple) | FPDF2 | `FPDF()` + `cell`/`multi_cell` |
| Create PDFs (avanzado) | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see [forms.md](forms.md)) | See [forms.md](forms.md) |

## Next Steps

- For advanced pypdfium2 usage, see [reference.md](reference.md)
- For JavaScript libraries (pdf-lib), see [reference.md](reference.md)
- If you need to fill out a PDF form, follow the instructions in [forms.md](forms.md)
- For troubleshooting guides, see [reference.md](reference.md)
