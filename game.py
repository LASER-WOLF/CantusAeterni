import os
import ctypes
import json
import re
import keyboard

class MainWindowContent:
  def __init__(self, lines, centered_horizontal = False, centered_vertical = False):
    self.lines = lines
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical

def initialize():
  global queue_list
  global mode
  global previous_mode
  queue_list = []
  mode = "start_menu"
  previous_mode = mode

def import_settings():
  global settings
  settings = json.load(open('settings.json','r'))

def initialize_new_game():
  global rooms
  global cutscenes
  global interactables
  global portals
  global statuses
  global items
  rooms = json.load(open('data/rooms.json','r')) 
  cutscenes = json.load(open('data/cutscenes.json','r')) 
  interactables = json.load(open('data/interactables.json','r')) 
  portals = json.load(open('data/portals.json','r')) 
  statuses = json.load(open('data/statuses.json','r')) 
  items = json.load(open('data/items.json','r')) 
  global log_list
  global inventory_list
  global active_cutscene
  global active_room
  global current_position
  log_list = ["You start the game"]
  inventory_list = []
  active_cutscene = "1"
  active_room = "1"
  current_position = "c"
  change_mode("cutscene")

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

def export_json(name, content):
  with open(name + ".json", "w") as outfile:
      json.dump(content, outfile, indent = 2)

def format_status(text):
  return color_status + text + color_end

def format_interactable(text):
  return color_interactable + text + color_end

def format_direction(text):
  return color_direction + text + color_end

def format_portal(text):
  return color_portal + text + color_end

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
    main_window_size_subtract = ui_size_upper+ui_size_lower
    if mode == "game":
      main_window_size_subtract += ui_size_log
    num_upper_padding = 0
    if content.centered_vertical:
      while num_upper_padding < ((window_size_x - main_window_size_subtract) - len(content.lines)) / 2:
        print_line("")
        num_upper_padding += 1
    for num, line in enumerate(content.lines):
      if content.centered_horizontal:
        print_line_centered(line)
      else:
        print_line(line)
    while num+num_upper_padding+1 < window_size_x-main_window_size_subtract:
      print_line("")
      num += 1
    print_seperator_line()

def ui_upper():
  ui_upper_string = ""
  ui_upper_content = []
  if mode == "start_menu":
    ui_upper_content.append("MAIN MENU")
  elif mode == "settings_menu":
    ui_upper_content.append("SETTINGS")
  elif mode == "test":
    ui_upper_content.append("TEST SCREEN")
  elif mode == "cutscene" or mode == "game":
    ui_upper_content.append("PLAYER LEVEL / HEALTH / ETC.")
  if settings['debug_mode']:
    ui_upper_content.append("DEBUG MODE")
    ui_upper_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
    ui_upper_content.append("LOOP #: " + str(loop_count))
    ui_upper_content.append("MODE: " + mode)
    ui_upper_content.append("DEBUG LOG: " + debug_log_list[-1])
  for num, item in enumerate(ui_upper_content):
    if num != 0:
      ui_upper_string += " | "
    ui_upper_string += item
  print_line("")
  print_line(ui_upper_string)
  print_seperator_line()

def ui_lower():
  global mode
  global quit_game
  global ui_quit_prompt
  global ui_restart_prompt
  global ui_current_menu
  global settings
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
  # RESTART PROMPT
  elif ui_restart_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
    command = user_input()
    if(command.lower() == "y"):
      initialize()
      change_mode(mode)
      ui_restart_prompt = False
    elif(command.lower() == "n"):
      ui_restart_prompt = False
  # START MENU
  elif mode == "start_menu": 
    print_line("[1] START GAME")
    print_line("[S] SETTINGS")
    if settings['debug_mode']:
      print_line("[T] TEST SCREEN")
    print_line("[Q] QUIT")
    command = user_input()
    if(command.lower() == "q"):
      ui_quit_prompt = True
    elif(settings['debug_mode'] and command.lower() == "t"):
      change_mode("test")
    elif(command == "1"):
      initialize_new_game()
    elif(command.lower() == "s"):
      change_mode("settings_menu")
  # SETTINGS MENU
  elif mode == "settings_menu": 
    print_line("[1] DEBUG MODE: " + str(settings['debug_mode']).upper())
    print_line("[B] <- GO BACK")
    command = user_input()
    if(command.lower() == "b"):
      export_json('settings', settings)
      change_mode(previous_mode)
    elif(command == "1"):
      settings['debug_mode'] = not settings['debug_mode']
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
    room = rooms[active_room]
    for line in room['interactable']:
      if line['position'] == current_position and not line['disabled']:
        menu_options_examine.append(line['link'])
        menu_options_examine_text.append("[" + str(num) + "] (EXAMINE) " + line['content'].upper())
        num += 1
    for line in room['portal']:
      if line['position'] == current_position and not line['disabled']:
        menu_options_portal.append(line['link'])
        menu_options_examine_text.append("[" + str(num) + "] (EXIT) " + line['content'].upper())
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
        line_string += " OF " + rooms[active_room]['noun'].upper()
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
    # MAIN MENU (GAME)
    else:
      print_line("SELECT ACTION:")
      print_line("[1] MOVE")
      if menu_options_examine_text:
        print_line("[2] INTERACT")
      print_line("[M] MAP")
      print_line("[S] SETTINGS")
      print_line("[R] RESTART")
      print_line("[Q] QUIT")
      command = user_input()
      if(command.lower() == "q"):
        ui_quit_prompt = True
      elif(command == "1"):
        ui_current_menu = "move"
      elif(command == "2" and menu_options_examine_text):
        ui_current_menu = "interact"
      elif(command.lower() == "s"):
        change_mode("settings_menu")
      elif(command.lower() == "m"):
        change_mode("map")
      elif(command.lower() == "r"):
        ui_restart_prompt = True
  # DEFAULT BEHAVIOR
  else:
    press_to_continue()

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

def change_mode(new_mode):
  global mode
  global previous_mode
  previous_mode = mode
  mode = new_mode

def user_input():
  return input(line_margin +  "> ")

def press_to_continue():
  input(line_margin + "PRESS [ENTER] TO CONTINUE")

def enable_event(link, category, disable = False):
  for room in rooms.values():
    for line in room[category]:
        if line['link'] == link:
          line['disabled'] = disable

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
  if portals[link]['link1'] == active_room:
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
  #lines.append('')
  #lines.append('`7MM"""Mq.  `7MM"""YMM    .g8"""bgd `7MN.   `7MF\'`7MMF\'   ')
  #lines.append('  MM   `MM.   MM    `7  .dP\'     `M   MMN.    M    MM     ')
  #lines.append('  MM   ,M9    MM   d    dM\'       `   M YMb   M    MM     ')
  #lines.append('  MMmmdM9     MMmmMM    MM            M  `MN. M    MM     ')
  #lines.append('  MM  YM.     MM   Y  , MM.    `7MMF\' M   `MM.M    MM     ')
  #lines.append('  MM   `Mb.   MM     ,M `Mb.     MM   M     YMM    MM     ')
  #lines.append('.JMML. .JMM..JMMmmmmMMM   `"bmmmdPY .JML.    YM  .JMML.   ')
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
"""
def map_portal_check(loop_sel,loop_val):
  global map_room_list
  for portal in rooms[loop_sel]['portal']:
    if portal['disabled'] == False:
      loop_val_new = loop_val
      loop_next = portals[portal['link']]['link1']
      if portals[portal['link']]['link1'] == loop_sel:
        loop_next = portals[portal['link']]['link2']
      if portals[portal['link']]['dir'] == "nw" or portals[portal['link']]['dir'] == "n" or portals[portal['link']]['dir'] == "ne":
        loop_val_new -= 1
      if portals[portal['link']]['dir'] == "sw" or portals[portal['link']]['dir'] == "s" or portals[portal['link']]['dir'] == "se":
        loop_val_new += 1
      #add to list with loop_next and loop_val_new
      map_room_list.append(loop_sel + " " + str(loop_val_new))
      map_portal_check(loop_next, loop_val_new)

map_room_list = []
"""
def map():
  lines = []
  
  map_char_tile_top = color_bright_black + "┌───┐" + color_end
  map_char_tile_mid = color_bright_black + "│   │" + color_end
  map_char_tile_low = color_bright_black + "└───┘" + color_end
  map_char_tile_visited_top = color_bright_yellow + "┌───┐" + color_end
  map_char_tile_visited_mid = color_bright_yellow + "│   │" + color_end
  map_char_tile_visited_low = color_bright_yellow + "└───┘" + color_end
  map_char_tile_current_top = color_bright_yellow + "┌───┐" + color_end
  map_char_tile_current_mid = color_bright_yellow + "│YOU│" + color_end
  map_char_tile_current_low = color_bright_yellow + "└───┘" + color_end
  map_char_portal_top = color_portal + "┌───┐" + color_end
  map_char_portal_mid = color_portal + "│ P │" + color_end
  map_char_portal_low = color_portal + "└───┘" + color_end
  map_char_tile_portal_current_top = color_portal + "┌───┐" + color_end
  map_char_tile_portal_current_mid = color_portal + "│" + color_bright_yellow + "YOU" + color_portal + "│" + color_end
  #map_char_tile_portal_current_mid = color_portal + "│YOU│" + color_end
  map_char_tile_portal_current_low = color_portal + "└───┘" + color_end
  map_char_interactable_top = color_interactable + "┌───┐" + color_end
  map_char_interactable_mid = color_interactable + "│ E │" + color_end
  map_char_interactable_low = color_interactable + "└───┘" + color_end
  map_char_tile_interactable_current_top = color_interactable + "┌───┐" + color_end
  map_char_tile_interactable_current_mid = color_interactable + "│" + color_bright_yellow + "YOU" + color_interactable + "│" + color_end
  #map_char_tile_interactable_current_mid = color_interactable + "│YOU│" + color_end
  map_char_tile_interactable_current_low = color_interactable + "└───┘" + color_end
  
  for y in range(3):
    line_top = ""
    line_mid = ""
    line_low = ""
    for x in range(3):
      pos = ""
      if y == 1 and x == 1:
        pos = "c"
      if y == 0:
        pos += "n"
      elif y == 2:
        pos += "s"
      if x == 0:
        pos += "w"
      elif x == 2:
        pos += "e"
      tile_top = map_char_tile_top
      tile_mid = map_char_tile_mid
      tile_low = map_char_tile_low
      if rooms[active_room]['visited'][pos]:
        tile_top = map_char_tile_visited_top
        tile_mid = map_char_tile_visited_mid
        tile_low = map_char_tile_visited_low
        if pos == current_position:
          tile_top = map_char_tile_current_top
          tile_mid = map_char_tile_current_mid
          tile_low = map_char_tile_current_low
      for portal in rooms[active_room]['portal']:
        if portal['position'] == pos and portal['disabled'] == False and rooms[active_room]['visited'][pos]:
          tile_top = map_char_portal_top
          tile_mid = map_char_portal_mid
          tile_low = map_char_portal_low
          if pos == current_position:
            tile_top = map_char_tile_portal_current_top
            tile_mid = map_char_tile_portal_current_mid
            tile_low = map_char_tile_portal_current_low
      for interactable in rooms[active_room]['interactable']:
        if interactable['position'] == pos and interactable['disabled'] == False and rooms[active_room]['visited'][pos]:
          tile_top = map_char_interactable_top
          tile_mid = map_char_interactable_mid
          tile_low = map_char_interactable_low
          if pos == current_position:
            tile_top = map_char_tile_interactable_current_top
            tile_mid = map_char_tile_interactable_current_mid
            tile_low = map_char_tile_interactable_current_low
      line_top += tile_top
      line_mid += tile_mid
      line_low += tile_low
    lines.append(line_top)
    lines.append(line_mid)
    lines.append(line_low)
  queue_action({'type': 'change_mode', 'link': previous_mode})
  return MainWindowContent(lines, False, True)

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
  if(settings['debug_mode']):
    lines.append("DEBUG: Running cutscene " + str(cutscene_id))
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
  if action['type'] == 'enter_room':
    enter_room(action['link'])
  elif action['type'] == 'change_position':
    change_position(action['link'])
  elif action['type'] == 'activate_status':
    activate_status(action['link'])
  elif action['type'] == 'change_mode':
    change_mode(action['link'])
  add_debug_log(action['type'] + " -> " + action['link'])

