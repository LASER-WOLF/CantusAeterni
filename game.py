import os
import ctypes
import json
import re
import msvcrt
import time
from datetime import datetime
import threading
import pygame
import random

MAIN_TITLE = "Cantus Aeterni"
MODE_MAIN_MENU = "main_menu"
MODE_DEBUG = "debug_screen"
MODE_SETTINGS = "settings_menu"
MODE_HELP = "help"
MODE_CUTSCENE = "cutscene"
MODE_GAME = "game"
MODE_MAP = "map"
MUSIC_TYPE_MAIN = "main"
MUSIC_TYPE_GAME = "game"
MUSIC = [
  {"file": "music/main1.mid", "type": MUSIC_TYPE_MAIN, "title": "Belle Qui Tiens Ma Vie"},
  {"file": "music/game_a1.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 1st Movement"},
  {"file": "music/game_a2.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 2nd Movement"},
  {"file": "music/game_a3.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 3rd Movement"},
  {"file": "music/game_a4.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 4th Movement"},
  {"file": "music/game_a5.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 5th Movement"},
  {"file": "music/game_a6.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 6th Movement"},
  {"file": "music/game_a7.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 7th Movement"},
  {"file": "music/game_b1.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 1st Movement"},
  {"file": "music/game_b2.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 2nd Movement"},
  {"file": "music/game_b3.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 3rd Movement"},
  {"file": "music/game_b4.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 4th Movement"},
  {"file": "music/game_b5.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 5th Movement"},
  {"file": "music/game_b6.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 6th Movement"},
  {"file": "music/game_c1.mid", "type": MUSIC_TYPE_GAME, "title": "Aria in Bm"},
  {"file": "music/game_c2.mid", "type": MUSIC_TYPE_GAME, "title": "Camille Tallard - Menuett in A"},
  {"file": "music/game_c3.mid", "type": MUSIC_TYPE_GAME, "title": "Rondeau in C"},
  {"file": "music/game_c4.mid", "type": MUSIC_TYPE_GAME, "title": "Ballet in D"},
  {"file": "music/game_c5.mid", "type": MUSIC_TYPE_GAME, "title": "Sylvius Leopold Weiss - Menuett in Dm"},
  {"file": "music/game_c6.mid", "type": MUSIC_TYPE_GAME, "title": "Favorita in D"},
  {"file": "music/game_c7.mid", "type": MUSIC_TYPE_GAME, "title": "Ivan Gelinek - Canarie in Bb"},
  {"file": "music/game_c8.mid", "type": MUSIC_TYPE_GAME, "title": "Gavotte in A"},
  {"file": "music/game_c9.mid", "type": MUSIC_TYPE_GAME, "title": "Ennemond Gaultier le vieux - Chaconne in A"},
  {"file": "music/game_c10.mid", "type": MUSIC_TYPE_GAME, "title": "Bouree in F"},
  {"file": "music/game_c11.mid", "type": MUSIC_TYPE_GAME, "title": "Ivan Gelinek - Allemande in Gm"}
]
#  {"file": "music/mystery1.mid", "title": "Courante in Am"},
#  {"file": "music/mystery2.mid", "title": "Johann Georg Weichenberger - Menuett in Gm"},
#  {"file": "music/drama1.mid", "title": "François Couperin - Les Plaisirs de Saint Germain en Laÿe"},
#  {"file": "music/drama2.mid", "title": "Germain Pinell - Branle des Frondeurs"},
#  {"file": "music/drama3.mid", "title": "Ennemond Gaultier le vieux - Canarie in A"},
#  {"file": "music/drama4.mid", "title": "Menuett in A"},
#  {"file": "music/drama5.mid", "title": "François Couperin - Les Baricades Misterieuses"},
#  {"file": "music/court1.mid", "title": "Greensleeves"},
#  {"file": "music/court2.mid", "title": "Trotto"},
#  {"file": "music/court3.mid", "title": "Saltarello"},

