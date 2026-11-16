---
title: "Accueil"
nav_order: 1
lang: "fr"
source: index.md
source_hash: "6e5d4ee92caa"
nav_exclude: true
search_exclude: true
permalink: /fr/
---
# 3DHeat Reforger {#dheat-reforger}

**Qu'est-ce que c'est ?** Cet outil transforme un monde d'Arma Reforger, lu dans **votre propre
installation**, en un niveau 3D - une maquette de la carte au-dessus de laquelle voler - pour la
visualiseur [3DHeat](https://github.com/Holdi601/3DHeat)
([documentation](https://holdi601.github.io/3DHeat/)) : le terrain dans ses propres couleurs, la mer,
et chaque bâtiment et objet que le monde place, sous forme de boîte.

**Pourquoi l'utiliser ?** Pour que la chaleur d'Arma Reforger ait sous elle le sol et les bâtiments,
dans les mètres du jeu : rien à placer ni à mettre à l'échelle dans le visualiseur.

**Exemple :** `heat3d-reforger-maps world <world> -o world.glb` -> `world.glb`.
(*Enfusion* est le moteur avec lequel Arma Reforger est fait ; un *monde* est ce que le jeu appelle une carte.)

## Démarrage rapide {#quick-start}

Vous n'avez jamais utilisé la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).
Il vous faut Python 3.10 ou plus récent, [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(la bibliothèque que cet outil utilise pour lire) et Arma Reforger installé via Steam.
Lancez ces commandes dans le dossier où vous avez cloné ou décompressé l'outil :

```bash
python -m pip install -e .                          # installs heat3d-reforger-maps, and GameFiles with it
heat3d-reforger-maps worlds                         # where the game is, and its worlds
heat3d-reforger-maps world <world> -o world.glb     # one world as a level
```

`worlds` commence par `Arma Reforger at <the game's folder>: <n> worlds with a terrain`
et liste un monde par ligne ; `world` se termine par son rapport (`ground`,
`structure`, `water`). Chargez ensuite `world.glb` dans le panneau
**Arrière-plan / niveau** du visualiseur ([charger un niveau](https://holdi601.github.io/3DHeat/levels.html)).

Le niveau est construit à partir des fichiers du jeu : il reste **sur votre machine**, pour le
visualiser, et non pour le partager ou le publier ([Conditions](terms.md)).

Chaque lecteur de jeu est un petit projet à part, avec son propre fichier de licence,
ses versions et son suivi des tickets : il peut être installé, mis à jour, maintenu - ou
retiré à la demande d'un ayant droit - seul, sans toucher au visualiseur ni aux autres outils.

## Pages {#pages}

| Page | Ce qu'elle couvre |
|---|---|
| [Avant de commencer](before-you-start.md) | Python, GameFiles, un terminal, un premier lancement |
| [Mondes Arma Reforger : worlds et world](level-arma-reforger.md) | lister les mondes, chaque option d'un export, ses parties, comment chaque format est lu et vérifié |
| [Identifier un fichier : identify](identify.md) | si un fichier est une archive, un terrain, un fichier de monde ou une texture Enfusion |
| [Conditions et licence](terms.md) | ce que l'outil lit, les sources, pourquoi c'est un projet à part |
| [Référence des commandes](../cli-reference.md) | chaque option, générée à partir du code |
| [Entretien de ces documents](maintaining.md) | la liste de contrôle de publication |

## Liens utiles {#related}

- Le visualiseur 3DHeat : [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentation sur [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) : l'écrivain glTF, la recherche dans la
  bibliothèque Steam et le décodage des textures sur lesquels cet outil s'appuie ; ses commandes
  `enfusion-worlds` et `enfusion-world` lancent cet outil lorsqu'il est installé.

## Les outils 3DHeat {#the-3dheat-tools}

| Outil | Ce qu'il fait | Code | Documentation |
|---|---|---|---|
| Visualiseur 3DHeat | affiche les données : cartes de chaleur, analyse de course, revue de match | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | niveaux et parcours tirés des fichiers propres à un jeu | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | télémétrie de tour, et niveaux reconstruits à partir de vidéos de jeu | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin pour l'éditeur Unreal : un niveau en un seul `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | démos et cartes de Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | enregistre ce que les jeux publient pendant que vous jouez | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | replays de War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | replays de World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | replays de World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | démos de serveurs Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | cartes de DCS World en niveaux 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | cartes d'IL-2 Sturmovik en niveaux 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | la carte de Dota 2 en niveau 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | replays de Dota 2 en tableaux | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | replays de League of Legends et VALORANT | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | parcours et voitures de Forza Horizon | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | cartes de Battlefield 6 en niveaux 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | parcours de BeamNG.drive autour de vos tours | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | épreuves d'Assetto Corsa Rally autour de vos tours | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mondes d'Arma Reforger en niveaux 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | replays de matchs Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |
