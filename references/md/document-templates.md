# Plantillas para Crear Archivos .md

## 1. README.md (estándar de GitHub)

Estructura recomendada para README de proyectos:

```markdown
# Nombre del Proyecto

> Breve descripcion de una linea.

## 🚀 Instalacion

```bash
comando de instalacion
```

## 📖 Uso

Ejemplo basico de uso.

## 🏗️ Estructura del Proyecto

```
src/
├── componente/
│   ├── index.js
│   └── styles.css
└── utils/
    └── helpers.js
```

## 🤝 Contribuir

Guia de contribucion.

## 📄 Licencia

MIT
```

## 2. Plantilla para Documentación Técnica

```markdown
---
title: Nombre del Documento
author: Autor
date: YYYY-MM-DD
status: draft|review|published
tags: [tag1, tag2]
version: 1.0.0
---

# Titulo del Documento

## Tabla de Contenidos

- [Introduccion](#introduccion)
- [Requisitos](#requisitos)
- [Instalacion](#instalacion)
- [Configuracion](#configuracion)
- [Uso](#uso)
- [API](#api)
- [Solucion de Problemas](#solucion-de-problemas)
- [Referencias](#referencias)

## Introduccion

## Requisitos

## Instalacion

## Configuracion

## Uso

## API

### endpoint()

## Solucion de Problemas

## Referencias
```

## 3. Plantilla CHANGELOG.md

```markdown
# Changelog

## [1.1.0] - YYYY-MM-DD

### Added
- Nueva funcionalidad X

### Changed
- Mejora en Y

### Fixed
- Correccion de bug en Z

## [1.0.0] - YYYY-MM-DD

### Added
- Lanzamiento inicial
```

## 4. Buenas prácticas al crear .md

1. **Un solo H1 por documento** — el titulo principal
2. **Jerarquia consistente** — no saltes niveles de heading
3. **Lineas en blanco** — alrededor de headings, listas, code blocks
4. **Maximo 80-120 caracteres por linea** — legibilidad en editores de texto
5. **Tabla de contenidos** — para documentos de mas de 3 secciones
6. **Frontmatter** — siempre incluir metadatos en documentos formales
7. **Enlaces estilo referencia** — para documentos largos, centraliza las URLs
8. **Código inline vs bloques** — usa `` ` `` para comandos cortos, `` ``` `` para bloques
