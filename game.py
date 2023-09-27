import os
import ctypes
import json
import re
import msvcrt
import time
from datetime import datetime

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
  add_debug_log("Main initialization")

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
  add_debug_log("Initializing new game")

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

def hide_cursor():
  print('\033[?25l')

def show_cursor():
  print('\033[?25h')

def get_keypress():
  while True:
    if msvcrt.kbhit():
      key = msvcrt.getwch()
      if key == " ":
        key = "space"
      elif key == "\r":
        key = "enter"
      global debug_input_char
      debug_input_char = key
      return key
    time.sleep(0.1)

def user_input():
  return input(line_margin +  "> ")

def press_to_continue(target_key = "enter"):
  print_line("PRESS [" + target_key.upper() + "] TO CONTINUE")
  key = ""
  while key != target_key:
    key = get_keypress()

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

def format_color_tags(content):
  content = re.sub("<i>(.*?)</i>", format_interactable(r"\1"), content)
  content = re.sub("<s>(.*?)</s>", format_status(r"\1"), content)
  content = re.sub("<d>(.*?)</d>", format_direction(r"\1"), content)
  content = re.sub("<p>(.*?)</p>", format_portal(r"\1"), content)
  return content

def format_position_text(abr):
  position_string = ""
  if abr in direction_abr:
    position_string = format_direction(direction_abr[abr])
    if abr != "c":
      position_string += " side"
  else:
    position_string = "INVALID"
  return position_string

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

def ui_main_window(content):
  if content.lines:
    main_window_size_subtract = ui_size_upper+ui_size_lower
    if mode == "game" or mode == "debug":
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
  elif mode == "debug":
    ui_upper_content.append("DEBUG SCREEN")
  elif mode == "cutscene" or mode == "game":
    ui_upper_content.append("PLAYER NAME / LEVEL / HEALTH / ETC.")
  elif mode == "map":
    ui_upper_content.append("MAP")
  if settings['debug_mode']:
    ui_upper_content.append("DEBUG MODE")
    ui_upper_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
    ui_upper_content.append("LOOP #: " + str(loop_count))
    #ui_upper_content.append("MODE: " + mode)
    #ui_upper_content.append("DEBUG LOG: " + debug_log_list[-1])
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
  global ui_pre_quit_prompt
  global ui_restart_prompt
  global ui_current_menu
  global settings
  # PRE QUIT PROMPT
  if ui_pre_quit_prompt:
    print_line("SELECT ACTION:")
    print_line("[1] RETURN TO TITLE SCREEN")
    print_line("[2] QUIT GAME")
    print_line("[B] <- GO BACK")
    key = get_keypress()
    if(key == "1"):
      ui_pre_quit_prompt = False
      ui_restart_prompt = True
    elif(key == "2"):
      ui_pre_quit_prompt = False
      ui_quit_prompt = True
    elif(key == "b"):
      ui_pre_quit_prompt = False
  # QUIT PROMPT
  elif ui_quit_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
    key = get_keypress()
    if(key.lower() == "y"):
      quit_game = True
    elif(key.lower() == "n"):
      ui_quit_prompt = False
  # RESTART PROMPT
  elif ui_restart_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
    key = get_keypress()
    if(key.lower() == "y"):
      initialize()
      change_mode(mode)
      ui_restart_prompt = False
    elif(key.lower() == "n"):
      ui_restart_prompt = False
  # START MENU
  elif mode == "start_menu": 
    print_line("[1] START GAME")
    print_line("[S] SETTINGS")
    if settings['debug_mode']:
      print_line("[D] DEBUG SCREEN")
    print_line("[Q] QUIT")
    key = get_keypress()
    if(key.lower() == "q"):
      ui_quit_prompt = True
    elif(key.lower() == "d" and settings['debug_mode']):
      change_mode("debug")
    elif(key == "1"):
      initialize_new_game()
    elif(key.lower() == "s"):
      change_mode("settings_menu")
  # SETTINGS MENU
  elif mode == "settings_menu": 
    print_line("[1] DEBUG MODE: " + str(settings['debug_mode']).upper())
    print_line("[B] <- GO BACK")
    key = get_keypress()
    if(key.lower() == "b"):
      export_json('settings', settings)
      change_mode(previous_mode)
    elif(key == "1"):
      settings['debug_mode'] = not settings['debug_mode']
  # DEBUG SCREEN
  elif mode == "debug": 
    print_line("[B] <- GO BACK")
    key = get_keypress()
    if(key.lower() == "b"):
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
      key = get_keypress()
      if(key.lower() == "b"):
        ui_current_menu = ""      
      num = 1
      for item in menu_options_move:
        if(key == str(num)):
          ui_current_menu = ""
          change_position(menu_options_move[num-1], True)
        num += 1
    # INTERACT MENU
    elif ui_current_menu == "interact":
      print_line("AVAILABLE INTERACTIONS:")
      for line in menu_options_examine_text:
        print_line(line)
      print_line("[B] <- GO BACK")
      key = get_keypress()
      if(key.lower() == "b"):
        ui_current_menu = ""      
      num = 1
      for item in menu_options_examine:
        if(key == str(num)):
          ui_current_menu = ""
          examine(menu_options_examine[num-1])
        num += 1
      num = 1
      for item in menu_options_portal:
        if(key == str(num)):
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
      if settings['debug_mode']:
        print_line("[D] DEBUG SCREEN")
      print_line("[Q] QUIT")
      key = get_keypress()
      if(key.lower() == "q"):
        ui_pre_quit_prompt = True
      elif(key.lower() == "d" and settings['debug_mode']):
        change_mode("debug")
      elif(key.lower() == "s"):
        change_mode("settings_menu")
      elif(key.lower() == "m"):
        change_mode("map")
      elif(key == "1"):
        ui_current_menu = "move"
      elif(key == "2" and menu_options_examine_text):
        ui_current_menu = "interact"
  # DEFAULT BEHAVIOR
  else:
    press_to_continue()

