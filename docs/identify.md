---
title: "Identifying a file: identify"
nav_order: 3
---

# Identifying a file: `identify`

```bash
heat3d-reforger-maps identify <file>
```

says whether a file is one of the Enfusion files this tool reads, and what it
holds, by reading it rather than by its name:

| File | Recognised by | What it prints |
|---|---|---|
| an archive (`.pak`, in `addons\<addon>\`) | `FORM` ... `PAC1`, and a directory that reads to its end | the number of files, how many are zlib-compressed, their size unpacked |
| a terrain (`.terr`) | `FORM` ... `TERR` with a `HEAD` chunk | the vertices each way and their spacing, the blocks of a tile |
| a terrain tile (`.ttile`) | `FORM` ... `TERR` with a `HGHT` chunk | its chunks |
| a world file (`.ent`) | `EBIN`, and entities that parse to the last byte | the number of entities, resource GUIDs and names |
| a texture (`.edds`) | a DDS header with the DX10 extension, and level records that add up to the file | the size, the levels, the DXGI format, how the levels are stored |

The files inside an archive are read through `world`; `identify` takes files on
disk, an archive itself or a file unpacked from one.

```text
data.pak  (<n> bytes)
  Enfusion archive (.pak)
    files      <n>, <n> of them zlib-compressed
    holds      <n> bytes unpacked
```

## Anything else

A file that is none of these prints nothing on the output, the line
`not an Arma Reforger file` on the error output, and exits with 2 - a plain
`.dds` too, even though an `.edds` starts like one. That is what
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)' own
`identify` relies on: for a file its own readers do not know, it asks each
installed game tool in turn, and the one that exits with 0 has the answer.

| Message | Exit | Means |
|---|---|---|
| (a description as above) | 0 | an Enfusion file |
| `not an Arma Reforger file` | 2 | any other file |
| `no such file: <path>` | 2 | the path is wrong |
| `needs 3DHeat GameFiles: ...` | 2 | see [Before you start](before-you-start.md) |
