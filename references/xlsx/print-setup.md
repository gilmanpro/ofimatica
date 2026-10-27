# Configuración de impresión

```python
ws.print_options.horizontalCentered = True
ws.print_area = "A1:F10"
ws.print_title_cols = "A:B"   # repetir columnas en cada página
ws.print_title_rows = "1:1"   # repetir fila 1

ws.oddHeader.left.text = "Page &[Page] of &N"
ws.oddHeader.left.size = 14

ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0

ws.sheet_view.zoomScale = 85
ws.sheet_properties.tabColor = "1072BA"
```
