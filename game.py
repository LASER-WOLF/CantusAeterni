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

# SET VARS
run_game = True
loop_count = 0
mode = None
previous_mode = None
debug_log_list = ["Starting game"]
debug_input_char = None
ui_pre_quit_prompt = False
ui_quit_prompt = False
ui_restart_prompt = False
ui_selection_options = None
ui_selection_x = None
ui_selection_y = None
default_window_size_x = 200
default_window_size_y = 50
window_size_x = default_window_size_x
window_size_y = default_window_size_y
music_enable = False
music_title = None
music_type = None
music_skip_track_num = 0

# SET CONSTANTS
MAIN_TITLE = "Cantus Aeterni"
MODE_MAIN_MENU = "main_menu"
MODE_DEBUG = "debug_screen"
MODE_SETTINGS = "settings_menu"
MODE_HELP = "help"
MODE_CHARACTER_CREATOR = "character_creator"
MODE_CUTSCENE = "cutscene"
MODE_GAME = "game"
MODE_MAP = "map"
WINDOW_UPPER = "upper"
WINDOW_CENTER = "center"
WINDOW_LOWER = "lower"
WINDOW_LOG = "log"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
DIRECTION_ABR = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }
DIRECTION_TO_COORD = {'nw': {'x': -1, 'y': -1}, 'n': {'x': 0, 'y': -1}, 'ne': {'x': 1, 'y': -1}, 'w': {'x': -1, 'y': 0}, 'c': {'x': 0, 'y': 0}, 'e': {'x': 1, 'y': 0}, 'sw': {'x': -1, 'y': 1}, 's': {'x': 0, 'y': 1}, 'se': {'x': 1, 'y': 1} }
DIRECTION_REVERSE = {'nw': 'se', 'n': 's', 'ne': 'sw', 'w': 'e', 'c': 'c', 'e': 'w', 'sw': 'ne', 's': 'n', 'se': 'nw' }

# SET CONSTANTS, MUSIC
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

# SET CONSTANTS, SOUNDS
SOUNDS = {
  'boot': 'sound/boot.ogg',
  'ui_sel': 'sound/ui_sel.wav',
  'ui_confirm': 'sound/ui_confirm.wav',
  'ui_confirm_big': 'sound/ui_confirm_big.wav',
  'ui_back': 'sound/ui_back.wav',
}

# SET CONSTANTS, COLORS
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
COLOR_UNDERLINE = re.sub("\[0;", "[4;", COLOR_DEFAULT)
COLOR_DARK = COLORS['bright_black']
COLOR_UI_HIGHLIGHT = COLOR_DEFAULT
COLOR_UI_HIGHLIGHT_BG = COLORS['bg_bright_yellow']
COLOR_TITLE_SCREEN = COLORS['bright_cyan']
COLOR_INTERACTABLE = COLORS['bright_green']
COLOR_PORTAL = COLORS['bright_cyan']
COLOR_DIRECTION = COLORS['bright_blue']
COLOR_STATUS = COLORS['bright_magenta']
COLOR_FILL = COLOR_DARK
COLOR_MAP_INACTIVE = COLOR_DARK
COLOR_MAP_SELECTED = COLOR_DEFAULT

