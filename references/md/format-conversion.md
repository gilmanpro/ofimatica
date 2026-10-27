# Conversiones y Transformaciones de Formatos

## 1. .md → HTML (recomendado: marked o pandoc)

```bash
# Usando pandoc (si esta instalado)
pandoc input.md -o output.html --standalone --toc

# Usando marked (Node.js)
npx marked input.md -o output.html
```

## 2. .md → PDF (via pandoc + wkhtmltopdf)

```bash
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

## 3. .md → DOCX (via pandoc)

```bash
pandoc input.md -o output.docx --reference-doc=template.docx
```

## 4. DOCX → .md

```bash
pandoc input.docx -o output.md --wrap=preserve
```

## 5. .md → PDF via Node.js (sin pandoc)

```javascript
// Usando showdown + puppeteer
const showdown = require('showdown');
const converter = new showdown.Converter();
const html = converter.makeHtml(markdownContent);
// Luego renderizar HTML a PDF con puppeteer
```

## 6. Workflow de conversion

```
1. Copiar el .md a la carpeta temporal .tmp\md-<timestamp>\ del proyecto
2. Ejecutar la herramienta de conversion (pandoc, marked, etc.)
3. Validar el output (abrir, revisar)
4. Entregar al usuario
```
