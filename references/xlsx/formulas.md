# openpyxl — Fórmulas y Parsing

## Escribir fórmulas

```python
# Fórmula simple
ws['A1'] = "=SUM(B1:B10)"
ws['A2'] = "=IF(A1>100, "Alto", "Bajo")"
ws['A3'] = "=VLOOKUP(D1, A:B, 2, FALSE)"

# Fórmula con referencia a otra hoja
ws['A4'] = "=SUM(Hoja2!A1:A10)"

# Fórmula 3D (varias hojas)
ws['A5'] = "=SUM(Ene:Mar!B2)"
```

## Fórmulas de Array

```python
from openpyxl.worksheet.formula import ArrayFormula

# Aplica a un RANGO pero solo visible en la celda superior izquierda
ws["E2"] = ArrayFormula("E2:E11", "=SUM(C2:C11*D2:D11)")

# ¡IMPORTANTE! La celda a la que asignas debe ser la top-left del rango
```

## Data Table Formulae

```python
# Tablas de datos (what-if analysis)
# ws.table_formulae para detectar tablas existentes
```

## Verificar nombres de función

```python
from openpyxl.utils import FORMULAE

"SUM" in FORMULAE       # True
"HEX2DEC" in FORMULAE  # True
"XLOOKUP" in FORMULAE  # False (más nueva, requiere _xlfn.)
```

## Fórmulas no estándar (_xlfn.)

Para funciones modernas de Excel no incluidas en la especificación original, prefija con `_xlfn.`:

```python
ws['A1'] = "=_xlfn.XLOOKUP(D1, A:A, B:B)"
ws['A2'] = "=_xlfn.TEXTJOIN(\", \", TRUE, A1:A10)"
```

## Traducción de fórmulas (al mover celdas)

```python
from openpyxl.formula.translate import Translator

# Traducir fórmula de una celda a otra
original = "=SUM(B2:E2)"
traducida = Translator(original, origin="F2").translate_formula("G2")
# resultado: '=SUM(C2:F2)'

# A1 references only! No soporta nombres definidos
```

## Tokenizer (Parseo de fórmulas)

```python
from openpyxl.formula import Tokenizer

tok = Tokenizer("=IF($A$1,\"then True\",MAX(DEFAULT_VAL,'Sheet 2'!B1))")

for t in tok.items:
    print(f"{t.value:20s} {t.type:10s} {t.subtype:10s}")

# .value = substring de la fórmula
# .type = LITERAL, OPERAND, FUNC, ARRAY, PAREN, SEP, OP_PRE, OP_IN, OP_POST, WSPACE
# .subtype = TEXT, NUMBER, LOGICAL, ERROR, RANGE, OPEN, CLOSE, ARG, ROW
```

### Tipos de token
| Tipo | Descripción |
|------|-------------|
| `LITERAL` | Celda sin fórmula |
| `OPERAND` | Valor en la fórmula |
| `FUNC` | Llamada a función (incluye nombre + paréntesis) |
| `ARRAY` | Literal de array `{}` |
| `PAREN` | Paréntesis de agrupación |
| `SEP` | Separador (coma=ARG, punto y coma=ROW) |
| `OP_PRE` | Operador prefijo unario (+/-) |
| `OP_IN` | Operador infijo binario (>=, <=, <>, =, >, <, *, /, +, -, ^, &) |
| `OP_POST` | Operador postfijo (%) |
| `WSPACE` | Espacio en blanco |

## Consideraciones importantes
- Usa SIEMPRE comas como separadores de argumentos (no punto y coma)
- Los nombres de función deben estar en INGLÉS
- openpyxl NO evalúa fórmulas — usa `data_only=True` al cargar para obtener valores cacheados
- Las fórmulas de array no llevan llaves `{}` en el código — Excel las añade automáticamente
