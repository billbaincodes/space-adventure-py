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
  def __init__(self, name='initial name', job='initial job', hp=0, mana=0, status_effects=[], location='a1', game_over=False):
    self.name = name
    self.job = job
    self.hp = hp
    self.mana = mana
    self.status_effects = status_effects
    self.location = location
    self.game_over = game_over

myPlayer = player()

### Puzzles / Solutions ###

def medbay_solution():
  statement1 = "Hello...?\n"
  statement2 = myPlayer.name + "??\n"
  statement3 = "It's Tara, I'm outside the ship replacing our solar panels.\n"
  statement4 = "Open the hatch to let me in, I set the password to 505!\n"

  os.system('clear')
  flush_speech(statement1, 0.2)
  flush_speech(statement2, 0.035)
  flush_speech(statement3, 0.05)
  flush_speech(statement4, 0.05)
  time.sleep(0.5)

def dock_solution():
  print("what is the password?\n")
  password = input("> ")
  if password == "505":
    statement1 = "Thanks " + myPlayer.name + "!\n"
    statement2 = "Hey, where is everybody ?\n"
    statement3 = "I'd look for Clarence in the lab, but I need to start fixing these!\n"

    os.system('clear')
    flush_speech(statement1, 0.05)
    flush_speech(statement2, 0.08)
    flush_speech(statement3, 0.05)
    time.sleep(0.5)
  else:
    print("\033[1;31;40mACCESS DENIED\033[0;37m")
    print(">:(")

### Map ###
###  |a1|a2|
###  |b1|b2|

ZONENAME = "zonename"
DESCRIPTION = "description"
PUZ_EXAMINATION = "puzzle examine"
SOL_EXAMINATION = 'solved examine'
ITEM = "item"
SOLUTION = "solution"
SOLVED = False
UP = "up", "north"
DOWN = "down", "south"
LEFT = "left", "west"
RIGHT = "right", "east"

zonemap = {
  "a1": {
      ZONENAME: "Cockpit",
      DESCRIPTION: "The controls to your vessel.",
      PUZ_EXAMINATION: "Large control panels dominate the room. A window shows stars outside passing by.",
      SOL_EXAMINATION: "A sparse room. Filled with bottles, chemicals and technological equipment.",
      SOLUTION: 'pit solution',
      ITEM: 'pit item',
      SOLVED: False,
      UP: None,
      DOWN: 'b1',
      LEFT: None,
      RIGHT: 'a2'
  },
  "a2": {
      ZONENAME: 'Labs',
      DESCRIPTION: "Onboard research laboratories",
      PUZ_EXAMINATION: "A sparse room. Filled with bottles, chemicals and technological equipment.",
      SOL_EXAMINATION: "A sparse room. Filled with bottles, chemicals and technological equipment.",
      SOLUTION: 'lab solution',
      ITEM: 'lab item',
      SOLVED: False,
      UP: None,
      DOWN: 'b2',
      LEFT: 'a1',
      RIGHT: None
  },
  "b1": {
      ZONENAME: 'Medbay',
      DESCRIPTION: "A bay for medical and healing purposes.",
      PUZ_EXAMINATION: "A sterile room with a table and medical tools. You see a \033[1mWalkie Talkie\033[0;37m on the table.",
      SOL_EXAMINATION: "A sterile room with a table and medical tools. You see an empty table.",
      SOLUTION: medbay_solution,
      ITEM: 'walkie talkie',
      SOLVED: False,
      UP: 'a1',
      DOWN: None,
      LEFT: None,
      RIGHT: 'b2'
  },
  "b2": {
      ZONENAME: 'Dock',
      DESCRIPTION: "A dock for the escape pod.",
      PUZ_EXAMINATION: "An open room with escape pods against the wall and a large \033[1mhatch\033[0;37m to the ship's exterior",
      SOL_EXAMINATION: "An open room with escape pods against the wall. Tara is inspecting broken solar panels on the floor.",
      SOLUTION: dock_solution,
      ITEM: 'hatch',
      SOLVED: False,
      UP: 'a2',
      DOWN: None,
      LEFT: 'b1',
      RIGHT: None
  }
}


