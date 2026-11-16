---
title: Términos y licencia
nav_order: 8
lang: "es"
source: terms.md
source_hash: "9c8f2a00998f"
nav_exclude: true
search_exclude: true
---
# Términos y licencia {#terms-and-licence}

Esta página dice qué lee la herramienta, qué incluye y de dónde vienen sus fuentes.

## El juego de Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger y sus mundos pertenecen a Bohemia Interactive. 3DHeat Reforger no está afiliado a Bohemia Interactive ni cuenta con su respaldo; Arma Reforger y los nombres y marcas relacionados pertenecen a sus propietarios.

Esta herramienta no incluye nada del juego - ningún contenido del juego, ningún código del juego, ninguna DLL - y no descarga nada: lee los archivos de la copia que **tú** instalaste, en tu equipo, fuera del juego. No modifica nada del juego, no se ejecuta junto a él y no se comunica con ningún servidor. Nada de los archivos del juego está cifrado, y nada se descifra.

El mundo que escribe se queda en tu equipo: es para tu propio uso, no para compartirlo, publicarlo ni venderlo. El `.gitignore` del repositorio mantiene los archivos del juego y las exportaciones fuera del control de versiones según su tipo.

Cada lector de juegos es un pequeño proyecto propio, con su propio archivo de licencia,
sus versiones y su gestor de incidencias, así que puede instalarse, actualizarse,
mantenerse - o retirarse a petición de un titular de derechos - por sí solo, sin afectar
al visor ni a las demás herramientas.

Titulares de derechos: pueden abrir una incidencia en
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
respondemos rápido y retiramos lo que se nos pida.

## Los formatos {#the-formats}

Los lectores de Enfusion (`enfusion.py`, `enfusionworld.py`) se elaboraron a partir de los propios archivos instalados de Arma Reforger, sin ninguna otra fuente. Bohemia Interactive publica sus scripts de juego bajo la Arma Public License, que no es compatible con MIT; ninguno de ellos se leyó para esto ni se copió. Cómo se lee cada formato, y contra qué se comprobó:
[Mundos de Arma Reforger](level-arma-reforger.md#how-it-is-read-and-checked).

## Licencia y fuentes {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSE)):
úsala, cámbiala, distribúyela, con fines comerciales o no. Se apoya en
[3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) (MIT) y necesita
numpy (BSD-3-Clause), Pillow (MIT-CMU) y lz4 (BSD-3-Clause); las pruebas necesitan
pytest (MIT). Ver
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSES.md).
