# openpyxl — Referencia Completa de Charts

## Tipos de Chart

| Tipo | Clase | Módulo |
|------|-------|--------|
| Barra | `BarChart` | `openpyxl.chart.bar_chart` |
| Área | `AreaChart` | `openpyxl.chart.area_chart` |
| Línea | `LineChart` | `openpyxl.chart.line_chart` |
| Dispersión | `ScatterChart` | `openpyxl.chart.scatter_chart` |
| Circular | `PieChart` | `openpyxl.chart.pie_chart` |
| Rosquilla | `DoughnutChart` | `openpyxl.chart.doughnut_chart` |
| Burbuja | `BubbleChart` | `openpyxl.chart.bubble_chart` |
| Radar | `RadarChart` | `openpyxl.chart.radar_chart` |
| Acciones | `StockChart` | `openpyxl.chart.stock_chart` |
| Superficie | `SurfaceChart` | `openpyxl.chart.surface_chart` |

## BarChart (Barras y Columnas)

```python
from openpyxl.chart import BarChart, Reference, Series

chart = BarChart()
chart.type = "col"          # "col" = vertical, "bar" = horizontal
chart.grouping = "stacked"  # "clustered" (default), "stacked", "percentStacked"
chart.title = "Título"
chart.y_axis.title = 'Eje Y'
chart.x_axis.title = 'Eje X'
chart.legend = None         # ocultar leyenda

# Añadir datos
data = Reference(ws, min_col=2, min_row=1, max_row=5, max_col=3)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

# Serie individual
from openpyxl.chart.series import DataPoint
s = Series(values=Reference(ws, min_col=2, min_row=2, max_row=5))
s.title = "Serie 1"
chart.series.append(s)
```

### 3D BarChart
```python
from openpyxl.chart import BarChart3D
chart = BarChart3D()
chart.type = "col"
chart.grouping = "stacked"
chart.title = "3D Bar Chart"
```

## LineChart

```python
from openpyxl.chart import LineChart

chart = LineChart()
chart.title = "Evolución"
chart.style = 10
chart.y_axis.title = 'Valor'
chart.x_axis.title = 'Tiempo'

data = Reference(ws, min_col=2, min_row=1, max_row=10, max_col=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

# Línea 3D
from openpyxl.chart import LineChart3D
chart3d = LineChart3D()
```

## PieChart

```python
from openpyxl.chart import PieChart, PieChart3D, ProjectedPieChart

chart = PieChart()
chart.title = "Distribución"
chart.style = 10

data = Reference(ws, min_col=2, min_row=1, max_row=6)
cats = Reference(ws, min_col=1, min_row=2, max_row=6)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

# Colores personalizados para cada segmento
from openpyxl.chart.series import DataPoint
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice
from copy import copy

colors = ["4472C4", "ED7D31", "A5A5A5", "FFC000", "5B9BD5"]
for i, color in enumerate(colors):
    pt = DataPoint(idx=i)
    pt.graphicalProperties.solidFill = color
    chart.series[0].data_points.append(pt)

# Pie 3D
chart3d = PieChart3D()

# Pie Proyectado
proj = ProjectedPieChart()
```

## ScatterChart

```python
from openpyxl.chart import ScatterChart

chart = ScatterChart()
chart.title = "Correlación"
chart.style = 13
chart.y_axis.title = 'Y'
chart.x_axis.title = 'X'

xvalues = Reference(ws, min_col=1, min_row=2, max_row=10)
values = Reference(ws, min_col=2, min_row=2, max_row=10)
series = Series(values, xvalues, title="Datos")
chart.series.append(series)
```

## DoughnutChart

```python
from openpyxl.chart import DoughnutChart

chart = DoughnutChart()
chart.title = "Donut"
data = Reference(ws, min_col=2, min_row=1, max_row=6)
cats = Reference(ws, min_col=1, min_row=2, max_row=6)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
```

## BubbleChart

