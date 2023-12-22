# BUILT-IN
import datetime
import json

# SET VERSION NUMBER
VERSION_NUMBER = '0000019'

# SET CONSTANTS
INPUT_COMBO_DEBUG_MODE = 'debugspacemode'
MODE_BOOT_SCREEN = "boot_screen"
MODE_MAIN_MENU = "main_menu"
MODE_DEBUG = "debug_screen"
MODE_SETTINGS = "settings_menu"
MODE_HELP = "help"
MODE_CUTSCENE = "cutscene"
MODE_GAME = "game"
MODE_MAP = "map"
MODE_CHARACTER = "character"
WINDOW_MODE_NORMAL = 'windowed'
WINDOW_MODE_FULLSCREEN = 'fullscreen'
WINDOW_MODE_BORDERLESS = 'borderless'
LAYER_TYPE_MAIN = 'main'
LAYER_TYPE_POPUP = 'popup'
RESOLUTIONS = {
    #'4:3': [
    #    (800, 600),
    #    (1024, 768),
    #    (1280, 960),
    #    (1600, 1200),
    #],
    '16:9': [
        (1280, 720),
        (1600, 900),
        (1920, 1080),
    ],
    '16:10': [
        (1280, 800),
        (1440, 900),
        (1680, 1050),
        (1920, 1200),
    ]
}
RESOLUTION_MIN = min([min(aspect_ratio) for aspect_ratio in RESOLUTIONS.values()])

# SET CONSTANTS, SKILLS
SKILL_NAMES = {
    'attack': 'weapon expertise',
    'attack_ranged': 'ranged weapon expertise',
}
EXPERIENCE_LEVELS = {
    'attack': {
        1: 10,
        2: 100,
        3: 1000,
    },
    'attack_ranged': {
        1: 10,
        2: 100,
        3: 1000,
    },
}

# SET CONSTANTS, GAME
START_POSITION = 'c'
START_ROOM = '1'
PLAYER_START_HP = 100
PLAYER_START_ATTACK_SKILL = 0
PLAYER_START_ATTACK_SKILL_RANGED = 0
PLAYER_START_ATTACK_SKILL_UNARMED = 2
PLAYER_START_LUCK = 0
PLAYER_DAMAGE_UNARMED = 5
PLAYER_START_EQUIPMENT_UPPER_BODY = '5'
PLAYER_START_EQUIPMENT_LOWER_BODY = '6'
PLAYER_START_EQUIPMENT_FEET = '7'

# SET CONSTANTS, FILE NAMES
FOLDER_NAME_RESOURCES = 'resources'
FOLDER_NAME_IMAGES = 'img'
FOLDER_NAME_DATA = 'data'

# SET CONSTANTS, TAGS
TAGS = {
    "black": "01",
    "red": "02",
    "green": "03",
    "yellow": "04",
    "blue": "05",
    "magenta": "06",
    "cyan": "07",
    "white": "08",
    "bright_black": "09",
    "bright_red": "10",
    "bright_green": "11",
    "bright_yellow": "12",
    "bright_blue": "13",
    "bright_magenta": "14",
    "bright_cyan": "15",
    "bright_white": "16",
    "foreground": "fg",
    "background": "bg",
    "underline": "ul",
    "strikethrough": "st",
}
UI_TAGS = {
    "none": "none",
    "back": "back",
    "continue": "cont",
    "action": "actn",
    "scroll": "scrl",
    "link": "link",
    "left": "left",
    "right": "rght",
    "data_center_up": "▲c",
    "data_center_down": "▼c",
    "data_log_up": "▲l",
    "data_log_down": "▼l",
}
TAGS_REVERSE = {v: k for k, v in TAGS.items()}
UI_TAGS_REVERSE = {v: k for k, v in UI_TAGS.items()}

# SET CONSTANTS, DEFAULT COLORS
DEFAULT_FG_COLOR = 'foreground'
DEFAULT_FILL_COLOR = 'bright_black'