def ui_log(target_list):
  log_list_shortened = target_list[-abs(ui_log_display_length):]
  num = len(log_list_shortened)
  while num < ui_log_display_length:
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
  if settings['debug_log_to_file']:
    with open('debug_log.txt', 'a') as file:
      file.write(datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + " | " + item + "\n")

def change_mode(new_mode):
  global mode
  global previous_mode
  previous_mode = mode
  mode = new_mode

def queue_action(action):
  queue_list.append(action)

def execute_action(action):
  if action['type'] == 'enter_room':
    enter_room(action['link'])
  elif action['type'] == 'change_position':
    change_position(action['link'])
  elif action['type'] == 'activate_status':
    activate_status(action['link'])
  elif action['type'] == 'change_mode':
    change_mode(action['link'])
  add_debug_log("Action: " + action['type'] + " -> " + action['link'])

def run_queued_actions():
  while queue_list:
    action = queue_list.pop(0)
    execute_action(action)

def enable_event(link, category, disable = False):
  num = 0
  for room in rooms.values():
    for line in room[category]:
        if line['link'] == link:
          line['disabled'] = disable
          num += 1
  if num > 0:
    disable_text = "enabled"
    if disable:
      disable_text = "disabled"
    add_debug_log("Change event (" + str(num) + "): " + category + ":" + link + " -> " + disable_text)

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

def main_window_start_menu():
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
  lines.append('      db      `7MM"""YMM MMP""MM""YMM `7MM"""YMM  `7MM"""Mq.  `7MN.   `7MF\'`7MMF\'   ')
  lines.append('     ;MM:       MM    `7 P\'   MM   `7   MM    `7    MM   `MM.   MMN.    M    MM     ')
  lines.append('    ,V^MM.      MM   d        MM        MM   d      MM   ,M9    M YMb   M    MM     ')
  lines.append('   ,M  `MM      MMmmMM        MM        MMmmMM      MMmmdM9     M  `MN. M    MM     ')
  lines.append('   AbmmmqMA     MM   Y  ,     MM        MM   Y  ,   MM  YM.     M   `MM.M    MM     ')
  lines.append('  A\'     VML    MM     ,M     MM        MM     ,M   MM   `Mb.   M     YMM    MM     ')
  lines.append('.AMA.   .AMMA..JMMmmmmMMM   .JMML.    .JMMmmmmMMM .JMML. .JMM..JML.    YM  .JMML.   ')
  lines.append(color_end)
  return MainWindowContent(lines, True, True)

