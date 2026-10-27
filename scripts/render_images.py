#!/usr/bin/env python3
"""
Renderiza un PDF a imagenes PNG (QA visual de documentos convertidos).

Uso:
    python render_images.py <input.pdf> <output_dir> [dpi]

No requiere poppler: usa PyMuPDF (fitz) para renderizar.
"""

import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Uso: render_images.py <input.pdf> <output_dir> [dpi]", file=sys.stderr)
        sys.exit(1)
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    if not pdf_path.exists():
        print(f"ERROR: {pdf_path} no existe", file=sys.stderr)
        sys.exit(1)
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: instala PyMuPDF: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        img_path = out_dir / f"page_{i + 1}.png"
        pix.save(img_path)
        print(f"Guardada pagina {i + 1} como {img_path} ({pix.width}x{pix.height})")
    print(f"Renderizadas {len(doc)} paginas a {out_dir}")


if __name__ == "__main__":
    main()