# SET CONSTANTS, PATTERNS
FILL_CHAR = "ƒ"
FILL_PATTERNS = {
  'dots1': [
    "  .",
    ".  "
  ],
  'dots2': [
    "      ",
    " ´    ",
    "      ",
    "      ",
    "    ` ",
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
}
FILL_PATTERN_COLORS = {
  'rygma': [
    COLORS['red'],
    COLORS['yellow'],
    COLORS['green'],
    COLORS['magenta'],
    COLORS['cyan'],
  ]
}

# MAP TILES
MAP_TILES = {
  'empty_top': "ƒƒƒ",
  'empty_low': "ƒƒƒ",
  'visited_top': COLOR_MAP_INACTIVE + "┌─┐" + COLOR_DEFAULT,
  'visited_low': COLOR_MAP_INACTIVE + "└─┘" + COLOR_DEFAULT,
  'selected_top': COLOR_MAP_SELECTED + "╔═╗" + COLOR_DEFAULT,
  'selected_low': COLOR_MAP_SELECTED + "╚═╝" + COLOR_DEFAULT,
  'active_top': COLOR_MAP_SELECTED + "┌|┐" + COLOR_DEFAULT,
  'active_low': COLOR_MAP_SELECTED + "└─┘" + COLOR_DEFAULT,
  'active_selected_top': COLOR_MAP_SELECTED + "╔|╗" + COLOR_DEFAULT,
  'active_selected_low': COLOR_MAP_SELECTED + "╚═╝" + COLOR_DEFAULT,
}

MINIMAP_TILES = {  
  'undiscovered_top': COLOR_MAP_INACTIVE + "     " + COLOR_DEFAULT,
  'undiscovered_mid': COLOR_MAP_INACTIVE + "  -  " + COLOR_DEFAULT,
  'undiscovered_low': COLOR_MAP_INACTIVE + "     " + COLOR_DEFAULT,
  'undiscovered_top_upper_left': COLOR_MAP_INACTIVE + "┌─   " + COLOR_DEFAULT,
  'undiscovered_top_upper_right': COLOR_MAP_INACTIVE + "   ─┐" + COLOR_DEFAULT,
  'undiscovered_bottom_lower_left': COLOR_MAP_INACTIVE + "└─   " + COLOR_DEFAULT,
  'undiscovered_bottom_lower_right': COLOR_MAP_INACTIVE + "   ─┘" + COLOR_DEFAULT,
  'visited_top': COLOR_MAP_INACTIVE + "┌───┐" + COLOR_DEFAULT,
  'visited_mid': COLOR_MAP_INACTIVE + "│   │" + COLOR_DEFAULT,
  'visited_low': COLOR_MAP_INACTIVE + "└───┘" + COLOR_DEFAULT,
  'current_top': COLOR_MAP_SELECTED + "┌───┐" + COLOR_DEFAULT,
  'current_mid': COLOR_MAP_SELECTED + "│YOU│" + COLOR_DEFAULT,
  'current_low': COLOR_MAP_SELECTED + "└───┘" + COLOR_DEFAULT,
  'portal_top': COLOR_PORTAL + "┌───┐" + COLOR_DEFAULT,
  'portal_mid': COLOR_PORTAL + "│ P │" + COLOR_DEFAULT,
  'portal_low': COLOR_PORTAL + "└───┘" + COLOR_DEFAULT,
  'portal_current_top': COLOR_PORTAL + "┌───┐" + COLOR_DEFAULT,
  'portal_current_mid': COLOR_PORTAL + "│" + COLOR_MAP_SELECTED + "YOU" + COLOR_PORTAL + "│" + COLOR_DEFAULT,
  'portal_current_low': COLOR_PORTAL + "└───┘" + COLOR_DEFAULT,
  'interactable_top': COLOR_INTERACTABLE + "┌───┐" + COLOR_DEFAULT,
  'interactable_mid': COLOR_INTERACTABLE + "│ E │" + COLOR_DEFAULT,
  'interactable_low': COLOR_INTERACTABLE + "└───┘" + COLOR_DEFAULT,
  'interactable_current_top': COLOR_INTERACTABLE + "┌───┐" + COLOR_DEFAULT,
  'interactable_current_mid': COLOR_INTERACTABLE + "│" + COLOR_MAP_SELECTED + "YOU" + COLOR_INTERACTABLE + "│" + COLOR_DEFAULT,
  'interactable_current_low': COLOR_INTERACTABLE + "└───┘" + COLOR_DEFAULT,
}

class WindowContent:
  def __init__(self, window_type, lines = None, line_color = None, fill = None, fill_color = None, centered_horizontal = False, centered_vertical = False, min_height = None):
    self.window_type = window_type
    self.lines = lines
    self.line_color = line_color
    self.fill = fill
    self.fill_color = fill_color
    self.centered_horizontal = centered_horizontal
    self.centered_vertical = centered_vertical
    self.min_height = min_height

class Line:
  def __init__(self, content, color = None, fill = None, fill_color = None, centered = False):
    self.content = content
    self.color = color
    self.fill = fill
    self.fill_color = fill_color
    self.centered = centered

class SelectionOption:
  def __init__(self, name, display_name, link = None, selection_type = None):
    self.name = name
    self.display_name = display_name
    self.link = link
    self.selection_type = selection_type

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

def initialize_music():
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

def play_sound(sound):
  pygame_mixer.Sound.play(pygame_mixer.Sound(sound))

def sound_ui(sound):
  if settings['enable_sound'] and settings['enable_sound_ui']:
      play_sound(SOUNDS[sound])

def import_settings():
  global settings
  settings = json.load(open('settings.json','r'))

def initialize_main_menu():
  global queue_list
  queue_list = []
  change_mode(MODE_MAIN_MENU)
  add_debug_log("Main initialization")
  if settings['debug_mode'] and settings['debug_on_start']:
    change_mode(MODE_DEBUG)

def initialize():
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
  #BOOT SCREEN
  if settings['enable_boot_screen']:
    boot_screen()
  # START THREADS
  thread_main = threading.Thread(target=main_loop)
  thread_main.start()
  if settings['enable_music']:
    music_start()

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
  add_debug_log("Initializing new game")
  change_mode(MODE_CHARACTER_CREATOR)
  global character_name
  character_name = ""

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

def refresh_screen(lines):
  final_string = HIDE_CURSOR
  for line_num, line in enumerate(lines):
    if line_num > 0:
      final_string += "\n"
    final_string += line
  clear_console()
  print (final_string)

def boot_screen():
  get_window_size()
  lines = []
  for line in range(window_size_y):
    lines.append("BOOTING")
  refresh_screen(ui_combine_windows_make_lines([ui_window_center(WindowContent(WINDOW_CENTER, lines, COLOR_DEFAULT, ["."], [COLOR_DEFAULT]))]))
  time.sleep(0.5)
  if settings['enable_sound']:
    play_sound(SOUNDS['boot'])
  refresh_screen(lines)
  time.sleep(0.25)
  refresh_screen(ui_combine_windows_make_lines([ui_window_center(WindowContent(WINDOW_CENTER, "", COLOR_DEFAULT, ["#"], [COLORS['bg_bright_yellow']]))]))
  time.sleep(0.05)

def main_loop():
  global loop_count
  while run_game:
    get_window_size()
    run_queued_actions()
    windows = []
    if mode == MODE_MAIN_MENU:
      windows = [
        upper_window(),
        center_window_main_menu(),
        lower_window_empty(),
      ]
    elif mode == MODE_DEBUG:
      windows = [
        upper_window(),
        center_window_debug(),
        log_window_debug(),
        lower_window_debug(),
      ]
    elif mode == MODE_HELP:
      windows = [
        upper_window(),
        center_window_help(),
        lower_window_help(),
      ]
    elif mode == MODE_SETTINGS:
      windows = [
        upper_window(),
        lower_window_settings(),
      ]
    elif mode == MODE_CHARACTER_CREATOR:
      windows = [
        upper_window(),
        lower_window_character_creator(),
      ]
    elif mode == MODE_CUTSCENE:
      windows = [
        upper_window(),
        center_window_cutscene(),
        lower_window_cutscene(),
      ]
    elif mode == MODE_GAME:
      windows = [
        upper_window(),
        center_window_game(),
        log_window_game(),
        lower_window_game(),
      ]
    elif mode == MODE_MAP:
      windows = [
        upper_window(),
        center_window_map(),
        lower_window_map(),
      ]
    refresh_screen(ui_combine_windows(windows))
    handle_input()
    loop_count += 1
  music_stop()
  add_debug_log("Quitting game")
  print(SHOW_CURSOR)
  clear_console()

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
      debug_input_char = (key, ord(key_raw))
      return key
    time.sleep(0.1)

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
  if abr in DIRECTION_ABR:
    position_string = format_direction(DIRECTION_ABR[abr])
    if abr != "c":
      position_string += " side"
  else:
    position_string = "INVALID"
  return position_string

def multi_replace(target_line, target_dict):
  for substring in target_dict.values():
    target_line = target_line.replace(substring, '')
  return target_line

def multi_replace_list(target_list, target_dict):
  new_list = []
  for line in target_list:
    new_list.append(multi_replace(line, target_dict))
  return new_list

def increment_number_loop(num, max_num):
  num += 1
  if num >= max_num:
    num = 0
  return num

def increment_list_loop(target_list, num):
  item = target_list
  if target_list:
    num += 1
    if num >= len(target_list):
      num = 0
    item = target_list[num]
  return item, num

def dict_key_by_value(target_dict, target_value):
  return [k for k, v in target_dict.items() if v == target_value]

def list_fill_whitespace(target_list):
  result = []
  for line in target_list:
    result.append(line.replace(" ", FILL_CHAR))
  return result

def list_none_filter(target_list):
  return [i for i in target_list if i is not None]

def list_longest_entry(target_list):
  return len(max(target_list, key = len))

def fill_empty_space_centered(line, length, char = None):
  return fill_empty_space(line, length, char, True)

def fill_empty_space(line, length, char = None, centered = False):
  if not char:
    char = FILL_CHAR
  for n in range(length):
    if centered and n < length / 2:
      line = char + line
    else:
      line += char
  return line

def fill_init(fill):
  fill_list = fill
  fill_num = 0
  if fill:
    fill = fill_list[fill_num]
  return fill, fill_list, fill_num

def make_line(line, line_color = None, fill = None, fill_color = None, align = "l", margin = 2):
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
              fill_num = increment_number_loop(fill_num, fill_length)
            non_fill_combo = ""
          line_formatted_fill += fill[fill_num]
          fill_num = increment_number_loop(fill_num, fill_length)
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
  if content.lines:
    for num, line in enumerate(content.lines):
      lines.append(Line(line, content.line_color, fill, fill_color))
      # INCREMENT FILL
      fill, fill_num = increment_list_loop(fill_list, fill_num)
      fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  # EMPTY LINE
  else:
    lines.append(Line("", None, fill, fill_color))
  lines.append(ui_seperator())
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
      lines.append(Line("", None, fill, fill_color))
      # INCREMENT FILL
      fill, fill_num = increment_list_loop(fill_list, fill_num)
      fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
      num_empty += 1
  # CONTENT
  num = 0
  for num, line in enumerate(content.lines):
    lines.append(Line(line, content.line_color, fill, fill_color, content.centered_horizontal))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  #EMPTY LINES BOTTOM
  while num + 1 + num_empty < window_size_y - padding:
    lines.append(Line("", None, fill, fill_color))
    # INCREMENT FILL
    fill, fill_num = increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
    num_empty += 1
  if padding_bottom > 0:
    lines.append(ui_seperator())
  return lines

def ui_window_lower(content):
  min_height = 10
  if content.min_height is not None:
    min_height = content.min_height
  lines = []
  # INIT FILL
  fill, fill_list, fill_num = fill_init(content.fill)
  fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
  # CONTENT
  num = 0
  if content.lines:
    for line in content.lines:
      lines.append(Line(line, content.line_color, fill, fill_color, content.centered_horizontal))
      num += 1
      # INCREMENT FILL
      fill, fill_num = increment_list_loop(fill_list, fill_num)
      fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  # EMPTY LINES
  while num == 0 or num < min_height:
    lines.append(Line("", None, fill, fill_color))
    num += 1
  return lines

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

def ui_window_log(content):
  lines = []
  # INIT FILL
  fill, fill_list, fill_num = fill_init(content.fill)
  fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
  # CONTENT
  if content.lines:
    for num, line in enumerate(content.lines):
      lines.append(Line(line, content.line_color, fill, fill_color))
      # INCREMENT FILL
      fill, fill_num = increment_list_loop(fill_list, fill_num)
      fill_color, fill_color_num = increment_list_loop(fill_color_list, fill_color_num)
  lines.append(ui_seperator())
  return lines

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

def log_window_content(target_list, max_num_lines = 10):
  global ui_log_scroll_pos
  result = []
  target_list_len = len(target_list)
  max_scroll_num = max(0, target_list_len-max_num_lines)
  ui_log_scroll_pos = max(0, ui_log_scroll_pos)
  ui_log_scroll_pos = min(max_scroll_num, ui_log_scroll_pos)
  ui_log_start_pos = -abs(max_num_lines + ui_log_scroll_pos)
  ui_log_end_pos = -abs(ui_log_scroll_pos)
  if ui_log_end_pos == 0:
    ui_log_end_pos = None
  target_list_shortened = target_list[ui_log_start_pos:ui_log_end_pos]
  scrollbar = make_scrollbar(max_num_lines, ui_log_scroll_pos, max_scroll_num)
  num = len(target_list_shortened)
  while num < max_num_lines:
    result.append(scrollbar[num-1] + "")
    num += 1
  for num, line in enumerate(target_list_shortened):
    result.append(scrollbar[num] + " " + line)
  return result

def coords_to_pos(x,y):
  pos = ""
  if y == 1 and x == 1:
    pos = "c"
  elif y == 0:
    pos += "n"
  elif y == 2:
    pos += "s"
  if x == 0:
    pos += "w"
  elif x == 2:
    pos += "e"
  return pos

def ui_block_minimap(room_id):
  lines = []
  lines.append("MEMORY (LOCAL):".ljust(15))
  for y in range(3):
    line_top = ""
    line_mid = ""
    line_low = ""
    for x in range(3):
      pos = coords_to_pos(x,y)
      tile_top = MINIMAP_TILES['undiscovered_top']
      tile_mid = MINIMAP_TILES['undiscovered_mid']
      tile_low = MINIMAP_TILES['undiscovered_low']
      if pos == 'nw':
        tile_top = MINIMAP_TILES['undiscovered_top_upper_left']
      elif pos == 'ne':
        tile_top = MINIMAP_TILES['undiscovered_top_upper_right']
      elif pos == 'sw':
        tile_low = MINIMAP_TILES['undiscovered_bottom_lower_left']
      elif pos == 'se':
        tile_low = MINIMAP_TILES['undiscovered_bottom_lower_right']
      if rooms[room_id]['visited'][pos]:
        tile_top = MINIMAP_TILES['visited_top']
        tile_mid = MINIMAP_TILES['visited_mid']
        tile_low = MINIMAP_TILES['visited_low']
        if pos == current_position:
          tile_top = MINIMAP_TILES['current_top']
          tile_mid = MINIMAP_TILES['current_mid']
          tile_low = MINIMAP_TILES['current_low']
      for portal in rooms[room_id]['portal']:
        if portal['position'] == pos and portal['disabled'] == False and rooms[room_id]['visited'][pos]:
          tile_top = MINIMAP_TILES['portal_top']
          tile_mid = MINIMAP_TILES['portal_mid']
          tile_low = MINIMAP_TILES['portal_low']
          if pos == current_position:
            tile_top = MINIMAP_TILES['portal_current_top']
            tile_mid = MINIMAP_TILES['portal_current_mid']
            tile_low = MINIMAP_TILES['portal_current_low']
      for interactable in rooms[room_id]['interactable']:
        if interactable['position'] == pos and interactable['disabled'] == False and rooms[room_id]['visited'][pos]:
          tile_top = MINIMAP_TILES['interactable_top']
          tile_mid = MINIMAP_TILES['interactable_mid']
          tile_low = MINIMAP_TILES['interactable_low']
          if pos == current_position:
            tile_top = MINIMAP_TILES['interactable_current_top']
            tile_mid = MINIMAP_TILES['interactable_current_mid']
            tile_low = MINIMAP_TILES['interactable_current_low']
      line_top += tile_top
      line_mid += tile_mid
      line_low += tile_low
    lines.append(line_top)
    lines.append(line_mid)
    lines.append(line_low)
  return lines

def ui_combine_blocks(blocks, margin_size = 4):
  margin = fill_empty_space("", margin_size)
  lines = []
  height = list_longest_entry([multi_replace_list(list_none_filter(single_block), COLORS) for single_block in list_none_filter(blocks)])
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

def ui_combine_windows(windows):
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
    elif window.window_type == WINDOW_LOG:
      window_formatted = ui_window_log(window)
      content_lower.append(window_formatted)
      size_lower += len(window_formatted)
  # FIND CENTER WINDOW
  content_center = []
  for window in windows:
    if window.window_type == WINDOW_CENTER:
      content_center.append(ui_window_center(window, size_upper, size_lower))
  # COMBINE ALL WINDOWS
  result = ui_combine_windows_make_lines(content_upper + content_center + content_lower)
  return result

def ui_combine_windows_make_lines(target_list):
  result = []
  for window in target_list:
    for line in window:
      if line.centered:
        result.append(make_line_centered(line.content, line.color, line.fill, line.fill_color))
      else:
        result.append(make_line(line.content, line.color, line.fill, line.fill_color))
  return result

def ui_selection_y_prev():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_y > 0:
    found = ui_selection_y - 1
    if ui_selection_options[ui_selection_x][found] is None:
      found = None
      for num in range(ui_selection_y - 1, -1, -1):
        if ui_selection_options[ui_selection_x][num] is not None:
          found = num
          break
    if found is not None:
      sound_ui("ui_sel")
      ui_selection_y = found
      while ui_selection_x > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_x -= 1
      while ui_selection_x < len(ui_selection_options) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_x += 1

def ui_selection_y_next():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_y < len(ui_selection_options[ui_selection_x])-1:
    found = ui_selection_y + 1
    if ui_selection_options[ui_selection_x][found] is None:
      found = None
      for num in range(ui_selection_y + 1, len(ui_selection_options[ui_selection_x])):
        if ui_selection_options[ui_selection_x][num] is not None:
          found = num
          break
    if found is not None:
      ui_selection_y = found
      sound_ui("ui_sel")
      while ui_selection_x > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_x -= 1
      while ui_selection_x < len(ui_selection_options) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_x += 1

def ui_selection_x_prev():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_x > 0:
    found = None
    for num in range(ui_selection_x - 1, -1, -1):
      if len(list_none_filter(ui_selection_options[num])) > 0:
        found = num
        break
    if found is not None:
      sound_ui("ui_sel")
      ui_selection_x = found
      while ui_selection_y > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_y -= 1
      while ui_selection_y < len(ui_selection_options[ui_selection_x]) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_y += 1

def ui_selection_x_next():
  global ui_selection_y
  global ui_selection_x
  if ui_selection_x < len(ui_selection_options)-1:
    found = None
    for num in range(ui_selection_x + 1, len(ui_selection_options)):
      if len(list_none_filter(ui_selection_options[num])) > 0:
        found = num
        break
    if found is not None:
      sound_ui("ui_sel")
      ui_selection_x = found
      while ui_selection_y > 0 and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_y -= 1
      while ui_selection_y < len(ui_selection_options[ui_selection_x]) and ui_selection_options[ui_selection_x][ui_selection_y] is None:
        ui_selection_y += 1

def handle_input():
  selected_option = None
  if ui_selection_options:
    selected_option = ui_selection_options[ui_selection_x][ui_selection_y]
  key = get_keypress()
  if mode == MODE_MAIN_MENU: 
    input_main_menu(key, selected_option)
  elif mode == MODE_DEBUG: 
    input_debug(key, selected_option)
  elif mode == MODE_HELP: 
    input_help(key, selected_option)
  elif mode == MODE_SETTINGS: 
    input_settings(key, selected_option)
  elif mode == MODE_CHARACTER_CREATOR: 
    input_character_creator(key, selected_option)
  elif mode == MODE_CUTSCENE: 
    input_cutscene(key, selected_option)
  elif mode == MODE_GAME:
    input_game(key, selected_option)
  elif mode == MODE_MAP:
    input_map(key, selected_option)

def quit_game():
  global run_game
  run_game = False

def restart_game():
  global ui_restart_prompt
  ui_restart_prompt = False
  initialize_main_menu()

def pre_quit_prompt():
  global ui_selection_x
  global ui_selection_y
  global ui_pre_quit_prompt
  ui_selection_x = 0
  ui_selection_y = 0
  ui_pre_quit_prompt = not ui_pre_quit_prompt

def quit_game_prompt():
  global ui_selection_x
  global ui_selection_y
  global ui_quit_prompt
  ui_selection_x = 0
  ui_selection_y = 0
  ui_quit_prompt = not ui_quit_prompt

def restart_game_prompt():
  global ui_selection_x
  global ui_selection_y
  global ui_restart_prompt
  ui_selection_x = 0
  ui_selection_y = 0
  ui_restart_prompt = not ui_restart_prompt

def press_to_continue(key, target_key = "enter"):
  while key != target_key:
    key = get_keypress()
  sound_ui("ui_confirm")

def press_to_continue_text(target_key = "enter"):
  return "PRESS [" + target_key.upper() + "] TO CONTINUE"

def press_to_go_back_text(target_key = "esc"):
  return "PRESS [" + target_key.upper() + "] TO GO BACK"

def format_selection_options(target_list):
  global ui_selection_options
  result = []
  num_x = len(target_list)
  num_y = len(max(target_list, key = len))
  for x in range(num_x):
    result.append([])
    for y in range(num_y):
      entry = None
      if y < len(target_list[x]):
        entry = target_list[x][y]
      result[x].append(entry)
  ui_selection_options = result

def format_selection_options_display(target_list, min_size = 20, underline = False):
  pre_line = "> "
  pre_line_empty = " "
  selected_color = COLOR_UI_HIGHLIGHT
  if underline:
    selected_color = COLOR_UNDERLINE
    pre_line = pre_line_empty = ""
  result = []
  for x, option_list in enumerate(target_list):
    just_num = min_size
    if list_none_filter(option_list):
      just_num = list_longest_entry(multi_replace_list([item.display_name for item in list_none_filter(option_list)], COLORS)) + 2
    just_num = max(min_size, just_num)
    result.append([])
    for y, option_entry in enumerate(option_list):
      entry = ""
      if len(list_none_filter(option_list)) == 0 and y == 0:
        entry = COLOR_DEFAULT + pre_line_empty + "(EMPTY)"
      if option_entry:
        entry = option_entry.display_name
        if x == ui_selection_x and y == ui_selection_y and ui_log_scroll_pos == 0:
          entry = selected_color + pre_line + entry + COLOR_DEFAULT
        else:
          entry = COLOR_DEFAULT + pre_line_empty + entry
      entry = fill_empty_space(entry, just_num - len(multi_replace(entry, COLORS)))
      result[x].append(entry)
  return result
  
def format_selection_options_display_toggle(target_list, min_size_value = 5, name_link_padding = 20):
  pre_line = "> "
  pre_line_empty = " "
  selected_color = COLOR_UI_HIGHLIGHT
  selected_color_link = COLOR_UNDERLINE
  result = []
  for x, option_list in enumerate(target_list):
    just_num_name = list_longest_entry(multi_replace_list([item.display_name for item in list_none_filter(option_list)], COLORS)) + 2 + name_link_padding
    just_num_link = list_longest_entry(multi_replace_list(list_none_filter([item.link for item in list_none_filter(option_list)]), COLORS))
    just_num_link = max (min_size_value, just_num_link)
    result.append([])
    for y, option_entry in enumerate(option_list):
      entry = ""
      if option_entry:
        entry_name = option_entry.display_name
        entry_link = option_entry.link
        entry_type = option_entry.selection_type
        this_color = COLOR_DEFAULT
        this_color_link = COLOR_DEFAULT
        this_pre_line = pre_line_empty
        if x == ui_selection_x and y == ui_selection_y:
          this_color = selected_color
          this_color_link = selected_color_link
          this_pre_line = pre_line
        entry_name = this_color + this_pre_line + entry_name + COLOR_DEFAULT
        entry = fill_empty_space(entry_name, just_num_name - len(multi_replace(entry_name, COLORS)))
        if entry_link is not None:
          entry_link = fill_empty_space(entry_link, just_num_link - len(multi_replace(entry_link, COLORS)), " ")
          sel_ind_l = ""
          sel_ind_r = ""
          if entry_type == "toggle":
            sel_ind_l = "<  "
            sel_ind_r = "  >"
          entry_link = this_color + sel_ind_l.ljust(2) + this_color_link + entry_link + this_color + sel_ind_r.rjust(2) + COLOR_DEFAULT
          entry += entry_link
      entry = fill_empty_space(entry, (just_num_name + just_num_link + 4) - len(multi_replace(entry, COLORS)))
      result[x].append(entry)
  return result

def format_selection_options_display_bg(target_list, centered = False, min_size = 10):
  padding_size = 2
  padding = fill_empty_space("", padding_size, " ")
  padding_fill = fill_empty_space("", padding_size)
  result = []
  for x, option_list in enumerate(target_list):
    just_num = max(min_size, list_longest_entry(multi_replace_list([item.display_name for item in list_none_filter(option_list)], COLORS)) + padding_size + padding_size)
    result.append([])
    for y, option_entry in enumerate(option_list):
      entry = ""
      if option_entry:
        entry = option_entry.display_name
        if x == ui_selection_x and y == ui_selection_y:
          entry = padding + entry + padding
          entry = fill_empty_space(entry, just_num - len(multi_replace(entry, COLORS)), " ", centered)
          entry = COLOR_UI_HIGHLIGHT_BG + entry + COLOR_DEFAULT
        else:
          entry = COLOR_DEFAULT + entry
          entry = padding_fill + entry + padding_fill
          entry = fill_empty_space(entry, just_num - len(multi_replace(entry, COLORS)), centered = centered)
      result[x].append(entry)
  return result

def format_selection_options_display_bg_centered(target_list, min_size = 10):
  return format_selection_options_display_bg(target_list, True, min_size)

def format_selection_options_display_add_titles(target_list, titles_list):
    for num, column in enumerate(target_list):
      target_list[num].insert(0, titles_list[num])
    return target_list

def upper_window():
  upper_window_content = []
  if mode == MODE_SETTINGS:
    upper_window_content.append("SETTINGS")
  elif mode == MODE_DEBUG:
    upper_window_content.append("DEBUG SCREEN")
  elif mode == MODE_HELP:
    upper_window_content.append("HELP")
  elif mode == MODE_CHARACTER_CREATOR:
    upper_window_content.append("CREATE CHARACTER")
  elif mode == MODE_CUTSCENE or mode == MODE_GAME:
    upper_window_content.append(character_name)
    upper_window_content.append("LVL 4")
    upper_window_content.append("HP 20 / 20")
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

def lower_window_empty():
  return WindowContent(WINDOW_LOWER, min_height = 0)

def input_main_menu(key, selected_option = None):
  if(key == "up"):
    ui_selection_y_prev()
  elif(key == "down"):
    ui_selection_y_next()
  elif(key == "left"):
    ui_selection_x_prev()
  elif(key == "right"):
    ui_selection_x_next()
  elif(key == "enter"):
    if selected_option.name == "start":
      sound_ui("ui_confirm")
      initialize_new_game()
    elif selected_option.name == "settings":
      sound_ui("ui_confirm")
      change_mode(MODE_SETTINGS)
    elif selected_option.name == "debug":
      sound_ui("ui_confirm")
      change_mode(MODE_DEBUG)
    elif selected_option.name == "help":
      sound_ui("ui_confirm")
      change_mode(MODE_HELP)
    elif selected_option.name == "quit_game_prompt":
      sound_ui("ui_confirm")
      quit_game_prompt()
    elif selected_option.name == "quit_game":
      quit_game()

def selection_options_main_menu():
  selection_options = []
  if ui_quit_prompt:
    selection_options.append([
    SelectionOption("quit_game", "YES"),
    SelectionOption("quit_game_prompt", "NO"),
    ])
  else:
    selection_options.append([
    SelectionOption("start", "START GAME"),
    SelectionOption("debug", "DEBUG SCREEN"),
    SelectionOption("settings", "SETTINGS"),
    SelectionOption("help", "HELP"),
    SelectionOption("quit_game_prompt", "QUIT"),
    ])
  return selection_options

def center_window_main_menu():
  lines = []
  line_color = COLOR_TITLE_SCREEN
  format_selection_options(selection_options_main_menu())
  if ui_quit_prompt:
    line_color = COLOR_DEFAULT
    lines.append('ARE YOU SURE?')
  else:
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('')
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
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append('')
    lines = list_fill_whitespace(lines)
  lines.extend(ui_combine_blocks(format_selection_options_display_bg_centered(ui_selection_options, 30)))
  return WindowContent(WINDOW_CENTER, lines, line_color, FILL_PATTERNS['dots2'], None, True, True)

def input_debug(key, selected_option = None):
  global ui_log_scroll_pos
  if(key == "up"):
    if ui_selection_y == 0:
      ui_log_scroll_pos += 1
    else:
      ui_selection_y_prev()
  elif(key == "down"):
    if ui_selection_y == 0 and ui_log_scroll_pos > 0:
      ui_log_scroll_pos -= 1
    else:
      ui_selection_y_next()
  elif(key == "left" and ui_log_scroll_pos == 0):
    ui_selection_x_prev()
  elif(key == "right" and ui_log_scroll_pos == 0):
    ui_selection_x_next()
  elif(key == "escape" or (key == "enter" and selected_option.name == "back")):
    sound_ui("ui_back")
    change_mode(previous_mode)
  elif(key == "enter"):
    if selected_option.name == "music_next":
      music_next(500)

def selection_options_debug():
  selection_options = [[]]
  if settings['enable_music']:
    selection_options[0].append(SelectionOption("music_next", "NEXT SONG"))
  selection_options[0].append(SelectionOption("back", "GO BACK"))
  return selection_options

def center_window_debug():
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
  lines.append('LAST INPUT: '.ljust(justnum) + '"' + str(debug_input_char[0])  + '" (' + str(debug_input_char[1]) + ')')
  lines.append('')
  lines.append('MUSIC STATUS: '.ljust(justnum) + str(music_enable) + ":" + str(music_type) + ":" + str(settings['music_volume']))
  lines.append('MUSIC TITLE: '.ljust(justnum) + str(music_title))
  return WindowContent(WINDOW_CENTER, lines)

def log_window_debug():
  lines = []
  lines.extend(log_window_content(debug_log_list))
  return WindowContent(WINDOW_LOG, lines)

def lower_window_debug():
  ui_blocks = []
  format_selection_options(selection_options_debug())
  selection_options_display = format_selection_options_display(ui_selection_options)
  selection_options_display[0].insert(0, 'SELECT OPTION:')
  ui_blocks.extend(selection_options_display)
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_blocks))

