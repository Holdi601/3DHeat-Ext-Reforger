---
title: Home
nav_order: 1
lang: "it"
source: index.md
source_hash: "6e5d4ee92caa"
nav_exclude: true
search_exclude: true
permalink: /it/
---
# 3DHeat Reforger {#dheat-reforger}

**Che cos'è?** Questo strumento trasforma un mondo di Arma Reforger, letto dalla **tua
installazione**, in un livello 3D - un modello della mappa sopra cui puoi volare - per il visualizzatore
[3DHeat](https://github.com/Holdi601/3DHeat)
([documentazione](https://holdi601.github.io/3DHeat/)): il terreno nei suoi colori, il mare e ogni edificio
e oggetto che il mondo colloca, come un riquadro.

**Perché usarlo?** Perché il calore di Arma Reforger abbia sotto di sé il suolo e gli edifici, nei metri del
gioco stesso: nessun posizionamento o ridimensionamento nel visualizzatore.

**Esempio:** `heat3d-reforger-maps world <world> -o world.glb` -> `world.glb`.
(*Enfusion* è il motore con cui è fatto Arma Reforger; un *mondo* è ciò che il gioco chiama mappa.)

## Avvio rapido {#quick-start}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).
Ti servono Python 3.10 o successivo, [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(la libreria con cui questo strumento legge) e Arma Reforger installato tramite Steam.
Esegui questi comandi nella cartella in cui hai clonato o decompresso lo strumento:

```bash
python -m pip install -e .                          # installa heat3d-reforger-maps, e con esso GameFiles
heat3d-reforger-maps worlds                         # dove si trova il gioco, e i suoi mondi
heat3d-reforger-maps world <world> -o world.glb     # un mondo come livello
```

`worlds` inizia con `Arma Reforger at <the game's folder>: <n> worlds with a terrain`
e elenca un mondo per riga; `world` termina con il suo rapporto (`ground`,
`structure`, `water`). Poi carica `world.glb` nel pannello **Sfondo / livello** del visualizzatore
([caricare un livello](https://holdi601.github.io/3DHeat/levels.html)).

Il livello è costruito dai file del gioco: resta **sul tuo computer**, per visualizzarlo, non per
condividerlo o pubblicarlo ([Termini](terms.md)).

Ogni lettore di giochi è un piccolo progetto a sé, con il proprio file di licenza, le
proprie release e il proprio tracker delle segnalazioni: si può installare, aggiornare,
mantenere - o ritirare su richiesta di un titolare dei diritti - da solo, senza toccare
il visualizzatore né gli altri strumenti.

## Pagine {#pages}

| Pagina | Cosa contiene |
|---|---|
| [Prima di iniziare](before-you-start.md) | Python, GameFiles, un terminale, una prima esecuzione |
| [Mondi di Arma Reforger: worlds e world](level-arma-reforger.md) | elencare i mondi, ogni opzione di un'esportazione, le sue parti, come è letto e verificato ogni formato |
| [Identificare un file: identify](identify.md) | se un file è un archivio Enfusion, un terreno, un file di mondo o una texture |
| [Termini e licenza](terms.md) | cosa legge lo strumento, le fonti, perché è un progetto a sé |
| [Riferimento dei comandi](../cli-reference.md) | ogni opzione, generata dal codice |
| [Manutenzione di questa documentazione](maintaining.md) | la lista di controllo per ogni rilascio |

## Collegamenti {#related}

- Il visualizzatore 3DHeat: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentazione su [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): lo scrittore glTF, la ricerca nelle
  librerie Steam e la decodifica delle texture su cui si basa questo strumento; i suoi `enfusion-worlds` e
  `enfusion-world` lanciano questo strumento quando è installato.

## Gli strumenti 3DHeat {#the-3dheat-tools}

| Strumento | Cosa fa | Codice | Documentazione |
|---|---|---|---|
| visualizzatore 3DHeat | mostra i dati: mappe di calore, analisi di gara, revisione delle partite | [3DHeat](https://github.com/Holdi601/3DHeat) | [documentazione](https://holdi601.github.io/3DHeat/) |
| GameFiles | livelli e percorsi dai file propri di un gioco | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [documentazione](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | telemetria dei giri, e livelli ricostruiti dal video di gioco | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [documentazione](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin per Unreal Editor: un livello come un unico `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [documentazione](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | demo e mappe di Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [documentazione](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | registra ciò che i giochi pubblicano mentre giochi | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [documentazione](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | replay di War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | replay di World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | replay di World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | demo dei server di Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | mappe di DCS World come livelli 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [documentazione](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | mappe di IL-2 Sturmovik come livelli 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [documentazione](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | la mappa di Dota 2 come livello 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | replay di Dota 2 come tabelle | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [documentazione](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | replay di League of Legends e VALORANT | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | percorsi e auto di Forza Horizon | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | livelli di Battlefield 6 come livelli 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | percorsi di BeamNG.drive intorno ai tuoi giri | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [documentazione](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | tappe di Assetto Corsa Rally intorno ai tuoi giri | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [documentazione](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mondi di Arma Reforger come livelli 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | replay di partite di Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [documentazione](https://holdi601.github.io/3DHeat-Ext-R6/) |