def enter_room(room_id, logging = False):
  global active_room
  active_room = room_id
  room = rooms[room_id]
  for line in room['on_enter']:
    if not line['disabled'] and (line['position'] == "" or line['position'] == current_position):
      execute_action(line['content'])
  if mode != "game":
    change_mode("game")
  if logging:
    log_string = "You enter the " + rooms[active_room]['noun']
    add_log(log_string)

def game():
  lines = []
  lines.extend(show_active_status())
  lines.append("")
  lines.extend(load_room(active_room))
  #lines.extend(show_log())
  return MainWindowContent(lines)

def load_room(room_id):
  lines = []
  if(settings['debug_mode']):
    lines.append("DEBUG: You are in room " + str(room_id))
  room = rooms[room_id]
  lines.append(room['location'])
  lines.extend(sense_sight(room_id))
  lines.extend(sense_sound(room_id))
  lines.extend(sense_smell(room_id))
  lines.append("")
  lines.append("You are positioned at the " + get_position(current_position) + " of the " + room['noun'] + ".")
  lines.extend(sense_sight(room_id, True))
  lines.extend(sense_sound(room_id, True))
  lines.extend(sense_smell(room_id, True))
  return lines

def sense_sight(room_id, position_mode = False):
  lines = []
  sense_text = "You look around: "
  if position_mode:
    sense_text = "You inspect your immediate surroundings: "
  room = rooms[room_id]
  if not statuses['blind']['active']:
    lines.extend(sense_scan("sight", sense_text, room_id, position_mode))
  if not lines:
    lines.append(sense_text + "You see nothing.")
  return lines

def sense_sound(room_id, position_mode = False):
  lines = []
  sense_text = "You focus on your sense of hearing: "
  if position_mode:
    sense_text = "You focus on the sounds in you immediate proximity: "
  if not statuses['deaf']['active']:
    lines.extend(sense_scan("sound", sense_text, room_id, position_mode))
  if statuses['blind']['active'] and not lines:
    lines.append(sense_text + "You don't hear anything.")
  return lines
  
def sense_smell(room_id, position_mode = False):
  lines = []
  sense_text = "You focus on your sense of smell: "
  if position_mode:
    sense_text = "You focus on the smells in you immediate proximity: "
  if not statuses['anosmic']['active']:
    lines.extend(sense_scan("smell", sense_text, room_id, position_mode))
  if statuses['blind']['active'] and not lines:
    lines.append(sense_text + "You don't smell anything.")
  return lines

def sense_scan(sense, sense_text, room_id, position_mode = False):
  lines = []
  room = rooms[room_id]
  for line in room[sense]:
    if not line['disabled']:
      content = format_color_tags(line['content'])
      if not position_mode and (line['position'] == "" or (line['position'][0] == "-" and line['position'][1:] != current_position)):
        lines.append(sense_text + content)
      elif (position_mode and line['position'] == current_position):
        lines.append(sense_text + content)
  return lines

def format_color_tags(content):
  content = re.sub("<i>(.*?)</i>", format_interactable(r"\1"), content)
  content = re.sub("<s>(.*?)</s>", format_status(r"\1"), content)
  content = re.sub("<d>(.*?)</d>", format_direction(r"\1"), content)
  content = re.sub("<p>(.*?)</p>", format_portal(r"\1"), content)
  return content

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
  rooms[active_room]['visited']["room"] = True
  rooms[active_room]['visited'][current_position] = True
  if logging:
    log_string = "You move to the " + direction_abr[position]
    if position != "c":
      log_string += " side"
    log_string += " of the " + rooms[active_room]['noun']
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

