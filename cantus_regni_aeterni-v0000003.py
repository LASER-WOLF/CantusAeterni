import os
import ctypes
import keyboard

# SETUP
log_list = ["You start the game"]
debug_log_list = ["Starting game"]
queue_list = []
inventory_list = []
active_cutscene = 1
current_room = 1
ui_size_top = 2
ui_bottom_input_options_length = 10
ui_size_bottom = ui_bottom_input_options_length + 3
ui_log_display_length = 10
ui_size_log = ui_log_display_length + 1
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

# SET COLORS
color_red = '\x1b[0;31;40m'
color_green = '\x1b[0;32;40m'
color_yellow = '\x1b[0;33;40m'
color_blue = '\x1b[0;34;40m'
color_magenta = '\x1b[0;35;40m'
color_cyan = '\x1b[0;36;40m'
color_white = '\x1b[0;37;40m'
color_bright_red = '\x1b[0;91;40m'
color_bright_green = '\x1b[0;92;40m'
color_bright_yellow = '\x1b[0;93;40m'
color_bright_blue = '\x1b[0;94;40m'
color_bright_magenta = '\x1b[0;95;40m'
color_bright_cyan = '\x1b[0;96;40m'
color_bright_white = '\x1b[0;97;40m'
color_bg_red = '\x1b[0;30;41m'
color_bg_green = '\x1b[0;30;42m'
color_bg_yellow = '\x1b[0;30;43m'
color_bg_blue = '\x1b[0;30;44m'
color_bg_magenta = '\x1b[0;30;45m'
color_bg_cyan = '\x1b[0;30;46m'
color_bg_white = '\x1b[0;30;47m'
color_bg_bright_red = '\x1b[0;30;101m'
color_bg_bright_green = '\x1b[0;30;102m'
color_bg_bright_yellow = '\x1b[0;30;103m'
color_bg_bright_blue = '\x1b[0;30;104m'
color_bg_bright_magenta = '\x1b[0;30;105m'
color_bg_bright_cyan = '\x1b[0;30;106m'
color_bg_bright_white = '\x1b[0;30;107m'
color_end = color_bright_yellow
color_title_screen = color_bright_cyan
color_status = color_bright_magenta
color_direction = color_bright_blue
color_interactable = color_bright_green
color_portal = color_bright_cyan

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

class MainWindowContent:
  def __init__(self, lines, centered_horizontal = False, centered_vertical = False):
    self.lines = lines
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical

class Event:
  def __init__(self, position, content, link = None, disabled = False):
    self.position = position
    self.link = link
    self.content = content
    self.disabled = disabled

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
  
def print_seperator_line():
  print_line_centered("", "-")

def main_window(content):
  if content.lines:
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
    print_seperator_line()

def ui_top():
  ui_top_string = ""
  ui_top_content = []
  if mode == "start_menu":
    ui_top_content.append("MAIN MENU")
  elif mode == "settings":
    ui_top_content.append("SETTINGS")
  elif mode == "test":
    ui_top_content.append("TEST SCREEN")
  elif mode == "cutscene" or mode == "game":
    ui_top_content.append("PLAYER LEVEL / HEALTH / ETC.")
  if option_debug_mode:
    ui_top_content.append("DEBUG MODE")
    ui_top_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
    ui_top_content.append("LOOP #: " + str(loop_count))
    #ui_top_content.append("Mode: " + mode)
    ui_top_content.append("DEBUG LOG: " + debug_log_list[-1])
  for num, item in enumerate(ui_top_content):
    if num != 0:
      ui_top_string += " | "
    ui_top_string += item
  print_line(ui_top_string)
  print_seperator_line()

