import os
import ctypes

# SETUP
log_list = ["Starting game"]
debug_log_list = ["Starting game"]
queue_list = []
active_cutscene = 1
current_room = 1
ui_size_top = 2
ui_size_bottom = 13
ui_size_log = 11
current_position = "c"
line_margin = "  "
default_window_size_x = 50
default_window_size_y = 200
mode = "start_menu"
previous_mode = mode
window_size_x = default_window_size_x
window_size_y = default_window_size_y
loop_count = 0
quit_game = False
ui_quit_prompt = False
option_debug_mode = True
ui_current_menu = ""

color_end = '\x1b[0m'

# SET WINDOW SIZE & FG/BG COLOR
os.system('color')
os.system("mode "+str(default_window_size_y)+","+str(default_window_size_x))
os.system("color 0E")

# MAXIMIZE WINDOW
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_MAXIMIZE = 3
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_MAXIMIZE)

"""
#prints table of formatted text format options
def print_format_table():
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')
"""

class MainWindowContent:
  def __init__(self, lines, centered_horizontal = False, centered_vertical = False):
    self.lines = lines
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical

class Event:
  def __init__(self, position, content):
    self.position = position
    self.content = content

def get_window_size():
  global window_size_x
  global window_size_y
  window_size_x = os.get_terminal_size().lines
  window_size_y = os.get_terminal_size().columns

def clear_console():
  if(os.name == 'posix'):
     os.system('clear')
  else:
     os.system('cls')

def make_line(line, fill = "", align = "<"):
  if align == "<":
    line = line_margin + line
  if align == ">":
    line = line + line_margin
  return '{message:{fill}{align}{width}}'.format(
   message=line,
   fill=fill,
   align=align,
   width=window_size_y,
  )

def print_line(line, fill = "", align = "<"):
  print(make_line(line, fill, align));
  
def print_line_centered(line, fill = ""):
  print_line(line, fill, "^")

def print_line_ui(line, fill = "", align = "<"):
  print_line(line.upper(), fill, align)
  
def print_seperator_line():
  print_line_centered("", "-")

def main_window(content):
  #lines = content.lines
  #centered_horizontal = content.centered_horizontal
  main_window_size_subtract = ui_size_top+ui_size_bottom
  if mode == "game":
    main_window_size_subtract += ui_size_log
  
  num_top_padding = 0
  
  if content.centered_vertical:
    while num_top_padding < ((window_size_x - main_window_size_subtract) - len(content.lines)) / 2:
      print_line("")
      num_top_padding += 1
  
  for num, line in enumerate(content.lines):
    if content.centered_horizontal:
      print_line_centered(line)
    else:
      print_line(line)
  
  while num+num_top_padding+1 < window_size_x-main_window_size_subtract:
    print_line("")
    num += 1

def ui_top():
  ui_top_string = ""
  ui_top_content = []
  if option_debug_mode:
    ui_top_content.append("Debug mode")
    ui_top_content.append("Window size: " + str(window_size_x) + "x" + str(window_size_y))
    ui_top_content.append("Loop #: " + str(loop_count))
    ui_top_content.append("Mode: " + mode)
    ui_top_content.append("Debug log: " + debug_log_list[-1])
  for num, item in enumerate(ui_top_content):
    if num != 0:
      ui_top_string += " | "
    ui_top_string += item
  print_line_ui(ui_top_string)
  print_seperator_line()

def ui_log():
  print_seperator_line()
  log_list_shortened = log_list[-10:]
  num = len(log_list_shortened)
  while num < ui_size_log-1:
    print_line("")
    num += 1
  for num, line in enumerate(log_list_shortened):
    #log_num = len(log_list) - len(log_list_shortened) + num + 1
    print_line_ui("- " + line)

def add_log(item):
  global log_list
  log_list.append(item)

def add_debug_log(item):
  global debug_log_list
  debug_log_list.append(item)