# SET CONSTANTS, TAG COLORS
TAG_COLOR_FG = TAGS['foreground']
TAG_COLOR_BG = TAGS['background']
TAG_COLOR_LINK = TAGS['blue']
TAG_COLOR_DARK = TAGS['bright_black']
TAG_COLOR_HL = TAGS['bright_white']
TAG_COLOR_WEAK = TAGS['white']
TAG_COLOR_TITLE_SCREEN = TAGS['bright_cyan']
TAG_COLOR_INTERACTABLE = TAGS['bright_green']
TAG_COLOR_PORTAL = TAG_COLOR_INTERACTABLE
TAG_COLOR_DIRECTION = TAGS['bright_blue']
TAG_COLOR_NPC = TAGS['bright_yellow']
TAG_COLOR_STATUS = TAGS['bright_magenta']
TAG_COLOR_ITEM_TYPE_BOOK = TAGS['bright_yellow']
TAG_COLOR_ITEM_TYPE_RING = TAGS['bright_red']
TAG_COLOR_ITEM_TYPE_ARMOR = TAGS['bright_green']
TAG_COLOR_ITEM_TYPE_WEAPON = TAGS['bright_cyan']
TAG_COLOR_ITEM_TYPE_CONSUMABLE = TAGS['bright_magenta']
TAG_COLOR_ITEM_TYPE_KEY = TAGS['bright_blue']
TAG_COLOR_ITEM_MAGICAL = TAGS['bright_white']
TAG_COLOR_STAGE_0 = TAG_COLOR_WEAK
TAG_COLOR_STAGE_1 = TAGS['red']
TAG_COLOR_STAGE_2 = TAGS['yellow']
TAG_COLOR_STAGE_3 = TAGS['green']
TAG_COLOR_HEALTH_1 = TAG_COLOR_STAGE_1
TAG_COLOR_HEALTH_2 = TAG_COLOR_STAGE_2
TAG_COLOR_HEALTH_3 = TAG_COLOR_STAGE_3
TAG_COLOR_HEALTH_STAGE_3 = TAG_COLOR_HEALTH_2
TAG_COLOR_HEALTH_STAGE_6 = TAG_COLOR_HEALTH_1
TAG_COLOR_UI_BG_SEL_FG = TAG_COLOR_BG
TAG_COLOR_UI_BG_SEL_BG = TAG_COLOR_FG
TAG_COLOR_UI_SEL_FG = TAG_COLOR_FG
TAG_COLOR_UI_SEL_HL = TAG_COLOR_HL
TAG_COLOR_UI_INACTIVE = TAG_COLOR_WEAK
TAG_COLOR_LOG_DAMAGE = TAG_COLOR_HEALTH_1
TAG_COLOR_LOG_HEAL = TAG_COLOR_HEALTH_3
TAG_COLOR_LOG_OLD = TAG_COLOR_UI_INACTIVE
TAG_COLOR_LOG_HL = TAGS['bright_yellow']
TAG_COLOR_MAP_INACTIVE = TAG_COLOR_DARK
TAG_COLOR_MAP_SELECTED = TAG_COLOR_FG
TAG_COLOR_SCROLLBAR_BG = TAG_COLOR_HL

# SET CONSTANTS, FONTS
FONTS = {
    'DOS/V re. ANK16': 'Px437_DOS-V_re_ANK16',
    'DOS/V re. JPN16': 'Px437_DOS-V_re_JPN16',
    'EverexME': 'Px437_EverexME_8x16',
    'FMTowns re.': 'Px437_FMTowns_re_8x16',
    'IBM VGA': 'Px437_IBM_VGA_8x16',
    'NEC APC III': 'Px437_NEC_APC3_8x16',
    'Robotron A7100': 'Px437_Robotron_A7100',
    'Telenova Compis': 'Px437_Compis',
    'ToshibaSat': 'Px437_ToshibaSat_8x16',
}