def main_loop():
  global loop_count
  while not quit_game:
    get_window_size()
    hide_cursor()
    clear_console()
    run_queued_actions()
    ui_upper()
    if mode == MODE_MAIN_MENU:
      ui_main_window(main_window_start_menu())
    elif mode == MODE_HELP:
      ui_main_window(main_window_help())
    elif mode == MODE_DEBUG:
      ui_main_window(main_window_debug())
      ui_log(debug_log_list)
    elif mode == MODE_CUTSCENE:
      ui_main_window(main_window_cutscene())
    elif mode == MODE_MAP:
      ui_main_window(main_window_map())
    elif mode == MODE_GAME:
      ui_main_window(main_window_game())
      ui_log(log_list)
    ui_lower()
    loop_count += 1
  music_stop()
  add_debug_log("Quitting game")

def music_loop():
  global music_title
  global music_skip_track_num
  while music_enable:
    for track in MUSIC:
      if (music_type is None or music_type == track['type']) and music_skip_track_num == 0:
        music_title = track['title']
        music_play(track['file'])
      if music_skip_track_num > 0:
        music_skip_track_num -= 1
      if not music_enable:
        music_title = None
        break

def music_initialize():
  freq = 44100  # audio CD quality
  bitsize = -16   # unsigned 16 bit
  channels = 1  # 1 is mono, 2 is stereo
  buffer = 1024   # number of samples
  pygame.mixer.init(freq, bitsize, channels, buffer)
  music_change_volume(settings['music_volume'])

def music_play(midi_filename):
  clock = pygame.time.Clock()
  pygame.mixer.music.load(midi_filename)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30)

def music_change_volume(volume = 1):
  global music_volume
  music_volume = volume
  pygame.mixer.music.set_volume(volume)  

def music_start():
  global music_enable
  music_enable = True
  thread_music = threading.Thread(target=music_loop)
  thread_music.start()

def music_stop():
  global music_enable
  music_enable = False
  pygame.mixer.music.stop()

def music_change_type(new_type = None):
  global music_type
  old_type = music_type
  music_type = new_type
  if old_type != new_type:
    music_next()

def music_next():
   pygame.mixer.music.fadeout(250)

def music_shuffle_next():
  global music_skip_track_num
  music_skip_track_num = random.randrange(0, len(MUSIC))

class MainWindowContent:
  def __init__(self, lines, centered_horizontal = False, centered_vertical = False):
    self.lines = lines
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical

def initialize():
  global queue_list
  queue_list = []
  change_mode(MODE_MAIN_MENU)
  add_debug_log("Main initialization")
  if settings['debug_mode'] and settings['debug_on_start']:
    change_mode(MODE_DEBUG)

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
  global log_list
  global inventory_list
  global active_cutscene
  global active_room
  global current_position
  rooms = json.load(open('data/rooms.json','r')) 
  cutscenes = json.load(open('data/cutscenes.json','r')) 
  interactables = json.load(open('data/interactables.json','r')) 
  portals = json.load(open('data/portals.json','r')) 
  statuses = json.load(open('data/statuses.json','r')) 
  items = json.load(open('data/items.json','r')) 
  log_list = ["You start the game"]
  inventory_list = []
  active_cutscene = "1"
  active_room = "1"
  current_position = "c"
  change_mode(MODE_CUTSCENE)
  add_debug_log("Initializing new game")

def initialize_new_mode():
  global ui_log_scroll_pos
  ui_log_scroll_pos = 0
  if mode == MODE_MAIN_MENU:
    music_change_type(MUSIC_TYPE_MAIN)
  elif mode == MODE_CUTSCENE or mode == MODE_GAME:
    music_shuffle_next()
    music_change_type(MUSIC_TYPE_GAME)

def change_mode(new_mode):
  global mode
  global previous_mode
  previous_mode = mode
  mode = new_mode
  initialize_new_mode()

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
      key = msvcrt.getch()
      if ord(key) == 224:
        key = ord(msvcrt.getch())
        if key == 72:
          key = "up"
        elif key == 77:
          key = "right"
        elif key == 80:
          key = "down"
        elif key == 75:
          key = "left"
        elif key == 73:
          key = "page_up"
        elif key == 81:
          key = "page_down"
        else:
          key = str(key)
      elif ord(key) == 13:
        key = "enter"
      elif ord(key) == 32:
        key = "space"
      elif ord(key) == 8:
        key = "backspace"
      else:
        if key.isascii():
          key = key.decode("ascii")
        else:
          key = "unknown"
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

