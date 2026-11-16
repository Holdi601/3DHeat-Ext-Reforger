---
title: "Conditions et licence"
nav_order: 8
lang: "fr"
source: terms.md
source_hash: "9c8f2a00998f"
nav_exclude: true
search_exclude: true
---
# Conditions et licence {#terms-and-licence}

Cette page dit ce que l'outil lit, ce qu'il fournit et d'où viennent ses sources.

## Le jeu de Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger et ses mondes appartiennent à Bohemia Interactive. 3DHeat Reforger n'est ni
affilié à Bohemia Interactive ni approuvé par elle ; Arma Reforger ainsi que les noms et
marques associés appartiennent à leurs propriétaires.

Cet outil n'embarque rien du jeu - aucun contenu du jeu, aucun code du jeu, aucune DLL - et
ne télécharge rien : il lit les fichiers de la copie **que vous** avez installée, sur votre
machine, en dehors du jeu. Il ne modifie rien dans le jeu, ne tourne pas à côté de lui et ne
parle à aucun serveur. Rien dans les fichiers du jeu n'est chiffré, et rien n'est déchiffré.

Le monde qu'il écrit reste sur votre machine : il est pour votre usage personnel, non à
partager, publier ou vendre. Le `.gitignore` du dépôt tient les fichiers du jeu et les
exports hors du contrôle de version, par type de fichier.

Chaque lecteur de jeu est un petit projet à part, avec son propre fichier de licence,
ses versions et son suivi des tickets : il peut être installé, mis à jour, maintenu - ou
retiré à la demande d'un ayant droit - seul, sans toucher au visualiseur ni aux autres outils.

Ayants droit : ouvrez un ticket sur
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
nous répondons rapidement et retirons tout ce qui est demandé.

## Les formats {#the-formats}

Les lecteurs Enfusion (`enfusion.py`, `enfusionworld.py`) ont été établis à partir des fichiers
installés d'Arma Reforger, sans autre source. Bohemia Interactive publie ses scripts de jeu sous
l'Arma Public License, qui n'est pas compatible avec la MIT ; aucun d'eux n'a été lu pour cela ni copié. Comment chaque format est lu,
et contre quoi il a été vérifié :
[Mondes Arma Reforger](level-arma-reforger.md#how-it-is-read-and-checked).

## Licence et sources {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSE)) :
utilisation, modification, distribution, commerciale ou non. Il s'appuie sur
[3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) (MIT) et a besoin
de numpy (BSD-3-Clause), Pillow (MIT-CMU) et lz4 (BSD-3-Clause) ; les tests ont besoin
de pytest (MIT). Voir
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSES.md).
