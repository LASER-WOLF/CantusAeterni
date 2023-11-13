# BUILT-IN
import json
import re

# PROJECT
import config

# SET CONSTANTS
DIRECTION_ABR = {'nw': 'north-west', 'n': 'north', 'ne': 'north-east', 'w': 'west', 'c': 'center', 'e': 'east', 'sw': 'south-west', 's': 'south', 'se': 'south-east' }
DIRECTION_TO_COORD = {'nw': {'x': -1, 'y': -1}, 'n': {'x': 0, 'y': -1}, 'ne': {'x': 1, 'y': -1}, 'w': {'x': -1, 'y': 0}, 'c': {'x': 0, 'y': 0}, 'e': {'x': 1, 'y': 0}, 'sw': {'x': -1, 'y': 1}, 's': {'x': 0, 'y': 1}, 'se': {'x': 1, 'y': 1} }
DIRECTION_REVERSE = {'nw': 'se', 'n': 's', 'ne': 'sw', 'w': 'e', 'c': 'c', 'e': 'w', 'sw': 'ne', 's': 'n', 'se': 'nw' }

def import_json(filename):
    return json.load(open(filename + '.json','r'))

def export_json(name, content):
    with open(name + ".json", "w") as outfile:
            json.dump(content, outfile, indent = 2)

def add_ui_tag(string, x = 0, y = 0, action = "00"):
    return "<ui=" + str(x).zfill(2) + ":" + str(y).zfill(2) + ":" + str(action) + ">" + string + "</ui>"

def add_tag(string, fg = "fg", bg = "bg", other = "00"):
    return "<text=" + str(fg) + ":" + str(bg) + ":" + str(other) + ">" + string + "</text>"

def remove_tag(target_line):
    target_line = remove_text_tag(target_line)
    target_line = remove_ui_tag(target_line)
    return target_line

def remove_text_tag(target_line):
    target_line = re.sub('<text=(.{2}):(.{2}):(.{2})>(.*?)</text>', r"\4", target_line)
    return target_line

def remove_ui_tag(target_line):
    target_line = re.sub('<ui=(.{2}):(.{2}):(.{2})>(.*?)</ui>', r"\4", target_line)
    return target_line

def remove_tag_list(target_list):
    new_list = []
    for line in target_list:
        new_list.append(remove_tag(line))
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

def format_position_text(abr):
    position_string = format_direction(DIRECTION_ABR[abr])
    if abr != "c":
        position_string += " side"
    return position_string

def format_position_text_room(abr, room_noun):
    return format_position_text(abr) + ' of the ' + room_noun

def format_status(text):
    return add_tag(text, fg = config.TAG_COLOR_STATUS)

def format_interactable(text):
    return add_tag(text, fg = config.TAG_COLOR_INTERACTABLE)

def format_npc(text):
    return add_tag(text, fg = config.TAG_COLOR_NPC)

def format_direction(text):
    return add_tag(text, fg = config.TAG_COLOR_DIRECTION)

def format_portal(text):
    return add_tag(text, fg = config.TAG_COLOR_PORTAL)

def format_log_damage(text):
    return add_tag(text, fg = config.TAG_COLOR_LOG_DAMAGE)

def format_log_npc(name, proper_noun):
    name = format_npc(name)
    if proper_noun is False:
        name = 'the ' + name
    return name

def format_health(stage, status):
    def add_color(text, color):
        if color:
            text = add_tag(text, fg = color)
        return text
    color = None
    if stage >= 6:
        color = config.TAG_COLOR_HEALTH_STAGE_6
    elif stage >= 3:
        color = config.TAG_COLOR_HEALTH_STAGE_3
    status = re.sub("<color>(.*?)</color>", add_color(r"\1", color), status)
    return status

def format_color_tags(content):
    content = re.sub("<i>(.*?)</i>", format_interactable(r"\1"), content)
    content = re.sub("<s>(.*?)</s>", format_status(r"\1"), content)
    content = re.sub("<d>(.*?)</d>", format_direction(r"\1"), content)
    content = re.sub("<p>(.*?)</p>", format_portal(r"\1"), content)
    content = re.sub("<n>(.*?)</n>", format_npc(r"\1"), content)
    return content