def ui_log():
  log_list_shortened = log_list[-abs(ui_log_display_length):]
  num = len(log_list_shortened)
  while num < ui_size_log-1:
    print_line("")
    num += 1
  for num, line in enumerate(log_list_shortened):
    #log_num = len(log_list) - len(log_list_shortened) + num + 1
    print_line("- " + line)
  print_seperator_line()

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
  
  # QUIT PROMPT
  if ui_quit_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
    command = user_input()
    if(command.lower() == "y"):
      quit_game = True
    elif(command.lower() == "n"):
      ui_quit_prompt = False
  
  # START MENU
  elif mode == "start_menu": 
    print_line("[1] START GAME")
    print_line("[S] SETTINGS")
    if option_debug_mode:
      print_line("[T] TEST SCREEN")
    print_line("[Q] QUIT")
    command = user_input()
    if(command.lower() == "q"):
      ui_quit_prompt = True
    elif(option_debug_mode and command.lower() == "t"):
      change_mode("test")
    elif(command == "1"):
      change_mode("cutscene")
    elif(command.lower() == "s"):
      change_mode("settings")
  
  # SETTINGS
  elif mode == "settings": 
    print_line("[1] DEBUG MODE: " + str(option_debug_mode).upper())
    print_line("[B] <- GO BACK")
    command = user_input()
    if(command.lower() == "b"):
      change_mode(previous_mode)
    elif(command == "1"):
      option_debug_mode = not option_debug_mode
  
  # TEST SCREEN
  elif mode == "test": 
    print_line("[B] <- GO BACK")
    command = user_input()
    if(command.lower() == "b"):
      change_mode(previous_mode)
  
  # GAME MODE
  elif mode == "game": 
    
    # CHECK INTERACT OPTIONS
    menu_options_examine = []
    menu_options_portal = []
    menu_options_examine_text = []
    num = 1
    room = rooms[current_room]
    for line in room['interactable']:
      if line.position == current_position and not line.disabled:
        menu_options_examine.append(line.link)
        menu_options_examine_text.append("[" + str(num) + "] (EXAMINE) " + line.content.upper())
        num += 1
    for line in room['portal']:
      if line.position == current_position and not line.disabled:
        menu_options_portal.append(line.link)
        menu_options_examine_text.append("[" + str(num) + "] (EXIT) " + line.content.upper())
        num += 1
    
    # CHECK MOVE OPTIONS
    menu_options_move = []
    menu_options_move_text = []
    num = 1
    for key, value in direction_abr.items():
      if key != current_position:
        menu_options_move.append(key)
        line_string = "[" + str(num) + "] " + value.upper()
        if key != "c":
          line_string += " SIDE"
        line_string += " OF " + rooms[current_room]['noun'].upper()
        menu_options_move_text.append(line_string)
        num += 1
    
    # MOVE MENU
    if ui_current_menu == "move":
      print_line("MOVE TO:")
      for line in menu_options_move_text:
        print_line(line)
      print_line("[B] <- GO BACK")
      command = user_input()
      if(command.lower() == "b"):
        ui_current_menu = ""      
      num = 1
      for item in menu_options_move:
        if(command == str(num)):
          ui_current_menu = ""
          change_position(menu_options_move[num-1], True)
        num += 1
    
    # INTERACT MENU
    elif ui_current_menu == "interact":
      print_line("AVAILABLE INTERACTIONS:")
      for line in menu_options_examine_text:
        print_line(line)
      print_line("[B] <- GO BACK")
      command = user_input()
      if(command.lower() == "b"):
        ui_current_menu = ""      
      num = 1
      for item in menu_options_examine:
        if(command == str(num)):
          ui_current_menu = ""
          examine(menu_options_examine[num-1])
        num += 1
      num = 1
      for item in menu_options_portal:
        if(command == str(num)):
          ui_current_menu = ""
          enter_portal(menu_options_portal[num-1])
        num += 1
    
    # GAME MENU
    else:
      print_line("SELECT ACTION:")
      print_line("[1] MOVE")
      if menu_options_examine_text:
        print_line("[2] INTERACT")
      print_line("[S] SETTINGS")
      print_line("[Q] QUIT")
      command = user_input()
      if(command.lower() == "q"):
        ui_quit_prompt = True
      elif(command == "1"):
        ui_current_menu = "move"
      elif(command == "2" and menu_options_examine_text):
        ui_current_menu = "interact"
      elif(command.lower() == "s"):
        change_mode("settings")
        
  else:
    press_to_continue()

