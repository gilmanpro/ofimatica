# Sintaxis Básica de Markdown — Referencia Completa

Referencia oficial: https://www.markdownguide.org/basic-syntax/

---

## 1. Encabezados (Headings)

Para crear un encabezado, agrega `#` delante de una palabra o frase. La cantidad de `#` indica el nivel.

```
# H1 — Título principal
## H2 — Sección
### H3 — Subsección
#### H4
##### H5
###### H6
```

### Sintaxis alternativa

En la línea debajo del texto, usa `==` para H1 y `--` para H2:

```
Heading level 1
===============

Heading level 2
---------------
```

### Mejores prácticas

✅ **Correcto:** `# Aquí hay un encabezado`
❌ **Incorrecto:** `#Aquí hay un encabezado` (sin espacio)

Siempre pon una línea en blanco antes y después de los encabezados.

Respeta la jerarquía: no saltes de H2 a H4 sin H3 intermedio.

---

## 2. Párrafos

Separa párrafos con una línea en blanco.

```markdown
Este es el primer párrafo. Tiene varias líneas de texto.

Este es el segundo párrafo. Separado del anterior por una línea en blanco.
```

**No sangres los párrafos** con espacios o tabs (a menos que estén dentro de una lista).

---

## 3. Saltos de Línea

Para un salto de línea (`<br>`), termina una línea con **dos o más espacios** y luego Enter:

```markdown
Esta es la primera línea.··
Y esta es la segunda línea.
```

Alternativa HTML: `<br>`

No recomendado: usar `\` al final de la línea (no todos los procesadores lo soportan).

---

## 4. Énfasis

### Negrita

```markdown
**texto en negrita**
__texto en negrita__
Love**is**bold  (en medio de una palabra)
```

Mejores prácticas: usa asteriscos `**` para compatibilidad en medio de palabras.

### Cursiva

```markdown
*texto en cursiva*
_texto en cursiva_
A*cat*meow  (en medio de una palabra)
```

Mejores prácticas: usa asteriscos `*` para compatibilidad en medio de palabras.

### Negrita y Cursiva

```markdown
***texto en negrita y cursiva***
___texto en negrita y cursiva___
__*texto*__
**_texto_**
```

---

## 5. Blockquotes (Citas)

```markdown
> Dorothy siguió su camino por muchas de las hermosas habitaciones del castillo.
```

### Blockquotes con múltiples párrafos

```markdown
> Dorothy siguió su camino.
>
> La bruja le ordenó limpiar los pisos.
```

### Blockquotes anidados

```markdown
> Cita principal
>
>> Cita anidada
```

### Blockquotes con otros elementos

```markdown
> #### El título
>
> - Elemento de lista
> - Otro elemento
>
> *Cursiva* y **negrita** dentro del blockquote
```

---

## 6. Listas

### Listas ordenadas

```markdown
1. Primer item
2. Segundo item
3. Tercer item
   1. Subitem indentado
   2. Otro subitem
4. Cuarto item
```

Los números no tienen que estar en orden (1, 1, 1 funciona), pero la lista debe empezar con 1.

### Listas desordenadas

```markdown
- Item uno
- Item dos
- Item tres
  - Subitem (indentado 2 o 4 espacios)
  - Otro subitem
```

Delimitadores: `-`, `*`, `+`. **No los mezcles** en la misma lista.

### Iniciar item de lista con número

```markdown
- 1968\. ¡Un gran año!
- 1969 fue el segundo mejor.
```

Usa `\` para escapar el punto.

### Agregar elementos en listas

Indenta 4 espacios o 1 tab para incluir elementos adicionales:

```markdown
* Primer item de la lista.
* Segundo item.

    Párrafo adicional dentro del segundo item.

* Tercer item.
```

Para code blocks dentro de listas, indenta 8 espacios (o 2 tabs):

```markdown
1. Abre el archivo.
2. Busca este bloque:

        <html>
          <head>
            <title>Test</title>
          </head>
        </html>

3. Actualiza el título.
```

---

## 7. Código

### Código en línea

Usa backticks (`` ` ``):

```markdown
En la terminal, escribe `nano`.
```

### Escaping backticks

Si el texto contiene backticks, usa backticks dobles (`` `` ``):