def make_line(line, fill = "", align = "<", margin = 0):
  line_margin = ""
  for n in range(margin):
    line_margin += " "
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

def print_line(line, fill = "", align = "<", margin = 2):
  print(make_line(line, fill, align, margin));
  
def print_line_centered(line, fill = ""):
  print_line(line, fill, "^")
  
def print_seperator_line():
  print_line_centered("", "-")

def ui_main_window(content):
  if content.lines:
    main_window_size_subtract = ui_size_upper+ui_size_lower
    if mode == MODE_GAME or mode == MODE_DEBUG:
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
  if mode == MODE_MAIN_MENU:
    ui_upper_content.append("MAIN MENU")
  elif mode == MODE_SETTINGS:
    ui_upper_content.append("SETTINGS")
  elif mode == MODE_DEBUG:
    ui_upper_content.append("DEBUG SCREEN")
  elif mode == MODE_HELP:
    ui_upper_content.append("HELP")
  elif mode == MODE_CUTSCENE or mode == MODE_GAME:
    ui_upper_content.append("PLAYER NAME / LEVEL / HEALTH / ETC.")
  elif mode == MODE_MAP:
    ui_upper_content.append("MAP")
  if settings['debug_mode']:
    ui_upper_content.append("DEBUG MODE")
    ui_upper_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
    ui_upper_content.append("LOOP #: " + str(loop_count))
  for num, item in enumerate(ui_upper_content):
    if num != 0:
      ui_upper_string += " | "
    ui_upper_string += item
  print_line("")
  print_line(ui_upper_string)
  print_seperator_line()

def ui_block_minimap():
  lines = []
  lines.append("MEMORY (LOCAL):")
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
  map_char_tile_portal_current_low = color_portal + "└───┘" + color_end
  map_char_interactable_top = color_interactable + "┌───┐" + color_end
  map_char_interactable_mid = color_interactable + "│ E │" + color_end
  map_char_interactable_low = color_interactable + "└───┘" + color_end
  map_char_tile_interactable_current_top = color_interactable + "┌───┐" + color_end
  map_char_tile_interactable_current_mid = color_interactable + "│" + color_bright_yellow + "YOU" + color_interactable + "│" + color_end
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
  return lines

def ui_combine_blocks(blocks, height = 10, margin = 4):
  line_margin = ""
  for n in range(margin):
    line_margin += " "
  lines = []
  num = 0
  while num < height:
    lines.append("")
    num += 1
  for block in blocks:
    num = 0
    for line in block:
      if num < height:
        if lines[num] != "":
          lines[num] += line_margin
        lines[num] += line
      num += 1
  return lines

