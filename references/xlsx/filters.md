# openpyxl — Filtros y Ordenación

## Autofiltro básico

```python
from openpyxl import Workbook
from openpyxl.worksheet.filters import FilterColumn, Filters

wb = Workbook()
ws = wb.active

# Datos
for r in [["Fruit", "Quantity"], ["Kiwi", 3], ["Grape", 15],
           ["Apple", 3], ["Peach", 3], ["Mango", 7]]:
    ws.append(r)

# Configurar autofiltro
ws.auto_filter.ref = "A1:B15"

# Filtro por valores seleccionados
col = FilterColumn(colId=0)   # colId es 0-based (columna A = 0)
col.filters = Filters(filter=["Kiwi", "Apple", "Mango"])
ws.auto_filter.filterColumn.append(col)

# Ordenar por columna B descendente
ws.auto_filter.add_sort_condition("B2:B15")

# Orden ascendente
ws.auto_filter.add_sort_condition("A2:A15")
```

## Filtros avanzados

### CustomFilter
```python
from openpyxl.worksheet.filters import CustomFilter, CustomFilters

# Un filtro: valor < 10
flt = CustomFilter(operator="lessThan", val=10)
col = FilterColumn(colId=2, customFilters=CustomFilters(customFilter=[flt]))

# Dos filtros combinados: valor < 10 AND > 90
flt1 = CustomFilter(operator="lessThan", val=10)
flt2 = CustomFilter(operator="greaterThan", val=90)
cfs = CustomFilters(customFilter=[flt1, flt2], and_=True)
col = FilterColumn(colId=2, customFilters=cfs)

# Operadores disponibles: 'equal', 'lessThan', 'lessThanOrEqual',
#   'notEqual', 'greaterThanOrEqual', 'greaterThan'
```

### Wildcards en CustomFilter
Para "comienza con", "termina con", "contiene":
```python
# Comienza con 'a'
flt = CustomFilter(operator="equal", val="a*")
# Termina con 'a'
flt = CustomFilter(operator="equal", val="*a")
# Contiene 'a'
flt = CustomFilter(operator="equal", val="*a*")
# Negación: NO contiene 'a'
flt = CustomFilter(operator="notEqual", val="*a*")
# ? = un carácter cualquiera
flt = CustomFilter(operator="equal", val="c?n")
# ~ = escape para wildcards
flt = CustomFilter(operator="equal", val="~*")  # literal asterisco
```

### NumberFilter, StringFilter, BlankFilter
```python
from openpyxl.worksheet.filters import NumberFilter, StringFilter, BlankFilter

# Numérico
nf = NumberFilter(operator="lessThan", val=10)  # val es float 10.0

# String
sf = StringFilter(operator="contains", val="xml", exclude=True)  # NO contiene
# Operadores String: 'contains', 'startswith', 'endswith', 'wildcard'

# Blanco (no editable)
bf = BlankFilter()
```

### DateGroupItem (filtros por fecha)
```python
from openpyxl.worksheet.filters import DateGroupItem

# Por mes (Marzo)
df = DateGroupItem(month=3, dateTimeGrouping="month")
col = FilterColumn(colId=1)
col.filters.dateGroupItem.append(df)

# Por año
df = DateGroupItem(year=1984, dateTimeGrouping="year")
col.filters.dateGroupItem.append(df)

# dateTimeGrouping: 'year', 'month', 'day', 'hour', 'minute', 'second'
```

## Notas importantes
- openpyxl CONFIGURA filtros pero NO los ejecuta
- La filtración real ocurre al abrir el archivo en Excel
- `colId` es 0-based (A=0, B=1, C=2, ...)
- Las tablas ya vienen con filtros automáticos en los encabezados
- Se puede tener autofiltro O tablas, pero las tablas son más flexibles para múltiples rangos
