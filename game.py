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
  def __init__(self, name='initial name', job='initial job', hp=0, mana=0, inventory=[], status_effects=[], location='a1', game_over=False):
    self.name = name
    self.job = job
    self.hp = hp
    self.mana = mana
    self.inventory = inventory
    self.status_effects = status_effects
    self.location = location
    self.game_over = game_over

myPlayer = player()

### Puzzle Solutions ###

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

  zonemap[myPlayer.location]['solved'] = True


def pit_solution():
  print("Enter Ignition Codes:\n")
  ignition_codes = input("> ")
  if ignition_codes == "1234":
    statement1 = "Ignition sequence initialized.\n"
    statement2 = "Registering pilot session for Captain " + myPlayer.name + "\n"
    statement3 = "Entering warp drive in \n"
    statement4 = "3...\n"
    statement5 = "2...\n"
    statement6 = "1...\n"

    os.system('clear')
    flush_speech(statement1, 0.05)
    flush_speech(statement2, 0.05)
    flush_speech(statement3, 0.05)
    flush_speech(statement4, 0.03)
    time.sleep(1)
    flush_speech(statement5, 0.03)
    time.sleep(1)
    flush_speech(statement6, 0.03)
    time.sleep(1)
    zonemap[myPlayer.location]['solved'] = True
  else:
    print("\033[1;31;40m INITIALIZATION FAILURE\033[0;37m")


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
    zonemap[myPlayer.location]['solved'] = True
  else:
    print("\033[1;31;40mACCESS DENIED\033[0;37m")

def lab_solution():
  print("what is the combination?\n")
  password = input("> ")
  if password == "567":
    statement1 = myPlayer.name + ", it's Clarence, I need you to man the cockpit.\n"
    statement2 = "There's some harmful radiation in this area we need to avoid\n"
    statement3 = "Use the thumbscanner to start the warp drive, hurry!\n"

    os.system('clear')
    flush_speech(statement1, 0.05)
    flush_speech(statement2, 0.05)
    flush_speech(statement3, 0.05)
    time.sleep(0.5)
  else:
    print("Can't get it open")

### Map ###
###  |a1|a2|
###  |b1|b2|

zonemap = {
  "a1": {
      "zonename": "Cockpit",
      "description": "The controls to your vessel.",
      "puz_examination": "A window shows stars outside passing by. At the helm is a large \033[1mControl Panel\033[0;37m.",
      "sol_examination": "A window shows stars outside passing by. The Control Panel shows an ignition sequence.",
      "solution": pit_solution,
      "item": 'control panel',
      "solved": False,
      "up": None,
      "down": 'b1',
      "left": None,
      "right": 'a2'
  },
  "a2": {
      "zonename": 'Labs',
      "description": "Onboard research laboratories",
      "puz_examination": "A sparse room. Filled with bottles, chemicals and technological equipment.",
      "sol_examination": "A sparse room. Filled with bottles, chemicals and technological equipment.",
      "solution": 'lab solution',
      "item": 'lab item',
      "solved": False,
      "up": None,
      "down": 'b2',
      "left": 'a1',
      "right": None
  },
  "b1": {
      "zonename": 'Medbay',
      "description": "A bay for medical and healing purposes.",
      "puz_examination": "A sterile room with a table and medical tools. You see a \033[1mWalkie Talkie\033[0;37m on the table.",
      "sol_examination": "A sterile room with a table and medical tools. You see an empty table.",
      "solution": medbay_solution,
      "item": 'walkie talkie',
      "solved": False,
      "up": 'a1',
      "down": None,
      "left": None,
      "right": 'b2'
  },
  "b2": {
      "zonename": 'Dock',
      "description": "A dock for the escape pod.",
      "puz_examination": "An open room with escape pods against the wall and a large \033[1mhatch\033[0;37m to the ship's exterior",
      "sol_examination": "An open room with escape pods against the wall. Tara is inspecting broken solar panels on the floor.",
      "solution": dock_solution,
      "item": 'hatch',
      "solved": False,
      "up": 'a2',
      "down": None,
      "left": 'b1',
      "right": None
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
def print_location():
  print('\n' + ('-' * (4 + len(zonemap[myPlayer.location]["description"]))))
  print('- ' + zonemap[myPlayer.location]["description"] + ' -')
  print(('-' * (4 + len(zonemap[myPlayer.location]["description"]))))

def player_move():
  ask = "Where would you like to move?\n(Up, Left, Down, Right)\n"
  desired_dest = input(ask)
  if desired_dest.lower() in ['up', 'north']:
    destination = zonemap[myPlayer.location]["up"]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['left', 'west']:
    destination = zonemap[myPlayer.location]["left"]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['right', 'east']:
    destination = zonemap[myPlayer.location]["right"]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)
  elif desired_dest.lower() in ['down', 'south']:
    destination = zonemap[myPlayer.location]["down"]
    if destination == None:
      print("There's nothing there.")
      time.sleep(1)
      prompt()
    else:
      movement_handler(destination)

def movement_handler(destination):
  print("\n" + "You have moved to " + zonemap[destination]["zonename"] + ".")
  myPlayer.location = destination
  print_location()

### Look Command ###
def player_look():
  if zonemap[myPlayer.location]['solved']:
    print(zonemap[myPlayer.location]['sol_examination'])
  else:
    print(zonemap[myPlayer.location]['puz_examination'])

### Status Command ###
def player_status():
  print(myPlayer.name, myPlayer.job, myPlayer.hp, myPlayer.mana)

### Use Command ###
def player_use():

  if zonemap[myPlayer.location]["solved"]:
    print('You already solved this room.')
  else :
    ask = 'What do you want to use?\n> '
    desired_item = input(ask)
    if desired_item.lower() == zonemap[myPlayer.location]["item"]:
      zonemap[myPlayer.location]["solution"]()
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

### Run Game
title_screen()