def ui_bottom():
  global mode
  global quit_game
  global ui_quit_prompt
  global ui_current_menu
  global option_debug_mode
  print_seperator_line()
  if ui_quit_prompt:
    print_line_ui("Are you sure?")
    print_line_ui("[Y] Yes")
    print_line_ui("[N] No")
    command = user_input()
    if(command.lower() == "y"):
      quit_game = True
    elif(command.lower() == "n"):
      ui_quit_prompt = False
  elif mode == "start_menu": 
    #print('\x1b[7;30;41m' + 'Success!' + color_end)
    print_line_ui("[1] Start game")
    print_line_ui("[2] Settings")
    print_line_ui("[Q] Quit")
    command = user_input()
    if(command.lower() == "q"):
      ui_quit_prompt = True
    elif(command == "1"):
      change_mode("cutscene")
    elif(command == "2"):
      change_mode("settings")
  elif mode == "settings": 
    print_line_ui("[1] Debug mode: " + str(option_debug_mode))
    print_line_ui("[B] <- Go back")
    command = user_input()
    if(command.lower() == "b"):
      change_mode(previous_mode)
    elif(command == "1"):
      option_debug_mode = not option_debug_mode
  elif mode == "game": 
    if ui_current_menu == "move":
      print_line_ui("Move to:")
      move_options = []
      num=1
      for key, value in direction_abr.items():
        if key != current_position:
          move_options.append(key)
          line_string = ""
          line_string += "[" + str(num) + "] " + value
          if key != "c":
            line_string += " side"
          line_string += " of " + rooms[current_room]['noun']
          print_line_ui(line_string)
          num += 1
      print_line_ui("[B] <- Go back")
      command = user_input()
      if(command.lower() == "b"):
        ui_current_menu = ""      
      num = 1
      for dir in move_options:
        if(command == str(num)):
          ui_current_menu = ""
          change_position(move_options[num-1], True)
        num += 1
    else:
      print_line_ui("Select action:")
      print_line_ui("[1] Move")
      print_line_ui("[2] Settings")
      print_line_ui("[Q] Quit")
      command = user_input()
      if(command.lower() == "q"):
        ui_quit_prompt = True
      elif(command == "1"):
        ui_current_menu = "move"
      elif(command == "2"):
        change_mode("settings")
  else:
    press_to_continue()

def change_mode(new_mode):
  global mode
  global previous_mode
  previous_mode = mode
  mode = new_mode

def user_input():
  return input(line_margin +  "> ")

def press_to_continue():
  input(line_margin + "PRESS [ENTER] TO CONTINUE")

def start_menu():
  lines = []
  lines.append('')
  lines.append('  .g8"""bgd     db      `7MN.   `7MF\'MMP""MM""YMM `7MMF\'   `7MF\'.M"""bgd    ')
  lines.append('.dP\'     `M    ;MM:       MMN.    M  P\'   MM   `7   MM       M ,MI    "Y    ')
  lines.append('dM\'       `   ,V^MM.      M YMb   M       MM        MM       M `MMb.        ')
  lines.append('MM           ,M  `MM      M  `MN. M       MM        MM       M   `YMMNq.    ')
  lines.append('MM.          AbmmmqMA     M   `MM.M       MM        MM       M .     `MM    ')
  lines.append('`Mb.     ,\' A\'     VML    M     YMM       MM        YM.     ,M Mb     dM    ')
  lines.append('  `"bmmmd\'.AMA.   .AMMA..JML.    YM     .JMML.       `bmmmmd"\' P"Ybmmd"     ')
  lines.append('')
  lines.append('`7MM"""Mq.  `7MM"""YMM    .g8"""bgd `7MN.   `7MF\'`7MMF\'   ')
  lines.append('  MM   `MM.   MM    `7  .dP\'     `M   MMN.    M    MM     ')
  lines.append('  MM   ,M9    MM   d    dM\'       `   M YMb   M    MM     ')
  lines.append('  MMmmdM9     MMmmMM    MM            M  `MN. M    MM     ')
  lines.append('  MM  YM.     MM   Y  , MM.    `7MMF\' M   `MM.M    MM     ')
  lines.append('  MM   `Mb.   MM     ,M `Mb.     MM   M     YMM    MM     ')
  lines.append('.JMML. .JMM..JMMmmmmMMM   `"bmmmdPY .JML.    YM  .JMML.   ')
  lines.append('')
  lines.append('      db      `7MM"""YMM MMP""MM""YMM `7MM"""YMM  `7MM"""Mq.  `7MN.   `7MF\'`7MMF\'   ')
  lines.append('     ;MM:       MM    `7 P\'   MM   `7   MM    `7    MM   `MM.   MMN.    M    MM     ')
  lines.append('    ,V^MM.      MM   d        MM        MM   d      MM   ,M9    M YMb   M    MM     ')
  lines.append('   ,M  `MM      MMmmMM        MM        MMmmMM      MMmmdM9     M  `MN. M    MM     ')
  lines.append('   AbmmmqMA     MM   Y  ,     MM        MM   Y  ,   MM  YM.     M   `MM.M    MM     ')
  lines.append('  A\'     VML    MM     ,M     MM        MM     ,M   MM   `Mb.   M     YMM    MM     ')
  lines.append('.AMA.   .AMMA..JMMmmmmMMM   .JMML.    .JMMmmmmMMM .JMML. .JMM..JML.    YM  .JMML.   ')
  lines.append('')
  return MainWindowContent(lines, True, True)

