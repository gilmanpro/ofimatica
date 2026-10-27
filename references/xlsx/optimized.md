# openpyxl — Modos Optimizados

## Read-Only Mode

Para abrir archivos enormes sin consumir mucha memoria:

```python
from openpyxl import load_workbook

wb = load_workbook(filename='large_file.xlsx', read_only=True)
ws = wb['big_data']

for row in ws.rows:
    for cell in row:
        print(cell.value)

wb.close()  # ¡OBLIGATORIO!
```

### Limitaciones
- Las celdas son `ReadOnlyCell` (no tienen todas las propiedades de Cell)
- `ws.iter_cols()` NO disponible
- `ws.columns` NO disponible
- Charts, imágenes, comentarios NO disponibles
- Solo lectura — no se puede modificar

### Dimensiones incorrectas
Si `ws.calculate_dimension()` devuelve A1:A1 (incorrecto):
```python
ws.reset_dimensions()
# Luego ws.max_row y ws.max_column se actualizan
```

### Paralelización
```python
from multiprocessing import Pool
from openpyxl import load_workbook

def process_sheet(sheet_name):
    wb = load_workbook('big.xlsx', read_only=True)
    ws = wb[sheet_name]
    result = 0
    for row in ws.rows:
        for cell in row:
            if cell.value and isinstance(cell.value, (int, float)):
                result += cell.value
    wb.close()
    return result

with Pool(4) as p:
    results = p.map(process_sheet, ['Sheet1', 'Sheet2', 'Sheet3'])
```

## Write-Only Mode

Para escribir archivos enormes:

```python
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.comments import Comment
from openpyxl.styles import Font

wb = Workbook(write_only=True)
ws = wb.create_sheet()  # ¡OBLIGATORIO! No hay hoja por defecto

# Sin estilo
for i in range(100000):
    ws.append([i, i*2, f"fila_{i}"])

# Con estilo
cell = WriteOnlyCell(ws, value="formateado")
cell.font = Font(name='Courier', size=36)
cell.comment = Comment(text="Comentario", author="Autor")
ws.append([cell, 3.14, None])

wb.save('enorme.xlsx')
```

### Reglas estrictas de Write-Only
1. **Solo `ws.append()`** — ni `cell()`, ni `iter_rows()`, ni acceso directo `ws['A1']`
2. **Solo se guarda UNA VEZ** — segundo `wb.save()` lanza `WorkbookAlreadySaved`
3. **Configuración ANTES de datos** — `freeze_panes`, `page_setup`, etc. deben ir antes del primer `append()`
4. **No hay hoja por defecto** — debes crear una con `wb.create_sheet()`
5. **Consumo de memoria < 10MB** incluso con millones de filas
6. **Rendimiento óptimo con lxml** instalado

### WriteOnlyCell avanzado
```python
cell = WriteOnlyCell(ws, value="texto")
cell.font = Font(bold=True, size=14)
cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
cell.border = Border(...)
cell.alignment = Alignment(horizontal="center")
cell.number_format = '#,##0.00'
cell.comment = Comment("nota", "autor")
```

### Write-Only + Tablas
```python
from openpyxl.worksheet.table import Table

# Opción 1: tabla sin encabezados
table = Table(displayName="Table1", ref="A1:C1001")
table.headerRowCount = False

# Opción 2: encabezados manuales
headings = ["Fruit", "2011", "2012"]
table._initialise_columns()
for column, value in zip(table.tableColumns, headings):
    column.name = value

ws.add_table(table)
```

### Recomendaciones de uso
| Escenario | Modo |
|-----------|------|
| < 10,000 filas, necesita estilo completo | Normal |
| 10,000 - 100,000 filas | Normal (con lxml) |
| > 100,000 filas | Write-Only |
| Archivo > 50MB para leer | Read-Only |
| Lectura+escritura de archivos grandes | Read-Only para leer, procesar en stream, Write-Only para escribir |