def ui_lower():
  global quit_game
  global ui_quit_prompt
  global ui_pre_quit_prompt
  global ui_restart_prompt
  global ui_current_menu
  global settings
  global ui_log_scroll_pos
  ui_blocks = []
  # PRE QUIT PROMPT
  if ui_pre_quit_prompt:
    print_line("SELECT ACTION:")
    print_line("[1] RETURN TO TITLE SCREEN")
    print_line("[2] QUIT GAME")
    print_line("[B] <- GO BACK")
  # QUIT PROMPT
  elif ui_quit_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
  # RESTART PROMPT
  elif ui_restart_prompt:
    print_line("ARE YOU SURE?")
    print_line("[Y] YES")
    print_line("[N] NO")
  # START MENU
  elif mode == MODE_MAIN_MENU: 
    print_line("[1] START GAME")
    print_line("[S] SETTINGS")
    if settings['debug_mode']:
      print_line("[D] DEBUG SCREEN")
    print_line("[?] HELP")
    print_line("[Q] QUIT")
  # SETTINGS MENU
  elif mode == MODE_SETTINGS: 
    print_line("[1] DEBUG MODE: " + str(settings['debug_mode']).upper())
    print_line("[2] DEBUG SCREEN ON START: " + str(settings['debug_on_start']).upper())
    print_line("[3] DEBUG LOG TO FILE: " + str(settings['debug_log_to_file']).upper())
    print_line("[4] ENABLE MINIMAP: " + str(settings['enable_minimap']).upper())
    print_line("[5] ENABLE MUSIC: " + str(settings['enable_music']).upper())
    print_line("[B] <- GO BACK")
  # DEBUG SCREEN
  elif mode == MODE_DEBUG: 
    print_line("[B] <- GO BACK")
  # GAME MODE
  elif mode == MODE_GAME:
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
    # INTERACT MENU
    elif ui_current_menu == "interact":
      print_line("AVAILABLE INTERACTIONS:")
      for line in menu_options_examine_text:
        print_line(line)
      print_line("[B] <- GO BACK")
    # MAIN MENU (GAME)
    else:
      lines = []
      lines.append("SELECT ACTION:")
      lines.append("[1] MOVE")
      if menu_options_examine_text:
        lines.append("[2] INTERACT")
      lines.append("[M] MAP")
      lines.append("[S] SETTINGS")
      if settings['debug_mode']:
        lines.append("[D] DEBUG SCREEN")
      lines.append("[?] HELP")
      lines.append("[Q] QUIT")
      
      if settings['enable_minimap']:
        ui_blocks.append(ui_block_minimap())
      ui_blocks.append(lines)
      for line in ui_combine_blocks(ui_blocks):
        print_line(line)
  # MAP / HELP SCREEN
  elif mode == MODE_MAP or mode == MODE_HELP: 
    print_line("[B] <- GO BACK")
    
  # HANDLE INPUT
  if mode == MODE_CUTSCENE:
    press_to_continue()
  else:
    key = get_keypress()
    # PRE QUIT PROMPT
    if ui_pre_quit_prompt:
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
      if(key.lower() == "y"):
        quit_game = True
      elif(key.lower() == "n"):
        ui_quit_prompt = False
    # RESTART PROMPT
    elif ui_restart_prompt:
      if(key.lower() == "y"):
        initialize()
        change_mode(mode)
        ui_restart_prompt = False
      elif(key.lower() == "n"):
        ui_restart_prompt = False
    # START MENU
    elif mode == MODE_MAIN_MENU: 
      if(key.lower() == "q"):
        ui_quit_prompt = True
      elif(key.lower() == "d" and settings['debug_mode']):
        change_mode(MODE_DEBUG)
      elif(key == "1"):
        initialize_new_game()
      elif(key.lower() == "s"):
        change_mode(MODE_SETTINGS)
      elif(key.lower() == "?"):
        change_mode(MODE_HELP)
    # SETTINGS MENU
    elif mode == MODE_SETTINGS: 
      if(key.lower() == "b"):
        export_json('settings', settings)
        change_mode(previous_mode)
      elif(key == "1"):
        settings['debug_mode'] = not settings['debug_mode']
      elif(key == "2"):
        settings['debug_on_start'] = not settings['debug_on_start']
      elif(key == "3"):
        settings['debug_log_to_file'] = not settings['debug_log_to_file']
      elif(key == "4"):
        settings['enable_minimap'] = not settings['enable_minimap']
      elif(key == "5"):
        settings['enable_music'] = not settings['enable_music']
        if settings['enable_music'] and not music_enable:
          music_start()
        elif not settings['enable_music'] and music_enable:
          music_stop()
    # DEBUG SCREEN
    elif mode == MODE_DEBUG: 
      if(key.lower() == "b"):
        change_mode(previous_mode)
      if(key == "up"):
        ui_log_scroll_pos += 1
      elif(key == "down"):
          ui_log_scroll_pos -= 1
      elif(key == "right"):
          music_next()
    # GAME MODE
    elif mode == MODE_GAME:
      # MOVE MENU
      if ui_current_menu == "move":
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
        if(key.lower() == "q"):
          ui_pre_quit_prompt = True
        elif(key.lower() == "d" and settings['debug_mode']):
          change_mode(MODE_DEBUG)
        elif(key.lower() == "s"):
          change_mode(MODE_SETTINGS)
        elif(key.lower() == "m"):
          change_mode(MODE_MAP)
        elif(key == "1"):
          ui_current_menu = "move"
        elif(key == "2" and menu_options_examine_text):
          ui_current_menu = "interact"
        elif(key.lower() == "?"):
          change_mode(MODE_HELP)
      if(key == "up"):
        ui_log_scroll_pos += 1
      elif(key == "down"):
          ui_log_scroll_pos -= 1
    # MAP / HELP SCREEN
    elif mode == MODE_MAP or mode == MODE_HELP: 
      if(key.lower() == "b"):
        change_mode(previous_mode)

