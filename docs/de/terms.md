---
title: Bedingungen und Lizenz
nav_order: 8
lang: "de"
source: terms.md
source_hash: "358a481eaf89"
nav_exclude: true
search_exclude: true
---
# Bedingungen und Lizenz {#terms-and-licence}

Diese Seite hält fest, was die Lizenzen sagen. Sie ist keine Rechtsberatung.

## Das Spiel von Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger und seine Welten gehören Bohemia Interactive, die dieses Projekt nicht
unterstützen. Dieses Werkzeug liefert nichts vom Spiel mit und lädt nichts herunter: Es
liest die Dateien der Kopie, die **du** installiert hast, auf deinem Rechner, außerhalb des
Spiels. Es ändert nichts am Spiel, läuft nicht neben ihm und spricht mit keinem Server.
Nichts in den Dateien des Spiels ist verschlüsselt, und nichts wird entschlüsselt.

Die Lizenz des Spiels erlaubt nichtkommerzielle Nutzung und verbietet das Reverse Engineering
der Spieldateien. Das Lesen deiner eigenen Installation ist deine Entscheidung unter dieser
Lizenz, und die Pflicht liegt bei der Person, die das Werkzeug ausführt. Die Welt, die es
schreibt, ist Inhalt des Spieleherausgebers: Sie ist für deinen eigenen Gebrauch gedacht, nicht
zum Teilen, Veröffentlichen oder Verkaufen. Die `.gitignore` des Repositorys hält Spieldateien
und Exporte nach Dateityp aus der Versionskontrolle heraus.

Bohemias eigener Zugang zu den Daten des Spiels ist **Arma Reforger Tools** (der Enfusion
Workbench), auf Steam kostenlos zum Erstellen von Mods unter Bohemias Modding-Bedingungen.
Dieses Werkzeug braucht es nicht und nutzt es nicht; es liest die Archive des installierten
Spiels direkt.

Darum ist es ein eigenes Paket: Wenn Bohemia Interactive jemals verlangt, dass es verschwindet,
geht es allein, und der Viewer, GameFiles und die anderen Werkzeuge bleiben.

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
