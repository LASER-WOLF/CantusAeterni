import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import ctypes
import json
import re
import msvcrt
import time
from datetime import datetime
import threading
from pygame import mixer as pygame_mixer
from pygame import time as pygame_time
import random
import math

# SET CONSTANTS
MAIN_TITLE = "Cantus Aeterni"
MODE_MAIN_MENU = "main_menu"
MODE_DEBUG = "debug_screen"
MODE_SETTINGS = "settings_menu"
MODE_HELP = "help"
MODE_CUTSCENE = "cutscene"
MODE_GAME = "game"
MODE_MAP = "map"
WINDOW_UPPER = "upper"
WINDOW_CENTER = "center"
WINDOW_LOWER = "lower"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# SET MUSIC
MUSIC_TYPE_MAIN = "main"
MUSIC_TYPE_GAME = "game"
MUSIC = [
  {"file": "music/main1.mid", "type": MUSIC_TYPE_MAIN, "title": "Belle Qui Tiens Ma Vie"},
  #{"file": "music/court1.mid", "type": MUSIC_TYPE_GAME, "title": "Greensleeves"},
  #{"file": "music/court2.mid", "type": MUSIC_TYPE_GAME, "title": "Trotto"},
  #{"file": "music/court3.mid", "type": MUSIC_TYPE_GAME, "title": "Saltarello"},
  {"file": "music/game_a1.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 1st Movement"},
  {"file": "music/game_a2.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 2nd Movement"},
  {"file": "music/game_a3.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 3rd Movement"},
  {"file": "music/game_a4.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 4th Movement"},
  {"file": "music/game_a5.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 5th Movement"},
  {"file": "music/game_a6.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 6th Movement"},
  {"file": "music/game_a7.mid", "type": MUSIC_TYPE_GAME, "title": "Robert deVisée - Guitar Suite in Gm - 7th Movement"},
  #{"file": "music/drama1.mid", "type": MUSIC_TYPE_GAME, "title": "François Couperin - Les Plaisirs de Saint Germain en Laÿe"},
  #{"file": "music/drama2.mid", "type": MUSIC_TYPE_GAME, "title": "Germain Pinell - Branle des Frondeurs"},
  #{"file": "music/drama3.mid", "type": MUSIC_TYPE_GAME, "title": "Ennemond Gaultier le vieux - Canarie in A"},
  #{"file": "music/drama4.mid", "type": MUSIC_TYPE_GAME, "title": "Menuett in A"},
  #{"file": "music/drama5.mid", "type": MUSIC_TYPE_GAME, "title": "François Couperin - Les Baricades Misterieuses"},
  {"file": "music/game_b1.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 1st Movement"},
  {"file": "music/game_b2.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 2nd Movement"},
  {"file": "music/game_b3.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 3rd Movement"},
  {"file": "music/game_b4.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 4th Movement"},
  {"file": "music/game_b5.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 5th Movement"},
  {"file": "music/game_b6.mid", "type": MUSIC_TYPE_GAME, "title": "Suite in Bm - 6th Movement"},
  #{"file": "music/mystery1.mid", "type": MUSIC_TYPE_GAME, "title": "Courante in Am"},
  #{"file": "music/mystery2.mid", "type": MUSIC_TYPE_GAME, "title": "Johann Georg Weichenberger - Menuett in Gm"},
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

# SET COLORS
COLORS = {
  "red": "\x1b[0;31;40m",
  "green": "\x1b[0;32;40m",
  "yellow": "\x1b[0;33;40m",
  "blue": "\x1b[0;34;40m",
  "magenta": "\x1b[0;35;40m",
  "cyan": "\x1b[0;36;40m",
  "white": "\x1b[0;37;40m",
  "bright_black": "\x1b[0;90;40m",
  "bright_red": "\x1b[0;91;40m",
  "bright_green": "\x1b[0;92;40m",
  "bright_yellow": "\x1b[0;93;40m",
  "bright_blue": "\x1b[0;94;40m",
  "bright_magenta": "\x1b[0;95;40m",
  "bright_cyan": "\x1b[0;96;40m",
  "bright_white": "\x1b[0;97;40m",
  "bg_red": "\x1b[0;30;41m",
  "bg_green": "\x1b[0;30;42m",
  "bg_yellow": "\x1b[0;30;43m",
  "bg_blue": "\x1b[0;30;44m",
  "bg_magenta": "\x1b[0;30;45m",
  "bg_cyan": "\x1b[0;30;46m",
  "bg_white": "\x1b[0;30;47m",
  "bg_bright_black": "\x1b[0;30;100m",
  "bg_bright_red": "\x1b[0;30;101m",
  "bg_bright_green": "\x1b[0;30;102m",
  "bg_bright_yellow": "\x1b[0;30;103m",
  "bg_bright_blue": "\x1b[0;30;104m",
  "bg_bright_magenta": "\x1b[0;30;105m",
  "bg_bright_cyan": "\x1b[0;30;106m",
  "bg_bright_white": "\x1b[0;30;107m",
}
COLOR_DEFAULT = COLORS['bright_yellow']
COLOR_DARK = COLORS['bright_black']
COLOR_UI_HIGHLIGHT = COLORS['bg_bright_yellow']
COLOR_TITLE_SCREEN = COLORS['bright_cyan']
COLOR_INTERACTABLE = COLORS['bright_green']
COLOR_PORTAL = COLORS['bright_cyan']
COLOR_DIRECTION = COLORS['bright_blue']
COLOR_STATUS = COLORS['bright_magenta']
COLOR_FILL = COLOR_DARK
COLOR_MAP_INACTIVE = COLOR_DARK
COLOR_MAP_SELECTED = COLOR_DEFAULT

# SET PATTERNS
FILL_CHAR = "ƒ"
FILL_PATTERNS = {
  'dots1': [
    "  .",
    ".  "
  ],
  'dots2': [
    " ´    ",
    "      ",
    "      ",
    "    ` ",
    "      ",
    "      ",
  ],
  'crosses1': [
    " ┼    ",
    "      ",
    "    ┼ ",
  ],
  'floral1': [
    " ,´    ",
    "       ",
    "    `, ",
  ],
  'arrows1': [
    " »    ",
    "    « ",
  ],
  'stars1': [
    "     *  ",
    "      -    ",
    "    *     ",
    "    -      ",
    "  *   ",
    "       - ",
    "      * ",
    "  -       ",
    " *      ",
    " -    ",
  ],
  'title_screen': [
    "      ",
    " ´    ",
    "      ",
    "      ",
    "    ` ",
    "      ",
  ]
}
FILL_PATTERN_COLORS = {
  'title_screen': [
    COLORS['red'],
    COLORS['yellow'],
    COLORS['green'],
    COLORS['magenta'],
    COLORS['cyan'],
  ]
}

"""
def refresh_screen(lines):
  clear_console()
  final_string = ""
  for line_num, line in enumerate(lines):
    print (line)
"""

def refresh_screen(lines):
  final_string = HIDE_CURSOR
  for line_num, line in enumerate(lines):
    if line_num > 0:
      final_string += "\n"
    final_string += line
  clear_console()
  print (final_string)

def main_loop():
  global loop_count
  while not quit_game:
    get_window_size()
    #hide_cursor()
    #clear_console()
    run_queued_actions()
    if mode == MODE_MAIN_MENU:
      refresh_screen(ui_combine_windows([
        upper_window(),
        center_window_main_menu(),
        lower_window_main_menu(),
      ]))
    """
    elif mode == MODE_HELP:
      ui_window_main(main_window_help())
    elif mode == MODE_DEBUG:
      ui_window_main(main_window_debug())
      ui_log(debug_log_list)
    elif mode == MODE_CUTSCENE:
      ui_window_main(main_window_cutscene())
    elif mode == MODE_MAP:
      ui_window_main(main_window_map())
    elif mode == MODE_GAME:
      ui_window_main(main_window_game())
      ui_log(log_list)
    """
    #ui_lower()
    handle_input()
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
  pygame_mixer.init(freq, bitsize, channels, buffer)
  music_change_volume(settings['music_volume'])

def music_play(midi_filename):
  clock = pygame_time.Clock()
  pygame_mixer.music.load(midi_filename)
  pygame_mixer.music.play()
  while pygame_mixer.music.get_busy():
    clock.tick(30)

def music_change_volume(volume = 1):
  global music_volume
  music_volume = volume
  pygame_mixer.music.set_volume(volume)  

def music_start():
  global music_enable
  music_enable = True
  thread_music = threading.Thread(target=music_loop)
  thread_music.start()

def music_stop():
  global music_enable
  music_enable = False
  pygame_mixer.music.stop()

def music_change_type(new_type = None):
  global music_type
  old_type = music_type
  music_type = new_type
  if old_type != new_type:
    music_shuffle_next()
    music_next()

def music_next(fadeout = 250):
   pygame_mixer.music.fadeout(fadeout)

def music_shuffle_next():
  global music_skip_track_num
  music_skip_track_num = random.randrange(0, len(MUSIC))

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

def change_mode(new_mode):
  global mode
  global previous_mode
  global ui_selection_options
  global ui_selection_x
  global ui_selection_y
  global ui_log_scroll_pos
  previous_mode = mode
  mode = new_mode
  ui_log_scroll_pos = 0
  ui_selection_options = None
  ui_selection_x = 0
  ui_selection_y = 0
  if mode == MODE_MAIN_MENU:
    music_change_type(MUSIC_TYPE_MAIN)
  elif mode == MODE_CUTSCENE or mode == MODE_GAME:
    music_change_type(MUSIC_TYPE_GAME)

def get_window_size():
  global window_size_x
  global window_size_y
  window_size_x = os.get_terminal_size().columns
  window_size_y = os.get_terminal_size().lines - 1

def clear_console():
  if(os.name == 'posix'):
     os.system('clear')
  else:
     os.system('cls')

def get_keypress():
  while True:
    if msvcrt.kbhit():
      key_raw = msvcrt.getch()
      key = key_raw
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
      elif ord(key) == 27:
        key = "escape"
      else:
        if key.isascii():
          key = key.decode("ascii")
        else:
          key = "unknown"
      global debug_input_char
      global debug_input_char_ord
      debug_input_char = key
      debug_input_char_ord = ord(key_raw)
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
  return COLOR_STATUS + text + COLOR_DEFAULT

def format_interactable(text):
  return COLOR_INTERACTABLE + text + COLOR_DEFAULT

def format_direction(text):
  return COLOR_DIRECTION + text + COLOR_DEFAULT

def format_portal(text):
  return COLOR_PORTAL + text + COLOR_DEFAULT

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

def multi_replace_list(target_list, target_dict):
  new_list = []
  for line in target_list:
    new_list.append(multi_replace(line, target_dict))
  return new_list

def multi_replace(target_line, target_dict):
  for substring in target_dict.values():
    target_line = target_line.replace(substring, '')
  return target_line

def make_line(line, line_color = None, fill = None, fill_color = None, align = "l", margin = 2):
  def increment_fill(fill_num, fill_length):
    fill_num += 1
    if fill_num >= fill_length:
      fill_num = 0
    return fill_num
  line_without_hidden_chars = multi_replace(line, COLORS)
  line_length = len(line_without_hidden_chars)
  centered_start = math.floor((window_size_x - line_length) / 2)
  if fill:
    fill_length = len(fill)
    if not fill_color:
      fill_color = COLOR_FILL
  line_formatted = ""
  num = 0
  while num < window_size_x:
    if line_length > 0 and ((align == "l" and num == margin) or (align == "c" and num == centered_start) or (align == "r" and num == window_size_x - (line_length + margin))):
      num += line_length
      line_formatted += line
    else:
      line_formatted += FILL_CHAR
      num += 1
  if line_color:
    line_formatted_color = ""
    non_fill_combo = ""
    for character in line_formatted:
      if character == FILL_CHAR:
        if non_fill_combo:
          line_formatted_color += line_color + non_fill_combo
          non_fill_combo = ""
        line_formatted_color += FILL_CHAR
      else:
        non_fill_combo += character
    if non_fill_combo:
          line_formatted_color += line_color + non_fill_combo
    line_formatted = line_formatted_color
  if fill:
    line_formatted = re.sub("(" + FILL_CHAR + "+)", fill_color + r"\1" + COLOR_DEFAULT, line_formatted)
    if fill_length <= 1:
      line_formatted = line_formatted.replace(FILL_CHAR, fill)
    else:
      fill_num = 0
      line_formatted_fill = ""
      non_fill_combo = ""
      for character in line_formatted:
        if character == FILL_CHAR:
          if non_fill_combo:
            line_formatted_fill += non_fill_combo
            for n in range(len(multi_replace(non_fill_combo, COLORS))):
              fill_num = increment_fill(fill_num, fill_length)
            non_fill_combo = ""
          line_formatted_fill += fill[fill_num]
          fill_num = increment_fill(fill_num, fill_length)
        else:
          non_fill_combo += character
      if non_fill_combo:
            line_formatted_fill += non_fill_combo
      line_formatted = line_formatted_fill
  else:
    line_formatted = line_formatted.replace(FILL_CHAR, " ")
  return line_formatted

def make_line_centered(line, line_color = None, fill = None, fill_color = None):
  return make_line(line, line_color, fill, fill_color, "c")

"""
def print_line(line, line_color = None, fill = None, fill_color = None, align = "l", margin = 2):
  print(make_line(line, line_color, fill, fill_color, align, margin));
  
def print_line_centered(line, line_color = None, fill = None, fill_color = None):
  print_line(line, line_color, fill, fill_color, "c")
  
def print_seperator_line():
  print_line_centered("", None, "-", COLOR_DEFAULT)
"""

def increment_list_loop(target_list, num):
  item = target_list
  if target_list:
    num += 1
    if num >= len(target_list):
      num = 0
    item = target_list[num]
  return item, num

class WindowContent:
  def __init__(self, window_type, lines, line_color = None, fill = None, fill_color = None, centered_horizontal = False, centered_vertical = False):
    self.window_type = window_type
    self.lines = lines
    self.line_color = line_color
    self.fill = fill
    self.fill_color = fill_color
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical

class Line:
  def __init__(self, content, color = None, fill = None, fill_color = None, centered = False):
    self.content = content
    self.color = color
    self.fill = fill
    self.fill_color = fill_color
    self.centered = centered

def fill_init(fill):
  fill_list = fill
  fill_num = 0
  if fill:
    fill = fill_list[fill_num]
  return fill, fill_list, fill_num

def ui_seperator():
  return Line("", fill = "-", fill_color = COLOR_DEFAULT)

def ui_window_upper(content):
  lines = []
  # INIT FILL
  fill, fill_list, fill_num = fill_init(content.fill)
  fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
  # FIRST LINE EMPTY
  lines.append(Line("", None, fill, fill_color))
  # INCREMENT FILL
  fill, fill_num = increment_list_loop(fill_list, fill_num)
  fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  # CONTENT
  for num, line in enumerate(content.lines):
    lines.append(Line(line, content.line_color, fill, fill_color))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  lines.append(ui_seperator())
  return lines

def ui_window_lower(content):
  lines = []
  # INIT FILL
  fill, fill_list, fill_num = fill_init(content.fill)
  fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
  # CONTENT
  for num, line in enumerate(content.lines):
    lines.append(Line(line, content.line_color, fill, fill_color))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  return lines

def ui_combine_windows(windows):
  lines = []
  # FIND UPPER AND LOWER WINDOWS
  size_upper = 0
  size_lower = 0
  content_upper = []
  content_lower = []
  for window in windows:
    if window.window_type == WINDOW_UPPER:
      window_formatted = ui_window_upper(window)
      content_upper.append(window_formatted)
      size_upper += len(window_formatted)
    elif window.window_type == WINDOW_LOWER:
      window_formatted = ui_window_lower(window)
      content_lower.append(window_formatted)
      size_lower += len(window_formatted)
  # FIND CENTER WINDOW
  content_center = []
  for window in windows:
    if window.window_type == WINDOW_CENTER:
      content_center.append(ui_window_center(window, size_upper, size_lower))
  # PRINT ALL WINDOWS
  for window in content_upper + content_center + content_lower:
    for line in window:
      if line.centered:
        lines.append(make_line_centered(line.content, line.color, line.fill, line.fill_color))
      else:
        lines.append(make_line(line.content, line.color, line.fill, line.fill_color))
  return lines

def ui_window_center(content, padding_top = 0, padding_bottom = 0):
  if padding_bottom > 0:
    padding_bottom += 1
  padding = padding_top + padding_bottom
  lines = []
  # INIT FILL
  fill, fill_list, fill_num = fill_init(content.fill)
  fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
  # CENTER CONTENT
  num_empty = 0
  if content.centered_vertical:
    while num_empty < ((window_size_y - padding) - len(content.lines)) / 2:
      # FIRST LINE EMPTY
      lines.append(Line("", None, fill, fill_color))
      # INCREMENT FILL
      fill, fill_num = increment_list_loop(fill_list, fill_num)
      fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
      num_empty += 1
  # CONTENT
  for num, line in enumerate(content.lines):
    lines.append(Line(line, content.line_color, fill, fill_color, content.centered_horizontal))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  #EMPTY LINES BOTTOM
  while num + 1 + num_empty < window_size_y - padding:
    # FIRST LINE EMPTY
    lines.append(Line("", None, fill, fill_color))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
    num_empty += 1
  if padding_bottom > 0:
    lines.append(ui_seperator())
  add_debug_log(str(padding_bottom))
  return lines

def ui_block_minimap(room_id):
  lines = []
  lines.append("MEMORY (LOCAL):".ljust(15))
  map_char_tile_top_upper_left = COLOR_MAP_INACTIVE + "┌─   " + COLOR_DEFAULT
  map_char_tile_top_upper_right = COLOR_MAP_INACTIVE + "   ─┐" + COLOR_DEFAULT
  map_char_tile_bottom_lower_left = COLOR_MAP_INACTIVE + "└─   " + COLOR_DEFAULT
  map_char_tile_bottom_lower_right = COLOR_MAP_INACTIVE + "   ─┘" + COLOR_DEFAULT
  map_char_tile_top = COLOR_MAP_INACTIVE + "     " + COLOR_DEFAULT
  map_char_tile_mid = COLOR_MAP_INACTIVE + "  -  " + COLOR_DEFAULT
  map_char_tile_low = COLOR_MAP_INACTIVE + "     " + COLOR_DEFAULT
  map_char_tile_visited_top = COLOR_MAP_INACTIVE + "┌───┐" + COLOR_DEFAULT
  map_char_tile_visited_mid = COLOR_MAP_INACTIVE + "│   │" + COLOR_DEFAULT
  map_char_tile_visited_low = COLOR_MAP_INACTIVE + "└───┘" + COLOR_DEFAULT
  map_char_tile_current_top = COLOR_MAP_SELECTED + "┌───┐" + COLOR_DEFAULT
  map_char_tile_current_mid = COLOR_MAP_SELECTED + "│YOU│" + COLOR_DEFAULT
  map_char_tile_current_low = COLOR_MAP_SELECTED + "└───┘" + COLOR_DEFAULT
  map_char_portal_top = COLOR_PORTAL + "┌───┐" + COLOR_DEFAULT
  map_char_portal_mid = COLOR_PORTAL + "│ P │" + COLOR_DEFAULT
  map_char_portal_low = COLOR_PORTAL + "└───┘" + COLOR_DEFAULT
  map_char_tile_portal_current_top = COLOR_PORTAL + "┌───┐" + COLOR_DEFAULT
  map_char_tile_portal_current_mid = COLOR_PORTAL + "│" + COLOR_MAP_SELECTED + "YOU" + COLOR_PORTAL + "│" + COLOR_DEFAULT
  map_char_tile_portal_current_low = COLOR_PORTAL + "└───┘" + COLOR_DEFAULT
  map_char_interactable_top = COLOR_INTERACTABLE + "┌───┐" + COLOR_DEFAULT
  map_char_interactable_mid = COLOR_INTERACTABLE + "│ E │" + COLOR_DEFAULT
  map_char_interactable_low = COLOR_INTERACTABLE + "└───┘" + COLOR_DEFAULT
  map_char_tile_interactable_current_top = COLOR_INTERACTABLE + "┌───┐" + COLOR_DEFAULT
  map_char_tile_interactable_current_mid = COLOR_INTERACTABLE + "│" + COLOR_MAP_SELECTED + "YOU" + COLOR_INTERACTABLE + "│" + COLOR_DEFAULT
  map_char_tile_interactable_current_low = COLOR_INTERACTABLE + "└───┘" + COLOR_DEFAULT
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
      if pos == 'nw':
        tile_top = map_char_tile_top_upper_left
      elif pos == 'ne':
        tile_top = map_char_tile_top_upper_right
      elif pos == 'sw':
        tile_low = map_char_tile_bottom_lower_left
      elif pos == 'se':
        tile_low = map_char_tile_bottom_lower_right
      if rooms[room_id]['visited'][pos]:
        tile_top = map_char_tile_visited_top
        tile_mid = map_char_tile_visited_mid
        tile_low = map_char_tile_visited_low
        if pos == current_position:
          tile_top = map_char_tile_current_top
          tile_mid = map_char_tile_current_mid
          tile_low = map_char_tile_current_low
      for portal in rooms[room_id]['portal']:
        if portal['position'] == pos and portal['disabled'] == False and rooms[room_id]['visited'][pos]:
          tile_top = map_char_portal_top
          tile_mid = map_char_portal_mid
          tile_low = map_char_portal_low
          if pos == current_position:
            tile_top = map_char_tile_portal_current_top
            tile_mid = map_char_tile_portal_current_mid
            tile_low = map_char_tile_portal_current_low
      for interactable in rooms[room_id]['interactable']:
        if interactable['position'] == pos and interactable['disabled'] == False and rooms[room_id]['visited'][pos]:
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

def list_none_filter(target_list):
  return [i for i in target_list if i is not None]

def list_longest_entry(target_list):
  return len(max(target_list, key = len))

def fill_empty_space(line, length, char = None):
  if not char:
    char = FILL_CHAR
  for n in range(length):
    line += char
  return line

def ui_combine_blocks(blocks, height = 10, margin_size = 4):
  margin = fill_empty_space("", margin_size)
  lines = []
  for block_num, block in enumerate(blocks):
    just_num = list_longest_entry(multi_replace_list(list_none_filter(block), COLORS))
    for line_num in range(height):
      line = ""
      if line_num < len(block):
        if block[line_num]:
          line = block[line_num]
      if line_num < height:
        line = fill_empty_space(line, just_num - len(multi_replace(line, COLORS)))
        if block_num == 0:
          lines.append(line)
        else:
          lines[line_num] += margin + line
  return lines

def dict_key_by_value(target_dict, target_value):
  return [k for k, v in target_dict.items() if v == target_value]

def move_north():
  global current_position
  pos = direction_to_coord[current_position]
  if pos['y'] > -1:
    change_position(dict_key_by_value(direction_to_coord, {'x': pos['x'], 'y': pos['y']-1})[0], True)
    
def move_south():
  global current_position
  pos = direction_to_coord[current_position]
  if pos['y'] < 1:
    change_position(dict_key_by_value(direction_to_coord, {'x': pos['x'], 'y': pos['y']+1})[0], True)
    
def move_west():
  global current_position
  pos = direction_to_coord[current_position]
  if pos['x'] > -1:
    change_position(dict_key_by_value(direction_to_coord, {'x': pos['x']-1, 'y': pos['y']})[0], True)

def move_east():
  global current_position
  pos = direction_to_coord[current_position]
  if pos['x'] < 1:
    change_position(dict_key_by_value(direction_to_coord, {'x': pos['x']+1, 'y': pos['y']})[0], True)

def ui_selection_y_prev():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_y > 0:
    ui_selection_y -= 1
    while ui_selection_x > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_x -= 1
    while ui_selection_x < len(ui_selection_options) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_x += 1

def ui_selection_y_next():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_y < len(ui_selection_options[ui_selection_x])-1:
    ui_selection_y += 1
    while ui_selection_x > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_x -= 1
    while ui_selection_x < len(ui_selection_options) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_x += 1

def ui_selection_x_prev():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_x > 0:
    ui_selection_x -= 1
    while ui_selection_y > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_y -= 1
    while ui_selection_y < len(ui_selection_options[ui_selection_x]) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_y += 1

def ui_selection_x_next():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_x < len(ui_selection_options)-1:
    ui_selection_x += 1
    while ui_selection_y > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_y -= 1
    while ui_selection_y < len(ui_selection_options[ui_selection_x]) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
      ui_selection_y += 1

def make_scrollbar(scrollbar_window_height, scroll_pos, scroll_max):
  scrollbar_style_line = "│"
  scrollbar_style_body_top = COLORS['bg_bright_yellow'] + " " + COLOR_DEFAULT
  scrollbar_style_body_mid = COLORS['bg_bright_yellow'] + " " + COLOR_DEFAULT
  scrollbar_style_body_low = COLORS['bg_bright_yellow'] + " " + COLOR_DEFAULT
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

def add_debug_log(item, error = False):
  global debug_log_list
  if error:
    item = "ERROR: " + item
  debug_log_list.append(item)
  if settings['debug_error_log_to_file'] and error:
    with open('error_log.txt', 'a') as file:
      file.write(datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + " | " + item + "\n")
  elif settings['debug_log_to_file']:
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

def upper_window():
  upper_window_content = []
  if mode == MODE_MAIN_MENU:
    upper_window_content.append("MAIN MENU")
  elif mode == MODE_SETTINGS:
    upper_window_content.append("SETTINGS")
  elif mode == MODE_DEBUG:
    upper_window_content.append("DEBUG SCREEN")
  elif mode == MODE_HELP:
    upper_window_content.append("HELP")
  elif mode == MODE_CUTSCENE or mode == MODE_GAME:
    upper_window_content.append("PLAYER NAME / LEVEL / HEALTH / ETC.")
  elif mode == MODE_MAP:
    upper_window_content.append("MAP")
  if settings['debug_mode']:
    if mode != MODE_DEBUG:
      upper_window_content.append("DEBUG MODE")
    upper_window_content.append("WINDOW SIZE: " + str(window_size_x) + "x" + str(window_size_y))
    upper_window_content.append("LOOP #: " + str(loop_count))
  upper_window_string = ""
  for num, item in enumerate(upper_window_content):
    if num != 0:
      upper_window_string += " | "
    upper_window_string += item
  lines = []
  lines.append(upper_window_string)
  return WindowContent(WINDOW_UPPER, lines)

def lower_window_main_menu():
  global ui_selection_options
  ui_selection_options = []
  
  
  
  options_column1 = []
  options_column1.append("START GAME")
  options_column1.append("PREFERENCES")
  if settings['debug_mode']:
    options_column1.append("DEBUG SCREEN")
  options_column1.append("HELP")
  options_column1.append("QUIT")
  #ui_selection_options.append(options_column1)
  
  options_column2 = []
  options_column2.append("option")
  options_column2.append("option")
  options_column2.append("option")
  options_column2.append("option")
  options_column2.append("option")
  options_column2.append("option")
  #ui_selection_options.append(options_column2)
  
  options = []
  options.append(options_column1)
  options.append(options_column2)
  
  #selection_indicator = ">"
  
  #ui_selection_options[ui_selection_x][ui_selection_y] = COLOR_HIGHLIGHT + "> " + ui_selection_options[ui_selection_x][ui_selection_y] + COLOR_DEFAULT
  
  
  
  #if ui_selection_options[ui_selection_y][ui_selection_x]==
  #selection_indicator = ">"
  
  
  #just_num = 2
  num_x = len(options)
  num_y = len(max(options, key = len))
  
  for x in range(num_x):
    just_num = list_longest_entry(multi_replace_list(list_none_filter(options[x]), COLORS)) + 2
    ui_selection_options.append([])
    for y in range(num_y):
      entry = None
      if y < len(options[x]):
        entry = " " + options[x][y] + " "
        entry = fill_empty_space(entry, just_num - len(multi_replace(entry, COLORS)), " ")
        if x == ui_selection_x and y == ui_selection_y:
          #entry = COLOR_UI_HIGHLIGHT + ">".ljust(just_num) + entry + COLOR_DEFAULT
          entry = COLOR_UI_HIGHLIGHT + entry + COLOR_DEFAULT
        #else:
        #  entry = "".ljust(just_num) + entry
      ui_selection_options[x].append(entry)
        #ui_selection_options[x].append("TEST")
      #else:
        #ui_selection_options[x].append(None)
  """
  for column_num, column in enumerate(ui_selection_options):
    for row_num in range(longest_row_num):
      if row_num > len(column):
        if column_num == ui_selection_x and row_num == ui_selection_y:
          ui_selection_options[column_num][row_num] = COLOR_HIGHLIGHT + ">".ljust(just_num) + ui_selection_options[column_num][row_num] + COLOR_DEFAULT
        else:
          ui_selection_options[column_num][row_num] = "".ljust(just_num) + ui_selection_options[column_num][row_num]
      else:
        ui_selection_options[column_num][row_num] = None
  """
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_selection_options))