def make_scrollbar(scrollbar_window_height, scroll_pos, scroll_max):
  scrollbar_style_line = "│"
  scrollbar_style_body_top = color_bg_bright_yellow + " " + color_end
  scrollbar_style_body_mid = color_bg_bright_yellow + " " + color_end
  scrollbar_style_body_low = color_bg_bright_yellow + " " + color_end
  lines = []
  scrollbar_pos = 0
  scrollbar_size = 1
  if scroll_pos > 0 and scroll_max > 0:
    scrollbar_pos = int(scrollbar_window_height - (scrollbar_window_height * scroll_pos/scroll_max))+1
    if scrollbar_pos - scrollbar_size <= 1 and scroll_pos != scroll_max:
      scrollbar_pos = scrollbar_size + 1
  num = 0
  scrollbar_body_pos = 1
  while num < scrollbar_window_height:
    scrollbar = scrollbar_style_line
    if scrollbar_pos != 0:
      scrollbar_pos = min(scrollbar_pos, scrollbar_window_height - scrollbar_size)
      scrollbar_pos = max(scrollbar_pos, scrollbar_size + 1 )
      if num + 1 in range(scrollbar_pos-scrollbar_size, scrollbar_pos + scrollbar_size + 1):
        if scrollbar_body_pos == 1:
          scrollbar = scrollbar_style_body_top
        elif scrollbar_body_pos == scrollbar_size + 1 + scrollbar_size:
          scrollbar = scrollbar_style_body_low
        else:
          scrollbar = scrollbar_style_body_mid
        scrollbar_body_pos += 1
    lines.append(scrollbar)
    num += 1
  return lines

def ui_log(target_list):
  global ui_log_scroll_pos
  target_list_len = len(target_list)
  max_scroll_num = max(0, target_list_len-ui_size_log_num_lines)
  ui_log_scroll_pos = max(0, ui_log_scroll_pos)
  ui_log_scroll_pos = min(max_scroll_num, ui_log_scroll_pos)
  ui_log_start_pos = -abs(ui_size_log_num_lines + ui_log_scroll_pos)
  ui_log_end_pos = -abs(ui_log_scroll_pos)
  if ui_log_end_pos == 0:
    ui_log_end_pos = None
  target_list_shortened = target_list[ui_log_start_pos:ui_log_end_pos]
  scrollbar = make_scrollbar(ui_size_log_num_lines, ui_log_scroll_pos, max_scroll_num)
  num = len(target_list_shortened)
  while num < ui_size_log_num_lines:
    print_line(scrollbar[num-1] + "")
    num += 1
  for num, line in enumerate(target_list_shortened):
    print_line(scrollbar[num] + " " + line)
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
  justnum = 15
  lines.append('RED: '.ljust(justnum) + color_red + ' FG ' + color_bright_red + ' BRIGHT ' + color_bg_red + ' BG ' + color_end + ' ' + color_bg_bright_red + ' BRIGHT ' + color_end)
  lines.append('GREEN: '.ljust(justnum) + color_green + ' FG ' + color_bright_green + ' BRIGHT ' + color_bg_green + ' BG ' + color_end + ' ' + color_bg_bright_green + ' BRIGHT ' + color_end)
  lines.append('YELLOW: '.ljust(justnum) + color_yellow + ' FG ' + color_bright_yellow + ' BRIGHT ' + color_bg_yellow + ' BG ' + color_end + ' ' + color_bg_bright_yellow + ' BRIGHT ' + color_end)
  lines.append('BLUE: '.ljust(justnum) + color_blue + ' FG ' + color_bright_blue + ' BRIGHT ' + color_bg_blue + ' BG ' + color_end + ' ' + color_bg_bright_blue + ' BRIGHT ' + color_end)
  lines.append('MAGENTA: '.ljust(justnum) + color_magenta + ' FG ' + color_bright_magenta + ' BRIGHT ' + color_bg_magenta + ' BG ' + color_end + ' ' + color_bg_bright_magenta + ' BRIGHT ' + color_end)
  lines.append('CYAN: '.ljust(justnum) + color_cyan + ' FG ' + color_bright_cyan + ' BRIGHT ' + color_bg_cyan + ' BG ' + color_end + ' ' + color_bg_bright_cyan + ' BRIGHT ' + color_end)
  lines.append('WHITE: '.ljust(justnum) + color_white + ' FG ' + color_bright_white + ' BRIGHT ' + color_bg_white + ' BG ' + color_end + ' ' + color_bg_bright_white + ' BRIGHT ' + color_end)
  lines.append("")
  lines.append('LAST INPUT: '.ljust(justnum) + '"' + str(debug_input_char)  + '"')
  lines.append('')
  lines.append('MUSIC STATUS: '.ljust(justnum) + str(music_enable) + ":" + str(music_type) + ":" + str(settings['music_volume']))
  lines.append('MUSIC TITLE: '.ljust(justnum) + str(music_title))
  
  return MainWindowContent(lines)

