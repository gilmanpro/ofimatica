# Obsidian CLI — Gestión de bóvedas desde terminal

> Este archivo absorbe el cuerpo de la antigua skill `obsidian` (archivada el 2026-10-13 en `~/.agents/skills-archive/obsidian`). Experto en Obsidian CLI: opera bóvedas Obsidian programáticamente — crear, leer, buscar, editar notas y automatizar flujos de trabajo.

## Cuándo aplica
- Crear, leer o editar notas de Obsidian desde terminal
- Buscar en la bóveda por contenido o propiedades
- Automatizar flujos de trabajo con scripts
- Gestionar tareas diarias y plantillas

La nota Obsidian **es un archivo `.md`**: para la sintaxis Markdown profunda (frontmatter YAML, tablas, enlaces) aplica también `references/md/guia-general.md` de esta misma skill; las particularidades de Obsidian (wikilinks, `%%` comentarios, block IDs) están más abajo.

## Requisitos
- Obsidian app instalada y en ejecución
- CLI habilitado en **Ajustes → General → Comando line interface**
- CLI registrado en PATH: paso manual en Ajustes (macOS crea symlink en /usr/local/bin, requiere admin y reiniciar el terminal)

## Comandos esenciales

### Notas diarias
```bash
obsidian daily                          # Abrir nota diaria de hoy
obsidian daily:append content="- [ ] Tarea"  # Agregar contenido
obsidian tasks daily                    # Listar tareas de la nota diaria
```

### Leer y buscar
```bash
obsidian read                           # Leer archivo activo
obsidian search query="texto"           # Buscar en la bóveda
obsidian search query="status::active" format=json  # Buscar + exportar JSON
obsidian tags counts                    # Ver etiquetas con frecuencia
obsidian unresolved                     # Enlaces sin resolver
```

### Crear y editar
```bash
obsidian create name="Nota"             # Crear nota
obsidian create name="Viaje" template=Viaje  # Crear desde plantilla
obsidian diff file=README from=1 to=3   # Comparar versiones
```

### Archivos
```bash
obsidian files sort=modified limit=5    # Archivos recientes
obsidian files sort=modified limit=5 --copy  # Copiar al portapapeles
```

### Desarrollo
```bash
obsidian devtools                       # Abrir DevTools
obsidian plugin:reload my-plugin        # Recargar plugin
obsidian dev:screenshot file=shot.png   # Capturar screenshot
obsidian eval "app.vault.getFiles().length"  # Ejecutar JS
obsidian dev:errors                     # Revisar errores JS
obsidian dev:css selector=".workspace"  # Inspeccionar CSS
obsidian dev:dom selector=".nav"        # Consultar DOM
```

### Ayuda
```bash
obsidian help                           # Mostrar ayuda
obsidian                                # Abrir TUI con autocompletado
```

## Headless Sync

Ejecuta Obsidian Sync sin GUI. Ideal para servidores, CI/CD y automatizaciones.

```bash
# Sincronizar bóveda en servidor
obsidian sync vault="Mi Bóveda"

# Automatizar backups remotos (verificar flags exactos con: obsidian help sync)
obsidian sync vault="Equipo" --remote
```

## Automatización (scripts shell)

```bash
#!/bin/bash
# Rutina matutina
obsidian daily
obsidian daily:append content="- [ ] Revisar bandeja de entrada"
obsidian daily:append content="- [ ] Revisar calendario"
obsidian files sort=modified limit=5 --copy
obsidian unresolved
```

## Formato Markdown de Obsidian

Al crear/editar notas, usar sintaxis Obsidian:

```markdown
# Título
## Subtítulo

**negrita** *cursiva* `código`

- Lista
- [ ] Tarea pendiente
- [x] Tarea completada

> Cita

[[Enlace a otra nota]]
![[Imagen.png]]

#etiqueta

| Tabla | Columna |
|-------|---------|

%% Comentario oculto %%

^id-de-bloque (para enlaces a bloques)
```

(Nota: los bloques de código con sintaxis se escriben con fenced code block estándar ``` + lenguaje; aquí omitido para no anidar fences dentro de este ejemplo.)

## Buenas prácticas

- Obsidian app debe estar **en ejecución** para que el CLI funcione
- Usar `obsidian search query="status::active"` para filtrar por propiedades
- Usar `--copy` flag para copiar resultados al portapapeles
- Usar `format=json` para procesar resultados programáticamente
- Headless Sync requiere licencia de Obsidian Sync
- Para scripts complejos, combinar comandos CLI en scripts shell
- Usar TUI (`obsidian` sin argumentos) para explorar comandos con autocompletado
