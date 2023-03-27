# Pokemon Game Wiki Generator

Credit to [@FredericDlugi's](https://github.com/FredericDlugi) original [platinum renegade wiki](https://github.com/FredericDlugi/platinum-renegade-wiki) that served as base design and idea for this project. This project mainly serves as a way to create user-friendly documentation for new and existing pokemon rom hacks (and maybe fan games down the line)

This ReadMe will ser as a step-by-step guide to generating and deploying your own versions of the platinum-renegade-wiki.

## Step 1 - Preparing Large Data
NB: _The current scope is limited to existing pokemon and moves. Therefore, it's not currently possible to add fakemon data. This can be added in a later version_

Before any of the documentation can be generated, all the data has to be prepared. This is all done in the `prepare_large_data.py` file. You can prepare pokemon data, moves, machines and sprites.

### Pokemon
Command to download current pokemon data up to a specified range. The pokemon data will be stored in `temp/pokemon.json`.
```
python prepare_large_data.py --pokemon [--range, -r] <range_start> <range_end>
```
For example `python prepare_large_data.py --pokemon -r 1 5` will download pokemon data from Bulbasaur to Charmeleon

### Moves and Technical Machines
Command will download all current moves and technical machines in pokemon. The moves and technical machines will be downloaded to the `/temp/moves.json` and `temp/machines.json` respectively.
```
python prepare_large_data.py --moves --machines
```

### Sprites
Command will download current pokemon sprites up to the specified range. The sprites will be downloaded to the `/docs/img/pokemon` folder.
```
python prepare_large_data.py --sprites [--range, -r] <range_start> <range_end>
```
Usage is the same as Pokemon section above

## Step 2 - Data Modification
Naturally, since this is for rom hacks, data for pokemon, moves, routes, encounter, etc. are be modifiable.

I built a separate interface to make this goal easier to accomplish. Currently you can edit pokemon and moves. Routes, encounters, trainers etc will be added down the line
NB: The interface is currently a separate react project. [wiki-generator-interface](https://github.com/AkeemAllen/wiki-generator-interface). I plan on tieing it together with this project to make everything more cohesive.

## Step 3 - Generation
Now for the meat of the matter
Once you're satisfied with the modifications you've made, you can run `python generate-wiki.py` to generate your wiki!