# SET CONSTANTS, PALETTES
PALETTES = {
    "Apprentice": {
        "black": (28, 28, 28),
        "red": (175, 95, 95),
        "green": (95, 135, 95),
        "yellow": (135, 135, 95),
        "blue": (95, 135, 175),
        "magenta": (95, 95, 135),
        "cyan": (95, 135, 135),
        "white": (108, 108, 108),
        "bright_black": (68, 68, 68),
        "bright_red": (255, 135, 0),
        "bright_green": (135, 175, 135),
        "bright_yellow": (255, 255, 175),
        "bright_blue": (143, 175, 215),
        "bright_magenta": (135, 135, 175),
        "bright_cyan": (95, 175, 175),
        "bright_white": (255, 255, 255),
        "background": (38, 38, 38),
        "foreground": (188, 188, 188),
    },
    "Borland": {
        "black": (79, 79, 79),
        "red": (255, 108, 96),
        "green": (168, 255, 96),
        "yellow": (255, 255, 182),
        "blue": (150, 203, 254),
        "magenta": (255, 115, 253),
        "cyan": (198, 197, 254),
        "white": (238, 238, 238),
        "bright_black": (124, 124, 124),
        "bright_red": (255, 182, 176),
        "bright_green": (206, 255, 172),
        "bright_yellow": (255, 255, 204),
        "bright_blue": (181, 220, 255),
        "bright_magenta": (255, 156, 254),
        "bright_cyan": (223, 223, 254),
        "bright_white": (255, 255, 255),
        "background": (0, 0, 164),
        "foreground": (255, 255, 78),
    },
    "Dracula": {
        "black": (68, 71, 90),
        "red": (255, 85, 85),
        "green": (80, 250, 123),
        "yellow": (255, 184, 108),
        "blue": (139, 233, 253),
        "magenta": (189, 147, 249),
        "cyan": (255, 121, 198),
        "white": (248, 248, 242),
        "bright_black": (0, 0, 0),
        "bright_red": (255, 85, 85),
        "bright_green": (80, 250, 123),
        "bright_yellow": (255, 184, 108),
        "bright_blue": (139, 233, 253),
        "bright_magenta": (189, 147, 249),
        "bright_cyan": (255, 121, 198),
        "bright_white": (255, 255, 255),
        "background": (40, 42, 54),
        "foreground": (248, 248, 242),
    },
    "Gruvbox Dark": {
        "black": (40, 40, 40),
        "red": (204, 36, 29),
        "green": (152, 151, 26),
        "yellow": (215, 153, 33),
        "blue": (69, 133, 136),
        "magenta": (177, 98, 134),
        "cyan": (104, 157, 106),
        "white": (168, 153, 132),
        "bright_black": (146, 131, 116),
        "bright_red": (251, 73, 52),
        "bright_green": (184, 187, 38),
        "bright_yellow": (250, 189, 47),
        "bright_blue": (131, 165, 152),
        "bright_magenta": (211, 134, 155),
        "bright_cyan": (142, 192, 124),
        "bright_white": (235, 219, 178),
        "background": (40, 40, 40),
        "foreground": (235, 219, 178),
    },
    "Ibm3270": {
        "black": (34, 34, 34),
        "red": (240, 24, 24),
        "green": (36, 216, 48),
        "yellow": (240, 216, 36),
        "blue": (120, 144, 240),
        "magenta": (240, 120, 216),
        "cyan": (84, 228, 228),
        "white": (165, 165, 165),
        "bright_black": (136, 136, 136),
        "bright_red": (239, 131, 131),
        "bright_green": (126, 214, 132),
        "bright_yellow": (239, 226, 139),
        "bright_blue": (179, 191, 239),
        "bright_magenta": (239, 179, 227),
        "bright_cyan": (156, 226, 226),
        "bright_white": (255, 255, 255),
        "background": (0, 0, 0),
        "foreground": (253, 253, 253),
    },
    "Monokai Pro": {
        "black": (54, 53, 55),
        "red": (255, 97, 136),
        "green": (169, 220, 118),
        "yellow": (255, 216, 102),
        "blue": (252, 152, 103),
        "magenta": (171, 157, 242),
        "cyan": (120, 220, 232),
        "white": (253, 249, 243),
        "bright_black": (144, 142, 143),
        "bright_red": (255, 97, 136),
        "bright_green": (169, 220, 118),
        "bright_yellow": (255, 216, 102),
        "bright_blue": (252, 152, 103),
        "bright_magenta": (171, 157, 242),
        "bright_cyan": (120, 220, 232),
        "bright_white": (253, 249, 243),
        "background": (54, 53, 55),
        "foreground": (253, 249, 243),
    },
    "Powershell": {
        "black": (0, 0, 0),
        "red": (126, 0, 8),
        "green": (9, 128, 3),
        "yellow": (196, 160, 0),
        "blue": (1, 0, 131),
        "magenta": (211, 54, 130),
        "cyan": (14, 128, 127),
        "white": (127, 124, 127),
        "bright_black": (128, 128, 128),
        "bright_red": (239, 41, 41),
        "bright_green": (28, 254, 60),
        "bright_yellow": (254, 254, 69),
        "bright_blue": (38, 138, 210),
        "bright_magenta": (254, 19, 250),
        "bright_cyan": (41, 255, 254),
        "bright_white": (194, 193, 195),
        "background": (5, 36, 84),
        "foreground": (246, 246, 247),
    },
    "Solarized Dark": {
        "black": (7, 54, 66),
        "red": (220, 50, 47),
        "green": (133, 153, 0),
        "yellow": (207, 154, 107),
        "blue": (38, 139, 210),
        "magenta": (211, 54, 130),
        "cyan": (42, 161, 152),
        "white": (238, 232, 213),
        "bright_black": (101, 123, 131),
        "bright_red": (216, 121, 121),
        "bright_green": (136, 207, 118),
        "bright_yellow": (101, 123, 131),
        "bright_blue": (38, 153, 255),
        "bright_magenta": (211, 54, 130),
        "bright_cyan": (67, 184, 195),
        "bright_white": (253, 246, 227),
        "background": (0, 43, 54),
        "foreground": (131, 148, 150),
    },
    "Zenburn": {
        "black": (77, 77, 77),
        "red": (112, 80, 80),
        "green": (96, 180, 138),
        "yellow": (240, 223, 175),
        "blue": (80, 96, 112),
        "magenta": (220, 140, 195),
        "cyan": (140, 208, 211),
        "white": (220, 220, 204),
        "bright_black": (112, 144, 128),
        "bright_red": (220, 163, 163),
        "bright_green": (195, 191, 159),
        "bright_yellow": (224, 207, 159),
        "bright_blue": (148, 191, 243),
        "bright_magenta": (236, 147, 211),
        "bright_cyan": (147, 224, 227),
        "bright_white": (255, 255, 255),
        "background": (63, 63, 63),
        "foreground": (220, 220, 204),
    },
}

