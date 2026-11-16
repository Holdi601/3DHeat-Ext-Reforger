---
title: "Identifier un fichier : identify"
nav_order: 3
lang: "fr"
source: identify.md
source_hash: "c7c88815247e"
nav_exclude: true
search_exclude: true
---
# Identifier un fichier : `identify` {#identifying-a-file-identify}

```bash
heat3d-reforger-maps identify <file>
```

indique si un fichier est l'un des fichiers Enfusion que cet outil lit, et ce qu'il
contient, en le lisant plutôt qu'en regardant son nom :

| Fichier | Reconnu par | Ce qu'il affiche |
|---|---|---|
| une archive (`.pak`, dans `addons\<addon>\`) | `FORM` ... `PAC1`, et un répertoire qui se lit jusqu'à sa fin | le nombre de fichiers, combien sont compressés en zlib, leur taille décompressée |
| un terrain (`.terr`) | `FORM` ... `TERR` avec un morceau `HEAD` | les sommets dans chaque sens et leur écart, les blocs d'une tuile |
| une tuile de terrain (`.ttile`) | `FORM` ... `TERR` avec un morceau `HGHT` | ses morceaux |
| un fichier de monde (`.ent`) | `EBIN`, et des entités qui se lisent jusqu'au dernier octet | le nombre d'entités, les GUID et noms de ressources |
| une texture (`.edds`) | un en-tête DDS avec l'extension DX10, et des niveaux qui additionnent à la taille du fichier | la taille, les niveaux, le format DXGI, la façon dont les niveaux sont stockés |

Les fichiers contenus dans une archive se lisent avec `world` ; `identify` prend des fichiers
sur le disque, une archive elle-même ou un fichier extrait d'une archive.

```text
data.pak  (<n> bytes)
  Enfusion archive (.pak)
    files      <n>, <n> of them zlib-compressed
    holds      <n> bytes unpacked
```

## Tout le reste {#anything-else}

Un fichier qui n'est rien de cela n'affiche rien sur la sortie, la ligne
`not an Arma Reforger file` sur la sortie d'erreur, et se termine avec 2 - un simple
`.dds` aussi, même si un `.edds` commence comme lui. C'est sur quoi s'appuie le propre
`identify` de [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) : pour un
fichier que ses propres lecteurs ne connaissent pas, il interroge chaque outil de jeu installé
à tour de rôle, et celui qui se termine avec 0 a la réponse.

| Message | Sortie | Signification |
|---|---|---|
| (une description comme ci-dessus) | 0 | un fichier Enfusion |
| `not an Arma Reforger file` | 2 | tout autre fichier |
| `no such file: <path>` | 2 | le chemin est faux |
| `needs 3DHeat GameFiles: ...` | 2 | voir [Avant de commencer](before-you-start.md) |
