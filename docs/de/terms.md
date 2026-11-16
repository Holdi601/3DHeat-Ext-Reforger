---
title: Bedingungen und Lizenz
nav_order: 8
lang: "de"
source: terms.md
source_hash: "9c8f2a00998f"
nav_exclude: true
search_exclude: true
---
# Bedingungen und Lizenz {#terms-and-licence}

Diese Seite sagt, was das Werkzeug liest, was es mitliefert und woher seine Quellen
stammen.

## Das Spiel von Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger und seine Welten gehören Bohemia Interactive. 3DHeat Reforger ist nicht mit
Bohemia Interactive verbunden und wird von Bohemia Interactive nicht unterstützt; Arma
Reforger sowie zugehörige Namen und Marken gehören ihren Inhabern.

Dieses Werkzeug liefert nichts vom Spiel mit - keine Spielinhalte, keinen Spielcode, keine
DLLs - und lädt nichts herunter: Es liest die Dateien der Kopie, die **du** installiert hast,
auf deinem Rechner, außerhalb des Spiels. Es ändert nichts am Spiel, läuft nicht neben ihm
und spricht mit keinem Server. Nichts in den Dateien des Spiels ist verschlüsselt, und
nichts wird entschlüsselt.

Die Welt, die es schreibt, bleibt auf deinem Rechner: Sie ist für deinen eigenen Gebrauch
gedacht, nicht zum Teilen, Veröffentlichen oder Verkaufen. Die `.gitignore` des Repositorys
hält Spieldateien und Exporte nach Dateityp aus der Versionskontrolle heraus.

Jeder Spiel-Leser ist ein eigenes kleines Projekt mit eigener Lizenzdatei, eigenen
Releases und eigenem Issue-Tracker. So lässt er sich für sich allein installieren,
aktualisieren, pflegen - oder auf Wunsch eines Rechteinhabers zurückziehen -, ohne den
Viewer oder die anderen Werkzeuge zu berühren.

Rechteinhaber: Eröffnet ein Issue unter
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
wir antworten schnell und entfernen auf Anfrage alles.

## Die Formate {#the-formats}

Die Enfusion-Leser (`enfusion.py`, `enfusionworld.py`) wurden allein aus den installierten
Dateien von Arma Reforger erarbeitet, ohne andere Quelle. Bohemia Interactive veröffentlicht
seine Spielskripte unter der Arma Public License, die nicht mit MIT kompatibel ist; keines
davon wurde dafür gelesen oder kopiert. Wie jedes Format gelesen wird und woran es geprüft
wurde: [Arma-Reforger-Welten](level-arma-reforger.md#how-it-is-read-and-checked).

## Lizenz und Quellen {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSE)):
benutzen, ändern, weitergeben, kommerziell oder nicht. Es baut auf
[3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) (MIT) auf und braucht numpy
(BSD-3-Clause), Pillow (MIT-CMU) und lz4 (BSD-3-Clause); die Tests brauchen pytest (MIT). Siehe
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSES.md).