# SET CONTANTS, ANIMATIONS
ANIMATION_UI_DEFAULT = 'ui_sel_3'
ANIMATION_UI_CONTINUE_DEFAULT = 'ui_sel_3_fg'
ANIMATIONS = {
    'boot': {
        'fps': 8,
        'block_until_frame': 0,
        'frames': [
            'boot1',
            'boot2',
            'fade1_fg',
            'fade1_bg',
        ]
    },
    'fade': {
        'fps': 16,
        'block_until_frame': 1,
        'frames': [
            'fade1_bg',
            'fade2_bg',
            'fade1_bg',
        ]
    },
    'fade_popup': {
        'fps': 8,
        'block_until_frame': 0,
        'frames': [
            'fade1_bg',
            'fade2_bg',
        ]
    },
    'take_damage': {
        'fps': 8,
        'block_until_frame': 0,
        'frames': [
            'fade2_fg',
            'fade1_fg',
            'fade1_bg',
        ]
    },
    'change_room': {
        'fps': 8,
        'block_until_frame': 2,
        'frames': [
            'fade1_bg',
            'fade2_bg',
            'fade3_bg',
            'fade2_bg',
            'fade1_bg',
        ]
    },
}
ANIMATIONS_UI = {
    'ui_sel_1': {
        'fps': 30,
        'length': 1,
        'highlight': True,
    },
    'ui_sel_3': {
        'fps': 8,
        'length': 3,
        'highlight': True,
    },
    'ui_sel_5': {
        'fps': 8,
        'length': 5,
        'highlight': True,
    },
    'ui_sel_7': {
        'fps': 8,
        'length': 7,
        'highlight': True,
    },
    'ui_sel_3_fg': {
        'fps': 8,
        'length': 5,
        'highlight': False,
    },
    'ui_sel_5_fg': {
        'fps': 8,
        'length': 5,
        'highlight': False,
    },
}

