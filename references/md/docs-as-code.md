# Organización de Documentación (Docs-as-Code)

## 1. Estructura recomendada

```
docs/
├── README.md                    # Indice de documentacion
├── getting-started/
│   ├── index.md
│   ├── installation.md
│   └── quickstart.md
├── guides/
│   ├── advanced-config.md
│   └── deployment.md
├── api/
│   ├── overview.md
│   ├── auth.md
│   └── endpoints/
│       ├── users.md
│       └── posts.md
├── tutorials/
│   └── beginner-guide.md
└── assets/
    ├── images/
    └── diagrams/
```

## 2. Convenciones de nombres

| Estilo | Ejemplo | Uso |
|--------|---------|-----|
| `kebab-case` | `getting-started.md` | **RECOMENDADO** para archivos |
| `snake_case` | `advanced_config.md` | Alternativo |
| `index.md` | `index.md` | Para pagina principal de carpeta |

## 3. Enlaces entre documentos

```markdown
[Enlace relativo](../guides/advanced-config.md)
[Enlace absoluto](/docs/api/overview.md)
[Enlace a seccion](../guides/advanced-config.md#configuracion)
```

**Reglas:**
- Usa rutas relativas SIEMPRE (portabilidad entre entornos)
- Un solo `#` en el proyecto = raiz del sitio/documentacion
- Para GitHub, usa extension `.md` en los enlaces
