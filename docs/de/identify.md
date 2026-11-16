---
title: "Eine Datei erkennen: identify"
nav_order: 3
lang: "de"
source: identify.md
source_hash: "c7c88815247e"
nav_exclude: true
search_exclude: true
---
# Eine Datei erkennen: `identify` {#identifying-a-file-identify}

```bash
heat3d-reforger-maps identify <file>
```

sagt, ob eine Datei eine der Enfusion-Dateien ist, die dieses Werkzeug liest, und was sie
enthält, indem es sie liest und nicht ihren Namen:

| Datei | Erkannt an | Was es ausgibt |
|---|---|---|
| ein Archiv (`.pak`, in `addons\<addon>\`) | `FORM` ... `PAC1`, und ein Verzeichnis, das bis zu seinem Ende lesbar ist | die Anzahl der Dateien, wie viele davon zlib-komprimiert sind, ihre entpackte Größe |
| ein Gelände (`.terr`) | `FORM` ... `TERR` mit einem `HEAD`-Chunk | die Eckpunkte in beide Richtungen und ihr Abstand, die Blöcke einer Kachel |
| eine Geländekachel (`.ttile`) | `FORM` ... `TERR` mit einem `HGHT`-Chunk | ihre Chunks |
| eine Weltdatei (`.ent`) | `EBIN`, und Entitäten, die bis zum letzten Byte parsen | die Anzahl der Entitäten, Ressourcen-GUIDs und Namen |
| eine Textur (`.edds`) | ein DDS-Header mit der DX10-Erweiterung, und Stufen, die sich zur Dateigröße addieren | die Größe, die Stufen, das DXGI-Format, wie die Stufen gespeichert sind |

Die Dateien innerhalb eines Archivs werden über `world` gelesen; `identify` nimmt
Dateien auf der Festplatte, ein Archiv selbst oder eine aus einem Archiv entpackte Datei.

```text
data.pak  (<n> bytes)
  Enfusion archive (.pak)
    files      <n>, <n> of them zlib-compressed
    holds      <n> bytes unpacked
```

## Alles andere {#anything-else}

Eine Datei, die keine davon ist, gibt auf der Ausgabe nichts aus, auf der Fehlerausgabe
die Zeile `not an Arma Reforger file` und endet mit 2. Das gilt auch für eine einfache
`.dds`, obwohl eine `.edds` wie eine beginnt. Darauf verlässt sich das eigene
`identify` von [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): Für eine
Datei, die seine eigenen Leser nicht kennen, fragt es jedes installierte Spielewerkzeug der
Reihe nach, und das, das mit 0 endet, hat die Antwort.

| Meldung | Exit | Bedeutet |
|---|---|---|
| (eine Beschreibung wie oben) | 0 | eine Enfusion-Datei |
| `not an Arma Reforger file` | 2 | jede andere Datei |
| `no such file: <path>` | 2 | der Pfad ist falsch |
| `needs 3DHeat GameFiles: ...` | 2 | siehe [Vor dem Start](before-you-start.md) |