def input_help(key, selected_option = None):
  if(key == "up"):
    ui_selection_y_prev()
  elif(key == "down"):
    ui_selection_y_next()
  elif(key == "left"):
    ui_selection_x_prev()
  elif(key == "right"):
    ui_selection_x_next()
  elif(key == "escape" or (key == "enter" and selected_option.name == "back")):
    sound_ui("ui_back")
    change_mode(previous_mode)

def selection_options_help():
  selection_options = [[
    SelectionOption("back", "GO BACK")
  ]]
  return selection_options

def center_window_help():
  lines = []
  lines.append('MUSIC BY:')
  lines.append('Lory Werths')
  lines.append('www.mandolingals.tripod.com')
  lines.append('')
  return WindowContent(WINDOW_CENTER, lines)

def lower_window_help():
  ui_blocks = []
  format_selection_options(selection_options_help())
  selection_options_display = format_selection_options_display(ui_selection_options)
  selection_options_display[0].insert(0, 'SELECT OPTION:')
  ui_blocks.extend(selection_options_display)
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_blocks))

def input_settings(key, selected_option = None):
  if(key == "up"):
    ui_selection_y_prev()
  elif(key == "down"):
    ui_selection_y_next()
  elif(key == "escape" or (key == "enter" and selected_option.name == "back")):
    sound_ui("ui_back")
    export_json('settings', settings)
    change_mode(previous_mode)
  elif(key == "enter" or key == "left" or key == "right"):
    if selected_option.name == "debug_mode":
      sound_ui("ui_confirm")
      settings['debug_mode'] = not settings['debug_mode']
    elif selected_option.name == "debug_on_start":
      sound_ui("ui_confirm")
      settings['debug_on_start'] = not settings['debug_on_start']
    elif selected_option.name == "debug_log_to_file":
      sound_ui("ui_confirm")
      settings['debug_log_to_file'] = not settings['debug_log_to_file']
    elif selected_option.name == "debug_error_log_to_file":
      sound_ui("ui_confirm")
      settings['debug_error_log_to_file'] = not settings['debug_error_log_to_file']
    elif selected_option.name == "enable_minimap":
      sound_ui("ui_confirm")
      settings['enable_minimap'] = not settings['enable_minimap']
    elif selected_option.name == "enable_music":
      settings['enable_music'] = not settings['enable_music']
      sound_ui("ui_confirm")
      if settings['enable_music'] and not music_enable:
        music_start()
      elif not settings['enable_music'] and music_enable:
        music_stop()
        sound_ui("ui_confirm")
    elif selected_option.name == "enable_boot_screen":
      sound_ui("ui_confirm")
      settings['enable_boot_screen'] = not settings['enable_boot_screen']
    elif selected_option.name == "enable_sound":
      settings['enable_sound'] = not settings['enable_sound']
      sound_ui("ui_confirm")
    elif selected_option.name == "enable_sound_ui":
      settings['enable_sound_ui'] = not settings['enable_sound_ui']
      sound_ui("ui_confirm")

