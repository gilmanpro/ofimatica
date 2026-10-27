# Validación de datos

Restringe los valores que se pueden introducir en un rango.

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Lista desplegable
dv = DataValidation(type="list", formula1='"Alto,Medio,Bajo"', allow_blank=True)
dv.error = "Selecciona un valor válido"
dv.prompt = "Elige una prioridad"
dv.add("A1:A100")
ws.add_data_validation(dv)
```

Tipos: `whole`, `decimal`, `list`, `date`, `time`, `textLength`, `custom`.
Operadores: `between`, `notBetween`, `equal`, `notEqual`, `greaterThan`, `lessThan`, `greaterThanOrEqual`, `lessThanOrEqual`.