### Title Screen ###
def title_screen_selections():
  option = input("> ")
  if option.lower() == ("play"):
    setup_game()
  elif option.lower() == ("quit"):
    sys.exit()
  while option.lower() not in ['play', 'help', 'quit']:
    print("Please enter a valid command. (play, quit)`")
    option = input("> ")
    if option.lower() == ("play"):
      setup_game()
    elif option.lower() == ("quit"):
      sys.exit()

def title_screen():
  os.system('clear')
  print('\033[0;37m---------------------------------')
  print('|         LOST IN SPACE         |')
  print('---------------------------------')
  print('             * Play *            ')
  print('             * Quit *            ')
  title_screen_selections()

### Game Interactivity ###
def print_location():
  print('\n' + ('-' * (4 + len(zonemap[myPlayer.location][DESCRIPTION]))))
  print('- ' + zonemap[myPlayer.location][DESCRIPTION] + ' -')
  print(('-' * (4 + len(zonemap[myPlayer.location][DESCRIPTION]))))

### Main Prompt ###
def prompt():
  print("What would you like to do?")
  action = input("> ")
  acceptable_actions = ['move', 'look', 'quit', 'use', 'help', 'status']
  while action.lower() not in acceptable_actions:
    print('Unknown action, try again.')
    action = input("> ")
  if action.lower() == 'quit':
    sys.exit()
  elif action.lower() == 'move':
    player_move()
  elif action.lower() == 'look':
    player_look()
  elif action.lower() == 'status':
    player_status()
  elif action.lower() == 'use':
    player_use()
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
    print(zonemap[myPlayer.location][SOL_EXAMINATION])
  else:
    print(zonemap[myPlayer.location][PUZ_EXAMINATION])

### Status Command ###
def player_status():
  print(myPlayer.name, myPlayer.job, myPlayer.hp, myPlayer.mana)

### Use Command ###
def player_use():

  if zonemap[myPlayer.location][SOLVED]:
    print('You already solved this room.')
  else :
    ask = 'What do you want to use?\n> '
    desired_item = input(ask)
    if desired_item.lower() == zonemap[myPlayer.location][ITEM]:
      zonemap[myPlayer.location][SOLVED] = True
      zonemap[myPlayer.location][SOLUTION]()
      # SOLUTIONS[myPlayer.location]()
      prompt()
    else:
      print('Cant seem to find that...')
      time.sleep(0.5)
      prompt()

### Help Command ###
def player_help():
  os.system('clear')
  print("-------------- H E L P --------------")
  print("  Commands: Move, Look, Use, Help    ")
  prompt()

### Game Functionality ###

def main_game_loop():
  while myPlayer.game_over is False:
    prompt()
    # Where to handle if game has been beaten.

def flush_speech(statement, speed):
  for character in statement:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(speed)


def setup_game():
  os.system('clear')

  # Setup Questions
  question1 = "Hello, what's your name?\n"
  question2 = "What is your job?\n(Scientist, Pilot, Tech)\n"
  question2invalid = "Valid jobs are, Scientist, Pilot and Tech\n"

  ### Name Request
  flush_speech(question1, 0.05)
  player_name= input("> ")
  myPlayer.name = player_name
  

  ### Job Request
  flush_speech(question2, 0.05)
  player_job = input("> ")
  valid_jobs = ['scientist', 'pilot', 'tech']
  if player_job.lower() in valid_jobs:
    myPlayer.job = player_job
    print("You are now a " + player_job + "!\n")
  while myPlayer.job.lower() not in valid_jobs:
    flush_speech(question2invalid, 0.05)
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
  welcome = "Welcome, " + myPlayer.name + " the " + myPlayer.job + "."
  flush_speech(welcome, 0.05)
  time.sleep(1)

  intro1 = "You awaken in an empty spaceship.\n"
  intro2 = "The rest of your crew is missing.\n"
  intro3 = "Try to figure out why...\n"
  intro4 = "heh. heh.. heh...\n"


  os.system('clear')
  
  flush_speech(intro1, 0.04)
  flush_speech(intro2, 0.04)
  flush_speech(intro3, 0.08)
  flush_speech(intro4, 0.18)
  time.sleep(0.5)

  os.system('clear')
  print('---------------------------------')
  print('|            Lets Begin         |')
  print('---------------------------------')
  print('Commands: Move, Look, Use, Help\n')
  main_game_loop()


title_screen()

# dock_solution()