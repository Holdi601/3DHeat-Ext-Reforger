---
title: Términos y licencia
nav_order: 8
lang: "es"
source: terms.md
source_hash: "358a481eaf89"
nav_exclude: true
search_exclude: true
---
# Términos y licencia {#terms-and-licence}

Esta página es un registro de lo que dicen las licencias, no asesoramiento legal.

## El juego de Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger y sus mundos pertenecen a Bohemia Interactive, que no respalda este proyecto. Esta herramienta no incluye nada del juego y no descarga nada: lee los archivos de la copia que **tú** instalaste, en tu equipo, fuera del juego. No modifica nada del juego, no se ejecuta junto a él y no se comunica con ningún servidor. Nada de los archivos del juego está cifrado, y nada se descifra.

La licencia del juego permite el uso no comercial y prohíbe la ingeniería inversa de los archivos del juego. Leer tu propia instalación es decisión tuya bajo esa licencia, y la obligación recae en quien ejecuta la herramienta. El mundo que escribe es contenido de la editora del juego: es para tu propio uso, no para compartirlo, publicarlo ni venderlo. El `.gitignore` del repositorio mantiene los archivos del juego y las exportaciones fuera del control de versiones según su tipo.

La vía propia de Bohemia hacia los datos del juego es **Arma Reforger Tools** (el Enfusion Workbench), gratuito en Steam para crear mods según las normas de modding de Bohemia. Esta herramienta no lo necesita ni lo usa; lee directamente los archivos comprimidos del juego instalado.

Por eso es un paquete aparte: si Bohemia Interactive algún día pide que se retire, se retira solo, y el visor, GameFiles y las demás herramientas siguen.

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
