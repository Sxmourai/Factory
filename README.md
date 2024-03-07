# ARCHIVED

I'm archiving this repo because I stopped working on this project, currently I'm working on a x86_64 operating system & all...
MAYBE I will work back on it, if I'm (re?)-interrested in game development & physics

# Factory

This is an automation game
I hope this game will interest you !

## Features

- Infinite canvas
- Live previews
- Infinite gameplay ?
- Easy download and start
- Cross platform

## Running

TODO

### Description

This is the part that I will use to put the project into my head. There will be user's description
(this one)
And the technical description (below).
You are a robot, that lost his only hard drive that had data on it. When building your factory you will find it back, but the data is corrupted. The more you do researchs, the more data you find on the hard drive... Maybe you will finally understand this little voice.
The game is on a grid, the map is infinite.
The game will have the following buildings:

- Hydrogen generator, will have different tiers, and will create hydrogen (maybe with energy... Working on it)
- Stars, to fuse the hydrogen into heavier materials (helium, carbon... Each new atoms will be kind of tiers for the star)
- More (let my imaginary get some rest first.)
Goal: Produce as much energy, and research. Find where you come from.

#### Technical description

                                        App class
                          Game class                                Menu-Controller
          Event-Controller        World    Camera                  Menus Buttons-controller *SC
    Event-Handler Keys-Handler  Builds PositionManager Renderer  
SC = SUBJECT TO CHANGE

Event-Handler: takes the pygame events, and process them.
Current problem: pygame_gui events go into pygame events, so the ui buttons from Menu-Controller are processed in Event-Handler.
Keys-Handler: Handles the movement of camera, and some keyboard shortcuts (building, exiting guis...)

Builds: The buildings that you can place in the world. See user's description for the list.
PositionManager: Manages position of the cursor, builds etc. SUBJECT TO CHANGE
Renderer: Renders the game and his objects.
Menus: Menus for the user e.g. Construct menu
Click events are SUBJECT TO CHANGE

Made with obsidian (also everything in notes/*)
