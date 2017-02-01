# A rapid game development project template

## Requirements

[LÖVE](http://love2d.org/) of **any** version

[Moonscript](http://moonscript.org/)

[Python](https://www.python.org/) 3.x, or you can make the build scripts 2.x compatible

## Features & Usage

### One-click Build
`build.py`

You may (and likely) need to change variables named `EXE_*` in `build.py`.

### One-click Testing
Firstly, make sure `build.py` is functional.

For Windows, run `test.cmd`.
For other systems,
```
python build.py
love _out/src
```

### One-click Distribution - Windows
Before you do that, please see inside `build_win.py` and set the correct `EXE_LOVE_DIR`.
Also, make sure you can test your game.

Run `build_win.py`.

### Source Compiling

- [X] Mix `.moon` and `.lua` files
- [x] Incremental Build (caution: do not build twice in 1 second)
- [ ] Compile to bytecode

### Asset Pipeline
i.e. auto-process in one click

- [X] [Aseprite](http://www.aseprite.org/)
- [X] [Tiled](http://www.mapeditor.org/)


## Directory Structure
Those directories don't need to exist.

### `dynamic/`
These files will be processed before written to the output.

Files that are not end in any of the following extensions are ignored.
- [X] `.lua`: lua script
- [X] `.moon` -> `.lua`: moonscript script
- [X] `.ase` or `.aseprite` -> `.png`: Aseprite document (image)
- [X] `.tmx` -> `.lua`: Tiled document (map)

Make sure you put your "raw" assets here!

### `static/`
These files will be copied as-is to the output.

### `external/`
Simliar to `dynamic/`, except that these files will not be fused in the game executable. i.e. placed beside the executable.
When testing, same as `dynamic/`.

Files inside `external/` will be processed but **not a single file is ignored**.