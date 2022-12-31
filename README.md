# Factory

This is an automation game, inspired by the mobile game "Reactor". \
There will be multiblocks. \
I hope this game will interest you !

## Features

- Infinite canvas
- Live previews
- Infinite gameplay ?
- Easy download and start
- Cross platform


## Running

To run this project type:

Install the modules:
```bash
  pip install -r requirements.txt
```
Run the program !
```bash
  python main.py
```

### Description
This is the part that I will use to put the project into my head. There will be user's description
(this one)
And the technical description (below).
This game is inspired by Reactor. The game is on a grid, the map is infinite.
The game has the following buildings:
- The factory, produces points.
- The core, usefull for research.
- The generator, multiplies the production of the factories.

Goal: Get as much points, and research

#### Technical description
                                    Game class
          Event-Controller        World    Camera                          Menu-Controller 
    Event-Handler Keys-Handler  Builds PositionManager Renderer   Menus Click events go into Event-Handler
                                                                                    ^problem^

Event-Handler: takes the pygame events, and process them.
Current problem: pygame_gui events go into pygame events, so the ui buttons from Menu-Controller are processed in Event-Handler.
Keys-Handler: Handles the movement of camera, and some keyboard shortcuts (building, exiting guis...)

Builds: The buildings that you can place in the world. See user's description for the list.
PositionManager: Manages position of the cursor, builds etc. SUBJECT TO CHANGE
Renderer: Renders the game and his objects.
Menus: Menus for the user e.g. Construct menu
Click events are SUBJECT TO CHANGE