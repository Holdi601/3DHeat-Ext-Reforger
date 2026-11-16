---
title: Antes de empezar
nav_order: 1.5
lang: "es"
source: before-you-start.md
source_hash: "0b6fa46724ea"
nav_exclude: true
search_exclude: true
---
# Antes de empezar {#before-you-start}

¿Nuevo en la línea de comandos? Esta página te lleva de cero a una primera ejecución.
Lleva unos quince minutos, una sola vez.

## 1. Instalar Python {#install-python}

Esta herramienta necesita **Python 3.10 o posterior**.

- **Windows:** descarga Python desde [python.org/downloads](https://www.python.org/downloads/)
  y ejecuta el instalador. En su primera pantalla, marca **Add python.exe to PATH**
  y luego haz clic en **Install Now**.
- **macOS y Linux:** Python 3 suele estar ya instalado. Donde estas páginas dicen
  `python`, escribe `python3`.

## 2. Obtener esta herramienta {#get-this-tool}

Abre [github.com/Holdi601/3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger), haz clic en el
botón verde **Code** y luego en **Download ZIP**, y descomprímela en una carpeta a tu elección. Si usas git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Reforger`.

## 3. 3DHeat GameFiles viene incluido {#dheat-gamefiles-comes-with-it}

La herramienta lee con [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(su escritor de glTF, la búsqueda en la biblioteca de Steam, la decodificación de texturas). El paso 5 lo
instala por ti. Sin pip (una carpeta descargada que ejecutas en su sitio), pon GameFiles
junto a esta herramienta como `3DHeat-GameFiles`, o define `HEAT3D_GAMEFILES` con su
carpeta; dentro de un checkout de 3DHeat (`exporters/ext/reforger-maps`) se encuentra
en `exporters/gamefiles` por sí solo.

## 4. Abrir una terminal en esa carpeta {#open-a-terminal-in-that-folder}

Una terminal es una ventana donde escribes comandos.

- **Windows:** abre la carpeta en el Explorador, haz clic en la barra de direcciones, escribe
  `powershell` y pulsa Intro. Se abre una ventana azul o negra, ya en esa carpeta.
- **macOS:** abre **Terminal**, escribe `cd ` (con un espacio), arrastra la carpeta a
  la ventana y pulsa Intro.

`cd` significa "cambiar de carpeta": `cd C:\Tools\3DHeat-Ext-Reforger` va a esa carpeta.

## 5. Instalar la herramienta {#install-the-tool}

Escribe esto y pulsa Intro:

```bash
python -m pip install -e .
```

Al final deberías ver: `Successfully installed heat3d-ext-reforger-...`
(y `heat3d-gamefiles-...` con ella).

## 6. Ejecutarla {#run-it}

```bash
heat3d-reforger-maps worlds
```

Deberías ver algo como:

```text
Arma Reforger at D:\Games\Steam\steamapps\common\Arma Reforger: <n> worlds with a terrain
  <world>                                  worlds/<world>/.../<world>.terr
  ...
```

Siguiente: [Mundos de Arma Reforger](level-arma-reforger.md).

## Cómo leer los comandos de estas páginas {#how-to-read-the-commands-on-these-pages}

| Ves | Significa |
|---|---|
| `<world>` | un marcador: escribe tu propio valor en su lugar, sin los `< >` |
| `[--texture-size PIXELS]` | opcional: déjalo fuera, o escríbelo tal como se muestra |
| `# a note` | un comentario para ti: no lo escribas |
| `"C:\My Files\x"` | pon entre comillas una ruta que tenga espacios |

## Cuando algo sale mal {#when-something-goes-wrong}

| El mensaje | Qué hacer |
|---|---|
| `'python' is not recognized` | Python no está instalado, o no se marcó la casilla PATH: instálalo de nuevo y márcala (o escribe `py` en lugar de `python`). |
| `'heat3d-reforger-maps' is not recognized` | Repite el paso 5 en la carpeta de la herramienta, o escribe `python -m heat3d_ext_reforger` en lugar de `heat3d-reforger-maps`: hace lo mismo. |
| `needs 3DHeat GameFiles: ...` | El paso 5 no lo instaló, o ejecutas la carpeta en su sitio: mira el paso 3. |
| `Arma Reforger not found; ...` | Instala el juego a través de Steam, o indica su carpeta (la que tiene `addons` dentro): `--install "D:\Games\Arma Reforger"`. |
| `no world '<name>'; there are: ...` | Usa uno de los nombres que muestra la línea, tal como los imprime `worlds`. |
| cualquier otra cosa | Lee la última línea del mensaje y luego abre una incidencia en GitHub con ella. |

Cada comando también termina con un **código de salida**: 0 significa que funcionó, 2 que
no se encontró el juego, el mundo, el archivo o GameFiles, 1 que la lectura falló. Para verlo,
escribe `echo $LASTEXITCODE` en PowerShell o `echo $?` en macOS y Linux.