def examine(link):
  interactable = interactables[link]
  disable_event_interactable(link)
  if interactable['enable']:
    enable_event_all(interactable['enable'])
  if interactable['disable']:
    disable_event_all(interactable['disable'])
  if interactable['type'] == "item":
    add_to_inventory(interactable['link'])
    add_log("You pick up: " + interactable['text'])
  if interactable['type'] == "portal":
    enable_event_portal(interactable['link'])
    add_log("You have discovered: " + interactable['text'])
  for line in interactable['on_interact']:
    execute_action(line)

def enter_portal(link):
  portal = portals[link]
  target_room = None
  target_pos = None
  if portals[link]['link1'] == current_room:
    target_room = portals[link]['link2']
    target_pos = portals[link]['pos2']
    add_log(portals[link]['text1to2'])
  else:
    target_room = portals[link]['link1']
    target_pos = portals[link]['pos1']
    add_log(portals[link]['text2to1'])
  enter_room(target_room)
  change_position(target_pos)
  for line in portal['on_interact']:
    execute_action(line)

def add_to_inventory(item):
  global inventory_list
  inventory_list.append(item)

def enable_event(link, category, disable = False):
  for room in rooms.values():
    for line in room[category]:
        if line.link == link:
          line.disabled = disable

def disable_event(link, category):
  enable_event(link, category, True)

def enable_event_interactable(link, disable = False):
  enable_event(link, "interactable", disable)

def disable_event_interactable(link):
  enable_event_interactable(link, True)
  
def enable_event_sight(link, disable = False):
  enable_event(link, "sight", disable)

def disable_event_sight(link):
  enable_event_sight(link, True)
  
def enable_event_smell(link, disable = False):
  enable_event(link, "smell", disable)

def disable_event_smell(link):
  enable_event_smell(link, True)
  
def enable_event_sound(link, disable = False):
  enable_event(link, "sound", disable)

def disable_event_sound(link):
  enable_event_sound(link, True)

def enable_event_portal(link, disable = False):
  enable_event(link, "portal", disable)

def disable_event_portal(link):
  enable_event_portal(link, True)

def enable_event_all(link):
  enable_event_sight(link)
  enable_event_smell(link)
  enable_event_sound(link)

def disable_event_all(link):
  disable_event_sight(link)
  disable_event_smell(link)
  disable_event_sound(link)







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
  lines.append(color_title_screen)
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
  lines.append(color_end)
  return MainWindowContent(lines, True, True)

def settings():
  lines = []
  #lines.append('SETTINGS')
  return MainWindowContent(lines, True, True)

