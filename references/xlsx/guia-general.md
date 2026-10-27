# Hojas de cálculo (.xlsx/.xlsm/.csv/.tsv) — guía general

> Este archivo absorbe el cuerpo íntegro de la antigua skill `xlsx` (archivada el 2026-10-13 en `~/.agents/skills-archive/xlsx`; a su vez `xlsx` había absorbido a `openpyxl`). El flujo completo de hoja de cálculo vive en esta skill `ofimatica`: herramientas incluidas `scripts/recalc.py` (recálculo de fórmulas con LibreOffice) y `scripts/office/soffice.py`.

## Cuándo aplica esta guía

- Crear archivos Excel (.xlsx) con Python
- Leer y modificar libros existentes
- Aplicar estilos, fórmulas y gráficos
- Exportar datos desde pandas a Excel
- Automatizar reportes y análisis de datos
- Limpiar o reestructurar archivos de datos tabulares sucios
- Convertir entre formatos tabulares

**NO aplica si:** el entregable final es una base de datos (los datos van a SQL/NoSQL, no a una hoja). Word, PDF y presentaciones ya NO son "otra skill": son secciones de esta misma `ofimatica` (ver dispatch en `SKILL.md`).

## Regla de Carpetas de Trabajo (OBLIGATORIA)

**NUNCA crees archivos sueltos directamente en la raíz del proyecto ni fuera de él (`%TEMP%`, `AppData\Local\Temp`).** Trabaja siempre en una carpeta temporal **dentro del proyecto**, que **no se elimina** al terminar para que el usuario pueda auditar scripts e intermedios.

### 1. Crear carpeta temporal

Al inicio de CUALQUIER tarea con hojas de cálculo, crea una carpeta dedicada con timestamp dentro de `.tmp\` del proyecto actual:

```bash
# Windows (cmd)
mkdir ".tmp\ofimatica-YYYYMMDD-HHMMSS"
```
```bash
# Unix
mkdir -p ".tmp/ofimatica-YYYYMMDD-HHMMSS"
```

Todos los archivos de trabajo (inputs copiados, `output.xlsx`, `modified.xlsx`, scripts `.py` de generación, `recalc_errors.json`) van **DENTRO** de esta carpeta.

### 2. Convención de rutas

| Tipo de archivo | Ubicación |
|------------------|-----------|
| Inputs del usuario (xlsx, xls, csv originales) | Copiados a `.tmp\ofimatica-<timestamp>\` al inicio |
| Trabajo intermedio (`.xlsx` modificados, scripts `.py`, `recalc.json`) | `.tmp\ofimatica-<timestamp>\` |
| Outputs (`.xlsx` final, `.csv` limpios, gráficos) | `.tmp\ofimatica-<timestamp>\` |
| **Entrega final al usuario** | Carpeta destino que indique el usuario, o mostrarle la ruta absoluta de `.tmp\ofimatica-<timestamp>\` |

### 3. Flujo típico (crear nuevo Excel)

```bash
# 1. Crear carpeta temporal DENTRO del proyecto (no fuera, no se elimina al final)
set WORKDIR=.tmp\ofimatica-20260629-103000
mkdir "%WORKDIR%"

# 2. Generar script .py DENTRO de la carpeta temporal
# (escribir create_xlsx.py con write tool en WORKDIR)

# 3. Ejecutar y generar el archivo
cd /d "%WORKDIR%"
python create_xlsx.py

# 4. Recalcular fórmulas (MANDATORIO si usas fórmulas)
# recalc.py vive en la skill ofimatica, NO en el proyecto: usa la ruta absoluta
# (base dir de la skill anunciado al cargarla; el cwd es WORKDIR)
python "<base-dir-skill-ofimatica>\scripts\recalc.py" output.xlsx 90

# 5. Verificar errores
python "<base-dir-skill-ofimatica>\scripts\recalc.py" output.xlsx

# 6. Entrega final
copy "%WORKDIR%\output.xlsx" "%USERPROFILE%\reporte_final.xlsx"
```

### 4. Flujo típico (editar Excel existente)

```bash
# 1. Crear carpeta temporal DENTRO del proyecto
set WORKDIR=.tmp\ofimatica-20260629-103000
mkdir "%WORKDIR%"

# 2. Copiar input del usuario
copy "%USERPROFILE%\datos_originales.xlsx" "%WORKDIR%\input.xlsx"

# 3. Trabajar dentro de WORKDIR
cd /d "%WORKDIR%"
python -c "from openpyxl import load_workbook; wb=load_workbook('input.xlsx'); wb.active['A1']='Nuevo'; wb.save('output.xlsx')"