```markdown
``Usa `codigo` en tu archivo Markdown.``
```

### Bloques de código

Indenta cada línea por **4 espacios o 1 tab**:

```markdown
    <html>
      <head>
        <title>Test</title>
      </head>
    </html>
```

**Nota:** Para bloques de código con resaltado de sintaxis, usa fenced code blocks (```).

---

## 8. Líneas Horizontales

Usa 3 o más caracteres en una línea propia:

```markdown
***         (asteriscos)
---         (guiones)
___         (guiones bajos)
```

Pon líneas en blanco antes y después.

---

## 9. Enlaces

```markdown
[texto del enlace](https://ejemplo.com)
[texto con tooltip](https://ejemplo.com "Tooltip opcional")
```

### URLs y emails automáticos

```markdown
<https://www.markdownguide.org>
<fake@example.com>
```

### Formato en enlaces

```markdown
**[EFF](https://eff.org)**          — negrita
*[Markdown Guide](https://www...)*   — cursiva
[`code`](#code)                    — código
```

### Enlaces estilo referencia

Primera parte (en el texto):

```markdown
En un agujero en el suelo vivía un [hobbit][1].

[hobbit-hole]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle "Hobbit lifestyles"
```

Segunda parte (en cualquier parte del documento):

```markdown
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle "Hobbit lifestyles"
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle 'Hobbit lifestyles'
[1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle (Hobbit lifestyles)
[1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> "Hobbit lifestyles"
```

### Mejores prácticas

- Espacios en URLs: usa `%20` (ej: `my%20page`)
- Paréntesis en URLs: usa `%28` y `%29`
- Alternativa: HTML `<a href="url">texto</a>`

---

## 10. Imágenes

```markdown
![texto alternativo](/ruta/a/imagen.jpg "Título opcional")
```

### Imágenes con enlace

```markdown
[![texto alternativo](img.jpg)](https://ejemplo.com)
```

---

## 11. Escaping de Caracteres

Usa `\` antes de un carácter especial para mostrarlo literalmente:

```markdown
\* Sin la barra invertida, esto sería una viñeta.
```

### Caracteres que se pueden escapar

| Carácter | Nombre |
|----------|--------|
| `\\` | barra invertida |
| `` \` `` | backtick |
| `\*` | asterisco |
| `\_` | guión bajo |
| `\{ \}` | llaves |
| `\[ \]` | corchetes |
| `\< \>` | ángulos |
| `\( \)` | paréntesis |
| `\#` | signo de número |
| `\+` | signo más |
| `\-` | guión |
| `\.` | punto |
| `\!` | exclamación |
| `\|` | pipe |

---

## 12. HTML en Markdown

Puedes usar HTML directamente cuando Markdown no sea suficiente:

```markdown
Esta **palabra** está en negrita. Esta <em>palabra</em> está en cursiva.
```

```markdown
<p style="color: red;">Texto rojo</p>
<mark>texto resaltado</mark>
<br>  <!-- salto de linea -->
```

### Reglas HTML

1. Pon líneas en blanco alrededor de elementos block-level (`<div>`, `<table>`, `<pre>`, `<p>`)
2. No sangres las etiquetas HTML con tabs/espacios
3. **No puedes** usar sintaxis Markdown DENTRO de etiquetas HTML block-level
   - ✅ `<p>Texto en <em>cursiva</em></p>` (HTML puro dentro funciona)
   - ❌ `<p>Texto en *cursiva*</p>` (Markdown no se procesa dentro de etiquetas block-level)
   - ✅ `<p>Texto en <em>cursiva</em></p>` usa HTML para énfasis

---

## 13. Resumen rápido (Cheat Sheet)

| Elemento | Sintaxis |
|----------|----------|
| Heading 1 | `# Texto` |
| Heading 2 | `## Texto` |
| Negrita | `**texto**` |
| Cursiva | `*texto*` |
| Blockquote | `> texto` |
| Lista ordenada | `1. Item` |
| Lista desordenada | `- Item` |
| Codigo inline | `` `codigo` `` |
| Codigo bloque | Indentar 4 espacios |
| Linea horizontal | `---` |
| Enlace | `[texto](url)` |
| Imagen | `![alt](img.png)` |
