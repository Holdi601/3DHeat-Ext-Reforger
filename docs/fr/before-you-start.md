---
title: "Avant de commencer"
nav_order: 1.5
lang: "fr"
source: before-you-start.md
source_hash: "0b6fa46724ea"
nav_exclude: true
search_exclude: true
---
# Avant de commencer {#before-you-start}

Vous n'avez jamais utilisé la ligne de commande ? Cette page vous mène de zéro à un premier lancement.
Cela prend environ quinze minutes, une seule fois.

## 1. Installer Python {#install-python}

Cet outil demande **Python 3.10 ou plus récent**.

- **Windows :** téléchargez Python sur [python.org/downloads](https://www.python.org/downloads/)
  et lancez l'installateur. Sur son premier écran, cochez **Add python.exe to PATH**,
  puis cliquez sur **Install Now**.
- **macOS et Linux :** Python 3 est souvent déjà là. Là où ces pages disent
  `python`, tapez `python3`.

## 2. Obtenir cet outil {#get-this-tool}

Ouvrez [github.com/Holdi601/3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger), cliquez sur le
bouton vert **Code**, puis sur **Download ZIP**, et décompressez-le dans le dossier de votre choix. Si vous utilisez git : `git clone https://github.com/Holdi601/3DHeat-Ext-Reforger`.

## 3. 3DHeat GameFiles vient avec {#dheat-gamefiles-comes-with-it}

L'outil lit avec [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(son écrivain glTF, la recherche dans la bibliothèque Steam, le décodage des textures). L'étape 5 l'installe
pour vous. Sans pip - un dossier téléchargé que vous lancez sur place -, placez GameFiles
à côté de cet outil sous le nom `3DHeat-GameFiles`, ou définissez `HEAT3D_GAMEFILES` avec
son dossier ; dans une copie de 3DHeat (`exporters/ext/reforger-maps`), il est trouvé
dans `exporters/gamefiles` tout seul.

## 4. Ouvrir un terminal dans ce dossier {#open-a-terminal-in-that-folder}

Un terminal est une fenêtre où vous tapez des commandes.

- **Windows :** ouvrez le dossier dans l'Explorateur, cliquez dans la barre d'adresse, tapez
  `powershell` et appuyez sur Entrée. Une fenêtre bleue ou noire s'ouvre, déjà dans ce
  dossier.
- **macOS :** ouvrez **Terminal**, tapez `cd ` (avec un espace), glissez le dossier dans la
  fenêtre et appuyez sur Entrée.

`cd` signifie « changer de dossier » : `cd C:\Tools\3DHeat-Ext-Reforger` va dans ce dossier.

## 5. Installer l'outil {#install-the-tool}

Tapez ceci et appuyez sur Entrée :

```bash
python -m pip install -e .
```

Vous devez voir, à la fin : `Successfully installed heat3d-ext-reforger-...`
(et `heat3d-gamefiles-...` avec).

## 6. Le lancer {#run-it}

```bash
heat3d-reforger-maps worlds
```

Vous devez voir quelque chose comme :

```text
Arma Reforger at D:\Games\Steam\steamapps\common\Arma Reforger: <n> worlds with a terrain
  <world>                                  worlds/<world>/.../<world>.terr
  ...
```

Suite : [Mondes Arma Reforger](level-arma-reforger.md).

## Comment lire les commandes de ces pages {#how-to-read-the-commands-on-these-pages}

| Vous voyez | Cela signifie |
|---|---|
| `<world>` | un espace réservé : tapez votre propre valeur à la place, sans les `< >` |
| `[--texture-size PIXELS]` | facultatif : omettez-le, ou tapez-le comme indiqué |
| `# a note` | un commentaire pour vous : ne le tapez pas |
| `"C:\My Files\x"` | mettez entre guillemets un chemin qui contient des espaces |

## Quand quelque chose ne va pas {#when-something-goes-wrong}

| Le message | Que faire |
|---|---|
| `'python' is not recognized` | Python n'est pas installé, ou la case PATH n'était pas cochée : réinstallez-le et cochez-la (ou tapez `py` au lieu de `python`). |
| `'heat3d-reforger-maps' is not recognized` | Refaites l'étape 5 dans le dossier de l'outil, ou tapez `python -m heat3d_ext_reforger` au lieu de `heat3d-reforger-maps` : cela fait la même chose. |
| `needs 3DHeat GameFiles: ...` | L'étape 5 ne l'a pas installé, ou vous lancez le dossier sur place : voir l'étape 3. |
| `Arma Reforger not found; ...` | Installez le jeu via Steam, ou donnez son dossier (celui qui contient `addons`) : `--install "D:\Games\Arma Reforger"`. |
| `no world '<name>'; there are: ...` | Utilisez l'un des noms que la ligne indique, tels que `worlds` les affiche. |
| autre chose | Lisez la dernière ligne du message, puis ouvrez un ticket sur GitHub avec elle. |

Chaque commande se termine aussi par un **code de sortie** : 0 signifie que cela a marché, 2 que
le jeu, le monde, le fichier ou GameFiles n'a pas été trouvé, 1 que la lecture a échoué. Pour le voir,
tapez `echo $LASTEXITCODE` dans PowerShell, ou `echo $?` sous macOS et Linux.
