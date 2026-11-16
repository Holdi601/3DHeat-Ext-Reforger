---
title: "Identificare un file: identify"
nav_order: 3
lang: "it"
source: identify.md
source_hash: "c7c88815247e"
nav_exclude: true
search_exclude: true
---
# Identificare un file: `identify` {#identifying-a-file-identify}

```bash
heat3d-reforger-maps identify <file>
```

dice se un file è uno dei file Enfusion che questo strumento legge, e cosa contiene, leggendolo anziché
basandosi sul nome:

| File | Riconosciuto da | Cosa stampa |
|---|---|---|
| un archivio (`.pak`, in `addons\<addon>\`) | `FORM` ... `PAC1`, e una directory che si legge fino alla fine | il numero di file, quanti sono compressi con zlib, la loro dimensione decompressa |
| un terreno (`.terr`) | `FORM` ... `TERR` con un chunk `HEAD` | i vertici nei due sensi e la loro spaziatura, i blocchi di una tessera |
| una tessera di terreno (`.ttile`) | `FORM` ... `TERR` con un chunk `HGHT` | i suoi chunk |
| un file di mondo (`.ent`) | `EBIN`, e entità che si analizzano fino all'ultimo byte | il numero di entità, i GUID e i nomi delle risorse |
| una texture (`.edds`) | un'intestazione DDS con l'estensione DX10, e record di livello che sommano alla dimensione del file | la dimensione, i livelli, il formato DXGI, come sono memorizzati i livelli |

I file dentro un archivio si leggono tramite `world`; `identify` prende file su disco, un archivio stesso o un
file estratto da uno.

```text
data.pak  (<n> bytes)
  Enfusion archive (.pak)
    files      <n>, <n> of them zlib-compressed
    holds      <n> bytes unpacked
```

## Tutto il resto {#anything-else}

Un file che non è nessuno di questi stampa nulla sull'output, la riga
`not an Arma Reforger file` sul flusso degli errori, ed esce con 2 - anche un `.dds` semplice, anche se un
`.edds` inizia come lui. È quello su cui si basa il comando `identify` di
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/): per un file che i suoi lettori non conoscono,
chiede a ogni strumento di gioco installato a turno, e quello che esce con 0 ha la risposta.

| Messaggio | Uscita | Significa |
|---|---|---|
| (una descrizione come sopra) | 0 | un file Enfusion |
| `not an Arma Reforger file` | 2 | ogni altro file |
| `no such file: <path>` | 2 | il percorso è sbagliato |
| `needs 3DHeat GameFiles: ...` | 2 | vedi [Prima di iniziare](before-you-start.md) |
