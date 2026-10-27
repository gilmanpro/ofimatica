# Sintaxis Extendida de Markdown — Referencia Completa

Referencia oficial: https://www.markdownguide.org/extended-syntax/

Estos elementos NO son parte del Markdown original de John Gruber, pero son soportados por la mayoría de los procesadores modernos (GitHub Flavored Markdown, CommonMark, etc.).

---

## 1. Tablas

### Sintaxis básica

Usa `---` para crear el encabezado y `|` para separar columnas:

```markdown
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
```

**Nota:** Pon pipe (`|`) al inicio y final de cada fila para compatibilidad.

### Alineación

| Marcador  | Alineación |
|-----------|------------|
| `:---`    | Izquierda  |
| `:---:`   | Centro     |
| `---:`    | Derecha    |

```markdown
| Izquierda | Centro | Derecha |
| :---      | :---:  | ---:    |
| celda     | celda  | celda   |
```

### Formato en tablas

Puedes usar: enlaces, código inline (`` ` ``, no bloques), énfasis.

No puedes usar: headings, blockquotes, listas, imágenes, líneas horizontales.

Para **saltos de línea** en celdas: `<br>`

```markdown
| Celda con salto |
|-----------------|
| Línea 1.<br><br>Línea 2. |
```

Para **listas** en celdas: HTML `<ul><li>`

```markdown
| Lista           |
|-----------------|
| <ul><li>Item</li><li>Item</li></ul> |
```

### Escaping pipe en tablas

Usa `&#124;` para mostrar `|` dentro de una celda.

---

## 2. Bloques de Código Delimitados (Fenced Code Blocks)

Usa tres backticks (`` ``` ``) o tres tildes (`~~~`) antes y después:

````markdown
```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
````

### Resaltado de sintaxis

Especifica el lenguaje después de los backticks de apertura:

````markdown
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
````

Lenguajes comunes: `javascript`, `python`, `html`, `css`, `bash`, `json`, `yaml`, `typescript`, `jsx`, `tsx`, `sql`, `go`, `rust`, `ruby`, `php`, `java`, `csharp`, `swift`, `kotlin`.

---

## 3. Notas al Pie (Footnotes)

```markdown
Aquí hay una nota al pie simple,[^1] y aquí hay una más larga.[^bignote]

[^1]: Esta es la primera nota al pie.

[^bignote]: Aquí hay una con múltiples párrafos.

    Indenta los párrafos para incluirlos en la nota.

    `{ mi código }`
```

Los identificadores pueden ser números o palabras, sin espacios. En el output, las notas se numeran secuencialmente.

---

## 4. IDs de Encabezado

### Asignar ID personalizado

```markdown
### Mi Gran Encabezado {#mi-encabezado}
```

### Enlazar a Heading ID

En el mismo documento:

```markdown
[Enlace al encabezado](#mi-encabezado)
```

Desde otro sitio web:

```markdown
[Enlace](https://ejemplo.com/pagina#mi-encabezado)
```

---

## 5. Listas de Definición

```markdown
Primer Término
: Esta es la definición del primer término.

Segundo Término
: Esta es una definición.
: Esta es otra definición del mismo término.
```

---

## 6. Tachado (Strikethrough)

```markdown
~~El mundo es plano.~~ Ahora sabemos que el mundo es redondo.
```

Output: ~~El mundo es plano.~~ Ahora sabemos que el mundo es redondo.

---

## 7. Listas de Tareas (Task Lists)

```markdown
- [x] Escribir el comunicado de prensa
- [ ] Actualizar el sitio web
- [ ] Contactar a los medios
```

---

## 8. Emojis

### Copiar y pegar

Simplemente copia un emoji de [Emojipedia](https://emojipedia.org/) y pégalo.

### Shortcodes

```markdown
¡De campamento! :tent: ¡Vuelvo pronto.

¡Qué divertido! :joy:
```

Shortcodes comunes: `:rocket:`, `:fire:`, `:memo:`, `:warning:`, `:bulb:`, `:tada:`, `:white_check_mark:`, `:x:`, `:100:`, `:sparkles:`, `:book:`, `:gear:`, `:lock:`, `:key:`, `:email:`, `:link:`, `:pushpin:`, `:clipboard:`, `:computer:`, `:cloud:`.

---

## 9. Resaltado (Highlight)

```markdown
Necesito resaltar estas ==palabras muy importantes==.
```

Alternativa HTML: `<mark>texto resaltado</mark>`

---

## 10. Subíndice

```markdown
H~2~O
```

Output: H₂O

Alternativa HTML: `H<sub>2</sub>O`

**Atención:** Algunos procesadores usan `~` para tachado, no para subíndice.

---

## 11. Superíndice

```markdown
X^2^
```

Output: X²

Alternativa HTML: `X<sup>2</sup>`

---

## 12. Enlace Automático de URLs

Muchos procesadores convierten URLs automáticamente:

```markdown
http://www.example.com
```

Output: [http://www.example.com](http://www.example.com)

### Deshabilitar enlace automático

Usa backticks para deshabilitarlo:

```markdown
`http://www.example.com`
```

---

## 13. Alertas de GitHub (GFM)

GitHub soporta **alertas** para destacar información crítica. Se muestran con colores e iconos distintivos según su tipo:

```markdown
> [!NOTE]
> Información útil que el usuario debe conocer, incluso al leer por encima.

> [!TIP]
> Consejo opcional para ayudar al usuario a tener éxito.

> [!IMPORTANT]
> Información crucial que el usuario necesita para tener éxito.

> [!WARNING]
> Contenido importante que requiere atención del usuario por posibles consecuencias negativas.

> [!CAUTION]
> Riesgos potenciales o acciones destructivas.
```

---

## 14. Referencias y Menciones de GitHub

Dentro de los entornos de GitHub (issues, pull requests, comentarios) existen atajos especiales:

### Menciones de usuarios

```markdown
@usuario
```

Notifica al usuario y lo enlaza a su perfil.

### Referencias a issues/PRs

```markdown
#123
```

Enlaza a la issue o pull request número 123 dentro del mismo repositorio.

### Referencias a otros repositorios

```markdown
propietario/repositorio#123
```

Enlaza a un issue/PR de otro repositorio.

### Referencias a commits

```markdown
SHA-del-commit
```

Referencia a un commit específico (basta con los primeros 7 caracteres).

---

## 15. Citas Abreviadas (Abbreviated Citations)

Algunos procesadores Markdown soportan una sintaxis abreviada para citas usando dos comillas dobles:

```markdown
Esto es una ""cita""
```

Representación HTML:

```html
<p>Esto es una <cite>cita</cite></p>
```

---

## 16. Sabores de Markdown (Lightweight Markup Languages)

Existen varios lenguajes de marcado ligero que son _supersets_ de Markdown. Añaden elementos como tablas, fenced code blocks, syntax highlighting, auto-linking y footnotes:

| Lenguaje | Características |
|----------|----------------|
| **CommonMark** | Estandarizado, especificación formal de Markdown básico |
| **GFM (GitHub Flavored Markdown)** | CommonMark + tablas, task lists, strikethrough, alerts, autolinks |
| **Markdown Extra** | Tablas, footnotes, abbreviation, definition lists |
| **MultiMarkdown** | Tablas, footnotes, math, metadatos, referencias cruzadas |
| **R Markdown** | Markdown + R para ciencia de datos y reportes dinámicos |
| **Pandoc Markdown** | El más completo: soporta múltiples salidas (PDF, DOCX, HTML, etc.) |

---

## 17. Tabla Resumen de Sintaxis Extendida

| Elemento | Sintaxis | Ejemplo |
|----------|----------|---------|
| Tabla | `\| Col1 \| Col2 \|` | Tablas con alineación |
| Fenced Code | ` ```lenguaje ` | Código con resaltado |
| Footnote | `[^1]` y `[^1]: texto` | Notas al pie numeradas |
| Heading ID | `### Título {#id}` | Anclas personalizadas |
| Definition List | `Término\n: def` | Glosarios |
| Strikethrough | `~~texto~~` | Texto tachado |
| Task List | `- [ ] tarea` | Checkboxes |
| Emoji | `:emoji:` | 😄 🚀 |
| Highlight | `==texto==` | Resaltado amarillo |
| Subscript | `H~2~O` | H₂O |
| Superscript | `X^2^` | X² |
| Auto Link | URL directa | Enlace automático |
| **Alertas GitHub** | `>[!NOTE/TIP/...]` | Alertas con color e ícono |
| **Menciones** | `@usuario` | Mención a usuario GitHub |
| **Ref. issues** | `#123` | Referencia a issue/PR |
| **Citas abreviadas** | `""texto""` | Cita con `<cite>` |
| **Sabores MD** | GFM, CommonMark, etc. | Supersets de Markdown |