def test():
  lines = []
  lines.append('COLORS:')
  lines.append('RED: '.ljust(10) + color_red + ' FG ' + color_bright_red + ' BRIGHT ' + color_bg_red + ' BG ' + color_end + ' ' + color_bg_bright_red + ' BRIGHT ' + color_end)
  lines.append('GREEN: '.ljust(10) + color_green + ' FG ' + color_bright_green + ' BRIGHT ' + color_bg_green + ' BG ' + color_end + ' ' + color_bg_bright_green + ' BRIGHT ' + color_end)
  lines.append('YELLOW: '.ljust(10) + color_yellow + ' FG ' + color_bright_yellow + ' BRIGHT ' + color_bg_yellow + ' BG ' + color_end + ' ' + color_bg_bright_yellow + ' BRIGHT ' + color_end)
  lines.append('BLUE: '.ljust(10) + color_blue + ' FG ' + color_bright_blue + ' BRIGHT ' + color_bg_blue + ' BG ' + color_end + ' ' + color_bg_bright_blue + ' BRIGHT ' + color_end)
  lines.append('MAGENTA: '.ljust(10) + color_magenta + ' FG ' + color_bright_magenta + ' BRIGHT ' + color_bg_magenta + ' BG ' + color_end + ' ' + color_bg_bright_magenta + ' BRIGHT ' + color_end)
  lines.append('CYAN: '.ljust(10) + color_cyan + ' FG ' + color_bright_cyan + ' BRIGHT ' + color_bg_cyan + ' BG ' + color_end + ' ' + color_bg_bright_cyan + ' BRIGHT ' + color_end)
  lines.append('WHITE: '.ljust(10) + color_white + ' FG ' + color_bright_white + ' BRIGHT ' + color_bg_white + ' BG ' + color_end + ' ' + color_bg_bright_white + ' BRIGHT ' + color_end)
  return MainWindowContent(lines)

def cutscene():
  lines = load_cutscene(active_cutscene)
  return MainWindowContent(lines)
  
def load_cutscene(cutscene_id):
  lines = []
  if(option_debug_mode):
    lines.append("DEBUG: Running cutscene #" + str(cutscene_id))
  cutscene = cutscenes[cutscene_id]
  for line in cutscene['on_enter']:
    execute_action(line)
  for line in cutscene['text']:
    lines.append(line)
  for line in cutscene['on_exit']:
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

def enter_room(room_id, logging = False):
  global current_room
  current_room = room_id
  room = rooms[room_id]
  for line in room['on_enter']:
    if not line.disabled and (line.position == "" or line.position == current_position):
      exec(line.content)
  if mode != "game":
    change_mode("game")
  if logging:
    log_string = "You enter the " + rooms[current_room]['noun']
    add_log(log_string)

def game():
  lines = []
  lines.extend(show_active_status())
  lines.append("")
  lines.extend(load_room(current_room))
  #lines.extend(show_log())
  return MainWindowContent(lines)

def load_room(room_id):
  lines = []
  if(option_debug_mode):
    lines.append("DEBUG: You are in room #" + str(room_id))
  room = rooms[room_id]
  lines.append(room['location'])
  lines.extend(sense_sight(room_id))
  lines.extend(sense_hearing(room_id))
  lines.extend(sense_smell(room_id))
  lines.append("")
  lines.append("You are positioned at the " + get_position(current_position) + " of the " + room['noun'] + ".")
  lines.extend(sense_sight(room_id, True))
  lines.extend(sense_hearing(room_id, True))
  lines.extend(sense_smell(room_id, True))
  return lines

def sense_sight(room_id, position_mode = False):
  lines = []
  sense_text = "You look around: "
  if position_mode:
    sense_text = "You inspect your immediate surroundings: "
  room = rooms[room_id]
  if not statuses['blind']['active']:
    for line in room['sight']:
      if not line.disabled:
        if not position_mode and (line.position == "" or (line.position[0] == "-" and line.position[1:] != current_position)):
          lines.append(sense_text + line.content)
        elif (position_mode and line.position == current_position):
          lines.append(sense_text + line.content)
  if not lines:
    lines.append(sense_text + "You see nothing.")
  return lines

def sense_hearing(room_id, position_mode = False):
  lines = []
  sense_text = "You focus on your sense of hearing: "
  if position_mode:
    sense_text = "You focus on the sounds in you immediate proximity: "
  room = rooms[room_id]
  for line in room['sound']:
    if not line.disabled:
      if not position_mode and (line.position == "" or (line.position[0] == "-" and line.position[1:] != current_position)):
        lines.append(sense_text + line.content)
      elif (position_mode and line.position == current_position):
        lines.append(sense_text + line.content)
  if statuses['blind']['active'] and not lines:
    lines.append(sense_text + "You don't hear anything.")
  return lines
  
