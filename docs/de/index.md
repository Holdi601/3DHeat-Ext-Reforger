---
title: Start
nav_order: 1
lang: "de"
source: index.md
source_hash: "df34d50532d2"
nav_exclude: true
search_exclude: true
permalink: /de/
---
# 3DHeat Reforger {#dheat-reforger}

**Was ist das?** Dieses Werkzeug macht aus einer Arma-Reforger-Welt, gelesen aus
**deiner eigenen Installation**, ein 3D-Level für den [3DHeat](https://github.com/Holdi601/3DHeat)-Viewer
([Dokumentation](https://holdi601.github.io/3DHeat/)), ein Modell der Karte, über das du
fliegen kannst: das Gelände in seinen eigenen Farben, das Meer und jedes Gebäude und
Objekt, das die Welt platziert, als Box.

**Wozu brauche ich das?** Damit die Hitze aus Arma Reforger das Gelände und die Gebäude
darunter hat, in den eigenen Metern des Spiels: ohne Platzieren oder Skalieren im Viewer.

**Beispiel:** `heat3d-reforger-maps world <world> -o world.glb` -> `world.glb`.
(*Enfusion* ist die Engine, mit der Arma Reforger gemacht ist; eine *Welt* ist das, was
das Spiel eine Karte nennt.)

## Schnellstart {#quick-start}

Du brauchst Windows, Python 3.10 oder neuer (im Installer "Add python.exe to PATH"
ankreuzen), Arma Reforger über Steam installiert (wird von selbst gefunden) und etwa
200 MB Platz für eine kleine Welt wie Arland, mehr für die großen; Git ist nicht nötig.
Neu in der Kommandozeile? Lies zuerst [Vor dem Start](before-you-start.md).

```bash
python -m pip install https://github.com/Holdi601/3DHeat-Ext-Reforger/archive/refs/tags/v0.1.0.zip
heat3d-reforger-maps worlds                          # wo das Spiel liegt, und seine Welten
heat3d-reforger-maps world Arland -o Arland.glb      # eine Welt als Level
```

Die Installation bringt [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
mit, die Bibliothek, mit der es liest. `worlds` beginnt mit
`Arma Reforger at <the game's folder>: <n> worlds with a terrain` und listet eine Welt
pro Zeile; `world` endet mit seinem Bericht (`ground`, `structure`, `water`).
`Arland.glb` landet in dem Ordner, in dem du den Befehl ausgeführt hast, etwa 200 MB
in etwa 10 Sekunden; ohne `-o` heißt sie `<world>.glb`. Liegt das Spiel in keiner
Steam-Bibliothek, nenne seinen Ordner mit `--install "<Spielordner>"`.

Dann öffne die `.glb` im [3DHeat-Viewer](https://github.com/Holdi601/3DHeat#quick-start):
herunterladen (**Code -> Download ZIP**, entpacken), `start.bat` doppelklicken (es bietet
an, Node.js zu installieren, wenn es fehlt, und öffnet `http://127.0.0.1:5273`), dann
**Hintergrund / Level -> 3D-Modell...** und die Datei wählen
([Level laden](https://holdi601.github.io/3DHeat/levels.html)). Das Koordinatensystem des
Spiels ist linkshändig: **Weltachse invertieren** (unter **Kamera & Szene**) zeigt es
ungespiegelt. Das Level bleibt auf deinem Rechner.

Wenn ein neues Release erscheint, sagt das Werkzeug es beim Start und bietet an, sich
selbst zu aktualisieren.

Jeder Spiel-Leser ist ein eigenes kleines Projekt mit eigener Lizenzdatei, eigenen
Releases und eigenem Issue-Tracker. So lässt er sich für sich allein installieren,
aktualisieren, pflegen - oder auf Wunsch eines Rechteinhabers zurückziehen -, ohne den
Viewer oder die anderen Werkzeuge zu berühren.

## Seiten {#pages}

| Seite | Was sie behandelt |
|---|---|
| [Vor dem Start](before-you-start.md) | Python, GameFiles, ein Terminal, ein erster Lauf |
| [Arma-Reforger-Welten: worlds und world](level-arma-reforger.md) | das Auflisten der Welten, jede Option eines Exports, seine Teile, wie jedes Format gelesen und geprüft wird |
| [Eine Datei erkennen: identify](identify.md) | ob eine Datei ein Enfusion-Archiv, ein Gelände, eine Weltdatei oder eine Textur ist |
| [Bedingungen und Lizenz](terms.md) | was das Werkzeug liest, die Quellen, warum es ein eigenes Projekt ist |
| [Befehlsreferenz](../cli-reference.md) | jede Option, aus dem Code erzeugt |
| [Diese Dokumentation pflegen](maintaining.md) | die Checkliste für ein Release |

## Verwandtes {#related}

- Der 3DHeat-Viewer: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  Dokumentation unter [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): der glTF-Schreiber, die
  Steam-Bibliothekssuche und die Texturdekodierung, auf denen dieses Werkzeug aufbaut; seine
  `enfusion-worlds` und `enfusion-world` führen dieses Werkzeug aus, wenn es installiert ist.

## Die 3DHeat-Werkzeuge {#the-3dheat-tools}

| Werkzeug | Was es tut | Code | Docs |
|---|---|---|---|
| 3DHeat viewer | zeigt die Daten: Heatmaps, Rennanalyse, Matchauswertung | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | Level und Strecken aus den eigenen Dateien eines Spiels | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | Rundentelemetrie, und Level, die aus Spielvideos nachgebaut werden | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | ein Plugin für den Unreal Editor: ein Level als eine `.glb`-Datei | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike-2-Demos und -Karten | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | nimmt auf, was Spiele veröffentlichen, während du spielst | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War-Thunder-Replays | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World-of-Tanks-Replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World-of-Warships-Replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad-Serverdemos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS-World-Karten als 3D-Level | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2-Sturmovik-Karten als 3D-Level | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | die Dota-2-Karte als 3D-Level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | Dota-2-Replays als Tabellen | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | League-of-Legends- und VALORANT-Replays | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | Forza-Horizon-Strecken und Autos | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | Battlefield-6-Level als 3D-Level | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | BeamNG.drive-Strecken rund um deine Runden | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | Assetto-Corsa-Rally-Etappen rund um deine Runden | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | Arma-Reforger-Welten als 3D-Level | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | Rainbow-Six-Siege-Matchreplays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |
