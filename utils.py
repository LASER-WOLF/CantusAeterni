# BUILT-IN
import random
import re

# PROJECT
import config

# SET CONSTANTS, DIRECTIONS
DIRECTION_ABR = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }
DIRECTION_TO_COORD = {'nw': {'x': -1, 'y': -1}, 'n': {'x': 0, 'y': -1}, 'ne': {'x': 1, 'y': -1}, 'w': {'x': -1, 'y': 0}, 'c': {'x': 0, 'y': 0}, 'e': {'x': 1, 'y': 0}, 'sw': {'x': -1, 'y': 1}, 's': {'x': 0, 'y': 1}, 'se': {'x': 1, 'y': 1} }
DIRECTION_REVERSE = {'nw': 'se', 'n': 's', 'ne': 'sw', 'w': 'e', 'c': 'c', 'e': 'w', 'sw': 'ne', 's': 'n', 'se': 'nw' }

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

def capitalize(text):
    char_in_tag = False
    for num, character in enumerate(text):
        if character == '<':
            char_in_tag = True
        elif char_in_tag is False:
            text = text[:num] + character.upper() + text[num + 1:]
            break
        elif character == '>':
            char_in_tag = False
    return text

def add_text_tag(string, fg = 'fg', bg = 'bg', other = '00'):
    return "<text=" + str(fg) + ":" + str(bg) + ":" + str(other) + ">" + string + "</text>"

def add_ui_tag(string, tag_type, tag_data = 'none'):
    return '<ui=' + str(tag_type) + ':' + str(tag_data) + '>' + string + '</ui>'

def add_ui_tag_sel_none(string, x = 0, y = 0):
    return add_ui_tag(string, config.UI_TAGS['none'], str(x) + '-' + str(y))

def add_ui_tag_sel_action(string, x = 0, y = 0):
    return add_ui_tag(string, config.UI_TAGS['action'], str(x) + '-' + str(y))

def add_ui_tag_sel_left(string, x = 0, y = 0):
    return add_ui_tag(string, config.UI_TAGS['left'], str(x) + '-' + str(y))

def add_ui_tag_sel_right(string, x = 0, y = 0):
    return add_ui_tag(string, config.UI_TAGS['right'], str(x) + '-' + str(y))

def add_ui_tag_scroll_center_up(string):
    return add_ui_tag(string, config.UI_TAGS['scroll'], config.UI_TAGS['data_center_up'])

def add_ui_tag_scroll_center_down(string):
    return add_ui_tag(string, config.UI_TAGS['scroll'], config.UI_TAGS['data_center_down'])

def add_ui_tag_scroll_log_up(string):
    return add_ui_tag(string, config.UI_TAGS['scroll'], config.UI_TAGS['data_log_up'])

def add_ui_tag_scroll_log_down(string):
    return add_ui_tag(string, config.UI_TAGS['scroll'], config.UI_TAGS['data_log_down'])

def add_ui_tag_continue(string):
    return add_ui_tag(string, config.UI_TAGS['continue'])

def add_ui_tag_back(string):
    return add_ui_tag(string, config.UI_TAGS['back'])

def add_ui_tag_link(string, link):
    return add_ui_tag(string, config.UI_TAGS['link'], link)

def format_link(string, link):
    return add_ui_tag_link(add_text_tag(string, fg = config.TAG_COLOR_LINK), link)

def remove_text_tags(target_line):
    target_line = re.sub('<text=(.{2}):(.{2}):(.{2})>(.*?)</text>', r"\4", target_line, flags = re.IGNORECASE)
    return target_line

def remove_ui_tags(target_line):
    target_line = re.sub('<ui=(.{4}):(.*?)>(.*?)</ui>', r"\3", target_line, flags = re.IGNORECASE)
    return target_line

def remove_all_tags(target_line):
    target_line = remove_text_tags(target_line)
    target_line = remove_ui_tags(target_line)
    return target_line

def remove_all_tags_multi(target_list):
    new_list = []
    for line in target_list:
        new_list.append(remove_all_tags(line))
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

def list_none_filter(target_list):
    return [i for i in target_list if i is not None]

def list_longest_entry(target_list):
    return max(target_list, key = len)

def list_longest_entry_length(target_list):
    return len(list_longest_entry(target_list))

def dict_key_by_value(target_dict, target_value):
    return [k for k, v in target_dict.items() if v == target_value]

def dict_swap_key_val(target_dict):
    return {v: k for k, v in target_dict.items()}

def format_color_tags(content):
    content = re.sub("<i>(.*?)</i>", format_interactable(r"\1"), content)
    content = re.sub("<s>(.*?)</s>", format_status(r"\1"), content)
    content = re.sub("<d>(.*?)</d>", format_direction(r"\1"), content)
    content = re.sub("<p>(.*?)</p>", format_portal(r"\1"), content)
    content = re.sub("<n>(.*?)</n>", format_npc(r"\1"), content)
    return content

def format_position_text(abr):
    position_string = format_direction(DIRECTION_ABR[abr])
    if abr != "c":
        position_string += " side"
    return position_string

def format_position_text_room(abr, room_noun):
    return format_position_text(abr) + ' of the ' + room_noun

def format_status(text):
    return add_text_tag(text, fg = config.TAG_COLOR_STATUS)

def format_interactable(text):
    return add_text_tag(text, fg = config.TAG_COLOR_INTERACTABLE)

def format_npc(text):
    return add_text_tag(text, fg = config.TAG_COLOR_NPC)

def format_direction(text):
    return add_text_tag(text, fg = config.TAG_COLOR_DIRECTION)

def format_portal(text):
    return add_text_tag(text, fg = config.TAG_COLOR_PORTAL)

def format_log_damage(text):
    return add_text_tag(text, fg = config.TAG_COLOR_LOG_DAMAGE)

def format_log_heal(text):
    return add_text_tag(text, fg = config.TAG_COLOR_LOG_HEAL)

def format_item_name(name, item_type, capitalized = True, colored = True, type_abr = False):
    name_formatted = name
    if capitalized:
        name_formatted = name_formatted.capitalize()
    if type_abr:
        name_formatted = abbreviate_item_type(item_type) + ' ' + name_formatted
    if colored:
        name_formatted = format_item_type_color(name_formatted, item_type)
    return name_formatted

def format_item_type(name, capitalized = True, colored = True):
    name_formatted = name
    if name == 'attack':
        name_formatted = 'weapon'
    elif name == 'attack_ranged':
        name_formatted = 'ranged weapon'
    elif name == 'hands':
        name_formatted = 'gloves'
    elif name == 'head':
        name_formatted = 'headgear'
    elif name == 'upper_body':
        name_formatted = 'upper body armor'
    elif name == 'lower_body':
        name_formatted = 'lower body armor'
    elif name == 'feet':
        name_formatted = 'footwear'
    if capitalized:
        name_formatted = name_formatted.capitalize()
    if colored:
        name_formatted = format_item_type_color(name_formatted, name)
    return name_formatted

def format_item_type_color(text, item_type):
    text_formatted = text
    if item_type == 'book':
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_BOOK)
    elif item_type == 'ring':
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_RING)
    elif item_type in config.equipped_armor:
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_ARMOR)
    elif item_type in config.equipped_weapons:
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_WEAPON)
    elif item_type in config.item_type_consumable:
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_CONSUMABLE)
    elif item_type == 'key':
        text_formatted = add_text_tag(text_formatted, fg = config.TAG_COLOR_ITEM_TYPE_KEY)
    return text_formatted

def abbreviate_item_type(item_type):
    item_type_formatted = item_type
    if item_type == 'upper_body':
        item_type_formatted = 'uppr'
    elif item_type == 'lower_body':
        item_type_formatted = 'lowr'
    elif item_type == 'hands':
        item_type_formatted = 'hand'
    elif item_type == 'shield':
        item_type_formatted = 'shld'
    elif item_type == 'attack':
        item_type_formatted = 'weap'
    elif item_type == 'attack_ranged':
        item_type_formatted = 'rang'
    elif item_type == 'drink':
        item_type_formatted = 'drnk'
    item_type_formatted = '[' + item_type_formatted + ']'.upper()
    item_type_formatted = item_type_formatted.upper()
    item_type_formatted = item_type_formatted.ljust(6)
    return item_type_formatted

def format_npc_name(npc, colored = True, force_default = False, force_secret = False):
    use_secret_name = False
    if force_secret or (npc['secret_name_unlocked'] and force_default is False):
        use_secret_name = True
    name = npc['name']
    if use_secret_name:
        name = npc['secret_name']
    if (use_secret_name is False and npc['proper_noun'] is False) or (use_secret_name is True and npc['secret_name_proper_noun'] is False):
        name = 'the ' + name
    if colored is True:
        name = format_npc(name)
    return name

def format_npc_pronoun(npc, form):
    pronoun = npc['pronoun']
    if npc['secret_name_unlocked']:
        pronoun = npc['secret_name_pronoun']
    if pronoun == 'it':
        if form == 'possesive': 
            pronoun = 'its'
        elif form == 'reflexive': 
            pronoun = 'itself'
    elif pronoun == 'he':
        if form == 'object': 
            pronoun = 'him'
        elif form == 'possesive': 
            pronoun = 'his'
        elif form == 'reflexive': 
            pronoun = 'himself'
    elif pronoun == 'she':
        if form == 'object': 
            pronoun = 'her'
        elif form == 'possesive': 
            pronoun = 'hers'
        elif form == 'reflexive': 
            pronoun = 'herself'
    elif pronoun == 'they' or pronoun == 'they_plural':
        if form == 'object': 
            pronoun = 'them'
        elif form == 'possesive': 
            pronoun = 'theirs'
        elif form == 'reflexive': 
            if pronoun == 'they_plural':
                pronoun = 'themselves'
            else:
                pronoun = 'themself'
    return pronoun

def format_health(stage, status, color1_stage, color2_stage):
    def add_color(text, color):
        if color:
            text = add_text_tag(text, fg = color)
        return text
    color = None
    if stage >= color2_stage:
        color = config.TAG_COLOR_HEALTH_STAGE_6
    elif stage >= color1_stage:
        color = config.TAG_COLOR_HEALTH_STAGE_3
    status = re.sub("<color>(.*?)</color>", add_color(r"\1", color), status)
    return status

def format_player_health(stage, status):
    return format_health(stage, status, 3, 6)

def format_npc_health(stage, status):
    return format_health(stage, status, 2, 3)

def format_color_stage(text, stage):
    color = config.TAG_COLOR_STAGE_2
    if stage <= 0:
        color = config.TAG_COLOR_STAGE_0
    elif stage <= 1:
        color = config.TAG_COLOR_STAGE_1
    elif stage >= 4:
        color = config.TAG_COLOR_STAGE_3
    return add_text_tag(text, fg = color)

def format_damage_num(damage, capitalized = True, colored = True):
    damage_level = 3
    damage_text = 'medium'
    if damage == 0:
        damage_text = 'none'
        damage_level = 0
    elif damage < 7:
        damage_text = 'very weak'
        damage_level = 1
    elif damage < 14:
        damage_text = 'weak'
        damage_level = 2
    elif damage > 35:
        damage_text = 'very strong'
        damage_level = 5
    elif damage > 21:
        damage_text = 'strong'
        damage_level = 4
    damage = str(damage) + ' points'
    if config.flags['show_battle_num'] is False:
        damage = damage_text
    if capitalized:
        damage = damage.capitalize()
    if colored:
        damage = format_color_stage(damage, damage_level)
    return damage

def format_defence_num(damage, num_items = None, capitalized = True, colored = True):
    damage_avg = damage
    if num_items is not None and damage > 0:
        damage_avg = damage / num_items
    damage_text = 'medium'
    damage_level = 3
    if damage_avg == 0:
        damage_text = 'none'
        damage_level = 0
    elif damage_avg < 2:
        damage_text = 'very weak'
        damage_level = 1
    elif damage_avg < 4:
        damage_text = 'weak'
        damage_level = 2
    elif damage_avg > 10:
        damage_text = 'very strong'
        damage_level = 5
    elif damage_avg > 8:
        damage_text = 'strong'
        damage_level = 4
    damage = str(damage) + ' points'
    if config.flags['show_battle_num'] is False:
        damage = damage_text
    if capitalized:
        damage = damage.capitalize()
    if colored:
        damage = format_color_stage(damage, damage_level)
    return damage

def format_skill_num(num, capitalized = True, colored = True):
    num_text = str(num)
    if num == 0:
        num_text = 'none'
    elif num == 1:
        num_text = 'unexperienced'
    elif num == 2:
        num_text = 'adequate'
    elif num == 3:
        num_text = 'proficient'
    elif num == 4:
        num_text = 'highly skilled'
    elif num == 5:
        num_text = 'master'
    if capitalized:
        num_text = num_text.capitalize()
    if colored:
        num_text = format_color_stage(num_text, num)
    return num_text

def random_chance(level):
    random_options = [False, False, False, False, True]
    if level == 2:
        random_options = [False, False, True]
    if level == 3:
        random_options = [False, True]
    if level == 4:
        random_options = [False, True, True, True]
    if level == 5:
        random_options = [False, True, True, True, True, True, True]
    if level == 0:
        random_options = [False, False, False, False ,False, False, False, False, False, False, False, False ,False, False, False, False, False, False, False, True]
    return random.choice(random_options)

def random_chance_luck_combat(level):
    random_options = [False, False, False, False, False, False, False, False, False, True]
    if level == 2:
        random_options = [False, False, False, False, False, False, False, False, True, True]
    if level == 3:
        random_options = [False, False, False, False, False, False, False, True, True, True]
    if level == 4:
        random_options = [False, False, False, False, False, False, True, True, True, True]
    if level == 5:
        random_options = [False, True]
    if level == 0:
        random_options = [False, False, False, False ,False, False, False, False, False, False, False, False ,False, False, False, False, False, False, False, True]
    return random.choice(random_options)

def randomize_damage(dmg):
    dmg_min = int(dmg * 0.75)
    dmg_max = int(dmg * 1.25)
    dmg_result = random.randrange(dmg_min, dmg_max + 1)
    return dmg_result