# 4. Recalcular fórmulas (ruta absoluta: recalc.py es de la skill, no del proyecto)
python "<base-dir-skill-ofimatica>\scripts\recalc.py" output.xlsx

# 5. Análisis con pandas (si aplica)
python -c "import pandas as pd; df=pd.read_excel('output.xlsx'); print(df.describe())"

# 6. Entrega final
copy "%WORKDIR%\output.xlsx" "%USERPROFILE%\datos_modificados.xlsx"
```

### 5. Limpieza

**NO borres la carpeta temporal** `.tmp\ofimatica-<timestamp>\`: debe quedar dentro del proyecto para que el usuario revise scripts, intermedios y outputs.

---

## Requisitos de las salidas

### Todos los archivos de Excel

#### Fuente profesional
- Usa una fuente consistente y profesional (p. ej., Arial, Times New Roman) en todos los entregables, salvo que el usuario indique otra cosa

#### Cero errores de fórmula
- Todo modelo Excel DEBE entregarse con CERO errores de fórmula (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

#### Preservar las plantillas existentes (al actualizar plantillas)
- Estudia y replica EXACTAMENTE el formato, estilo y convenciones existentes al modificar archivos
- Nunca impongas un formateo estandarizado sobre archivos con patrones establecidos
- Las convenciones de la plantilla existente SIEMPRE prevalecen sobre estas directrices

### Modelos financieros

#### Estándares de codificación por color
Salvo que el usuario o una plantilla existente indiquen lo contrario

**Convenciones de color estándar de la industria:**
- **Texto azul (RGB: 0,0,255)**: entradas hardcodeadas (inputs) y números que el usuario cambiará para escenarios
- **Texto negro (RGB: 0,0,0)**: TODAS las fórmulas y cálculos
- **Texto verde (RGB: 0,128,0)**: enlaces que traen valores de otras hojas dentro del mismo libro
- **Texto rojo (RGB: 255,0,0)**: enlaces externos a otros archivos
- **Fondo amarillo (RGB: 255,255,0)**: supuestos clave que requieren atención o celdas que deben actualizarse

#### Estándares de formato de números

**Reglas de formato obligatorias:**
- **Años**: formatear como cadenas de texto (p. ej., "2024" y no "2,024")
- **Moneda**: usar el formato $#,##0; SIEMPRE indicar las unidades en los encabezados (p. ej., "Revenue ($mm)")
- **Ceros**: usar el formato de número para mostrar todos los ceros como "-", incluidos los porcentajes (p. ej., "$#,##0;($#,##0);-")
- **Porcentajes**: formato por defecto 0.0% (un decimal)
- **Múltiplos**: formatear como 0.0x para múltiplos de valoración (EV/EBITDA, P/E)
- **Números negativos**: usar paréntesis (123) en lugar de signo menos -123

#### Reglas de construcción de fórmulas

**Ubicación de los supuestos:**
- Coloca TODOS los supuestos (tasas de crecimiento, márgenes, múltiplos, etc.) en celdas de supuestos separadas
- Usa referencias de celda en lugar de valores hardcodeados dentro de las fórmulas
- Ejemplo: usa =B5*(1+$B$6) en lugar de =B5*1.05

**Prevención de errores de fórmula:**
- Verifica que todas las referencias de celda sean correctas
- Revisa errores off-by-one (desfase de índices) en los rangos
- Garantiza fórmulas consistentes en todos los periodos de proyección
- Prueba con casos límite (valores cero, números negativos)
- Verifica que no haya referencias circulares no deseadas

**Requisitos de documentación de los valores hardcodeados:**
- Coméntalos con una nota o en celdas adyacentes (si es al final de la tabla). Formato: "Fuente: [Sistema/Documento], [Fecha], [Referencia concreta], [URL si aplica]"
- Ejemplos:
  - "Fuente: Company 10-K, FY2024, página 45, Revenue Note, [URL de SEC EDGAR]"
  - "Fuente: Company 10-Q, Q2 2025, Exhibit 99.1, [URL de SEC EDGAR]"
  - "Fuente: Bloomberg Terminal, 15/8/2025, AAPL US Equity"
  - "Fuente: FactSet, 20/8/2025, pantalla Consensus Estimates"

## Lectura y análisis de datos

### Análisis de datos con pandas
Para análisis de datos, visualización y operaciones básicas, usa **pandas**, que ofrece potentes capacidades de manipulación de datos:

```python
import pandas as pd

# Leer Excel
df = pd.read_excel('file.xlsx')  # Por defecto: primera hoja
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # Todas las hojas como dict