def handle_input():
  global quit_game
  if mode == MODE_CUTSCENE:
    press_to_continue()
  else:
    key = get_keypress()
    """
    # PRE QUIT PROMPT
    if ui_pre_quit_prompt:
      if(key == "1"):
        ui_pre_quit_prompt = False
        ui_restart_prompt = True
      elif(key == "2"):
        ui_pre_quit_prompt = False
        ui_quit_prompt = True
      elif(key == "escape"):
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
    """
    # MAIN MENU
    if mode == MODE_MAIN_MENU: 
      if(key == "escape"):
        #ui_quit_prompt = True
        quit_game = True
      elif(key.lower() == "w"):
        ui_selection_y_prev()
      elif(key.lower() == "s"):
        ui_selection_y_next()
      elif(key.lower() == "a"):
        ui_selection_x_prev()
      elif(key.lower() == "d"):
        ui_selection_x_next()

def center_window_main_menu():
  lines = []
  lines.append('')
  lines.append('ƒƒ.g8"""bgdƒƒƒƒƒdbƒƒƒƒƒƒ`7MN.ƒƒƒ`7MF\'MMP""MM""YMMƒ`7MMF\'ƒƒƒ`7MF\'.M"""bgdƒ')
  lines.append('.dP\'ƒƒƒƒƒ`Mƒƒƒƒ;MM:ƒƒƒƒƒƒƒMMN.ƒƒƒƒMƒƒP\'ƒƒƒMMƒƒƒ`7ƒƒƒMMƒƒƒƒƒƒƒMƒ,MIƒƒƒƒ"Yƒ')
  lines.append('dM\'ƒƒƒƒƒƒƒ`ƒƒƒ,V^MM.ƒƒƒƒƒƒMƒYMbƒƒƒMƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒMƒ`MMb.ƒƒƒƒƒ')
  lines.append('MMƒƒƒƒƒƒƒƒƒƒƒ,Mƒƒ`MMƒƒƒƒƒƒMƒƒ`MN.ƒMƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒMƒƒƒ`YMMNq.ƒ')
  lines.append('MM.ƒƒƒƒƒƒƒƒƒƒAbmmmqMAƒƒƒƒƒMƒƒƒ`MM.MƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒMƒ.ƒƒƒƒƒ`MMƒ')
  lines.append('`Mb.ƒƒƒƒƒ,\'ƒA\'ƒƒƒƒƒVMLƒƒƒƒMƒƒƒƒƒYMMƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒYM.ƒƒƒƒƒ,MƒMbƒƒƒƒƒdMƒ')
  lines.append('ƒƒ`"bmmmd\'.AMA.ƒƒƒ.AMMA..JML.ƒƒƒƒYMƒƒƒƒƒ.JMML.ƒƒƒƒƒƒƒ`bmmmmd"\'ƒP"Ybmmd"ƒƒ')
  lines.append('')
  lines.append('ƒƒƒƒƒƒdbƒƒƒƒƒƒ`7MM"""YMMƒMMP""MM""YMMƒ`7MM"""YMMƒƒ`7MM"""Mq.ƒƒ`7MN.ƒƒƒ`7MF\'`7MMF\'')
  lines.append('ƒƒƒƒƒ;MM:ƒƒƒƒƒƒƒMMƒƒƒƒ`7ƒP\'ƒƒƒMMƒƒƒ`7ƒƒƒMMƒƒƒƒ`7ƒƒƒƒMMƒƒƒ`MM.ƒƒƒMMN.ƒƒƒƒMƒƒƒƒMMƒƒ')
  lines.append('ƒƒƒƒ,V^MM.ƒƒƒƒƒƒMMƒƒƒdƒƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒdƒƒƒƒƒƒMMƒƒƒ,M9ƒƒƒƒMƒYMbƒƒƒMƒƒƒƒMMƒƒ')
  lines.append('ƒƒƒ,Mƒƒ`MMƒƒƒƒƒƒMMmmMMƒƒƒƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMmmMMƒƒƒƒƒƒMMmmdM9ƒƒƒƒƒMƒƒ`MN.ƒMƒƒƒƒMMƒƒ')
  lines.append('ƒƒƒAbmmmqMAƒƒƒƒƒMMƒƒƒYƒƒ,ƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒYƒƒ,ƒƒƒMMƒƒYM.ƒƒƒƒƒMƒƒƒ`MM.MƒƒƒƒMMƒƒ')
  lines.append('ƒƒA\'ƒƒƒƒƒVMLƒƒƒƒMMƒƒƒƒƒ,MƒƒƒƒƒMMƒƒƒƒƒƒƒƒMMƒƒƒƒƒ,MƒƒƒMMƒƒƒ`Mb.ƒƒƒMƒƒƒƒƒYMMƒƒƒƒMMƒƒ')
  lines.append('.AMA.ƒƒƒ.AMMA..JMMmmmmMMMƒƒƒ.JMML.ƒƒƒƒ.JMMmmmmMMMƒ.JMML.ƒ.JMM..JML.ƒƒƒƒYMƒƒ.JMML.')
  lines.append('')
  return WindowContent(WINDOW_CENTER, lines, COLOR_TITLE_SCREEN, FILL_PATTERNS['title_screen'], None, True, True)