def selection_options_settings():
  selection_options = [[
    SelectionOption("debug_mode", "DEBUG MODE:", str(settings['debug_mode']).upper(), "toggle"),
    SelectionOption("debug_on_start", "DEBUG SCREEN ON START:", str(settings['debug_on_start']).upper(), "toggle"),
    SelectionOption("debug_log_to_file", "DEBUG LOG TO FILE:", str(settings['debug_log_to_file']).upper(), "toggle"),
    SelectionOption("debug_error_log_to_file", "ERROR LOG TO FILE:", str(settings['debug_error_log_to_file']).upper(), "toggle"),
    SelectionOption("enable_boot_screen", "ENABLE BOOT SCREEN:", str(settings['enable_boot_screen']).upper(), "toggle"),
    SelectionOption("enable_minimap", "ENABLE MINIMAP:", str(settings['enable_minimap']).upper(), "toggle"),
    SelectionOption("enable_music", "ENABLE MUSIC:", str(settings['enable_music']).upper(), "toggle"),
    SelectionOption("enable_sound", "ENABLE SOUND:", str(settings['enable_sound']).upper(), "toggle"),
    SelectionOption("enable_sound_ui", "ENABLE UI SOUND:", str(settings['enable_sound_ui']).upper(), "toggle"),
    SelectionOption("back", "GO BACK"),
  ]]
  return selection_options

