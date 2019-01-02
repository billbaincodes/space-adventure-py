# Python Text Adventure
# billBainCodes

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

### Player Setup ###$
class player:
  def __init__(self):
    self.name = ''
    self.job = ''
    self.hp = 0
    self.mana = 0
    self.status_effects = []
    self.location = 'a1'
    self.game_over = False
    
myPlayer = player()

### Title Screen ###
def title_screen_selections():
  option = input("> ")
  if option.lower() == ("play"):
    setup_game()
  elif option.lower() == ("quit"):
    sys.exit()
  while option.lower() not in ['play', 'help', 'quit']:
    print("Please enter a command.")
    option = input("> ")
    if option.lower() == ("play"):
      setup_game()
    elif option.lower() == ("quit"):
      sys.exit()

def title_screen():
  os.system('clear')
  print('#################################')
  print('#         LOST IN SPACE         #')
  print('#################################')
  print('             * Play *            ')
  print('             * Quit *            ')
  title_screen_selections()

### Map ###
###  |a1|a2|
###  |b1|b2|

ZONENAME = ""
DESCRIPTION = "description"
EXAMINATION = "examine"
SOLVED = False
UP = "up", "north"
DOWN = "down", "south"
LEFT = "left", "west"
RIGHT = "right", "east"

solved_places = {
                "a1" : False, "a2": False,
                "b1" : False, "b2" : False
                }

zonemap = {
  "a1": {
      ZONENAME: "Cockpit",
      DESCRIPTION: "The controls to your vessel.",
      EXAMINATION: "Large control panels dominate the room. A window shows stars outside whizzing by.",
      SOLVED: False,
      UP: None,
      DOWN: 'b1',
      LEFT: None,
      RIGHT: 'a2'
  },
  "a2": {
      ZONENAME: 'Labs',
      DESCRIPTION: "Onboard research laboratories",
      EXAMINATION: "A sparse room. Filled with bottles, chemicals and technological equipment.",
      SOLVED: False,
      UP: None,
      DOWN: 'b2',
      LEFT: 'a1',
      RIGHT: None
  },
  "b1": {
      ZONENAME: 'Medbay',
      DESCRIPTION: "A bay for medical and healing purposes.",
      EXAMINATION: "A sterile room with a table and medical tools. You see a \033[1;33;40m Walkie Talkie] on the floor",
      SOLVED: False,
      UP: 'a1',
      DOWN: None,
      LEFT: None,
      RIGHT: 'b2'
  },
  "b2": {
      ZONENAME: 'Dock',
      DESCRIPTION: "A dock for the escape pod.",
      EXAMINATION: "An empty room. The escape pod is missing!",
      SOLVED: False,
      UP: 'a2',
      DOWN: None,
      LEFT: 'b1',
      RIGHT: None
  }
}

### Game Interactivity ###
def print_location():
  print('\n' + ('#' * (4 + len(zonemap[myPlayer.location][DESCRIPTION]))))
  print('# ' + zonemap[myPlayer.location][DESCRIPTION] + ' #')
  print(('#' * (4 + len(zonemap[myPlayer.location][DESCRIPTION]))))

### Main Prompt ###
def prompt():
  print("What would you like to do?")
  action = input("> ")
  acceptable_actions = ['move', 'look', 'quit', 'use', 'help']
  while action.lower() not in acceptable_actions:
    print('Unknown action, try again.')
    action = input("> ")
  if action.lower() == 'quit':
    sys.exit()
  elif action.lower() == 'move':
    player_move()
  elif action.lower() == 'look':
    player_look()
  elif action.lower() == 'help':
    player_help()

### Player Movement ###
def player_move():
  ask = "Where would you like to move?\n(Up, Left, Down, Right)\n"
  desired_dest = input(ask)
  if desired_dest.lower() in ['up', 'north']:
    destination = zonemap[myPlayer.location][UP]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['left', 'west']:
    destination = zonemap[myPlayer.location][LEFT]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['right', 'east']:
    destination = zonemap[myPlayer.location][RIGHT]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['down', 'south']:
    destination = zonemap[myPlayer.location][DOWN]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)

def movement_handler(destination):
  print("\n" + "You have moved to " + zonemap[destination][ZONENAME] + ".")
  myPlayer.location = destination
  print_location()

### Look Command ###
def player_look():
  if zonemap[myPlayer.location][SOLVED]:
    print("You have already solved this zone")
  else:
    print(zonemap[myPlayer.location][EXAMINATION])

### Help Command ###
def player_help():
  os.system('clear')
  print("############# H E L P ###############")
  print("  Commands: Move, Look, Use, Help    ")
  prompt()

### Game Functionality ###

def main_game_loop():
  while myPlayer.game_over is False:
    prompt()
    # Where to handle if game has been beaten.

def setup_game():
  os.system('clear')

  ### Name Request
  question1 = "Hello, what's your name?\n"
  for character in question1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  player_name = input("> ")
  myPlayer.name = player_name

  ### Job Request
  question2 = "What is your job?\n(Scientist, Pilot, Tech)\n"
  question2invalid = "Valid jobs are, Scientist, Pilot and Tech\n"
  for character in question2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  player_job = input("> ")
  valid_jobs = ['scientist', 'pilot', 'tech']
  if player_job.lower() in valid_jobs:
    myPlayer.job = player_job
    print("You are now a " + player_job + "!\n")
  while myPlayer.job.lower() not in valid_jobs:
    for character in question2invalid:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.05)
    player_job = input("> ")
    if player_job.lower() in valid_jobs:
      myPlayer.job = player_job
      print("You are now a " + player_job + "!\n")

  ### Stat Assignment
  if myPlayer.job is 'scientist':
    self.hp = 25
    self.mp = 75
  elif myPlayer.job is 'pilot':
    self.hp = 75
    self.mp = 25
  elif myPlayer.job is 'tech':
    self.hp = 50
    self.mp = 50

  ### Introduction
  question3 = "Welcome, " + myPlayer.name + " the " + myPlayer.job + "."
  for character in question3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  time.sleep(1)

  speech1 = "You awaken in an empty spaceship.\n"
  speech2 = "The rest of your crew is missing.\n"
  speech3 = "Try to figure out why...\n"
  speech4 = "heh. heh.. heh...\n"

  os.system('clear')
  for character in speech1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.04)
  for character in speech2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.04)
  for character in speech3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.08)
  for character in speech4:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.18)
  time.sleep(0.5)

  os.system('clear')
  print('###############################')
  print('#          Lets Begin         #')
  print('###############################')
  print('Commands: Move, Look, Use, Help\n')
  main_game_loop()


title_screen()