def settings():
  lines = []
  lines.append('SETTINGS')
  return MainWindowContent(lines, True, True)

def cutscene():
  lines = load_cutscene(active_cutscene)
  return MainWindowContent(lines)
  
def load_cutscene(cutscene_id):
  lines = []
  if(option_debug_mode):
    lines.append("DEBUG: Running cutscene #" + str(cutscene_id))
  cutscene = cutscenes[cutscene_id]
  for line in cutscene['enter']:
    execute_command(line)
  for line in cutscene['text']:
    lines.append(line)
  for line in cutscene['exit']:
    queue_action(line)
  return lines

def queue_action(action):
  queue_list.append(action)

def run_queued_actions():
  while queue_list:
    action = queue_list.pop(0)
    execute_action(action)

def execute_action(action):
  exec(action)
  add_debug_log(action)

def enter_room(room_id):
  global current_room
  current_room = room_id
  room = rooms[room_id]
  for line in room['enter']:
    if line.position == "" or line.position == current_position:
      exec(line.content)
  change_mode("game")

def game():
  lines = []
  lines.extend(show_active_status())
  lines.extend(load_room(current_room))
  #lines.extend(show_log())
  return MainWindowContent(lines)

def load_room(room_id):
  lines = []
  if(option_debug_mode):
    lines.append("DEBUG: You are in room #" + str(room_id))
  room = rooms[room_id]
  lines.append(room['location'])
  lines.append("You are positioned in the " + get_position(current_position) + " of the " + room['noun'] + ".")
  if not statuses['blind']['active']:
    for line in room['sight']:
      if line.position == "" or line.position == current_position:
        lines.append("You look around: " + line.content)
  return lines

def get_position(abr):
  position_string = ""
  if abr in direction_abr:
    position_string = direction_abr[abr]
    if abr != "c":
      position_string += " side"
  else:
    position_string = "INVALID"
  return position_string

def change_position(position, logging = False):
  global current_position
  current_position = position
  if logging:
    log_string = "You moved to the " + direction_abr[position]
    if position != "c":
      log_string += " side"
    log_string += " of " + rooms[current_room]['noun']
    add_log(log_string)

def show_active_status():
  lines = []
  for line in statuses:
    if (statuses[line]['active']):
      lines.append(statuses[line]['text'])
  return lines

def activate_status(status):
  global statuses
  if status in statuses:
    statuses[status]['active'] = True










def sense_hearing(room_id):
  lines = []
  room = rooms[room_id]
  for line in room['sound']:
    if line.position == "" or line.position == current_position:
      lines.append("You listen: " + line.content)
  return lines
  
def sense_smell(room_id):
  lines = []
  room = rooms[room_id]
  for line in room['smell']:
    if line.position == "" or line.position == current_position:
      lines.append("You listen: " + line.content)
  return lines

direction_abr = {'c': 'center', 'n': 'north', 'ne': 'north-east', 'e': 'east', 'se': 'south-east', 's': 'south', 'sw': 'south-west', 'w': 'west', 'nw': 'north-west'}

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

cutscenes = {
    1: {
        'enter': [
        ],
        'exit': [
        "change_position('e')",
        "enter_room(1)",
        ],
        'text': [
        "You regain consciousness.",
        ],
    }
}

rooms = {
    1: {
        'noun': "grotto",
        'location': "You find yourself in a slimy grotto. The walls are covered in sticky slime and the floor is made of hard rock.",
        'sight': [
        Event("","It is very dark, but you see a deep pool of slime in the center of the grotto."),
        Event("","It is very dark, but you see something glinting in the darkness in the north-east corner of the grotto."),
        Event("","It is very dark, but you see a narrow cave entrance on the southern wall of the grotto.")
        ],
        'smell': [
        Event("","The grotto smells like wet slime."),
        Event("c","The smell of slime is very strong here."),
        ],
        'sound': [
        Event("","You hear the faint sound of slime dripping on slime."),
        ],
        'enter': [
        Event("","activate_status('slime')"),
        ],
        'exit': [
        ],
    }
}

# MAIN LOOP
while not quit_game:
  get_window_size()
  clear_console()
  run_queued_actions()
  ui_top()
  exec("main_window(" + mode + "())")
  if mode == "game":
    ui_log()
  ui_bottom()
  loop_count += 1

#move
#listen
#smell
#inventory
#dialogue
#exit room actions
#stats
#auto-smell
#auto-listen
#touch
# taste
# sight
# touch
# smell
# sound