# openpyxl — Referencia de Formato Condicional

## Arquitectura

El formato condicional en openpyxl usa 3 capas:
1. **Rule** — define el tipo de regla y su configuración
2. **DifferentialStyle (dxf)** — define el estilo a aplicar cuando se cumple la regla
3. **Worksheet.conditional_formatting** — colección que asocia rangos con reglas

## Convenience Functions (recomendadas)

```python
from openpyxl.formatting.rule import (
    ColorScaleRule, CellIsRule, FormulaRule,
    DataBarRule, IconSetRule
)
from openpyxl.styles import PatternFill, Font, Border
```

### ColorScaleRule
```python
# 2 colores
ColorScaleRule(
    start_type='min', start_color='AA0000',
    end_type='max', end_color='00AA00'
)

# 3 colores
ColorScaleRule(
    start_type='percentile', start_value=10, start_color='AA0000',
    mid_type='percentile', mid_value=50, mid_color='0000AA',
    end_type='percentile', end_value=90, end_color='00AA00'
)

# Tipos de referencia: 'min', 'max', 'num', 'percent', 'percentile', 'formula'
```

### CellIsRule
```python
# Menor que
CellIsRule(operator='lessThan', formula=['C$1'], stopIfTrue=True, fill=redFill)
# Entre
CellIsRule(operator='between', formula=['1','5'], fill=redFill)
# Mayor o igual que
CellIsRule(operator='greaterThanOrEqual', formula=['100'], fill=greenFill)

# Operadores: 'lessThan', 'lessThanOrEqual', 'equal', 'notEqual',
#             'greaterThanOrEqual', 'greaterThan', 'between', 'notBetween'
```

### FormulaRule
```python
# Fórmula personalizada
FormulaRule(formula=['ISBLANK(E1)'], fill=yellowFill)
FormulaRule(formula=['E1=0'], font=myFont, border=myBorder, fill=redFill)

# Resaltar filas enteras
FormulaRule(formula=['$A1="Pendiente"'], fill=orangeFill)
```

### DataBarRule
```python
DataBarRule(
    start_type='min',                     # 'min', 'max', 'num', 'percent', ...
    start_value=None,                     # valor inicial
    end_type='max',
    end_value=None,
    color="FF638EC6",                     # color de la barra
    showValue="None",                     # mostrar valor: None, "None"
    minLength=None,                       # longitud mínima
    maxLength=None                        # longitud máxima
)
```

### IconSetRule
```python
IconSetRule(
    '3TrafficLights1',                    # conjunto de iconos
    'percent',                            # tipo de valor
    [0, 33, 67],                          # valores umbral
    showValue=None,
    percent=None,
    reverse=None
)

# Conjuntos disponibles:
# 3: '3Arrows', '3ArrowsGray', '3Flags', '3TrafficLights1', '3TrafficLights2',
#    '3Signs', '3Symbols', '3Symbols2'
# 4: '4Arrows', '4ArrowsGray', '4RedToBlack', '4Rating', '4TrafficLights'
# 5: '5Arrows', '5ArrowsGray', '5Rating', '5Quarters'
```

## API Directa (más control)

### Construir con FormatObject y DifferentialStyle
```python
from openpyxl.formatting import Rule
from openpyxl.formatting.rule import FormatObject, ColorScale, IconSet, DataBar
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.styles import Color, PatternFill, Font, Border

# 1. Crear DifferentialStyle
dxf = DifferentialStyle(
    font=Font(bold=True, color="FFFFFF"),
    fill=PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid'),
    border=Border()
)

# 2. Crear Rule
rule = Rule(type='cellIs', dxf=dxf, formula=["10"])
rule.operator = 'greaterThan'

# 3. Añadir al worksheet
ws.conditional_formatting.add('A1:A10', rule)
```

### ColorScale manual
```python
first = FormatObject(type='min')
last = FormatObject(type='max')
# O: FormatObject(type='num', val=40)
colors = [Color('AA0000'), Color('00AA00')]
cs = ColorScale(cfvo=[first, last], color=colors)
rule = Rule(type='colorScale', colorScale=cs)
```

### Formatear filas enteras
```python
# La clave es usar $ antes de la columna en la fórmula
red_fill = PatternFill(bgColor="FFC7CE")
dxf = DifferentialStyle(fill=red_fill)
r = Rule(type="expression", dxf=dxf, stopIfTrue=True)
r.formula = ['$A2="Microsoft"']    # $A = columna absoluta, 2 = fila relativa
ws.conditional_formatting.add("A1:C10", r)
```

### ContainsText (resaltar celdas con texto específico)
```python
red_text = Font(color="9C0006")
red_fill = PatternFill(bgColor="FFC7CE")
dxf = DifferentialStyle(font=red_text, fill=red_fill)
rule = Rule(type="containsText", operator="containsText", text="highlight", dxf=dxf)
rule.formula = ['NOT(ISERROR(SEARCH("highlight",A1)))']
ws.conditional_formatting.add('A1:F40', rule)
```

## Notas importantes
- openpyxl NO evalúa las reglas — solo las escribe en el XML
- Las reglas se evalúan al abrir el archivo en Excel/LibreOffice
- El orden de las reglas importa (Excel procesa en orden, se detiene en stopIfTrue)
- `stopIfTrue=True` detiene la evaluación de reglas posteriores si se cumple esta
