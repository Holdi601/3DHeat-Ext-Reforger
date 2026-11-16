---
title: "Identificar un archivo: identify"
nav_order: 3
lang: "es"
source: identify.md
source_hash: "c7c88815247e"
nav_exclude: true
search_exclude: true
---
# Identificar un archivo: `identify` {#identifying-a-file-identify}

```bash
heat3d-reforger-maps identify <file>
```

indica si un archivo es uno de los archivos Enfusion que esta herramienta lee, y qué contiene,
leyéndolo en lugar de fijarse en su nombre:

| Archivo | Se reconoce por | Lo que imprime |
|---|---|---|
| un archivo comprimido (`.pak`, en `addons\<addon>\`) | `FORM` ... `PAC1`, y un directorio que se lee hasta el final | el número de archivos, cuántos están comprimidos con zlib, su tamaño descomprimido |
| un terreno (`.terr`) | `FORM` ... `TERR` con un fragmento `HEAD` | los vértices en cada sentido y su separación, los bloques de una loseta |
| una loseta de terreno (`.ttile`) | `FORM` ... `TERR` con un fragmento `HGHT` | sus fragmentos |
| un archivo de mundo (`.ent`) | `EBIN`, y entidades que se parsean hasta el último byte | el número de entidades, los GUID y nombres de recursos |
| una textura (`.edds`) | una cabecera DDS con la extensión DX10, y niveles de registro que suman el tamaño del archivo | el tamaño, los niveles, el formato DXGI, cómo están guardados los niveles |

Los archivos dentro de un archivo comprimido se leen con `world`; `identify` toma archivos en
disco, un archivo comprimido en sí o un archivo extraído de uno.

```text
data.pak  (<n> bytes)
  Enfusion archive (.pak)
    files      <n>, <n> of them zlib-compressed
    holds      <n> bytes unpacked
```

## Cualquier otra cosa {#anything-else}

Un archivo que no es ninguno de estos no imprime nada en la salida, la línea
`not an Arma Reforger file` en la salida de errores, y termina con 2; tampoco un `.dds` normal,
aunque un `.edds` empiece igual. Eso es lo que usa el propio `identify` de
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): para un archivo que sus
propios lectores no conocen, pregunta a cada herramienta de juego instalada por turno, y la que termina con 0 tiene la respuesta.

| Mensaje | Salida | Significa |
|---|---|---|
| (una descripción como las de arriba) | 0 | un archivo Enfusion |
| `not an Arma Reforger file` | 2 | cualquier otro archivo |
| `no such file: <path>` | 2 | la ruta es incorrecta |
| `needs 3DHeat GameFiles: ...` | 2 | mira [Antes de empezar](before-you-start.md) |
