import os
import ctypes

# MAXIMIZE WINDOW
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_MAXIMIZE = 3
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_MAXIMIZE)

# SET WINDOW SIZE
#cmd = 'mode 200,50'
#os.system(cmd)

# SET COLORS
cmd = 'color 0E'
os.system(cmd)

# GET WINDOW SIZE
window_size_x = os.get_terminal_size().lines
window_size_y = os.get_terminal_size().columns



active_room = {}
debug_mode = True
current_position = "e"

line_margin = "  "
line_length = window_size_y

def print_line(line):
  print(line_margin + line)
  
def print_line_centered(line):
  #print(line_margin + line)
  print('{message:{fill}{align}{width}}'.format(
   message=line,
   fill='',
   align='^',
   width=line_length,
  ))
  
def seperator_line():
  #print('hi'.ljust(10))
  print('{message:{fill}{align}{width}}'.format(
   message='',
   fill='-',
   align='^',
   width=line_length,
  ))

def start_game():

  #print_line('')
  
  #print_line("--------------------------------------------------------------------------------------------------------------")
#  seperator_line()

  #print_line('')

  print_line_centered('')
  print_line_centered('  .g8"""bgd     db      `7MN.   `7MF\'MMP""MM""YMM `7MMF\'   `7MF\'.M"""bgd    ')
  print_line_centered('.dP\'     `M    ;MM:       MMN.    M  P\'   MM   `7   MM       M ,MI    "Y    ')
  print_line_centered('dM\'       `   ,V^MM.      M YMb   M       MM        MM       M `MMb.        ')
  print_line_centered('MM           ,M  `MM      M  `MN. M       MM        MM       M   `YMMNq.    ')
  print_line_centered('MM.          AbmmmqMA     M   `MM.M       MM        MM       M .     `MM    ')
  print_line_centered('`Mb.     ,\' A\'     VML    M     YMM       MM        YM.     ,M Mb     dM    ')
  print_line_centered('  `"bmmmd\'.AMA.   .AMMA..JML.    YM     .JMML.       `bmmmmd"\' P"Ybmmd"     ')
  print_line_centered('')
  #print_line_centered('')
  print_line_centered('`7MM"""Mq.  `7MM"""YMM    .g8"""bgd `7MN.   `7MF\'`7MMF\'   ')
  print_line_centered('  MM   `MM.   MM    `7  .dP\'     `M   MMN.    M    MM     ')
  print_line_centered('  MM   ,M9    MM   d    dM\'       `   M YMb   M    MM     ')
  print_line_centered('  MMmmdM9     MMmmMM    MM            M  `MN. M    MM     ')
  print_line_centered('  MM  YM.     MM   Y  , MM.    `7MMF\' M   `MM.M    MM     ')
  print_line_centered('  MM   `Mb.   MM     ,M `Mb.     MM   M     YMM    MM     ')
  print_line_centered('.JMML. .JMM..JMMmmmmMMM   `"bmmmdPY .JML.    YM  .JMML.   ')
  #print_line_centered('')
  print_line_centered('')
  print_line_centered('      db      `7MM"""YMM MMP""MM""YMM `7MM"""YMM  `7MM"""Mq.  `7MN.   `7MF\'`7MMF\'   ')
  print_line_centered('     ;MM:       MM    `7 P\'   MM   `7   MM    `7    MM   `MM.   MMN.    M    MM     ')
  print_line_centered('    ,V^MM.      MM   d        MM        MM   d      MM   ,M9    M YMb   M    MM     ')
  print_line_centered('   ,M  `MM      MMmmMM        MM        MMmmMM      MMmmdM9     M  `MN. M    MM     ')
  print_line_centered('   AbmmmqMA     MM   Y  ,     MM        MM   Y  ,   MM  YM.     M   `MM.M    MM     ')
  print_line_centered('  A\'     VML    MM     ,M     MM        MM     ,M   MM   `Mb.   M     YMM    MM     ')
  print_line_centered('.AMA.   .AMMA..JMMmmmmMMM   .JMML.    .JMMmmmmMMM .JMML. .JMM..JML.    YM  .JMML.   ')
  print_line_centered('')
  seperator_line()
  #print_line("---------------------------------------------------------------------------------------------------------")

  press_to_continue(True)
  clear_console()
  print_line("Welcome traveller.")
  print_line("You regain consciousness.")
  press_to_continue()
  enter_room('1')

def press_to_continue(centered = False):
  #print_line('')
  input(line_margin + "PRESS [ENTER] TO CONTINUE")

def clear_console():
  if(os.name == 'posix'):
     os.system('clear')
  else:
     os.system('cls')

def enter_room(room_id):
  global active_room
  active_room = room_id
  room = rooms[room_id]
  for line in room['enter']:
    exec(line)

