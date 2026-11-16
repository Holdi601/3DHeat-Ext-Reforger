---
title: Termini e licenza
nav_order: 8
lang: "it"
source: terms.md
source_hash: "9c8f2a00998f"
nav_exclude: true
search_exclude: true
---
# Termini e licenza {#terms-and-licence}

Questa pagina dice cosa legge lo strumento, cosa include e da dove vengono le sue fonti.

## Il gioco di Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger e i suoi mondi appartengono a Bohemia Interactive. 3DHeat Reforger non è
affiliato a Bohemia Interactive né approvato da essa; Arma Reforger e i nomi e marchi
correlati appartengono ai rispettivi proprietari.

Questo strumento non include nulla del gioco - nessun contenuto del gioco, nessun codice del
gioco, nessuna DLL - e non scarica nulla: legge i file della copia **che hai** installato,
sul tuo computer, al di fuori del gioco. Non modifica nulla nel gioco, non gira insieme ad
esso e non parla con nessun server. Nessun file del gioco è cifrato, e nulla viene decifrato.

Il mondo che scrive resta sul tuo computer: è per uso personale, non da condividere,
pubblicare o vendere. Il `.gitignore` del repository tiene fuori dal controllo di versione i
file del gioco e le esportazioni, per tipo di file.

Ogni lettore di giochi è un piccolo progetto a sé, con il proprio file di licenza, le
proprie release e il proprio tracker delle segnalazioni: si può installare, aggiornare,
mantenere - o ritirare su richiesta di un titolare dei diritti - da solo, senza toccare
il visualizzatore né gli altri strumenti.

Titolari dei diritti: aprite una segnalazione su
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
rispondiamo rapidamente e rimuoviamo qualsiasi cosa su richiesta.

## I formati {#the-formats}

I lettori Enfusion (`enfusion.py`, `enfusionworld.py`) sono stati ricavati dai file installati di Arma Reforger
stessa, senza altre fonti. Bohemia Interactive pubblica i suoi script di gioco sotto la Arma Public License, che non
è compatibile con MIT; nessuno di essi è stato letto per questo lavoro né copiato. Come viene letto ogni formato, e
con cosa è stato verificato: [Mondi di Arma Reforger](level-arma-reforger.md#how-it-is-read-and-checked).

## Licenza e fonti {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSE)):
usalo, modificalo, distribuiscilo, commercialmente o no. Si basa su
[3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) (MIT) e richiede
numpy (BSD-3-Clause), Pillow (MIT-CMU) e lz4 (BSD-3-Clause); i test richiedono
pytest (MIT). Vedi
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSES.md).