# Analizar
df.head()      # Vista previa de los datos
df.info()      # Información de las columnas
df.describe()  # Estadísticas

# Escribir Excel
df.to_excel('output.xlsx', index=False)
```

### Dependencias e instalación
```bash
pip install openpyxl
pip install pillow   # imágenes
pip install lxml     # mejor rendimiento
```
(Todas están en `requirements.txt` de la skill `ofimatica`.)

## Flujos de trabajo con archivos Excel

### CRÍTICO: usar fórmulas, no valores hardcodeados

**Usa siempre fórmulas de Excel en lugar de calcular los valores en Python y hardcodearlos.** Así garantizas que la hoja de cálculo siga siendo dinámica y actualizable.

**❌ INCORRECTO — hardcodear valores calculados:**
```python
# Mal: calcular en Python y hardcodear el resultado
total = df['Sales'].sum()
sheet['B10'] = total  # hardcodea 5000

# Mal: calcular la tasa de crecimiento en Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # hardcodea 0.15

# Mal: cálculo del promedio en Python
avg = sum(values) / len(values)
sheet['D20'] = avg  # hardcodea 42.5
```

**✅ CORRECTO — usar fórmulas de Excel:**
```python
# Bien: deja que Excel calcule la suma
sheet['B10'] = '=SUM(B2:B9)'

# Bien: tasa de crecimiento como fórmula de Excel
sheet['C5'] = '=(C4-C2)/C2'

# Bien: promedio con función de Excel
sheet['D20'] = '=AVERAGE(D2:D19)'
```

Esto aplica a TODOS los cálculos: totales, porcentajes, ratios, diferencias, etc. La hoja de cálculo debe poder recalcular cuando cambien los datos de origen.

### Flujo de trabajo común
1. **Elegir la herramienta**: pandas para datos, openpyxl para fórmulas y formato
2. **Crear/cargar**: crear un libro nuevo o cargar un archivo existente
3. **Modificar**: añadir o editar datos, fórmulas y formato
4. **Guardar**: escribir el archivo
5. **Recalcular las fórmulas (OBLIGATORIO SI USAS FÓRMULAS)**: usa `scripts/recalc.py` de la skill ofimatica (ruta absoluta — el script pertenece a la skill; el cwd es el WORKDIR del proyecto, no la carpeta de la skill)
   ```bash
   python "<base-dir-skill-ofimatica>\scripts\recalc.py" output.xlsx
   ```
6. **Verificar y corregir cualquier error**:
   - El script devuelve JSON con detalles de los errores
   - Si `status` es `errors_found`, revisa `error_summary` para ver los tipos y ubicaciones concretos de los errores
   - Corrige los errores identificados y vuelve a recalcular
   - Errores comunes que hay que corregir:
     - `#REF!`: referencias de celda inválidas
     - `#DIV/0!`: división por cero
     - `#VALUE!`: tipo de dato incorrecto en la fórmula
     - `#NAME?`: nombre de fórmula no reconocido

### Crear archivos Excel nuevos

```python
# Usando openpyxl para fórmulas y formato
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Añadir datos
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Añadir fórmula
sheet['B2'] = '=SUM(A1:A10)'

# Formato
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Ancho de columna
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editar archivos Excel existentes

```python
# Usar openpyxl para preservar fórmulas y formato
from openpyxl import load_workbook

# Cargar archivo existente
wb = load_workbook('existing.xlsx')
sheet = wb.active  # o wb['SheetName'] para una hoja concreta

# Trabajar con múltiples hojas
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modificar celdas
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insertar fila en la posición 2
sheet.delete_cols(3)  # Eliminar columna 3

# Añadir una hoja nueva
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Recetas esenciales de openpyxl desde Python

### Manipular libros, hojas y celdas
Crea o carga un `Workbook`, accede a un `Worksheet` y lee/escribe `Cell`.
```python
from openpyxl import Workbook, load_workbook
wb = Workbook()
ws = wb.active
ws['A1'] = 42
ws.cell(row=2, column=1, value="hola")
ws.append([1, 2, 3])
wb.save('output.xlsx')

# Cargar
wb = load_workbook('file.xlsx')                   # conserva fórmulas
wb = load_workbook('file.xlsx', data_only=True)   # valores cacheados
wb = load_workbook('file.xlsx', read_only=True)   # bajo consumo

# Hojas
ws = wb.create_sheet("Nueva", 0)
ws.title = "Renombrada"
del wb["Hoja1"]

# Rangos
for row in ws.iter_rows(min_row=1, max_col=3, max_row=2, values_only=True):
    print(row)
```

