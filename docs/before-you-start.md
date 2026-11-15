---
title: Before you start
nav_order: 1.5
---

# Before you start

New to the command line? This page takes you from nothing to a first run.
It takes about fifteen minutes, once.

## 1. Install Python

This tool needs **Python 3.10 or later**.

- **Windows:** download Python from [python.org/downloads](https://www.python.org/downloads/)
  and run the installer. On its first screen, tick **Add python.exe to PATH**,
  then click **Install Now**.
- **macOS and Linux:** Python 3 is often there already. Where these pages say
  `python`, type `python3`.

## 2. Get this tool

Open [github.com/Holdi601/3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger), click the
green **Code** button, then **Download ZIP**, and unzip it into a folder of your
choice. If you use git: `git clone https://github.com/Holdi601/3DHeat-Ext-Reforger`.

## 3. 3DHeat GameFiles comes with it

The tool reads with [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/)
(its glTF writer, the Steam library search, the texture decoding). Step 5 installs
it for you. Without pip - a downloaded folder you run in place - put GameFiles
next to this tool as `3DHeat-GameFiles`, or set `HEAT3D_GAMEFILES` to its
folder; inside a 3DHeat checkout (`exporters/ext/reforger-maps`) it is found
in `exporters/gamefiles` on its own.

## 4. Open a terminal in that folder

A terminal is a window where you type commands.

- **Windows:** open the folder in Explorer, click into the address bar, type
  `powershell` and press Enter. A blue or black window opens, already in that
  folder.
- **macOS:** open **Terminal**, type `cd ` (with a space), drag the folder into
  the window and press Enter.

`cd` means "change folder": `cd C:\Tools\3DHeat-Ext-Reforger` goes to that folder.

## 5. Install the tool

Type this and press Enter:

```bash
python -m pip install -e .
```

You should see, at the end: `Successfully installed heat3d-ext-reforger-...`
(and `heat3d-gamefiles-...` with it).

## 6. Run it

```bash
heat3d-reforger-maps worlds
```

You should see something like:

```text
Arma Reforger at D:\Games\Steam\steamapps\common\Arma Reforger: <n> worlds with a terrain
  <world>                                  worlds/<world>/.../<world>.terr
  ...
```

Next: [Arma Reforger worlds](level-arma-reforger.md).

## How to read the commands on these pages

| You see | It means |
|---|---|
| `<world>` | a placeholder: type your own value instead, without the `< >` |
| `[--texture-size PIXELS]` | optional: leave it out, or type it as shown |
| `# a note` | a comment for you: do not type it |
| `"C:\My Files\x"` | put a path that has spaces in quotes |

## When something goes wrong

| The message | What to do |
|---|---|
| `'python' is not recognized` | Python is not installed, or the PATH box was not ticked: install it again and tick it (or type `py` instead of `python`). |
| `'heat3d-reforger-maps' is not recognized` | Run step 5 again in the tool's folder, or type `python -m heat3d_ext_reforger` instead of `heat3d-reforger-maps`: it does the same. |
| `needs 3DHeat GameFiles: ...` | Step 5 did not install it, or you run the folder in place: see step 3. |
| `Arma Reforger not found; ...` | Install the game through Steam, or give its folder (the one with `addons` in it): `--install "D:\Games\Arma Reforger"`. |
| `no world '<name>'; there are: ...` | Use one of the names the line lists, as `worlds` prints them. |
| anything else | Read the last line of the message, then open an issue on GitHub with it. |

Every command also ends with an **exit status**: 0 means it worked, 2 that
the game, the world, the file or GameFiles was not found, 1 that reading failed. To see
it, type `echo $LASTEXITCODE` in PowerShell or `echo $?` on macOS and Linux.
