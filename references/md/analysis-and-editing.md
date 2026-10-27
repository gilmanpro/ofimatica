# Análisis y Edición de Archivos .md

## 1. Leer y Analizar Archivos .md

### 1.1 Extraer estructura (TOC)

```python
# Ejemplo: extraer headings de un .md
import re

def extract_headings(text):
    pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    for line in text.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2)
            headings.append({'level': level, 'title': title})
    return headings
```

### 1.2 Extraer frontmatter

```python
import yaml
import re

def extract_frontmatter(text):
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}
```

### 1.3 Extraer enlaces

Busca patrones `[texto](url)` y `[texto][ref]` + `[ref]: url`.

### 1.4 Contar palabras y estadisticas

```python
def md_stats(text):
    # Remover frontmatter
    text_no_fm = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)
    # Remover codigo
    text_no_code = re.sub(r'```.*?```', '', text_no_fm, flags=re.DOTALL)
    # Contar palabras
    words = text_no_code.split()
    # Contar headings
    headings = re.findall(r'^#{1,6}\s+', text, re.MULTILINE)
    return {
        'words': len(words),
        'headings': len(headings),
        'links': len(re.findall(r'\[([^\]]+)\]\([^)]+\)', text))
    }
```

### 1.5 Flujo de análisis recomendado

```
1. Leer el archivo .md con la herramienta read
2. Identificar frontmatter (YAML/TOML entre ---)
3. Extraer estructura de headings → TOC
4. Identificar secciones principales
5. Detectar enlaces e imágenes (para verificar que no estén rotos)
6. Verificar consistencia: jerarquía de headings, sintaxis correcta
```

## 2. Editar y Modificar Archivos .md

### 2.1 Modificaciones comunes

| Accion | Herramienta | Ejemplo |
|--------|-------------|---------|
| Renombrar seccion | `edit` | Cambiar `## Old` por `## New` |
| Agregar contenido | `edit` o `write` | Insertar nuevo parrafo |
| Reestructurar | `edit` (multiples) | Mover secciones de orden |
| Formatear codigo | `edit` | Agregar ``` alrededor de bloques |
| Actualizar enlaces | `edit` | Cambiar URLs |

### 2.2 Agregar Tabla de Contenidos

Para documentos largos, genera un TOC al inicio basado en los headings H2-H3:

```markdown
## Tabla de Contenidos

- [Seccion 1](#seccion-1)
  - [Subseccion 1.1](#subseccion-11)
- [Seccion 2](#seccion-2)
```

**Reglas:**
- Convierte headings a lowercase
- Reemplaza espacios por guiones
- Elimina caracteres especiales
- Para headings con IDs personalizados, usa el ID

### 2.3 Normalizar Sintaxis

Corrige automaticamente problemas comunes:

```python
def normalize_md(text):
    # Espacio despues de #
    text = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', text, flags=re.MULTILINE)
    # Linea en blanco antes de heading (si no es el inicio)
    text = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', text)
    # Unificar asteriscos en enfasis
    text = re.sub(r'__(.+?)__', r'**\1**', text)
    return text
```

### 2.4 Workflow de edicion

```
1. Leer el archivo completo con read (para entender contexto)
2. Identificar secciones que requieren cambios
3. Usar edit para cada cambio especifico
4. Verificar: leer el resultado final
5. Opcional: convertir a HTML para previsualizar
```