def lower_window_settings():
  ui_blocks = []
  format_selection_options(selection_options_settings())
  selection_options_display = format_selection_options_display_toggle(ui_selection_options)
  ui_blocks.extend(selection_options_display)
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_blocks))

def input_character_creator(key, selected_option = None):
  if(key == "up"):
    ui_selection_y_prev()
  elif(key == "down"):
    ui_selection_y_next()
  elif(key == "escape" or (key == "enter" and selected_option.name == "back")):
    sound_ui("ui_back")
    change_mode(previous_mode)
  elif(key == "enter"):
    if selected_option.name == "name":
      character_change_name(user_input("ENTER NAME:"))
    elif selected_option.name == "start" and character_name:
      sound_ui("ui_confirm_big")
      change_mode(MODE_CUTSCENE)

def selection_options_character_creator():
  selection_options = [[
    SelectionOption("name", "NAME:", character_name, "input"),
    SelectionOption("start", "START GAME"),
  ]]
  return selection_options

def user_input(text = ""):
  return input(text)

def character_change_name(new_name):
  global character_name
  character_name = new_name

def lower_window_character_creator():
  ui_blocks = []
  format_selection_options(selection_options_character_creator())
  selection_options_display = format_selection_options_display_toggle(ui_selection_options, 10)
  ui_blocks.extend(selection_options_display)
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_blocks), min_height = 0)

