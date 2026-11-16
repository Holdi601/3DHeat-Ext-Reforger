---
title: Vor dem Start
nav_order: 1.5
lang: "de"
source: before-you-start.md
source_hash: "0b6fa46724ea"
nav_exclude: true
search_exclude: true
---
# Vor dem Start {#before-you-start}

Neu in der Kommandozeile? Diese Seite führt dich von null bis zu einem ersten Lauf.
Sie dauert einmal etwa fünfzehn Minuten.

## 1. Python installieren {#install-python}

Dieses Werkzeug braucht **Python 3.10 oder neuer**.

- **Windows:** Lade Python von [python.org/downloads](https://www.python.org/downloads/)
  herunter und starte das Installationsprogramm. Setze auf dessen erster Seite den Haken
  bei **python.exe zu PATH hinzufügen** (englisch: **Add python.exe to PATH**) und klicke
  auf **Jetzt installieren** (englisch: **Install Now**).
- **macOS und Linux:** Python 3 ist oft schon vorhanden. Wo diese Seiten `python`
  schreiben, tippe `python3`.

## 2. Dieses Werkzeug holen {#get-this-tool}

Öffne [github.com/Holdi601/3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger),
klicke auf den grünen Button **Code** und dann auf **Download ZIP**, und entpacke es in
einen Ordner deiner Wahl. Wenn du git benutzt: `git clone https://github.com/Holdi601/3DHeat-Ext-Reforger`.

## 3. 3DHeat GameFiles kommt mit {#dheat-gamefiles-comes-with-it}

Das Werkzeug liest mit [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(dessen glTF-Schreiber, der Steam-Bibliothekssuche, der Texturdekodierung). Schritt 5
installiert es für dich. Ohne pip, also einen heruntergeladenen Ordner, den du an Ort
und Stelle startest, legst du GameFiles neben dieses Werkzeug als `3DHeat-GameFiles`,
oder du setzt `HEAT3D_GAMEFILES` auf seinen Ordner. Innerhalb eines 3DHeat-Checkouts
(`exporters/ext/reforger-maps`) wird es in `exporters/gamefiles` von selbst gefunden.

## 4. Ein Terminal in diesem Ordner öffnen {#open-a-terminal-in-that-folder}

Ein Terminal ist ein Fenster, in das du Befehle tippst.

- **Windows:** Öffne den Ordner im Explorer, klicke in die Adressleiste, tippe
  `powershell` und drücke Enter. Ein blaues oder schwarzes Fenster öffnet sich, schon in
  diesem Ordner.
- **macOS:** Öffne **Terminal**, tippe `cd ` (mit einem Leerzeichen), ziehe den Ordner in
  das Fenster und drücke Enter.

`cd` heißt „Ordner wechseln“: `cd C:\Tools\3DHeat-Ext-Reforger` geht in diesen Ordner.

## 5. Das Werkzeug installieren {#install-the-tool}

Tippe dies und drücke Enter:

```bash
python -m pip install -e .
```

Am Ende solltest du sehen: `Successfully installed heat3d-ext-reforger-...`
(und `heat3d-gamefiles-...` dazu).

## 6. Starten {#run-it}

```bash
heat3d-reforger-maps worlds
```

Du solltest etwa so etwas sehen:

```text
Arma Reforger at D:\Games\Steam\steamapps\common\Arma Reforger: <n> worlds with a terrain
  <world>                                  worlds/<world>/.../<world>.terr
  ...
```

Weiter: [Arma-Reforger-Welten](level-arma-reforger.md).

## So liest du die Befehle auf diesen Seiten {#how-to-read-the-commands-on-these-pages}

| Du siehst | Es bedeutet |
|---|---|
| `<world>` | ein Platzhalter: tippe stattdessen deinen eigenen Wert, ohne die `< >` |
| `[--texture-size PIXELS]` | optional: lass es weg, oder tippe es wie gezeigt |
| `# a note` | ein Kommentar für dich: nicht mittippen |
| `"C:\My Files\x"` | einen Pfad mit Leerzeichen in Anführungszeichen setzen |

## Wenn etwas schiefgeht {#when-something-goes-wrong}

| Die Meldung | Was zu tun ist |
|---|---|
| `'python' is not recognized` | Python ist nicht installiert, oder das PATH-Kästchen war nicht angehakt: installiere es noch einmal und hake es an (oder tippe `py` statt `python`). |
| `'heat3d-reforger-maps' is not recognized` | Führe Schritt 5 im Ordner des Werkzeugs noch einmal aus, oder tippe `python -m heat3d_ext_reforger` statt `heat3d-reforger-maps`: das tut dasselbe. |
| `needs 3DHeat GameFiles: ...` | Schritt 5 hat es nicht installiert, oder du startest den Ordner an Ort und Stelle: siehe Schritt 3. |
| `Arma Reforger not found; ...` | Installiere das Spiel über Steam, oder gib seinen Ordner an (den mit `addons` darin): `--install "D:\Games\Arma Reforger"`. |
| `no world '<name>'; there are: ...` | Nimm einen der Namen, die die Zeile nennt, so wie `worlds` sie ausgibt. |
| alles andere | Lies die letzte Zeile der Meldung und eröffne damit ein Issue auf GitHub. |

Jeder Befehl endet außerdem mit einem **Exit-Status**: 0 heißt, es hat geklappt; 2, dass
das Spiel, die Welt, die Datei oder GameFiles nicht gefunden wurde; 1, dass das Lesen
fehlschlug. Um ihn zu sehen, tippe `echo $LASTEXITCODE` in PowerShell oder `echo $?`
unter macOS und Linux.
