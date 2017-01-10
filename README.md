# A rapid game development project template

## Requirements

[L×VE](http://love2d.org/)

[Moonscript](http://moonscript.org/)

[Python 3.x](https://www.python.org/), or you can make the script 2.x compatible

## Features

### General
- [X] One-click testing
- [ ] One-click Windows distribution

### Source
- [X] Mix `.moon` and `.lua` files
- [ ] Incremental Build
- [ ] Compile to bytecode

### Asset Pipeline
i.e. One-click Export

- [ ] [Aseprite](http://www.aseprite.org/)
- [ ] [Tiled](http://www.mapeditor.org/)


## Directory Structure

### `dynamic/`
These files will be processed before written to the output.

### `static/`
These files will be copied as-is to the output.

### `external/`
Simliar to `dynamic/`, except that these files will not be fused in the game executable. i.e. placed beside the executable.

When testing, same as `dynamic/`.