# SET CONSTANTS, HEALTH STAGES
PLAYER_HEALTH_STAGES = {
    1: [
    'You have received some <color>minor scratches</color>.',
    'You are <color>slighty bruised</color>.'
    ],
    2: [
    'You are <color>injured</color>.',
    ],
    3: [
    'You are <color>badly injured</color>.' 
    ],
    4: [
    'You are <color>very badly wounded</color>.'
    ],
    5: [
    'You are <color>seriously wounded</color>. Your body aches.'
    ],
    6: [
    'You are in <color>a bad state of health</color> You have sustained a number of serious injuries.'
    ],
    7: [
    'You are <color>mortally wounded</color> and barely able to remain conscious.',
    'You have sustained <color>life treatening injuries</color> and are in dire need of medical treatment.'
    ],
    8: [
    'You are <color>dead</color>.',
    ]
}
NPC_HEALTH_STAGES = {
    1: [
    '<name> is slighty <color>wounded</color>.',
    ],
    2: [
    '<name> is <color>injured</color>.',
    ],
    3: [
    '<name> is badly <color>wounded</color>.',
    ],
    4: [
    '<name> is <color>dead</color>.'
    ]
}

# SET CONSTANTS, ATTACK / DODGE TEXT
PLAYER_DODGE_TEXT = [
'The attack misses you.',
'You successfully dodge the attack.',
'You evade the attack.',
'You manage to successfully evade the attack.',
'The attack doesn\'t hit you.',
]
PLAYER_ATTACK_TEXT = [
'You attack <name>.',
'You try to hit <name>.',
'You strike <name>.',
]
PLAYER_ATTACK_TEXT_RANGED = [
'You attack <name> from a distance.',
'You try to hit <name> with your ranged weapon.',
'You strike <name> from afar.',
]
NPC_DODGE_TEXT = [
'Your attack misses <name>.',
'<name> successfully dodges your attack.',
'<name> evades your attack.',
'<name> successfully evades your attack.',
]
NPC_ATTACK_TEXT = [
'<name> attacks you.',
'<name> hits you.',
'<name> strikes you.',
]

# SET VARS
screen_width_full = None
screen_height_full = None
system_error = None
run_game = True
display_changed = False
font_changed = False
palette_changed = False
settings = {}
mode = None
previous_mode = None
size_x = 0
size_y = 0
debug_log_list = []
ui_selection_current = None
ui_selection_x = 0
ui_selection_y = 0
ui_selection_x_prev = 0
ui_selection_y_prev = 0
ui_selection_x_popup_prev = 0
ui_selection_y_popup_prev = 0
animation_queue = []
last_input = None
last_input_device = None
ui_scroll_start_pos = 0
ui_scroll_end_pos = 0
ui_scroll = {
    'center': {
        'pos': 0,
        'max': 0,
    },
    'log': {
        'pos': 0,
        'max': 0,
    },
}

# SET VARS, GAME
game = {
    'game_init': None,
    'turn': None,
    'game_over': None,
    'game_over_text': None,
}
game_settings = {
    'show_minimap': None,
}
flags = {
    'show_battle_num': None,
    'show_player_hp': None,
    'show_npc_hp': None,
}
stats = {
    'times_moved': None,
    'portals_entered': None,
    'npcs_killed': None,
    'times_player_attack': None,
    'times_player_attack_ranged': None,
    'times_npc_attack': None,
    'times_npc_attack_ranged': None,
    'damage_dealt': None,
    'damage_received': None,
    'damage_defended': None,
    'health_healed': None,
    'times_player_missed': None,
    'times_npc_missed': None,
    'drinks_consumed': None,
    'foods_consumed': None,
    'books_consumed': None,
    'times_player_attack_luck': None,
    'times_npc_missed_luck': None,
}
player = {
    'health_points_max': None,
    'health_points': None,
    'health_stage': None,
    'health_status': None,
    'skill_level_attack': None,
    'skill_level_attack_ranged': None,
    'skill_level_attack_unarmed': None,
    'luck': None,
    'damage_unarmed': None,
    'experience_attack': None,
    'experience_level_attack': None,
    'experience_attack_ranged': None,
    'experience_level_attack_ranged': None,
}
equipped_armor = {
    'head': None,
    'upper_body': None,
    'lower_body': None,
    'hands': None,
    'feet': None,
    'shield': None,
}
equipped_weapons = {
    'attack': None,
    'attack_ranged': None,
}
equipped_rings = []

