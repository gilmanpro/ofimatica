# openpyxl — Integración con Pandas

## DataFrame → Worksheet

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

df = pd.DataFrame({
    'Producto': ['A', 'B', 'C'],
    'Ventas': [100, 200, 150],
    'Mes': ['Ene', 'Feb', 'Mar']
})

wb = Workbook()
ws = wb.active

# Convertir y escribir fila por fila
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Con estilo 'Pandas' para header e índice
for cell in ws['A'] + ws[1]:
    cell.style = 'Pandas'
```

### Parámetros de dataframe_to_rows()
| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `df` | — | DataFrame de pandas |
| `index` | True | Incluir índice del DataFrame |
| `header` | True | Incluir nombres de columnas |

## Worksheet → DataFrame

```python
import pandas as pd
from openpyxl import load_workbook
from itertools import islice

wb = load_workbook('datos.xlsx')
ws = wb.active

# Caso simple (sin headers ni índices)
df = pd.DataFrame(ws.values)

# Caso con headers e índices (como los exporta Pandas)
data = ws.values
cols = next(data)[1:]                     # primera fila, omitir col1 (índice)
data = list(data)
idx = [r[0] for r in data]               # primera columna como índice
data = (islice(r, 1, None) for r in data) # omitir col1 en datos
df = pd.DataFrame(data, index=idx, columns=cols)

# Especificando columnas manualmente
headers = [cell.value for cell in ws[1]]
data_rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    data_rows.append(row)
df = pd.DataFrame(data_rows, columns=headers)
```

## Write-only mode con Pandas (recomendado para grandes volúmenes)

```python
from openpyxl import Workbook
from openpyxl.cell.cell import WriteOnlyCell
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

df = pd.read_csv('large_file.csv')  # cualquier fuente de datos

wb = Workbook(write_only=True)
ws = wb.create_sheet()

cell = WriteOnlyCell(ws)
cell.style = 'Pandas'

def format_first_row(row, cell):
    """Formatear la primera fila (headers) con estilo Pandas"""
    for c in row:
        cell.value = c
        yield cell

rows = dataframe_to_rows(df, index=False)
first_row = format_first_row(next(rows), cell)
ws.append(first_row)

for row in rows:
    row = list(row)
    cell.value = row[0]
    row[0] = cell
    ws.append(row)

wb.save("output.xlsx")
```

## Leer rangos específicos con pandas

```python
import pandas as pd
from openpyxl import load_workbook

wb = load_workbook('datos.xlsx', data_only=True)
ws = wb['Sheet1']

# Leer solo ciertas filas/columnas
data = []
for row in ws.iter_rows(min_row=2, max_row=100, min_col=1, max_col=5, values_only=True):
    data.append(row)

df = pd.DataFrame(data, columns=['A', 'B', 'C', 'D', 'E'])
```

## Consideraciones de rendimiento
- `dataframe_to_rows()` es un generador — no carga todo en memoria
- Para DataFrames enormes (>100k filas), usa write-only mode
- Si necesitas estilo en celdas individuales, usa WriteOnlyCell
- `values_only=True` al cargar evita problemas con fórmulas sin evaluar
