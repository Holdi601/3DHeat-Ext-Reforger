---
title: Inicio
nav_order: 1
lang: "es"
source: index.md
source_hash: "859ac798f673"
nav_exclude: true
search_exclude: true
permalink: /es/
---
# 3DHeat Reforger {#dheat-reforger}

**¿Qué es?** Esta herramienta convierte un mundo de Arma Reforger, leído de **tu propia
instalación**, en un nivel 3D: un modelo del mapa sobre el que puedes volar, para el
visor de [3DHeat](https://github.com/Holdi601/3DHeat)
([documentación](https://holdi601.github.io/3DHeat/)): el terreno con sus propios colores, el mar, y cada
edificio y objeto que el mundo coloca, como una caja.

**¿Para qué sirve?** Para que el calor de Arma Reforger tenga debajo el suelo y los edificios, en los
metros propios del juego: sin colocar ni escalar nada en el visor.

**Ejemplo:** `heat3d-reforger-maps world <world> -o world.glb` -> `world.glb`.
(*Enfusion* es el motor con el que está hecho Arma Reforger; un *mundo* es lo que el juego llama mapa.)

## Inicio rápido {#quick-start}

¿Nuevo en la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).
Necesitas Python 3.10 o posterior, [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(la biblioteca con la que lee esta herramienta) y Arma Reforger instalado a través de Steam.
Ejecuta esto en la carpeta que clonaste o descomprimiste:

```bash
python -m pip install -e .                          # instala heat3d-reforger-maps, y GameFiles con él
heat3d-reforger-maps worlds                         # dónde está el juego, y sus mundos
heat3d-reforger-maps world <world> -o world.glb     # un mundo como nivel
```

`worlds` empieza con `Arma Reforger at <la carpeta del juego>: <n> worlds with a terrain`
y lista un mundo por línea; `world` termina con su informe (`ground`,
`structure`, `water`). Después carga `world.glb` en el panel **Fondo / nivel** del visor
([cargar un nivel](https://holdi601.github.io/3DHeat/levels.html)).

El nivel se construye con los archivos del juego: se queda **en tu equipo**, para verlo,
no para compartirlo ni publicarlo ([Términos](terms.md)).

## Páginas {#pages}

| Página | Qué cubre |
|---|---|
| [Antes de empezar](before-you-start.md) | Python, GameFiles, una terminal, una primera ejecución |
| [Mundos de Arma Reforger: worlds y world](level-arma-reforger.md) | listar los mundos, cada opción de una exportación, sus partes, cómo se lee y comprueba cada formato |
| [Identificar un archivo: identify](identify.md) | si un archivo es un archivo comprimido, terreno, archivo de mundo o textura de Enfusion |
| [Términos y licencia](terms.md) | el juego de Bohemia Interactive, las fuentes, por qué es un paquete aparte |
| [Referencia de comandos](../cli-reference.md) | cada opción, generada desde el código |
| [Mantenimiento de estos documentos](maintaining.md) | la lista de comprobación de cada versión |

## Relacionado {#related}

- El visor de 3DHeat: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentación en [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): el escritor de glTF, la búsqueda
  en la biblioteca de Steam y la decodificación de texturas sobre las que se apoya esta herramienta; sus
  `enfusion-worlds` y `enfusion-world` ejecutan esta herramienta cuando está instalada.

## Las herramientas de 3DHeat {#the-3dheat-tools}

| Herramienta | Qué hace | Código | Documentación |
|---|---|---|---|
| visor de 3DHeat | muestra los datos: mapas de calor, análisis de carrera, revisión de partidas | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | niveles y recorridos a partir de los archivos propios de un juego | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | telemetría de vueltas, y niveles reconstruidos a partir de vídeo de juego | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin del editor de Unreal: un nivel como un único `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | demos y mapas de Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | registra lo que publican los juegos mientras juegas | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | repeticiones de War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | repeticiones de World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | repeticiones de World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | demos de servidores de Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | mapas de DCS World como niveles 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | mapas de IL-2 Sturmovik como niveles 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | el mapa de Dota 2 como nivel 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | repeticiones de Dota 2 como tablas | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | repeticiones de League of Legends y VALORANT | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | recorridos y coches de Forza Horizon | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | mundos de Battlefield 6 como niveles 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | recorridos de BeamNG.drive alrededor de tus vueltas | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | tramos de Assetto Corsa Rally alrededor de tus vueltas | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mundos de Arma Reforger como niveles 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | repeticiones de partidas de Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |
