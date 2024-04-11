# BetterDatapack
A simple Minecraft Datapack preprocessor written in python.


## Usage

```
$ py -m bdp --help
usage: bdp [-h] [--output OUTPUT] datapack

positional arguments:
  datapack              The datapack folder you wish to compile. Must contain *.btr.mcfunction files.

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        The output datapack folder.
```

Unprocessed BDP files have the extension `.btr.mcfunction`.

### Example
```bash
py -m bdp main -o datapack
```

## Syntax
### Code Blocks
Code blocks are preprocessed now, turning:
```mcfunction
execute as @a[name="RedBigz"] run ${
    say Hello, World!
    give @s minecraft:diamond 64
}$
```
into:
```mcfunction
execute as @a[name="RedBigz"] run function <uuid>:<fsid>
```

`<uuid>/functions/<fsid>.mcfunction`:
```mcfunction
    say Hello, World!
    give @s minecraft:diamond 64
```