def main_window_help():
  lines = []
  lines.append('MUSIC BY:')
  lines.append('Lory Werths')
  lines.append('www.mandolingals.tripod.com')
  lines.append('')
  lines.append('CONTROLS:')
  lines.append('[UP]'.ljust(6) + ' SCROLL UP')
  lines.append('[DOWN]'.ljust(6) + ' SCROLL DOWN')
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

def main_window_map():
  lines = []
  lines.append("MEMORY (LOCAL):")
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
  map_char_tile_portal_current_low = color_portal + "└───┘" + color_end
  map_char_interactable_top = color_interactable + "┌───┐" + color_end
  map_char_interactable_mid = color_interactable + "│ E │" + color_end
  map_char_interactable_low = color_interactable + "└───┘" + color_end
  map_char_tile_interactable_current_top = color_interactable + "┌───┐" + color_end
  map_char_tile_interactable_current_mid = color_interactable + "│" + color_bright_yellow + "YOU" + color_interactable + "│" + color_end
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
  if mode != MODE_GAME:
    change_mode(MODE_GAME)
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
mode = None
previous_mode = None
debug_log_list = ["Starting game"]
debug_input_char = None
ui_size_upper = 3
ui_size_lower_num_lines = 10
ui_size_lower = ui_size_lower_num_lines + 3
ui_size_log_num_lines = 10
ui_size_log = ui_size_log_num_lines + 1
ui_pre_quit_prompt = False
ui_quit_prompt = False
ui_restart_prompt = False
ui_current_menu = ""
default_window_size_x = 50
default_window_size_y = 200
window_size_x = default_window_size_x
window_size_y = default_window_size_y
loop_count = 0
quit_game = False
direction_abr = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }
music_enable = False
music_title = None
music_type = None
music_skip_track_num = 0
import_settings()
music_initialize()
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
os.system("title " + MAIN_TITLE)

# MAXIMIZE WINDOW
if(os.name == 'nt'):
  kernel32 = ctypes.WinDLL('kernel32')
  user32 = ctypes.WinDLL('user32')
  SW_NORMAL = 1
  SW_MAXIMIZE = 3
  hWnd = kernel32.GetConsoleWindow()
  user32.ShowWindow(hWnd, SW_NORMAL)
  user32.ShowWindow(hWnd, SW_MAXIMIZE)

# START THREADS
thread_main = threading.Thread(target=main_loop)
thread_main.start()
if settings['enable_music']:
  music_start()
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