# SETUP
initialize()
import_settings()
main_title = "Cantus Aeterni"
debug_log_list = ["Starting game"]
ui_size_upper = 3
ui_lower_input_options_length = 10
ui_size_lower = ui_lower_input_options_length + 3
ui_log_display_length = 10
ui_size_log = ui_log_display_length + 1
ui_quit_prompt = False
ui_restart_prompt = False
ui_current_menu = ""
line_margin = "  "
default_window_size_x = 50
default_window_size_y = 200
window_size_x = default_window_size_x
window_size_y = default_window_size_y
loop_count = 0
quit_game = False
direction_abr = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }

# SET COLORS
color_red = '\x1b[0;31;40m'
color_green = '\x1b[0;32;40m'
color_yellow = '\x1b[0;33;40m'
color_blue = '\x1b[0;34;40m'
color_magenta = '\x1b[0;35;40m'
color_cyan = '\x1b[0;36;40m'
color_white = '\x1b[0;37;40m'
color_bright_black = '\x1b[0;90;40m'
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
color_bg_bright_black = '\x1b[0;30;100m'
color_bg_bright_red = '\x1b[0;30;101m'
color_bg_bright_green = '\x1b[0;30;102m'
color_bg_bright_yellow = '\x1b[0;30;103m'
color_bg_bright_blue = '\x1b[0;30;104m'
color_bg_bright_magenta = '\x1b[0;30;105m'
color_bg_bright_cyan = '\x1b[0;30;106m'
color_bg_bright_white = '\x1b[0;30;107m'
color_end = color_bright_yellow
color_title_screen = color_bright_cyan
color_interactable = color_bright_green
color_direction = color_bright_blue
color_portal = color_bright_cyan
color_status = color_bright_magenta

# SET WINDOW TITLE & SIZE & FG/BG COLOR
os.system("mode "+str(default_window_size_y)+","+str(default_window_size_x))
os.system("color 0E")
os.system("title " + main_title)

# MAXIMIZE WINDOW
if(os.name == 'nt'):
  kernel32 = ctypes.WinDLL('kernel32')
  user32 = ctypes.WinDLL('user32')
  SW_NORMAL = 1
  SW_MAXIMIZE = 3
  hWnd = kernel32.GetConsoleWindow()
  user32.ShowWindow(hWnd, SW_NORMAL)
  user32.ShowWindow(hWnd, SW_MAXIMIZE)

"""
# FULLSCREEN
if(os.name == 'nt' and settings['start_fullscreen']):
  keyboard.press('f11')
"""

# MAIN LOOP
while not quit_game:
  get_window_size()
  clear_console()
  run_queued_actions()
  ui_upper()
  if mode == "start_menu":
    main_window(start_menu())
  elif mode == "test":
    main_window(test())
  elif mode == "cutscene":
    main_window(cutscene())
  elif mode == "map":
    main_window(map())
  elif mode == "game":
    main_window(game())
    ui_log()
  ui_lower()
  loop_count += 1
  #exec("main_window(" + mode + "())")

"""
color_tags = {'<i>': color_interactable, '</i>': color_end, '<s>': color_status, '</s>': color_end, '<d>': color_direction, '</d>': color_end, '<p>': color_portal, '</p>': color_end}

def replace_multi(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class EncodeJSON(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
with open("rooms.json", "w") as outfile:
    json.dump(rooms, outfile, indent = 2, cls=EncodeJSON)
with open("statuses.json", "w") as outfile:
    json.dump(statuses, outfile, indent = 2, cls=EncodeJSON)
with open("cutscenes.json", "w") as outfile:
    json.dump(cutscenes, outfile, indent = 2, cls=EncodeJSON)
with open("interactables.json", "w") as outfile:
    json.dump(interactables, outfile, indent = 2, cls=EncodeJSON)
with open("portals.json", "w") as outfile:
    json.dump(portals, outfile, indent = 2, cls=EncodeJSON)

rooms_pickled = jsonpickle.encode(rooms, indent = 2)
rooms_unpickled = jsonpickle.decode(rooms_pickled)
f = open("rooms-pickle.json", "w")
f.write(rooms_pickled)
f.close()

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
"""