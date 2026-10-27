# Tablas en openpyxl

Crea tablas de Excel con formato y estilos integrados.

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

tab = Table(displayName="Table1", ref="A1:E5")
tab.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium9",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=True
)
ws.add_table(tab)
```

- Los nombres de tabla deben ser únicos en todo el libro.
- Accede con `ws.tables["Table1"]`, `ws.tables.items()` o elimina con `del ws.tables["Table1"]`.
