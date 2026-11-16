---
title: "Conditions et licence"
nav_order: 8
lang: "fr"
source: terms.md
source_hash: "358a481eaf89"
nav_exclude: true
search_exclude: true
---
# Conditions et licence {#terms-and-licence}

Cette page est un relevé de ce que disent les licences, non un avis juridique.

## Le jeu de Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger et ses mondes appartiennent à Bohemia Interactive, qui ne soutient pas
ce projet. Cet outil n'embarque rien du jeu et ne télécharge rien : il lit les fichiers de la copie
**que vous** avez installée, sur votre machine, en dehors du jeu. Il ne modifie rien dans le jeu, ne
tourne pas à côté de lui et ne parle à aucun serveur. Rien dans les fichiers du jeu n'est chiffré, et rien n'est déchiffré.

La licence du jeu autorise l'usage non commercial et interdit la rétro-ingénierie des
fichiers du jeu. Lire votre propre installation relève de votre décision au titre de cette licence, et
l'obligation incombe à celui qui lance l'outil. Le monde qu'il écrit est le contenu de l'éditeur du jeu :
il est pour votre usage personnel, non à partager, publier ou vendre. Le `.gitignore` du dépôt tient les
fichiers du jeu et les exports hors du contrôle de version, par type de fichier.

La voie officielle de Bohemia vers les données du jeu est **Arma Reforger Tools** (l'Enfusion
Workbench), gratuit sur Steam pour créer des mods selon les conditions de modding de Bohemia. Cet outil
n'en a pas besoin et ne l'utilise pas ; il lit directement les archives du jeu installé.

C'est pour cela que c'est un paquet à part : si Bohemia Interactive demande un jour qu'il disparaisse,
il partira seul, et le visualiseur, GameFiles et les autres outils resteront.

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