def sense_smell(room_id, position_mode = False):
  lines = []
  sense_text = "You focus on your sense of smell: "
  if position_mode:
    sense_text = "You focus on the smells in you immediate proximity: "
  room = rooms[room_id]
  for line in room['smell']:
    if not line.disabled:
      if not position_mode and (line.position == "" or (line.position[0] == "-" and line.position[1:] != current_position)):
        lines.append(sense_text + line.content)
      elif (position_mode and line.position == current_position):
        lines.append(sense_text + line.content)
  if statuses['blind']['active'] and not lines:
    lines.append(sense_text + "You don't smell anything.")
  return lines

def get_position(abr):
  position_string = ""
  if abr in direction_abr:
    position_string = format_direction(direction_abr[abr])
    if abr != "c":
      position_string += " side"
  else:
    position_string = "INVALID"
  return position_string

def change_position(position, logging = False):
  global current_position
  current_position = position
  if logging:
    log_string = "You move to the " + direction_abr[position]
    if position != "c":
      log_string += " side"
    log_string += " of the " + rooms[current_room]['noun']
    add_log(log_string)

def show_active_status():
  lines = []
  for line in statuses:
    if (statuses[line]['active']):
      lines.append(format_status(statuses[line]['text']))
  return lines

def activate_status(status, activate = True):
  global statuses
  if status in statuses:
    if statuses[status]['active'] != activate:
      statuses[status]['active'] = activate
      if activate:
        add_log(statuses[status]['activation_text'])
      else:
        add_log(statuses[status]['deactivation_text'])

def deactivate_status(status):
  activate_status(status, False)



def format_status(text):
  return color_status + text + color_end

def format_interactable(text):
  return color_interactable + text + color_end

def format_direction(text):
  return color_direction + text + color_end

def format_portal(text):
  return color_portal + text + color_end





direction_abr = {'c': 'center', 'n': 'north', 'ne': 'north-east', 'e': 'east', 'se': 'south-east', 's': 'south', 'sw': 'south-west', 'w': 'west', 'nw': 'north-west'}

statuses = {
    'slime': {
        'active': False,
        'text': "You are engulfed in sticky slime.",
        'activation_text': "You have become completely covered in nasty slime.",
        'deactivation_text': "You are no longer covered in slime.",
    },
    'blind': {
        'active': False,
        'text': "You are blind.",
        'activation_text': "You have lost the ability to see.",
        'deactivation_text': "You've regained your vision.",
    }
}

cutscenes = {
    1: {
        'on_enter': [
        ],
        'on_exit': [
        "enter_room(1)",
        "change_position('e')",
        ],
        'text': [
        "You regain consciousness.",
        ],
    }
}

interactables = {
    1: {
        'type': "portal",
        'link': 1,
        'enable': 2,
        'disable': 1,
        'text': "A pool of slime that is very deep. You could dive in and try to swim to the end.",
        'on_interact': [
        ],
    },
    2: {
        'type': "item",
        'link': 1,
        'enable': None,
        'disable': 3,
        'text': "A key. It seems quite old. It has some slime on it.",
        'on_interact': [
        ],
    },
    3: {
        'type': "portal",
        'link': 2,
        'enable': 5,
        'disable': 4,
        'text': "A cave that looks big enough for you to fit inside.",
        'on_interact': [
        ],
    },
}

portals = {
    1: {
        'link1': 1,
        'link2': 2,
        'pos1': "c",
        'pos2': "c",
        'text1to2': "You dive into the deep slime pool. After a long and terrifying swim through the submerged cave you emerge in a pitch black grotto.",
        'text2to1': "You jump back into the slime pool. You emerge in a slimy grotto.",
        'on_interact': [
        "activate_status('slime')",
        ],
    },
    2: {
        'link1': 1,
        'link2': 3,
        'pos1': "s",
        'pos2': "n",
        'text1to2': "You squeeze yourself through the tight cave opening. You emerge on the other side.",
        'text2to1': "You head back into the cave. You emerge in a grotto.",
        'on_interact': [
        ],
    },
}