### Aplicar estilos básicos a celdas
Los estilos son inmutables; reasigna el objeto completo en lugar de modificar atributos.
```python
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

cell.font = Font(bold=True, color="FFFFFF")
cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
cell.alignment = Alignment(horizontal="center", wrap_text=True)
thin = Side(border_style="thin", color="000000")
cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
cell.number_format = '$#,##0.00'
```

### Escribir fórmulas en inglés con comas
openpyxl no evalúa fórmulas; Excel las calcula al abrir el archivo.
```python
ws["A1"] = "=SUM(B1:B10)"
ws["A2"] = "=IF(A1>100,\"Alto\",\"Bajo\")"

# Las funciones modernas requieren prefijo porque aún no están en la especificación OOXML base
ws["A3"] = "=_xlfn.XLOOKUP(D1, A:A, B:B)"

# Verifica soporte antes de escribir
from openpyxl.utils import FORMULAE
"SUM" in FORMULAE
```

### Receta: generar un reporte con encabezados formateados
```python
wb = Workbook(); ws = wb.active
headers = ["Producto", "Cantidad", "Total"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    cell.alignment = Alignment(horizontal="center")
ws.append(["Manzana", 10, 15.5])
ws.append(["Pera", 5, 8.25])
wb.save('reporte.xlsx')
```

### Receta: cargar datos y añadir un gráfico
```python
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference

wb = load_workbook('data.xlsx')
ws = wb.active
chart = BarChart()
chart.type = "col"
chart.title = "Ventas"
data = Reference(ws, min_col=2, min_row=1, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "E1")
wb.save('data_chart.xlsx')
```

## Recálculo de fórmulas

Los archivos Excel creados o modificados con openpyxl contienen las fórmulas como cadenas de texto, sin valores calculados. Usa el script `scripts/recalc.py` de la skill `ofimatica` (invócalo con su RUTA ABSOLUTA dentro del directorio base de la skill — el cwd es el WORKDIR del proyecto, no la carpeta de la skill):

```bash
python "<base-dir-skill-ofimatica>\scripts\recalc.py" <excel_file> [timeout_seconds]
```

Ejemplo:
```bash
python "<base-dir-skill-ofimatica>\scripts\recalc.py" output.xlsx 90
```