def load_room(room_id):
  if(debug_mode):
    print_line("DEBUG: You are in room " + room_id)
  room = rooms[room_id]
  print_line(room['location'])
  print_line("You are positioned in the " + get_position(current_position) + " of the " + room['noun'] + ".")
  if not statuses['blind']['active']:
    for line in room['sight']:
      if line.position == "" or line.position == current_position:
        print_line("You look around: " + line.text)
  for line in room['sound']:
    if line.position == "" or line.position == current_position:
      print_line("You focus on the sounds around you: " + line.text)
  for line in room['smell']:
    if line.position == "" or line.position == current_position:
      print_line("You focus on the smells around you: " + line.text)
  for line in room['enter']:
    exec(line)
    
def show_active_status():
  #global statuses
  for line in statuses:
    if (statuses[line]['active']):
      print_line(statuses[line]['text'])
    
def activate_status(status):
  global statuses
  if status in statuses:
    statuses[status]['active'] = True
  
def ui_top():
  ui_top_string = ""
  ui_top_content = []
  if debug_mode:
    ui_top_content.append("DEBUG MODE")
    ui_top_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
  for num, item in enumerate(ui_top_content):
    if num != 0:
      ui_top_string += " | "
    ui_top_string += item
  print(line_margin + ui_top_string)  
  seperator_line()

class Sense:
  def __init__(self, position, text):
    self.position = position
    self.text = text

def get_position(abr):
  position_string = ""
  if abr in direction_abr:
    position_string = direction_abr[abr]
    if abr != "c":
      position_string += " side"
  else:
    position_string = "INVALID"
  return position_string

direction_abr = {'c': 'center', 'n': 'north', 'ne': 'north-east', 'e': 'east', 'se': 'south-east', 's': 'south', 'sw': 'south-west', 'w': 'west', 'nw': 'north-west'}

rooms = {
    '1': {
        'noun': "grotto",
        'location': "You find yourself in a slimy grotto. The walls are covered in sticky slime and the floor is made of hard rock.",
        'sight': [
        Sense("","It is very dark, but you see a deep pool of slime in the center of the grotto."),
        Sense("","It is very dark, but you see something glinting in the darkness in the north-east corner of the grotto."),
        Sense("","It is very dark, but you see a narrow cave entrance on the southern wall of the grotto.")
        ],
        'smell': [
        Sense("","The grotto smells like wet slime."),
        Sense("c","The smell of slime is very strong here.")
        ],
        'sound': [
        Sense("","You hear the faint sound of slime dripping on slime."),
        Sense("c","The smell of slime is very strong here.")
        ],
        'enter': [
        "activate_status('slime')"
        ]
    }
}

statuses = {
    'slime': {
        'active': False,
        'text': "You are engulfed in sticky slime."
    },
    'blind': {
        'active': False,
        'text': "You are blind."
    }
}
# taste
# sight
# touch
# smell
# sound

count = 0
while True:
  ui_top()
  if count == 0:
    start_game()
  clear_console()
  show_active_status()
  load_room(active_room)
  
  # list commands
  print_line("\n---------------------------------------------------------------------------------------------------------\n")
  #print_line("\nCOMMANDS:")
  print_line("[1] MOVE")
  print_line("[2] EXAMINE")
  print_line("[Q] QUIT")
  command = input("> ")
  if(command.lower() == "q"):
    break
  elif(command == "1"):
    print_line("input 1")
  elif(command == "2"):
    print_line("input 2")
  else:
    print_line("INVALID")
  #count++


"""
roomChoice = input("> ")

if(roomChoice == "q"):
  break
elif(roomChoice == "1"):
  print_line("input 1")
elif(roomChoice == "0"):  
  print_line("You enter TEST.")
  print_line("You find yourself in an endless void.")
  print_line("You are neither cold nor warm.")
  print_line("You look around: It is neither dark nor bright. You see nothing.")
else:
  print_line("INVALID")





def add(a, b):
  return a + b

def subtract(a, b):
  return a - b

def multiply(a, b):
  return a * b

def divide(a, b):
  if b == 0:
    print_line("Can't divide by zero")
    return 0
  else:
    return a / b

while True:
  print_line("\nMain menu:")
  print_line("1. New game")
  print_line("q. Quit")
  
  choice = input("Enter choice: ")
  
  if choice == 'q':
    break
  
  if choice in ['1', '2']:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    
    if choice == '1':
      result = add(num1, num2)
      print_line("The result is: ", result)
    
    elif choice == '2':
      result = subtract(num1, num2)
      print_line("The result is: ", result)
      
    elif choice == '3':
      result = multiply(num1, num2)
      print_line("The result is: ", result)
      
    elif choice == '4':
      result = divide(num1, num2)
      print_line("The result is: ", result)
  
  else:
    print_line("Invalid input")
"""