def input_cutscene(key, selected_option = None):
  press_to_continue(key)

def center_window_cutscene():
  lines = load_cutscene(active_cutscene)
  return WindowContent(WINDOW_CENTER, lines)

def lower_window_cutscene():
  lines = [press_to_continue_text()]
  return WindowContent(WINDOW_LOWER, lines, min_height = 0)

def load_cutscene(cutscene_id):
  result = []
  if(settings['debug_mode']):
    result.append("DEBUG: Running cutscene " + str(cutscene_id))
  cutscene = cutscenes[cutscene_id]
  for line in cutscene['on_enter']:
    execute_action(line)
  for line in cutscene['text']:
    result.append(line)
  for line in cutscene['on_exit']:
    queue_action(line)
  return result

def input_game(key, selected_option = None):
  global ui_log_scroll_pos
  if(key == "up"):
    if ui_selection_y == 0:
      ui_log_scroll_pos += 1
    else:
      ui_selection_y_prev()
  elif(key == "down"):
    if ui_selection_y == 0 and ui_log_scroll_pos > 0:
      ui_log_scroll_pos -= 1
    else:
      ui_selection_y_next()
  elif(key == "left" and ui_log_scroll_pos == 0):
    ui_selection_x_prev()
  elif(key == "right" and ui_log_scroll_pos == 0):
    ui_selection_x_next()
  elif(key == "enter"):
    if selected_option.name == "pre_quit_prompt":
      sound_ui("ui_confirm")
      pre_quit_prompt()
    elif selected_option.name == "restart_game_prompt":
      sound_ui("ui_confirm")
      restart_game_prompt()
      if ui_pre_quit_prompt:
        pre_quit_prompt()
    elif selected_option.name == "quit_game_prompt":
      sound_ui("ui_confirm")
      quit_game_prompt()
      if ui_pre_quit_prompt:
        pre_quit_prompt()
    elif selected_option.name == "restart_game":
      sound_ui("ui_confirm")
      restart_game()
    elif selected_option.name == "quit_game":
      quit_game()
    elif selected_option.name == "help":
      sound_ui("ui_confirm")
      change_mode(MODE_HELP)
    elif selected_option.name == "settings":
      sound_ui("ui_confirm")
      change_mode(MODE_SETTINGS)
    elif selected_option.name == "debug":
      sound_ui("ui_confirm")
      change_mode(MODE_DEBUG)
    elif selected_option.name == "map":
      sound_ui("ui_confirm")
      change_mode(MODE_MAP)
    elif selected_option.name == "move":
      sound_ui("ui_confirm")
      change_position(selected_option.link, True)
    elif selected_option.name == "examine":
      sound_ui("ui_confirm")
      examine(selected_option.link)
    elif selected_option.name == "portal":
      sound_ui("ui_confirm")
      enter_portal(selected_option.link)