rooms = {
    1: {
        'noun': "grotto",
        'location': "You find yourself in a slimy grotto. The walls are covered in sticky slime and the floor is made of hard rock.",
        'interactable': [
        Event("c","A deep pool of slime on the grotto floor",1),
        Event("ne","Something glinting in the darkness",2),
        Event("s","A narrow cave entrance on the grotto wall",3),
        ],
        'sight': [
        Event("-c","It is very dark, but you see " + format_interactable("a deep pool of slime") + " in the " + format_direction("center") +" of the grotto.",1),
        Event("c","You see " + format_interactable("a deep pool of slime") + " in front of you.",1),
        Event("-c","It is very dark, but you see " + format_portal("a deep pool of slime") + " in the " + format_direction("center") +" of the grotto.",2,True),
        Event("c","You see " + format_portal("a deep pool of slime") + " leading in an " + format_direction("unknown") + " direction.",2,True),
        Event("-ne","It is very dark, but you see " + format_interactable("something glinting") + " in the darkness in the " + format_direction("north-east") +" corner of the grotto.",3),
        Event("ne","You see " + format_interactable("something glinting") + " in the darkness in front of you.",3),
        Event("-s","It is very dark, but you see " + format_interactable("a narrow cave entrance") + " on the " + format_direction("southern") + " wall of the grotto.",4),
        Event("s","You see " + format_interactable("a narrow cave entrance") + " in front of you.",4),
        Event("-s","It is very dark, but you see " + format_portal("a narrow cave entrance") + " on the " + format_direction("southern") + " wall of the grotto.",5,True),
        Event("s","You see " + format_portal("a narrow cave") + " leading " + format_direction("south") + ".",5,True),
        ],
        'smell': [
        Event("","The grotto smells like wet slime."),
        Event("c","The smell of slime is overwhelmingly strong here."),
        ],
        'sound': [
        Event("","You hear the faint sound of slime dripping on slime."),
        ],
        'on_enter': [
        ],
        'portal': [
        Event("c","Dive into the deep pool of slime leading in an unknown direction",1,True),
        Event("s","Climb into the cave leading south",2,True),
        ],
    },
    2: {
        'noun': "grotto",
        'location': "You find yourself in a pitch black grotto.",
        'interactable': [
        ],
        'sight': [
        #Event("-c","It is almost pitch black, but you can barely make out " + format_portal("a deep pool of slime") + " in the " + format_direction("center") +" of the grotto."),
        Event("-c","It is almost pitch black, you see nothing."),
        Event("c","It is very dark, but you make out " + format_portal("a deep pool of slime") + " leading in an " + format_direction("unknown") + " direction."),
        ],
        'smell': [
        Event("","The grotto smells like fungus and slime."),
        Event("c","The smell of slime is very strong here."),
        ],
        'sound': [
        Event("s","You hear a barely audible rumbling sound."),
        ],
        'on_enter': [
        ],
        'portal': [
        Event("c","Dive into the deep pool of slime leading back to the grotto",1,True),
        ],
    },
    3: {
        'noun': "void",
        'location': "You find yourself in a void.",
        'interactable': [
        ],
        'sight': [
        Event("-n","You see " + format_portal("a narrow cave entrance") + " on the " + format_direction("northern") + " side of the void."),
        Event("n","You see " + format_portal("a narrow cave") + " leading " + format_direction("north") + " to a grotto."),
        ],
        'smell': [
        Event("n","You detect a faint smell of slime coming from the " + format_direction("north") + "."),
        ],
        'sound': [
        ],
        'on_enter': [
        ],
        'portal': [
        Event("n","Climb back into the cave leading north",1,True),
        ],
    },
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