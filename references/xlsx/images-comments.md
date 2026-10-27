# Imágenes, comentarios y texto enriquecido

## Imágenes

```python
from openpyxl.drawing.image import Image
ws.add_image(Image("logo.png"), "A1")  # requiere pillow
```

## Comentarios

```python
from openpyxl.comments import Comment
ws["A1"].comment = Comment("Texto del comentario", "Autor")
```

## Texto enriquecido

```python
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

red = InlineFont(color="00FF0000")
ws["A1"] = CellRichText("Normal ", TextBlock(red, "rojo"))
```
