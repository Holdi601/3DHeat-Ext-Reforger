---
title: Prima di iniziare
nav_order: 1.5
lang: "it"
source: before-you-start.md
source_hash: "0b6fa46724ea"
nav_exclude: true
search_exclude: true
---
# Prima di iniziare {#before-you-start}

Non hai mai usato la riga di comando? Questa pagina ti porta da zero a una prima esecuzione.
Richiede circa quindici minuti, una volta sola.

## 1. Installa Python {#install-python}

Questo strumento richiede **Python 3.10 o successivo**.

- **Windows:** scarica Python da [python.org/downloads](https://www.python.org/downloads/)
  ed esegui il programma di installazione. Nella sua prima schermata spunta **Add python.exe to PATH**,
  poi clicca su **Install Now**.
- **macOS e Linux:** Python 3 spesso c'è già. Dove queste pagine dicono
  `python`, scrivi `python3`.

## 2. Ottieni questo strumento {#get-this-tool}

Apri [github.com/Holdi601/3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger), clicca sul
pulsante verde **Code**, poi su **Download ZIP**, e decomprimilo in una cartella a tua scelta.
Se usi git: `git clone https://github.com/Holdi601/3DHeat-Ext-Reforger`.

## 3. Con lo strumento arriva 3DHeat GameFiles {#dheat-gamefiles-comes-with-it}

Lo strumento legge con [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(il suo scrittore glTF, la ricerca nelle librerie Steam, la decodifica delle texture). Il passo 5 lo
installa per te. Senza pip - una cartella scaricata che esegui sul posto - metti GameFiles accanto a
questo strumento come `3DHeat-GameFiles`, oppure imposta `HEAT3D_GAMEFILES` con la sua cartella; dentro un
checkout di 3DHeat (`exporters/ext/reforger-maps`) viene trovato da solo in `exporters/gamefiles`.

## 4. Apri un terminale in quella cartella {#open-a-terminal-in-that-folder}

Un terminale è una finestra in cui scrivi i comandi.

- **Windows:** apri la cartella in Esplora risorse, clicca nella barra degli indirizzi, scrivi
  `powershell` e premi Invio. Si apre una finestra blu o nera, già in quella cartella.
- **macOS:** apri **Terminale**, scrivi `cd ` (con lo spazio), trascina la cartella nella
  finestra e premi Invio.

`cd` significa "cambia cartella": `cd C:\Tools\3DHeat-Ext-Reforger` va in quella cartella.

## 5. Installa lo strumento {#install-the-tool}

Scrivi questo e premi Invio:

```bash
python -m pip install -e .
```

Alla fine dovresti vedere: `Successfully installed heat3d-ext-reforger-...`
(e `heat3d-gamefiles-...` insieme ad esso).

## 6. Eseguilo {#run-it}

```bash
heat3d-reforger-maps worlds
```

Dovresti vedere qualcosa del genere:

```text
Arma Reforger at D:\Games\Steam\steamapps\common\Arma Reforger: <n> worlds with a terrain
  <world>                                  worlds/<world>/.../<world>.terr
  ...
```

Avanti: [Mondi di Arma Reforger](level-arma-reforger.md).

## Come leggere i comandi di queste pagine {#how-to-read-the-commands-on-these-pages}

| Vedi | Significa |
|---|---|
| `<world>` | un segnaposto: scrivi invece il tuo valore, senza i `< >` |
| `[--texture-size PIXELS]` | facoltativo: omettilo, oppure scrivilo come mostrato |
| `# a note` | un commento per te: non scriverlo |
| `"C:\My Files\x"` | metti tra virgolette un percorso che contiene spazi |

## Quando qualcosa va storto {#when-something-goes-wrong}

| Il messaggio | Cosa fare |
|---|---|
| `'python' is not recognized` | Python non è installato, oppure non era spuntata la casella PATH: installalo di nuovo e spuntala (o scrivi `py` al posto di `python`). |
| `'heat3d-reforger-maps' is not recognized` | Esegui di nuovo il passo 5 nella cartella dello strumento, oppure scrivi `python -m heat3d_ext_reforger` al posto di `heat3d-reforger-maps`: fa la stessa cosa. |
| `needs 3DHeat GameFiles: ...` | Il passo 5 non l'ha installato, oppure esegui la cartella sul posto: vedi il passo 3. |
| `Arma Reforger not found; ...` | Installa il gioco tramite Steam, oppure indica la sua cartella (quella con dentro `addons`): `--install "D:\Games\Arma Reforger"`. |
| `no world '<name>'; there are: ...` | Usa uno dei nomi che la riga elenca, come li stampa `worlds`. |
| qualsiasi altra cosa | Leggi l'ultima riga del messaggio, poi apri una segnalazione su GitHub con quella riga. |

Ogni comando termina anche con uno **stato di uscita**: 0 significa che ha funzionato, 2 che
il gioco, il mondo, il file o GameFiles non sono stati trovati, 1 che la lettura è fallita. Per vederlo,
scrivi `echo $LASTEXITCODE` in PowerShell oppure `echo $?` su macOS e Linux.