# SET VARS, CONTROLS
controls = {
    'up': [
        'up',
        'mouse_up',
        'joy_hat_up',
        'joy_axis_1_neg',
    ],
    'down': [
        'down',
        'mouse_down',
        'joy_hat_down',
        'joy_axis_1_pos',
    ],
    'left': [
        'left',
        'mouse_left',
        'joy_hat_left',
        'joy_axis_0_neg',
    ],
    'right': [
        'right',
        'mouse_right',
        'joy_hat_right',
        'joy_axis_0_pos',
    ],
    'action': [
        'return',
        'mouse_action',
        'joy_0',
    ],
    'back': [
        'escape',
        'mouse_back',
        'joy_1',
    ],
    'scroll_center_up': [
        'mouse_scroll_center_up',
        'joy_axis_3_neg',
    ],
    'scroll_center_down': [
        'mouse_scroll_center_down',
        'joy_axis_3_pos',
    ],
    'scroll_log_up': [
        'mouse_scroll_log_up',
    ],
    'scroll_log_down': [
        'mouse_scroll_log_down',
    ],
    'mod_scroll_center': [
        'shift',
    ],
}

# SET VARS, DEFINE ITEMS
item_type_consumable = [
'drink',
'food',
'book',
]

def initialize():
    import_settings()
    add_debug_log("Starting game")

def add_to_stats(stat, num):
    stats[stat] += num

def ui_scroll_zero():
    for key in ui_scroll:
        ui_scroll[key]['pos'] = 0
        ui_scroll[key]['max'] = 0

def import_json(filename):
    return json.load(open(filename + '.json','r'))

def export_json(name, content):
    with open(name + ".json", "w") as outfile:
        json.dump(content, outfile, indent = 2)

def import_settings():
    global settings
    settings = import_json(FOLDER_NAME_RESOURCES + '/' + 'settings')

def export_settings():
    export_json(FOLDER_NAME_RESOURCES + '/' + 'settings', settings)

def add_debug_log(item, error = False):
    global debug_log_list
    if error:
        item = "ERROR: " + item
    turn = 0
    if game['turn']:
        turn = game['turn']
    item = '(' + str(turn) + ') ' + item
    debug_log_list.append(item)
    if settings['debug_error_log_to_file'] and error:
        with open(FOLDER_NAME_RESOURCES + '/' + 'error_log.txt', 'a') as file:
            file.write(datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + " | " + item + "\n")
    elif settings['debug_log_to_file']:
        with open(FOLDER_NAME_RESOURCES + '/' + 'debug_log.txt', 'a') as file:
            file.write(datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + " | " + item + "\n")

def raise_system_error(error_name):
    global run_game
    global system_error
    run_game = False
    system_error = error_name
    add_debug_log('SYSTEM ERROR! ' + error_name, True)

def trigger_animation(animation_name, sound_name = None, sound_type = None, animation_type = None, animation_data = None):
    if animation_name in ANIMATIONS_UI:
        if animation_type is None:
            animation_type = 'sel'
        if animation_data is None:
            animation_data = str(ui_selection_x) + '-' + str(ui_selection_y)
    animation_queue.append((animation_name, (sound_name, sound_type), (animation_type, animation_data)))

def initialize_new_game():
    add_debug_log("Initializing new game")
    game['turn'] = 1
    game['game_init'] = True
    game['game_over'] = False
    game['game_over_text'] = None
    for key in game_settings:
        game_settings[key] = True
    for key in flags:
        flags[key] = False
    for key in stats:
        stats[key] = 0
    player['health_points_max'] = PLAYER_START_HP
    player['health_points'] = PLAYER_START_HP
    player['health_stage'] = 0
    player['health_status'] = None
    player['skill_level_attack'] = 0
    player['skill_level_attack_ranged'] = 0
    player['skill_level_attack_unarmed'] = PLAYER_START_ATTACK_SKILL_UNARMED
    player['damage_unarmed'] = PLAYER_DAMAGE_UNARMED
    player['luck'] = PLAYER_START_LUCK
    player['experience_attack'] = 0
    player['experience_level_attack'] = PLAYER_START_ATTACK_SKILL
    player['experience_attack_ranged'] = 0
    player['experience_level_attack_ranged'] = PLAYER_START_ATTACK_SKILL_RANGED
    for key in equipped_armor:
        equipped_armor[key] = None
    for key in equipped_weapons:
        equipped_weapons[key] = None
    equipped_rings = []
    equipped_armor['upper_body'] = PLAYER_START_EQUIPMENT_UPPER_BODY
    equipped_armor['lower_body'] = PLAYER_START_EQUIPMENT_LOWER_BODY
    equipped_armor['feet'] = PLAYER_START_EQUIPMENT_FEET