El script:
- Configura automáticamente la macro de LibreOffice en la primera ejecución (rutas de perfil por SO: Windows, macOS y Linux)
- Resuelve el binario `soffice`/`soffice.exe` en PATH y en las rutas de instalación estándar si no está en PATH
- Recalcula todas las fórmulas de todas las hojas
- Escanea TODAS las celdas buscando errores de Excel (#REF!, #DIV/0!, etc.)
- Devuelve JSON con ubicaciones y conteos detallados de los errores
- Funciona en Windows, Linux y macOS (en entornos sandboxed con AF_UNIX restringido lo maneja `scripts/office/soffice.py`)

> OJO en Windows nativo (verificado 2026-10-13): el recálculo por macro FUNCIONA, pero el primer arranque de LibreOffice (perfil en frío) puede tardar más de 80 s — pasa `timeout` de 60-90 s. `recalc.py` resuelve `soffice.exe` en PATH y en `C:\Program Files\LibreOffice\program`. Si aun así falla (LibreOffice no instalado, o el perfil no termina de arrancar), no lo fuerces: abre y guarda el archivo en Excel o LibreOffice de escritorio para que las fórmulas se calculen (otra opción probada: `soffice --headless --convert-to xlsx --outdir <dir> file.xlsx`, que recalcula al cargar), y si necesitas los valores en Python, validalos cargando el archivo guardado con `openpyxl` y `data_only=True`. Instalar LibreOffice: `winget install TheDocumentFoundation.LibreOffice`.

## Lista de verificación de fórmulas

Chequeos rápidos para asegurar que las fórmulas funcionan correctamente:

### Verificación esencial
- [ ] **Probar 2-3 referencias de muestra**: verifica que extraen los valores correctos antes de construir el modelo completo
- [ ] **Mapeo de columnas**: confirma que las columnas de Excel coinciden (p. ej., columna 64 = BL, no BK)
- [ ] **Desfase de filas**: ten en cuenta que las filas de Excel empiezan en 1 (fila 5 del DataFrame = fila 6 de Excel)

### Errores comunes
- [ ] **Manejo de NaN**: revisa los valores nulos con `pd.notna()`
- [ ] **Columnas muy a la derecha**: los datos FY suelen estar en columnas 50+
- [ ] **Múltiples coincidencias**: busca todas las coincidencias, no solo la primera
- [ ] **División por cero**: revisa los denominadores antes de usar `/` en fórmulas (#DIV/0!)
- [ ] **Referencias erróneas**: verifica que todas las referencias de celda apunten a las celdas previstas (#REF!)
- [ ] **Referencias entre hojas**: usa el formato correcto (Sheet1!A1) para enlazar hojas

### Estrategia de prueba de fórmulas
- [ ] **Empezar pequeño**: prueba las fórmulas en 2-3 celdas antes de aplicarlas a todo el modelo
- [ ] **Verificar dependencias**: comprueba que existan todas las celdas referenciadas en las fórmulas
- [ ] **Probar casos límite**: incluye ceros, negativos y valores muy grandes

### Interpretación de la salida de scripts/recalc.py
El script devuelve JSON con detalles de los errores:
```json
{
  "status": "success",           // o "errors_found"
  "total_errors": 0,              // número total de errores
  "total_formulas": 42,           // número de fórmulas en el archivo
  "error_summary": {              // solo presente si hay errores
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Buenas prácticas

### Selección de biblioteca
- **pandas**: lo mejor para análisis de datos, operaciones masivas y exportación simple de datos
- **openpyxl**: lo mejor para formato complejo, fórmulas y funciones propias de Excel

### Trabajar con openpyxl
- Los índices de celda empiezan en 1 (fila=1, columna=1 es la celda A1)
- Usa `data_only=True` para leer los valores calculados: `load_workbook('file.xlsx', data_only=True)`
- **Advertencia**: si abres con `data_only=True` y guardas, las fórmulas se reemplazan por valores y se pierden permanentemente
- Para archivos grandes: usa `read_only=True` para leer o `write_only=True` para escribir
- Las fórmulas se preservan pero no se evalúan: usa scripts/recalc.py para actualizar los valores

### Trabajar con pandas
- Especifica los tipos de dato para evitar problemas de inferencia: `pd.read_excel('file.xlsx', dtype={'id': str})`
- En archivos grandes, lee columnas concretas: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Maneja las fechas correctamente: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Guías de estilo de código

**IMPORTANTE**: al generar código Python para operaciones con Excel:
- Escribe código Python mínimo y conciso, sin comentarios innecesarios
- Evita nombres de variable verbosos y operaciones redundantes
- Evita sentencias print innecesarias

**Para los propios archivos de Excel**:
- Añade comentarios a las celdas con fórmulas complejas o supuestos importantes
- Documenta las fuentes de los datos hardcodeados
- Incluye notas para los cálculos clave y las secciones del modelo

## Índice de referencias avanzadas de openpyxl (con trigger de carga)

Carga el archivo SOLO cuando su trigger lo pida (rutas relativas a la carpeta de la skill `ofimatica`); documentación oficial: https://openpyxl.readthedocs.io/en/stable/

| Archivo | Contenido / cuándo cargarlo |
|---|---|
| `references/xlsx/charts.md` | Tipos de gráficos, ejes secundarios, layouts y chartsheets — al crear o ajustar gráficos |
| `references/xlsx/formatting.md` | Formato condicional con reglas y estilos diferenciales — al aplicar color-scale, data bars, icon sets |
| `references/xlsx/optimized.md` | Modos read-only y write-only, `WriteOnlyCell` y paralelización — con archivos muy grandes o exports masivos |
| `references/xlsx/pandas.md` | Conversión `DataFrame` ↔ `Worksheet` y write-only con Pandas — al exportar datos pandas a Excel |
| `references/xlsx/styles.md` | Colores aRGB/indexados, `NamedStyle` y celdas combinadas — con estilos complejos o merge |
| `references/xlsx/filters.md` | Autofiltros, `CustomFilter` y ordenación — al añadir filtros u orden a una tabla |
| `references/xlsx/formulas.md` | Fórmulas de array, `Tokenizer` y traducción de fórmulas — con arrays dinámicas o fórmulas complejas |
| `references/xlsx/tables.md` | Tablas de Excel (`Table`, estilos de banda) — al crear tablas formales |
| `references/xlsx/validation.md` | Validación de datos (listas desplegables, rangos) — al restringir entradas del usuario |
| `references/xlsx/images-comments.md` | Imágenes, comentarios y texto enriquecido — al incrustar logos o notas en celdas |
| `references/xlsx/protection.md` | Protección de libro y hoja — al bloquear celdas con contraseña |
| `references/xlsx/print-setup.md` | Configuración de impresión — cuando el entregable se imprimirá |
| `references/xlsx/dates.md` | Fechas y horas — con formatos de fecha o serial numbers |