def main_window_debug():
  lines = []
  lines.append('RED: '.ljust(10) + color_red + ' FG ' + color_bright_red + ' BRIGHT ' + color_bg_red + ' BG ' + color_end + ' ' + color_bg_bright_red + ' BRIGHT ' + color_end)
  lines.append('GREEN: '.ljust(10) + color_green + ' FG ' + color_bright_green + ' BRIGHT ' + color_bg_green + ' BG ' + color_end + ' ' + color_bg_bright_green + ' BRIGHT ' + color_end)
  lines.append('YELLOW: '.ljust(10) + color_yellow + ' FG ' + color_bright_yellow + ' BRIGHT ' + color_bg_yellow + ' BG ' + color_end + ' ' + color_bg_bright_yellow + ' BRIGHT ' + color_end)
  lines.append('BLUE: '.ljust(10) + color_blue + ' FG ' + color_bright_blue + ' BRIGHT ' + color_bg_blue + ' BG ' + color_end + ' ' + color_bg_bright_blue + ' BRIGHT ' + color_end)
  lines.append('MAGENTA: '.ljust(10) + color_magenta + ' FG ' + color_bright_magenta + ' BRIGHT ' + color_bg_magenta + ' BG ' + color_end + ' ' + color_bg_bright_magenta + ' BRIGHT ' + color_end)
  lines.append('CYAN: '.ljust(10) + color_cyan + ' FG ' + color_bright_cyan + ' BRIGHT ' + color_bg_cyan + ' BG ' + color_end + ' ' + color_bg_bright_cyan + ' BRIGHT ' + color_end)
  lines.append('WHITE: '.ljust(10) + color_white + ' FG ' + color_bright_white + ' BRIGHT ' + color_bg_white + ' BG ' + color_end + ' ' + color_bg_bright_white + ' BRIGHT ' + color_end)
  lines.append("")
  lines.append('LAST INPUT: "' + debug_input_char + '"')
  return MainWindowContent(lines)

def main_window_cutscene():
  lines = load_cutscene(active_cutscene)
  return MainWindowContent(lines)

def main_window_game():
  lines = []
  lines.extend(show_active_status())
  lines.append("")
  lines.extend(load_room(active_room))
  return MainWindowContent(lines)

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
def main_window_map():
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
  #change_mode(previous_mode)
  return MainWindowContent(lines, False, True)
  
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
  lines.append("You are positioned at the " + format_position_text(current_position) + " of the " + room['noun'] + ".")
  lines.extend(sense_sight(room_id, True))
  lines.extend(sense_sound(room_id, True))
  lines.extend(sense_smell(room_id, True))
  return lines

def show_active_status():
  lines = []
  for line in statuses:
    if (statuses[line]['active']):
      lines.append(format_status(statuses[line]['text']))
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

def add_to_inventory(item):
  global inventory_list
  inventory_list.append(item)

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

# SETUP
main_title = "Cantus Aeterni"
debug_log_list = ["Starting game"]
debug_input_char = None
ui_size_upper = 3
ui_lower_input_options_length = 10
ui_size_lower = ui_lower_input_options_length + 3
ui_log_display_length = 10
ui_size_log = ui_log_display_length + 1
ui_log_active = False
ui_pre_quit_prompt = False
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
import_settings()
initialize()

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

# MAIN LOOP
while not quit_game:
  get_window_size()
  hide_cursor()
  clear_console()
  run_queued_actions()
  ui_upper()
  if mode == "start_menu":
    ui_main_window(main_window_start_menu())
  elif mode == "debug":
    ui_main_window(main_window_debug())
    ui_log(debug_log_list)
  elif mode == "cutscene":
    ui_main_window(main_window_cutscene())
  elif mode == "map":
    ui_main_window(main_window_map())
  elif mode == "game":
    ui_main_window(main_window_game())
    ui_log(log_list)
  ui_lower()
  loop_count += 1

add_debug_log("Quitting game")