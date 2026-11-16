---
title: Mantenimiento de estos documentos
nav_order: 91
lang: "es"
source: maintaining.md
source_hash: "d9624d918107"
nav_exclude: true
search_exclude: true
---
# Mantenimiento de estos documentos {#maintaining-these-docs}

Una lista de comprobación para cada versión, para que las páginas nunca se queden atrás respecto al código.

1. **Regenerar la referencia.** `python tools/gen_docs_reference.py` reescribe
   [Referencia de comandos](../cli-reference.md) a partir del propio `--help` del programa y de
   sus columnas de salida. `python tools/gen_docs_reference.py --check` termina con 1 cuando
   la página guardada está desactualizada.
2. **Listar lo que cambió.** `git log v<VERSION>..HEAD --oneline`, donde
   `<VERSION>` es la última versión publicada (el archivo `VERSION` en la publicación).
   Dale a cada nueva función, opción y columna de salida un lugar en una página, y una
   fila en la sección **Docs** de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/CHANGELOG.md).
3. **Revisión independiente.** Alguien que no escribió las páginas lee el
   README y cada página cambiada, las imágenes incluidas, tres veces: como un principiante que nunca ha usado
   una terminal, como un niño de 8 años, y como un experto que comprueba cada opción contra
   `--help`. Los ejemplos usan solo nombres y números inventados.
4. **Corregir** todo lo que encuentre la revisión.
5. **Traducciones.** Cada página traducida registra el hash de la página inglesa de la que
   se hizo. Vuelve a traducir las páginas cuyo original en inglés cambió,
   y luego revisa cada idioma: texto claro, etiquetas correctas en los diagramas, las mismas
   palabras que la interfaz traducida del visor.
6. **Ejecutar las pruebas** (`pytest`).
7. **Subir** solo con el visto bueno del propietario.

## Traducciones: los comandos {#translations-the-commands}

El sitio se va a traducir a los 40 idiomas del visor de 3DHeat (hasta ahora: la página que venía de
3DHeat GameFiles, en 18 idiomas): el inglés en
`docs/`, cada otro idioma en `docs/<lang>/` con los mismos nombres de archivo. `tools/docs_i18n.py` lleva la contabilidad:

```bash
python tools/docs_i18n.py hashes             # tras cualquier cambio en inglés: registrar el hash de cada página
python tools/docs_i18n.py svg-strings        # tras cualquier cambio en imágenes: las etiquetas a traducir
python tools/docs_i18n.py status             # por idioma: al día, desfasadas, páginas que faltan
python tools/docs_i18n.py todo --lang de     # las páginas en alemán a (re)traducir
python tools/docs_i18n.py svg-build --lang de    # las imágenes en alemán desde docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marcar las páginas en alemán con el hash del inglés
python tools/docs_i18n.py check              # sale con 1 cuando los hashes o las etiquetas están desfasados
```

Traduce solo lo que lista `todo`: mantén el Markdown, los enlaces, el código, los nombres de archivo y de columnas tal como están,
traduce los títulos y las descripciones de las imágenes, y usa las palabras propias del visor de 3DHeat para sus botones
y paneles (su `src/i18n/locales/<lang>/`). Las páginas de referencia generadas y las imágenes de terminal siguen
en inglés. En el sitio, una traducción desactualizada lo indica y enlaza la página en inglés; una que falta
recurre al inglés. El menú de idiomas de la cabecera y la redirección por idioma del navegador de la página de inicio
vienen de `docs/_includes/`.

## Las imágenes {#the-pictures}

`docs/assets/img/enfusion-steps.svg` lo dibujó `tools/docs_diagrams.py` de 3DHeat GameFiles
cuando estas páginas formaban parte de GameFiles. Cámbialo a mano (es SVG plano), luego ejecuta
`svg-strings`, traduce las nuevas etiquetas en `docs/assets/i18n/svg/<lang>.json` y `svg-build`.
