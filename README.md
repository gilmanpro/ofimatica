# ofimatica

Super skill **ofimatica integral** para agentes: crear, editar y analizar Word `.docx`, PowerPoint `.pptx` y PDF (texto, tablas, facturas, OCR, combinar, formularios); Excel `.xlsx`/`.csv` (openpyxl, pandas, formulas, graficos, recalculo); Markdown y pandoc; bovedas de Obsidian; y CV profesional optimizado ATS.

Skill para [OpenCode](https://opencode.ai) bajo el estandar [Agent Skills](https://agentskills.io) (compatible con `.opencode/skills/`, `.claude/skills/` y `.agents/skills/`). Documentacion y cuerpo completos en `SKILL.md`; este repo es un espejo publico de la skill.

## Instalacion

```bash
cmdc skills add gilmanpro/ofimatica -g      # Command Code
```

Manual (OpenCode u otro arnes): copia esta carpeta a `~/.agents/skills/ofimatica/` (global) o `<proyecto>/.opencode/skills/ofimatica/`.

## Contenido

- `SKILL.md` — dispatch (entregable -> que leer), reglas innegociables y QA por dominio
- `references/` — docx, pptx, pptxgenjs, pdf, forms, editing, pandoc, obsidian + guias de `md/`, `xlsx/` y `cv/`
- `scripts/` — Python de conversion, QA, recalc (LibreOffice), formularios y edicion XML
- `examples/` y `evals/` — ejemplos funcionales y evaluaciones

## Verificacion

```bash
python skill-creator/scripts/quick_validate.py ofimatica
python skill-creator/scripts/auditar_seguridad.py ofimatica
```

Issues y PRs de mejora bienvenidos.