def main_window_debug():
  lines = []
  justnum = 15
  lines.append('RED: '.ljust(justnum) + COLORS['red'] + ' FG ' + COLORS['bright_red'] + ' BRIGHT ' + COLORS['bg_red'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_red'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('GREEN: '.ljust(justnum) + COLORS['green'] + ' FG ' + COLORS['bright_green'] + ' BRIGHT ' + COLORS['bg_green'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_green'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('YELLOW: '.ljust(justnum) + COLORS['yellow'] + ' FG ' + COLORS['bright_yellow'] + ' BRIGHT ' + COLORS['bg_yellow'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_yellow'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('BLUE: '.ljust(justnum) + COLORS['blue'] + ' FG ' + COLORS['bright_blue'] + ' BRIGHT ' + COLORS['bg_blue'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_blue'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('MAGENTA: '.ljust(justnum) + COLORS['magenta'] + ' FG ' + COLORS['bright_magenta'] + ' BRIGHT ' + COLORS['bg_magenta'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_magenta'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('CYAN: '.ljust(justnum) + COLORS['cyan'] + ' FG ' + COLORS['bright_cyan'] + ' BRIGHT ' + COLORS['bg_cyan'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_cyan'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('WHITE: '.ljust(justnum) + COLORS['white'] + ' FG ' + COLORS['bright_white'] + ' BRIGHT ' + COLORS['bg_white'] + ' BG ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_white'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append('BLACK: '.ljust(justnum)  + '    ' + COLORS['bright_black'] + ' BRIGHT ' + '    ' + COLOR_DEFAULT + ' ' + COLORS['bg_bright_black'] + ' BRIGHT ' + COLOR_DEFAULT)
  lines.append("")
  lines.append('LAST INPUT: '.ljust(justnum) + '"' + str(debug_input_char)  + '" (' + str(debug_input_char_ord) + ')')
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

def map_portal_check(portal_check_dict = {'selected_room': '1', 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}}):
  selected_room_root = portal_check_dict['selected_room']
  current_coords_root = portal_check_dict['current_coords']
  portal_check_dict['checked_rooms'][selected_room_root] = portal_check_dict['current_coords']
  for portal in rooms[selected_room_root]['portal']:
    if portal['disabled'] == False:
      next_room = portals[portal['link']]['link2']
      next_dir = portals[portal['link']]['dir']
      next_portal_pos = portals[portal['link']]['pos2']
      if next_room == selected_room_root:
        next_room = portals[portal['link']]['link1']
        next_dir = direction_reverse[next_dir]
        next_portal_pos = portals[portal['link']]['pos1']
      if not next_room in portal_check_dict['checked_rooms'] and rooms[next_room]['visited'][next_portal_pos]:
        next_coords = {'x': current_coords_root['x'] + direction_to_coord[next_dir]['x'], 'y': current_coords_root['y'] + direction_to_coord[next_dir]['y']}
        portal_check_dict['selected_room'] = next_room
        portal_check_dict['current_coords'] = next_coords
        portal_check_dict = map_portal_check(portal_check_dict)
  return portal_check_dict

def main_window_map():
  global ui_selection_options
  global ui_selection_y
  global ui_selection_x
  ui_selection_options_update = []
  lines = []
  map_tile_empty_top = "ƒƒƒ"
  map_tile_empty_low = "ƒƒƒ"
  map_tile_visited_top = COLOR_MAP_INACTIVE + "┌─┐" + COLOR_DEFAULT
  map_tile_visited_low = COLOR_MAP_INACTIVE + "└─┘" + COLOR_DEFAULT
  map_tile_selected_top = COLOR_MAP_SELECTED + "╔═╗" + COLOR_DEFAULT
  map_tile_selected_low = COLOR_MAP_SELECTED + "╚═╝" + COLOR_DEFAULT
  map_tile_active_top = COLOR_MAP_SELECTED + "┌|┐" + COLOR_DEFAULT
  map_tile_active_low = COLOR_MAP_SELECTED + "└─┘" + COLOR_DEFAULT
  map_tile_active_selected_top = COLOR_MAP_SELECTED + "╔|╗" + COLOR_DEFAULT
  map_tile_active_selected_low = COLOR_MAP_SELECTED + "╚═╝" + COLOR_DEFAULT
  known_rooms = map_portal_check({'selected_room': active_room, 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}})['checked_rooms']
  #known_rooms_sorted = sorted(known_rooms.items(), key=lambda room: (room[1]['y'], room[1]['x']))
  zero_x = min(coord['x'] for coord in known_rooms.values())
  zero_y = min(coord['y'] for coord in known_rooms.values())
  for room in known_rooms.values():
    room['x'] += abs(zero_x)
    room['y'] += abs(zero_y)
  max_x = max(coord['x'] for coord in known_rooms.values())+1
  max_y = max(coord['y'] for coord in known_rooms.values())+1
  y = 0
  x = 0
  while y < max_y:
    ui_selection_options_update.append([])
    map_line_top = ""
    map_line_low = ""
    while x < max_x:
      if x > 0:
        map_line_top += " "
        map_line_low += " "
      if {'x': x, 'y': y} in known_rooms.values():
        found_rooms = dict_key_by_value(known_rooms, {'x': x, 'y': y})
        found_room = found_rooms[0]
        ui_selection_options_update[y].append(found_room)
        if len(found_rooms) > 1:
          add_debug_log("Multiple rooms with same coordinates " + "(ID: " + str(found_rooms) + ")", True)
        selected_room = active_room
        if ui_selection_options:
          selected_room = ui_selection_options[ui_selection_y][ui_selection_x]
        elif found_room == selected_room:
          ui_selection_x = x
          ui_selection_y = y
        if found_room == active_room:
          if found_room == selected_room:
            map_line_top += map_tile_active_selected_top
            map_line_low += map_tile_active_selected_low
          else:
            map_line_top += map_tile_active_top
            map_line_low += map_tile_active_low
        elif found_room == selected_room:
          map_line_top += map_tile_selected_top
          map_line_low += map_tile_selected_low
        else:
          map_line_top += map_tile_visited_top
          map_line_low += map_tile_visited_low
      else:
        ui_selection_options_update[y].append(None)
        map_line_top += map_tile_empty_top
        map_line_low += map_tile_empty_low
      x += 1
    lines.append(map_line_top)
    lines.append(map_line_low)
    x = 0
    y += 1
  ui_selection_options = ui_selection_options_update
  if settings['debug_mode']:
    lines.append("DEBUG: " + str(ui_selection_options[ui_selection_y][ui_selection_x]))
  return MainWindowContent(lines, None, True, True, FILL_PATTERNS['dots1'])
  
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

def ui_lower():
  global quit_game
  global ui_quit_prompt
  global ui_pre_quit_prompt
  global ui_restart_prompt
  global ui_current_menu
  global settings
  global ui_log_scroll_pos
  global ui_selection_options
  ui_blocks = []
  # PRE QUIT PROMPT
  if ui_pre_quit_prompt:
    print_line("SELECT ACTION:")
    print_line("[1]   RETURN TO TITLE SCREEN")
    print_line("[2]   QUIT GAME")
    print_line("[ESC] <- GO BACK")
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
    print_line("[1]   START GAME")
    print_line("[P]   PREFERENCES")
    if settings['debug_mode']:
      print_line("[-]   DEBUG SCREEN")
    print_line("[?]   HELP")
    print_line("[ESC] QUIT")
  # SETTINGS MENU
  elif mode == MODE_SETTINGS: 
    print_line("[1]   DEBUG MODE: " + str(settings['debug_mode']).upper())
    print_line("[2]   DEBUG SCREEN ON START: " + str(settings['debug_on_start']).upper())
    print_line("[3]   DEBUG LOG TO FILE: " + str(settings['debug_log_to_file']).upper())
    print_line("[4]   ERROR LOG TO FILE: " + str(settings['debug_error_log_to_file']).upper())
    print_line("[5]   ENABLE MINIMAP: " + str(settings['enable_minimap']).upper())
    print_line("[6]   ENABLE MUSIC: " + str(settings['enable_music']).upper())
    print_line("[ESC] <- GO BACK")
  # DEBUG SCREEN
  elif mode == MODE_DEBUG: 
    print_line("[ESC] <- GO BACK")
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
        menu_options_examine_text.append("[" + str(num) + "]   (EXAMINE) " + line['content'].upper())
        num += 1
    for line in room['portal']:
      if line['position'] == current_position and not line['disabled']:
        menu_options_portal.append(line['link'])
        menu_options_examine_text.append("[" + str(num) + "]   (EXIT) " + line['content'].upper())
        num += 1
    # INTERACT MENU
    if ui_current_menu == "interact":
      print_line("AVAILABLE INTERACTIONS:")
      for line in menu_options_examine_text:
        print_line(line)
      print_line("[ESC] <- GO BACK")
    # MAIN MENU (GAME)
    else:
      lines = []
      lines.append("SELECT ACTION:")
      if menu_options_examine_text:
        lines.append("[E]   INTERACT")
      lines.append("[M]   MAP")
      lines.append("[P]   PREFERENCES")
      if settings['debug_mode']:
        lines.append("[-]   DEBUG SCREEN")
      lines.append("[?]   HELP")
      lines.append("[ESC] QUIT")
      if settings['enable_minimap']:
        ui_blocks.append(ui_block_minimap(active_room))
      ui_blocks.append(lines)
      for line in ui_combine_blocks(ui_blocks):
        print_line(line)
  # MAP SCREEN
  elif mode == MODE_MAP:
    lines = []
    lines.append("SELECT ACTION:")
    lines.append("[ESC] <- GO BACK")
    ui_blocks.append(ui_block_minimap(ui_selection_options[ui_selection_y][ui_selection_x]))
    ui_blocks.append(lines)
    for line in ui_combine_blocks(ui_blocks):
      print_line(line)
  # HELP SCREEN
  elif mode == MODE_HELP: 
    print_line("[ESC] <- GO BACK")
    
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
      elif(key == "escape"):
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
      if(key.lower() == "escape"):
        ui_quit_prompt = True
      elif(key.lower() == "-" and settings['debug_mode']):
        change_mode(MODE_DEBUG)
      elif(key == "1"):
        initialize_new_game()
      elif(key.lower() == "p"):
        change_mode(MODE_SETTINGS)
      elif(key.lower() == "?"):
        change_mode(MODE_HELP)
    # SETTINGS MENU
    elif mode == MODE_SETTINGS: 
      if(key == "escape"):
        export_json('settings', settings)
        change_mode(previous_mode)
      elif(key == "1"):
        settings['debug_mode'] = not settings['debug_mode']
      elif(key == "2"):
        settings['debug_on_start'] = not settings['debug_on_start']
      elif(key == "3"):
        settings['debug_log_to_file'] = not settings['debug_log_to_file']
      elif(key == "4"):
        settings['debug_error_log_to_file'] = not settings['debug_error_log_to_file']
      elif(key == "5"):
        settings['enable_minimap'] = not settings['enable_minimap']
      elif(key == "6"):
        settings['enable_music'] = not settings['enable_music']
        if settings['enable_music'] and not music_enable:
          music_start()
        elif not settings['enable_music'] and music_enable:
          music_stop()
    # DEBUG SCREEN
    elif mode == MODE_DEBUG: 
      if(key == "escape"):
        change_mode(previous_mode)
      if(key == "up"):
        ui_log_scroll_pos += 1
      elif(key == "down"):
          ui_log_scroll_pos -= 1
      elif(key == "right"):
          music_next(0)
    # GAME MODE
    elif mode == MODE_GAME:
      # INTERACT MENU
      if ui_current_menu == "interact":
        if(key == "escape"):
          ui_current_menu = None
        num = 1
        for item in menu_options_examine:
          if(key == str(num)):
            ui_current_menu = None
            examine(menu_options_examine[num-1])
          num += 1
        num = 1
        for item in menu_options_portal:
          if(key == str(num)):
            ui_current_menu = None
            enter_portal(menu_options_portal[num-1])
          num += 1
      # MAIN MENU (GAME)
      else:
        if(key.lower() == "escape"):
          ui_pre_quit_prompt = True
        elif(key.lower() == "-" and settings['debug_mode']):
          change_mode(MODE_DEBUG)
        elif(key.lower() == "p"):
          change_mode(MODE_SETTINGS)
        elif(key.lower() == "m"):
          change_mode(MODE_MAP)
        elif(key == "e" and menu_options_examine_text):
          ui_current_menu = "interact"
        elif(key.lower() == "?"):
          change_mode(MODE_HELP)
        elif(key.lower() == "w"):
          move_north()
        elif(key.lower() == "s"):
          move_south()
        elif(key.lower() == "a"):
          move_west()
        elif(key.lower() == "d"):
          move_east()
      if(key == "up"):
        ui_log_scroll_pos += 1
      elif(key == "down"):
          ui_log_scroll_pos -= 1
    # MAP SCREEN
    elif mode == MODE_MAP: 
      if(key == "escape"):
        change_mode(previous_mode)
      elif(key.lower() == "w"):
        ui_selection_y_prev()
      elif(key.lower() == "s"):
        ui_selection_y_next()
      elif(key.lower() == "a"):
        ui_selection_x_prev()
      elif(key.lower() == "d"):
        ui_selection_x_next()
    # HELP SCREEN
    elif mode == MODE_HELP: 
      if(key == "escape"):
        change_mode(previous_mode)

# SETUP
mode = None
previous_mode = None
debug_log_list = ["Starting game"]
debug_input_char = None
debug_input_char_ord = None
#ui_size_upper = 3
#ui_size_lower_num_lines = 10
#ui_size_lower = ui_size_lower_num_lines + 3
#ui_size_log_num_lines = 10
#ui_size_log = ui_size_log_num_lines + 1
ui_pre_quit_prompt = False
ui_quit_prompt = False
ui_restart_prompt = False
ui_current_menu = None
ui_selection_options = None
ui_selection_x = None
ui_selection_y = None
default_window_size_x = 200
default_window_size_y = 50
window_size_x = default_window_size_x
window_size_y = default_window_size_y
loop_count = 0
quit_game = False
direction_abr = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }
direction_to_coord = {'nw': {'x': -1, 'y': -1}, 'n': {'x': 0, 'y': -1}, 'ne': {'x': 1, 'y': -1}, 'w': {'x': -1, 'y': 0}, 'c': {'x': 0, 'y': 0}, 'e': {'x': 1, 'y': 0}, 'sw': {'x': -1, 'y': 1}, 's': {'x': 0, 'y': 1}, 'se': {'x': 1, 'y': 1} }
direction_reverse = {'nw': 'se', 'n': 's', 'ne': 'sw', 'w': 'e', 'c': 'c', 'e': 'w', 'sw': 'ne', 's': 'n', 'se': 'nw' }
music_enable = False
music_title = None
music_type = None
music_skip_track_num = 0
import_settings()
music_initialize()
initialize()

# SET WINDOW TITLE & SIZE & FG/BG COLOR
os.system("mode "+str(default_window_size_x)+","+str(default_window_size_y))
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