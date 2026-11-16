---
title: Termini e licenza
nav_order: 8
lang: "it"
source: terms.md
source_hash: "358a481eaf89"
nav_exclude: true
search_exclude: true
---
# Termini e licenza {#terms-and-licence}

Questa pagina registra ciò che dicono le licenze, non è un parere legale.

## Il gioco di Bohemia Interactive {#bohemia-interactives-game}

Arma Reforger e i suoi mondi appartengono a Bohemia Interactive, che non approva questo progetto. Questo
strumento non include nulla del gioco e non scarica nulla: legge i file della copia **che hai** installato,
sul tuo computer, al di fuori del gioco. Non modifica nulla nel gioco, non gira insieme ad esso e non parla
con nessun server. Nessun file del gioco è cifrato, e nulla viene decifrato.

La licenza del gioco consente l'uso non commerciale e vieta l'ingegneria inversa dei file del gioco. Leggere la
tua installazione è una tua decisione sotto quella licenza, e l'obbligo ricade su chi esegue lo strumento. Il
mondo che scrive è contenuto dell'editore del gioco: è per uso personale, non da condividere, pubblicare o
vendere. Il repository `.gitignore` tiene fuori dal controllo di versione i file del gioco e le esportazioni, per tipo di file.

Il percorso ufficiale di Bohemia verso i dati del gioco è **Arma Reforger Tools** (l'Enfusion Workbench), gratuito
su Steam per creare mod secondo i termini di modding di Bohemia. Questo strumento non ne ha bisogno e non lo usa;
legge direttamente gli archivi del gioco installato.

Per questo è un pacchetto a sé: se Bohemia Interactive un giorno chiedesse di ritirarlo, andrebbe ritirato da solo,
e il visualizzatore, GameFiles e gli altri strumenti restano.

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