def selection_options_game():
  selection_options = []
  if ui_pre_quit_prompt:
    selection_options.append([
    SelectionOption("restart_game_prompt", "RETURN TO TITLE SCREEN"),
    SelectionOption("quit_game_prompt", "QUIT GAME"),
    SelectionOption("pre_quit_prompt", "CANCEL"),
    ])
  elif ui_quit_prompt:
    selection_options.append([
    SelectionOption("quit_game", "YES"),
    SelectionOption("quit_game_prompt", "NO"),
    ])
  elif ui_restart_prompt:
    selection_options.append([
    SelectionOption("restart_game", "YES"),
    SelectionOption("restart_game_prompt", "NO"),
    ])
  else:
    selection_options.append(check_move_options())
    selection_options.append(check_interact_options())
    selection_options.append([
      SelectionOption("map", "MAP"),
    ])
    selection_options.append([
      SelectionOption("debug", "DEBUG SCREEN"),
      SelectionOption("settings", "SETTINGS"),
      SelectionOption("help", "HELP"),
      SelectionOption("pre_quit_prompt", "QUIT"),
    ])
  return selection_options

def center_window_game():
  lines = []
  lines.extend(show_active_status())
  lines.append("")
  lines.extend(load_room(active_room))
  return WindowContent(WINDOW_CENTER, lines)

def log_window_game():
  lines = []
  lines.extend(log_window_content(log_list))
  return WindowContent(WINDOW_LOG, lines)

def lower_window_game():
  ui_blocks = []
  format_selection_options(selection_options_game())
  selection_options_display = format_selection_options_display(ui_selection_options)
  if ui_pre_quit_prompt:
    selection_options_display[0].insert(0, 'SELECT ACTION:')
  elif ui_quit_prompt or ui_restart_prompt:
    selection_options_display[0].insert(0, 'ARE YOU SURE?')
  else:
    if settings['enable_minimap']:
      ui_blocks.append(ui_block_minimap(active_room))
    option_titles = ["MOVE:", "INTERACT:", "OTHER:", "SYSTEM:"]
    selection_options_display = format_selection_options_display_add_titles(selection_options_display, option_titles)
  ui_blocks.extend(selection_options_display)
  return WindowContent(WINDOW_LOWER, ui_combine_blocks(ui_blocks))

def check_move_options():
  result = []
  for pos, text in DIRECTION_ABR.items():
    position_text = text.upper()
    if pos != "c":
      position_text += " SIDE"
    position_text += " OF " + rooms[active_room]['noun'].upper()
    result.append(SelectionOption("move", position_text, pos))
  return result

def check_interact_options():
  result = []
  room = rooms[active_room]
  for entry in room['interactable']:
    if entry['position'] == current_position and not entry['disabled']:
      result.append(SelectionOption("examine", "(EXAMINE) " + entry['content'].upper(), entry['link']))
  for entry in room['portal']:
    if entry['position'] == current_position and not entry['disabled']:
      result.append(SelectionOption("portal", "(EXIT) " + entry['content'].upper(), entry['link']))
  return result

def input_map(key, selected_option = None):
  if(key == "up"):
    ui_selection_y_prev()
  elif(key == "down"):
    ui_selection_y_next()
  elif(key == "left"):
    ui_selection_x_prev()
  elif(key == "right"):
    ui_selection_x_next()
  elif(key == "escape"):
    sound_ui("ui_back")
    change_mode(previous_mode)

def center_window_map():
  lines = []
  lines.extend(map_window_content())
  return WindowContent(WINDOW_CENTER, lines, None, FILL_PATTERNS['dots1'], None, True, True)

def lower_window_map():
  lines = [press_to_go_back_text()]
  return WindowContent(WINDOW_LOWER, lines, min_height = 0)

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
        next_dir = DIRECTION_REVERSE[next_dir]
        next_portal_pos = portals[portal['link']]['pos1']
      if not next_room in portal_check_dict['checked_rooms'] and rooms[next_room]['visited'][next_portal_pos]:
        next_coords = {'x': current_coords_root['x'] + DIRECTION_TO_COORD[next_dir]['x'], 'y': current_coords_root['y'] + DIRECTION_TO_COORD[next_dir]['y']}
        portal_check_dict['selected_room'] = next_room
        portal_check_dict['current_coords'] = next_coords
        portal_check_dict = map_portal_check(portal_check_dict)
  return portal_check_dict

