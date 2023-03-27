# Pokemon Game Wiki Generator

Credit to [@FredericDlugi's](https://github.com/FredericDlugi) original [platinum renegade wiki](https://github.com/FredericDlugi/platinum-renegade-wiki) that served as base design and idea for this project. This project mainly serves as a way to create user-friendly documentation for new and existing pokemon rom hacks (and maybe fan games down the line)

This Readme is a guide to generating and deploying your own versions of the platinum-renegade-wiki.

## Step 1 - Preparing Large Data
NB: _The current scope is limited to existing pokemon and moves. So you won't be able to prepare something like fakemon data. This can hopefully be added in a later version_

Before any of the documentation can be generated, all the data has to be prepared. This is all done in the `prepare_large_data.py` file. You can prepare pokemon data, moves, machines and sprites.

### Pokemon
The following command will download current pokemon data up to a specified range. The pokemon data will be store in `temp/pokemon.json` for use throughout the documentation generation process.
```
python prepare_large_data.py --pokemon [--range, -r] <range_start> <range_end>
```
For example `python prepare_large_data.py --pokemon -r 1 5` will download pokemon data from Bulbasaur to Charmeleon

### Moves and Technical Machines
The following command will download all current moves and technical machines in pokemon. The moves and technical machines will be downloaded to the `/temp/moves.json` and `temp/machins.json` respectively.
```
python prepare_large_data.py --moves --machines
```

### Sprites
The following command will download current pokemon sprites up to the specified range. The sprites will be downloaded to the `/docs/img/pokemon` folder
```
python prepare_large_data.py --sprites [--range, -r] <range_start> <range_end>
```