```python
from openpyxl.chart import BubbleChart

chart = BubbleChart()
chart.style = 10

# Necesita 3 columnas: X, Y, Tamaño
xvalues = Reference(ws, min_col=1, min_row=2, max_row=10)
values = Reference(ws, min_col=2, min_row=2, max_row=10)
size = Reference(ws, min_col=3, min_row=2, max_row=10)
series = Series(values=values, xvalues=xvalues, zvalues=size, title="Burbujas")
chart.series.append(series)
```

## RadarChart

```python
from openpyxl.chart import RadarChart

chart = RadarChart()
chart.type = "filled"  # "standard", "filled", "marker"
data = Reference(ws, min_col=2, min_row=1, max_row=10, max_col=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
```

## StockChart (Gráfico de Acciones)

```python
from openpyxl.chart import StockChart

chart = StockChart()
chart.title = "Alta-Baja-Cierre"
# Requiere datos en orden: Fecha, Alta, Baja, Cierre
```

## Ejes Avanzados

```python
# Escala del eje
chart.y_axis.scaling.min = 0
chart.y_axis.scaling.max = 100
chart.y_axis.scaling.logBase = 10

# Orientación
chart.x_axis.orientation = "maxMin"  # invertir eje

# Eliminar ejes
chart.y_axis.delete = False

# Segundo eje (combinar charts)
from openpyxl.chart import BarChart
chart2 = BarChart()
chart2.y_axis.axId = 200  # segundo eje
chart.y_axis.crosses = "max"
chart += chart2  # combinar
```

## Layout y Posición

```python
# Layout manual del área de trazado
from openpyxl.chart.layout import Layout, ManualLayout

chart.plot_area.layout = Layout(
    manualLayout=ManualLayout(
        x=0.1, y=0.1,     # posición relativa (0-1)
        w=0.7, h=0.7       # tamaño relativo (0-1)
    )
)

# Posicionamiento de la leyenda
chart.legend.position = 'r'  # 'r' (right), 'l' (left), 't' (top), 'b' (bottom)
chart.legend.overlay = False  # superponer sobre el gráfico

# Tamaño del chart (en cm)
chart.width = 20
chart.height = 12

# Ancla (celda donde se posiciona)
chart.anchor = "E1"
ws.add_chart(chart, "E1")
```

## Formato Gráfico Avanzado

```python
# Fondo transparente
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.shapes import GraphicalProperties

# Quitar borde del chart
chart.graphicalProperties = GraphicalProperties()
chart.graphicalProperties.line = None

# Fondo del área de trazado
from openpyxl.chart.plotarea import PlotArea
chart.plot_area.graphicalProperties = GraphicalProperties(solidFill="F2F2F2")

# Colores de serie personalizados
for s in chart.series:
    s.graphicalProperties.solidFill = "4472C4"
    s.graphicalProperties.line.solidFill = "4472C4"
```

## Chartsheets (Hoja de chart dedicada)

```python
from openpyxl.chart.chartsheet import Chartsheet

# Crear chartsheet (no es una worksheet normal)
cs = wb.create_chartsheet()
cs.title = "Dashboard"

# Añadir chart
cs.add_chart(chart)
```

## Combinar Charts

```python
# Bar + Line en el mismo gráfico
from openpyxl.chart import BarChart, LineChart

chart1 = BarChart()
chart1.title = "Ventas vs Proyección"
data1 = Reference(ws, min_col=2, min_row=1, max_row=12)
cats = Reference(ws, min_col=1, min_row=2, max_row=12)
chart1.add_data(data1, titles_from_data=True)
chart1.set_categories(cats)

chart2 = LineChart()
data2 = Reference(ws, min_col=3, min_row=1, max_row=12)
chart2.add_data(data2, titles_from_data=True)
chart2.y_axis.axId = 200

chart1 += chart2  # superponer
```

## Guía de colores comunes para charts

| Color | Hex | Descripción |
|-------|-----|-------------|
| Azul oscuro | 4472C4 | Primary Excel |
| Naranja | ED7D31 | Accent |
| Gris | A5A5A5 | Neutro |
| Amarillo | FFC000 | Warn |
| Azul claro | 5B9BD5 | Secundario |
| Verde | 70AD47 | OK |
| Rojo | FF0000 | Alerta |
| Blanco | FFFFFF | Fondo |
