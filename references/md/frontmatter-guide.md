# Frontmatter para Archivos .md — Guía Completa

---

## ¿Qué es Frontmatter?

El frontmatter es un bloque de metadatos al inicio de un archivo Markdown, delimitado por `---` (YAML) o `+++` (TOML). Se utiliza para definir propiedades del documento como título, autor, fecha, tags, etc.

Es ampliamente usado por:
- **Static Site Generators** (Jekyll, Hugo, Eleventy, Next.js)
- **Documentation tools** (MkDocs, Docusaurus, VitePress)
- **Note-taking apps** (Obsidian, Bear)
- **GitHub Pages**

---

## Formato YAML (Recomendado)

Usa `---` como delimitadores. Es el formato más común y compatible.

```yaml
---
title: "Título del Documento"
description: "Breve descripción que aparece en buscadores y redes sociales"
author: "Nombre del Autor"
date: 2026-06-29
lastmod: 2026-06-30
version: 1.0.0
status: draft
tags:
  - markdown
  - documentacion
  - frontmatter
categories: [Guía, Tutorial]
draft: false
---
```

### Tipos de datos en YAML

```yaml
# String (comillas opcionales si no tiene caracteres especiales)
title: Mi Título
title: "Mi Título: con dos puntos"

# Número
year: 2026
version: 1.5

# Booleano
draft: false
published: true

# Lista (dos formatos)
tags: [tag1, tag2, tag3]
tags:
  - tag1
  - tag2
  - tag3

# Objeto/Mapa
author:
  name: Juan Pérez
  email: juan@ejemplo.com
  url: https://ejemplo.com

# Fecha
date: 2026-06-29
date: 2026-06-29T14:30:00Z
```

---

## Formato TOML (Alternativa)

Usa `+++` como delimitadores. Es menos común pero más estricto que YAML.

```toml
+++
title = "Título del Documento"
description = "Breve descripción"
author = "Nombre del Autor"
date = 2026-06-29
version = "1.0.0"
tags = ["markdown", "documentacion"]
draft = false
+++
```

---

## Campos Comunes por Framework

### Jekyll / GitHub Pages

```yaml
---
layout: post
title: "Mi Post"
date: 2026-06-29
categories: [tutorial, web]
tags: [markdown, jekyll]
permalink: /mi-post/
published: true
author: Juan
---
```

### Hugo

```yaml
---
title: "Mi Artículo"
date: 2026-06-29
draft: true
tags: ["hugo", "markdown"]
categories: ["Tutorial"]
weight: 10
aliases: ["/posts/mi-articulo"]
slug: mi-articulo
---
```

### Obsidian

```yaml
---
tags: [nota, diario]
created: 2026-06-29
modified: 2026-06-30
aliases: [NotaAntigua]
cssclass: my-custom-class
---
```

### MkDocs

```yaml
---
title: Mi Página
description: Descripción para SEO
hide:
  - navigation
  - toc
---
```

### Next.js / MDX

```yaml
---
title: "Mi Página"
description: "Descripción"
publishedAt: 2026-06-29
author:
  name: Juan Pérez
  avatar: /assets/avatars/juan.jpg
---
```

---

## Campos Recomendados (Estandarizados)

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `title` | string | Sí | Título del documento |
| `description` | string | Recomendado | Resumen para SEO y previsualización |
| `date` | date | Recomendado | Fecha de creación |
| `author` | string/object | Opcional | Autor del documento |
| `version` | string | Opcional | Version semantica |
| `status` | string | Opcional | `draft`, `review`, `published` |
| `language` | string | Opcional | Idioma del documento (p. ej. `es`) |
| `tags` | list | Opcional | Palabras clave |
| `draft` | boolean | Opcional | Si `true`, no publicar |
| `slug` | string | Opcional | URL personalizada |
| `aliases` | list | Opcional | URLs alternativas/redirecciones |

---

## Manipulación de Frontmatter

### Extraer frontmatter con Python

```python
import yaml
import re

def extract_frontmatter(text):
    """Extrae el frontmatter YAML de un archivo .md."""
    match = re.match(r'^---\s*\n(.*?)\n(?:---|\.\.\.)', text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}
```

### Extraer frontmatter con JavaScript/Node.js

```javascript
function extractFrontmatter(markdown) {
  const match = markdown.match(/^---\n([\s\S]*?)\n---/);
  if (match) {
    // Para YAML simple, usa gray-matter o js-yaml
    return require('gray-matter')(markdown).data;
  }
  return {};
}
```

### Actualizar frontmatter

```python
import yaml, re

def update_frontmatter(text, updates):
    """Actualiza o agrega campos al frontmatter."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    
    if match:
        # Frontmatter existente — actualizar
        fm = yaml.safe_load(match.group(1))
        fm.update(updates)
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
        return text.replace(match.group(0), f'---\n{new_fm}\n---')
    else:
        # Sin frontmatter — crear nuevo
        fm_str = yaml.dump(updates, default_flow_style=False, allow_unicode=True).strip()
        return f'---\n{fm_str}\n---\n\n{text}'
```

### Validar frontmatter

```python
def validate_frontmatter(text, required_fields=['title']):
    """Valida que el frontmatter tenga los campos requeridos."""
    fm = extract_frontmatter(text)
    missing = [f for f in required_fields if f not in fm]
    if missing:
        raise ValueError(f"Campos requeridos faltantes: {missing}")
    return fm
```

---

## Buenas Prácticas

1. **Siempre incluye `title`** — es el campo mínimo requerido por casi todos los procesadores
2. **Usa YAML** — es el formato más compatible (evita TOML a menos que el framework lo requiera)
3. **Comillas en strings con caracteres especiales** — si el título tiene `:`, `#`, `{`, usa comillas
4. **Fechas en ISO 8601** — `YYYY-MM-DD` es el formato más portable
5. **No dupliques información** — el título en frontmatter y el H1 no deben contradecirse
6. **Tags consistentes** — usa siempre minúsculas o siempre el mismo estilo (`tecnologia`, no `Tecnologia` y `TECNOLOGIA`)

---

## Errores Comunes

❌ **YAML mal indentado** — los listados deben tener indentación consistente
```yaml
# Incorrecto
tags:
- tag1
 - tag2

# Correcto
tags:
  - tag1
  - tag2
```

❌ **Falta espacio después de `:`**
```yaml
# Incorrecto
title:Mi Título

# Correcto
title: Mi Título
```

❌ **Líneas en blanco dentro del frontmatter** — rompen el parseo

❌ **Tabulaciones en YAML** — usa espacios (2 espacios por nivel de indentación)
