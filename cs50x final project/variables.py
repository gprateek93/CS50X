#!/bin/python3

#Game variables that can be changed!

#game background colour.
BACKGROUNDCOLOUR = 'lightblue'

#map variables.
MAXTILES  = 40
MAPWIDTH  = 20
MAPHEIGHT = 20

#variables representing the different resources.
DIRT    = 0
GRASS   = 1
WATER   = 2
BRICK   = 3
WOOD    = 4
SAND    = 5
PLANK   = 6
GLASS   = 7

#a list of all game resources.
resources = [DIRT,GRASS,WATER,BRICK,WOOD,SAND,PLANK,GLASS]

#the names of the resources.
names = {
  DIRT    : 'dirt',
  GRASS   : 'grass',
  WATER   : 'water',
  BRICK   : 'brick',
  WOOD    :  'wood',
  SAND    :  'sand',
  PLANK   :  'plank',
  GLASS    :  'glass'
}

#a dictionary linking resources to images.
textures = {
  DIRT    : 'dirt.png',
  GRASS   : 'grass.png',
  WATER   : 'water.png',
  BRICK   : 'brick.png',
  WOOD    :  'wood.png',
  SAND    :  'sand.png',
  PLANK   :  'plank.png',
  GLASS   :  'glass.png'
}

#the number of each resource the player has.
inventory = {
  DIRT    : 10,
  GRASS   : 10,
  WATER   : 10,
  BRICK   : 0,
  WOOD    : 5,
  SAND    : 8,
  PLANK   : 0,
  GLASS   : 0
}

#the player image.
playerImg = 'player.png'

#the player position.
playerX = 0
playerY = 0

#rules to make new resources.
crafting = {
  BRICK    : { WATER : 1, DIRT : 2 },
  PLANK    : { BRICK : 3},
  GLASS    : { SAND  : 3}
}

#keys for placing resources.
placekeys = {
  DIRT  : '1',
  GRASS : '2',
  WATER : '3',
  BRICK : '4',
  WOOD  : '5',
  SAND  : '6',
  PLANK : '7',
  GLASS : '8'
}

#keys for crafting tiles.
craftkeys = {
  BRICK : 'r',
  PLANK : 't',
  GLASS : 'f'
}

#game instructions that are displayed.
instructions =  [
  'Instructions:',
  'Use WASD to move'
]
