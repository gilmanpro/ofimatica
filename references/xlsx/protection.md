# Protección

La protección de openpyxl evita modificaciones accidentales; no encripta datos.

```python
# Libro
wb.security.workbookPassword = "pass"
wb.security.lockStructure = True

# Hoja
ws.protection.sheet = True
ws.protection.password = "pass"
ws.protection.enable()
ws.protection.disable()
```