def selection_options_map(known_rooms, max_x, max_y):
  global ui_selection_options
  global ui_selection_y
  global ui_selection_x
  result = []
  for x in range(max_x):
    result.append([])
    for y in range(max_y):
      if {'x': x, 'y': y} in known_rooms.values():
        found_rooms = dict_key_by_value(known_rooms, {'x': x, 'y': y})
        found_room = found_rooms[0]
        result[x].append(found_room)
        if len(found_rooms) > 1:
          add_debug_log("Multiple rooms with same coordinates " + "(ID: " + str(found_rooms) + ")", True)
        if found_room == active_room and not ui_selection_options:
          ui_selection_x = x
          ui_selection_y = y
      else:
        result[x].append(None)
  ui_selection_options = result

def make_map(known_rooms, max_x, max_y):
  result = []
  for y in range(max_y):
    map_line_top = ""
    map_line_low = ""
    for x in range(max_x):
      if x > 0:
        map_line_top += " "
        map_line_low += " "
      if {'x': x, 'y': y} in known_rooms.values():
        found_rooms = dict_key_by_value(known_rooms, {'x': x, 'y': y})
        found_room = found_rooms[0]
        selected_room = ui_selection_options[ui_selection_x][ui_selection_y]
        if found_room == active_room:
          if found_room == selected_room:
            map_line_top += MAP_TILES['active_selected_top']
            map_line_low += MAP_TILES['active_selected_low']
          else:
            map_line_top += MAP_TILES['active_top']
            map_line_low += MAP_TILES['active_low']
        elif found_room == selected_room:
          map_line_top += MAP_TILES['selected_top']
          map_line_low += MAP_TILES['selected_low']
        else:
          map_line_top += MAP_TILES['visited_top']
          map_line_low += MAP_TILES['visited_low']
      else:
        map_line_top += MAP_TILES['empty_top']
        map_line_low += MAP_TILES['empty_low']
    result.append(map_line_top)
    result.append(map_line_low)
  return result

def map_window_content():
  known_rooms = map_portal_check({'selected_room': active_room, 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}})['checked_rooms']
  #known_rooms_sorted = sorted(known_rooms.items(), key=lambda room: (room[1]['y'], room[1]['x']))
  zero_x = min(coord['x'] for coord in known_rooms.values())
  zero_y = min(coord['y'] for coord in known_rooms.values())
  for room in known_rooms.values():
    room['x'] += abs(zero_x)
    room['y'] += abs(zero_y)
  max_x = max(coord['x'] for coord in known_rooms.values())+1
  max_y = max(coord['y'] for coord in known_rooms.values())+1
  selection_options_map(known_rooms, max_x, max_y)
  result = make_map(known_rooms, max_x, max_y)
  if settings['debug_mode']:
    result.append("DEBUG: " + str(ui_selection_options[ui_selection_x][ui_selection_y]))
  return result

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

def queue_action(action):
  queue_list.append(action)

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
    add_log("You enter the " + rooms[active_room]['noun'])

def load_room(room_id):
  result = []
  if(settings['debug_mode']):
    result.append("DEBUG: You are in room " + str(room_id))
  room = rooms[room_id]
  result.append(room['location'])
  result.extend(sense_sight(room_id))
  result.extend(sense_sound(room_id))
  result.extend(sense_smell(room_id))
  result.append("")
  result.append("You are positioned at the " + format_position_text(current_position) + " of the " + room['noun'] + ".")
  result.extend(sense_sight(room_id, True))
  result.extend(sense_sound(room_id, True))
  result.extend(sense_smell(room_id, True))
  return result

def show_active_status():
  result = []
  for line in statuses:
    if (statuses[line]['active']):
      result.append(format_status(statuses[line]['text']))
  return result

def sense_scan(sense, sense_text, room_id, position_mode = False):
  result = []
  room = rooms[room_id]
  for line in room[sense]:
    if not line['disabled']:
      content = format_color_tags(line['content'])
      if not position_mode and (line['position'] == "" or (line['position'][0] == "-" and line['position'][1:] != current_position)):
        result.append(sense_text + content)
      elif (position_mode and line['position'] == current_position):
        result.append(sense_text + content)
  return result

def sense_sight(room_id, position_mode = False):
  result = []
  sense_text = "You look around: "
  if position_mode:
    sense_text = "You inspect your immediate surroundings: "
  room = rooms[room_id]
  if not statuses['blind']['active']:
    result.extend(sense_scan("sight", sense_text, room_id, position_mode))
  if not result:
    result.append(sense_text + "You see nothing.")
  return result

def sense_sound(room_id, position_mode = False):
  result = []
  sense_text = "You focus on your sense of hearing: "
  if position_mode:
    sense_text = "You focus on the sounds in you immediate proximity: "
  if not statuses['deaf']['active']:
    result.extend(sense_scan("sound", sense_text, room_id, position_mode))
  if statuses['blind']['active'] and not result:
    result.append(sense_text + "You don't hear anything.")
  return result
  
def sense_smell(room_id, position_mode = False):
  result = []
  sense_text = "You focus on your sense of smell: "
  if position_mode:
    sense_text = "You focus on the smells in you immediate proximity: "
  if not statuses['anosmic']['active']:
    result.extend(sense_scan("smell", sense_text, room_id, position_mode))
  if statuses['blind']['active'] and not result:
    result.append(sense_text + "You don't smell anything.")
  return result

def move_north():
  global current_position
  pos = DIRECTION_TO_COORD[current_position]
  if pos['y'] > -1:
    change_position(dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']-1})[0], True)
    
def move_south():
  global current_position
  pos = DIRECTION_TO_COORD[current_position]
  if pos['y'] < 1:
    change_position(dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']+1})[0], True)
    
def move_west():
  global current_position
  pos = DIRECTION_TO_COORD[current_position]
  if pos['x'] > -1:
    change_position(dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']-1, 'y': pos['y']})[0], True)

def move_east():
  global current_position
  pos = DIRECTION_TO_COORD[current_position]
  if pos['x'] < 1:
    change_position(dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']+1, 'y': pos['y']})[0], True)

def change_position(position, logging = False):
  global current_position
  wait = current_position == position
  action_text = "move to"
  if wait:
    action_text = "wait at"
  current_position = position
  rooms[active_room]['visited'][current_position] = True
  if logging:
    log_string = "You " + action_text + " the " + DIRECTION_ABR[position]
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

# START THE GAME
import_settings()
initialize_music()
initialize_main_menu()
initialize()