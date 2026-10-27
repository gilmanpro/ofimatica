# openpyxl — Referencia Avanzada de Estilos

## Colores en openpyxl

### aRGB (recomendado)
```python
from openpyxl.styles import Font, Color

# Formato: AARRGGBB (Alpha, Red, Green, Blue)
font = Font(color="FF0000")              # rojo, alpha automático 00
font.color.rgb                           # '0000FF00' (00 + FF0000 = 0000FF00)

# Colores por índice (legacy)
c = Color(indexed=32)

# Colores por tema
c = Color(theme=6, tint=0.5)
```

### Colores indexados (0-63)
Los índices 0-63 corresponden a colores predefinidos. Los índices 64 y 65 son reservados (foreground/background del sistema).

### Paleta indexada completa
| Índices | Colores |
|---------|---------|
| 0-4 | #000000, #FFFFFF, #FF0000, #00FF00, #0000FF |
| 5-9 | #FFFF00, #FF00FF, #00FFFF, #000000, #FFFFFF |
| 10-14 | #FF0000, #00FF00, #0000FF, #FFFF00, #FF00FF |
| 15-19 | #00FFFF, #800000, #008000, #000080, #808000 |
| 20-24 | #800080, #008080, #C0C0C0, #808080, #9999FF |
| 25-29 | #993366, #FFFFCC, #CCFFFF, #660066, #FF8080 |
| 30-34 | #0066CC, #CCCCFF, #000080, #FF00FF, #FFFF00 |
| 35-39 | #00FFFF, #800080, #800000, #008080, #0000FF |
| 40-44 | #00CCFF, #CCFFFF, #CCFFCC, #FFFF99, #99CCFF |
| 45-49 | #FF99CC, #CC99FF, #FFCC99, #3366FF, #33CCCC |
| 50-54 | #99CC00, #FFCC00, #FF9900, #FF6600, #666699 |
| 55-59 | #969696, #003366, #339966, #003300, #333300 |
| 60-63 | #993300, #993366, #333399, #333333 |

## Named Styles avanzados

```python
from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill, Alignment

# Crear estilo completo
mi_estilo = NamedStyle(name="mi_estilo")
mi_estilo.font = Font(name='Calibri', size=12, bold=True, color='1F4E79')
mi_estilo.fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
mi_estilo.border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='medium'),
)
mi_estilo.alignment = Alignment(horizontal='center', vertical='center')
mi_estilo.number_format = '#,##0.00'

wb.add_named_style(mi_estilo)
ws['A1'].style = 'mi_estilo'
```

## Side — Estilos de borde disponibles
`border_style` puede ser: `'thin'`, `'medium'`, `'thick'`, `'dashed'`, `'dotted'`, `'double'`, `'hair'`, `'mediumDashed'`, `'dashDot'`, `'mediumDashDot'`, `'dashDotDot'`, `'mediumDashDotDot'`, `'slantDashDot'`

## PatternFill — Tipos de relleno
`fill_type` puede ser: `'solid'`, `'darkDown'`, `'darkGray'`, `'darkGrid'`, `'darkHorizontal'`, `'darkTrellis'`, `'darkUp'`, `'darkVerical'`, `'gray0625'`, `'gray125'`, `'lightDown'`, `'lightGray'`, `'lightGrid'`, `'lightHorizontal'`, `'lightTrellis'`, `'lightUp'`, `'lightVertical'`, `'mediumGray'`, `None`

## GradientFill
```python
fill = GradientFill(degree=90, stop=("FFFFFF", "4472C4"))
# degree: ángulo del degradado (0=izquierda a derecha, 90=arriba a abajo)
```

## Estilos a filas y columnas completas

```python
# Aplicar a TODA una columna (solo celdas nuevas creadas después de guardar)
col = ws.column_dimensions['A']
col.font = Font(bold=True)
col.width = 20

# Para aplicar a celdas YA EXISTENTES, hay que iterar
for row in ws.iter_rows(min_col=1, max_col=1):
    for cell in row:
        cell.font = Font(bold=True)

# Altura de fila
ws.row_dimensions[1].height = 30

# Grupos de columnas (para outline/agrupación)
ws.column_dimensions.group('A', 'D', hidden=True)
ws.row_dimensions.group(1, 10, hidden=True)
```

## Styling Merged Cells

```python
ws.merge_cells('B2:F4')
top_left = ws['B2']
top_left.value = "My Cell"
top_left.font = Font(b=True, color="FF0000")
top_left.alignment = Alignment(horizontal="center", vertical="center")
top_left.border = Border(
    top=Side(border_style="double", color="ff0000"),
    bottom=Side(border_style="double", color="ff0000"),
    left=Side(border_style="thin"),
    right=Side(border_style="thin")
)
top_left.fill = PatternFill("solid", fgColor="DDDDDD")
# El borde de la celda superior izquierda SE EXTIENDE a toda la fusión
```
