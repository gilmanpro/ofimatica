#!/usr/bin/env python3
"""
Conversión bidireccional entre .docx y .pdf.

Uso:
    python convert.py <entrada.docx> <salida.pdf>   # DOCX -> PDF
    python convert.py <entrada.pdf> <salida.docx>   # PDF -> DOCX
    python convert.py <entrada> <salida> --engine word|soffice|manual

Estrategias (en orden de prioridad):
1. Word (COM)   -> maxima fidelidad de formato (Windows con MS Office)
2. LibreOffice  -> fallback en cualquier SO (soffice --headless)
3. Manual       -> SOLO pdf->docx: PyMuPDF + python-docx; OCR con tesseract
                   si el PDF no tiene capa de texto

Exit: 0 = exito, 1 = error (mensaje claro en stderr).
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXT_DOCX = {".docx", ".doc"}
EXT_PDF = {".pdf"}

SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
    "/opt/libreoffice/program/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
]


def err(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- Word (COM)

def _disable_word_pdf_prompt():
    """Evita el dialogo de confirmacion al abrir PDFs con Word (Windows)."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Office\16.0\Word\Options",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DontShowPDFConversionPrompt", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except Exception:
        pass


def _word_com():
    try:
        import win32com.client
        import pythoncom

        pythoncom.CoInitialize()
        _disable_word_pdf_prompt()
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        return word, pythoncom
    except ImportError:
        return None, None
    except Exception as e:
        err(f"No se pudo iniciar Microsoft Word via COM: {e}")


def _word_quit(word, pythoncom):
    try:
        word.Quit()
    except Exception:
        pass
    try:
        pythoncom.CoUninitialize()
    except Exception:
        pass


def docx_to_pdf_word(inp: Path, out: Path):
    word, pythoncom = _word_com()
    doc = None
    try:
        doc = word.Documents.Open(
            str(inp), ConfirmConversions=False, ReadOnly=True, AddToRecentFiles=False
        )
        doc.SaveAs2(str(out), FileFormat=17)  # wdFormatPDF
        print(f"Convertido con Word: {inp.name} -> {out.name}")
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        _word_quit(word, pythoncom)


def pdf_to_docx_word(inp: Path, out: Path):
    word, pythoncom = _word_com()
    doc = None
    try:
        # Word 2013+ abre PDFs y los reconstruye como documento editable.
        doc = word.Documents.Open(
            str(inp), ConfirmConversions=False, ReadOnly=True, AddToRecentFiles=False
        )
        doc.SaveAs2(str(out), FileFormat=16)  # wdFormatDocumentDefault (.docx)
        print(f"Convertido con Word: {inp.name} -> {out.name}")
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        _word_quit(word, pythoncom)


# ------------------------------------------------------------- LibreOffice

def find_soffice():
    found = shutil.which("soffice")
    if found:
        return found
    for candidate in SOFFICE_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def soffice_convert(inp: Path, out: Path):
    soffice = find_soffice()
    if not soffice:
        return False
    out_ext = out.suffix.lower()
    fmt = "pdf" if out_ext in EXT_PDF else "docx"
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [soffice, "--headless", "--convert-to", fmt, "--outdir", tmp, str(inp)],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            print(f"LibreOffice fallo: {result.stderr.strip() or result.stdout.strip()}", file=sys.stderr)
            return False
        produced = Path(tmp) / (inp.stem + "." + fmt)
        if not produced.exists():
            print(f"LibreOffice no genero el archivo esperado: {produced}", file=sys.stderr)
            return False
        shutil.move(str(produced), str(out))
    print(f"Convertido con LibreOffice: {inp.name} -> {out.name}")
    return True


# ---------------------------------------------------------------- Manual

def _extract_pdf_text(inp: Path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        err("PyMuPDF (fitz) no esta instalado: pip install pymupdf")
    doc = fitz.open(inp)
    pages = []
    total = 0
    for page in doc:
        blocks = [b[4] for b in page.get_text("blocks") if b[6] == 0]
        text = "\n".join(b.strip() for b in blocks if b.strip())
        pages.append(text)
        total += len(text)
    return pages, total


def _ocr_pdf(inp: Path):
    try:
        import fitz
        from PIL import Image
        import pytesseract
        import io
    except ImportError:
        err("Para OCR se necesita: pip install pymupdf pillow pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        err(
            "El PDF no tiene capa de texto y tesseract no esta instalado. "
            "Instala tesseract o usa la ruta Word (--engine word)."
        )
    doc = fitz.open(inp)
    pages = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        pages.append(text)
        print(f"OCR pagina {i + 1}/{len(doc)}: {len(text)} chars")
    return pages


def pdf_to_docx_manual(inp: Path, out: Path):
    try:
        from docx import Document
    except ImportError:
        err("python-docx no esta instalado: pip install python-docx")

    pages, total = _extract_pdf_text(inp)
    if total < 50:
        print(f"Capa de texto insuficiente ({total} chars) -> OCR")
        pages = _ocr_pdf(inp)

    document = Document()
    for i, text in enumerate(pages):
        for paragraph in text.split("\n"):
            if paragraph.strip():
                document.add_paragraph(paragraph.strip())
        if i < len(pages) - 1:
            document.add_page_break()
    document.save(out)
    print(f"Convertido (manual): {inp.name} -> {out.name} (paginas: {len(pages)})")


# ------------------------------------------------------------------ Main

def main():
    if len(sys.argv) < 3:
        err("Uso: python convert.py <entrada> <salida> [--engine word|soffice|manual]")
    inp = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    engine = None
    if "--engine" in sys.argv:
        i = sys.argv.index("--engine")
        engine = sys.argv[i + 1] if len(sys.argv) > i + 1 else None
        if engine not in ("word", "soffice", "manual"):
            err("--engine debe ser: word, soffice o manual")

    if not inp.exists():
        err(f"El archivo de entrada no existe: {inp}")
    if inp.suffix.lower() in EXT_DOCX and out.suffix.lower() in EXT_PDF:
        direction = "docx2pdf"
    elif inp.suffix.lower() in EXT_PDF and out.suffix.lower() in EXT_DOCX:
        direction = "pdf2docx"
    else:
        err(f"Combinacion no soportada: {inp.suffix} -> {out.suffix}. Usa .docx<->.pdf")

    if engine:
        engines = [engine]
    else:
        engines = ["word", "soffice", "manual"]

    for eng in engines:
        try:
            if direction == "docx2pdf":
                if eng == "word":
                    return docx_to_pdf_word(inp, out)
                if eng == "soffice":
                    if soffice_convert(inp, out):
                        return
            else:
                if eng == "word":
                    return pdf_to_docx_word(inp, out)
                if eng == "soffice":
                    if soffice_convert(inp, out):
                        return
                if eng == "manual":
                    return pdf_to_docx_manual(inp, out)
        except Exception as e:
            print(f"[{eng}] fallo: {e}", file=sys.stderr)

    err(
        "Ninguna estrategia funciono. "
        + ("Para DOCX->PDF instala LibreOffice (soffice) o usa Microsoft Word. "
           if direction == "docx2pdf" else
           "Para PDF->DOCX instala Word/LibreOffice, o pymupdf+python-docx (texto) / tesseract (OCR).")
    )


if __name__ == "__main__":
    main()
