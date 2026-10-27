# Fechas y horas

```python
import datetime

ws["A1"] = datetime.datetime.now()    # formato automático
ws["A2"] = datetime.date(2024, 1, 15)
ws["A3"] = datetime.timedelta(hours=3, minutes=30)

wb.iso_dates = True                   # guardar en ISO 8601
wb.epoch = CALENDAR_MAC_1904          # sistema de fechas 1904
```
