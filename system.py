# BUILT-IN
import datetime
import json
import time

# PROJECT
import audio
import config
import utils

class SelectionOption:
    def __init__(self, name, display_name, link = None, s_type = None, s_options = None):
        self.name = name
        self.display_name = display_name
        self.link = link
        self.s_type = s_type
        self.s_options = s_options

# SET VARS
queue_list = []
ui_selection_options = None
ui_pre_quit_prompt = False
ui_restart_prompt = False
ui_quit_prompt = False

def quit_game():
    config.run_game = False

def restart_game():
    global ui_restart_prompt
    ui_restart_prompt = False
    change_mode(config.MODE_MAIN_MENU)

def pre_quit_prompt():
    global ui_pre_quit_prompt
    ui_selection_none()
    ui_pre_quit_prompt = not ui_pre_quit_prompt

def quit_game_prompt():
    global ui_quit_prompt
    ui_selection_none()
    ui_quit_prompt = not ui_quit_prompt

def restart_game_prompt():
    global ui_restart_prompt
    ui_selection_none()
    ui_restart_prompt = not ui_restart_prompt

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
    ui_selection_none()
    active_room = room_id
    room = rooms[room_id]
    for line in room['on_enter']:
        if not line['disabled'] and (line['position'] == "" or line['position'] == current_position):
            execute_action(line['content'])
    if config.mode != config.MODE_GAME:
        change_mode(config.MODE_GAME)
    else:
        config.trigger_animation(config.ANIMATION_CHANGE_ROOM)
    if logging:
        add_log("You enter the " + rooms[active_room]['noun'])

def change_position(position, logging = False):
    global current_position
    ui_selection_none()
    wait = current_position == position
    action_text = "move to"
    if wait:
        action_text = "wait at"
    current_position = position
    rooms[active_room]['visited'][current_position] = True
    if logging:
        log_string = "You " + action_text + " the " + utils.DIRECTION_ABR[position]
        if position != "c":
            log_string += " side"
        log_string += " of the " + rooms[active_room]['noun']
        add_log(log_string)

def execute_action(action):
    if action['type'] == 'enter_room':
        enter_room(action['link'])
    elif action['type'] == 'change_position':
        change_position(action['link'])
    elif action['type'] == 'activate_status':
        activate_status(action['link'])
    elif action['type'] == 'change_mode':
        change_mode(action['link'])
    config.add_debug_log("Action: " + action['type'] + " -> " + action['link'])

def queue_action(action):
    queue_list.append(action)

def run_queued_actions():
    while queue_list:
        action = queue_list.pop(0)
        execute_action(action)

def add_log(item):
    global log_list
    log_list.append(item)

def get_selected_option():
    selected_option = None
    if ui_selection_options:
        selected_option = ui_selection_options[config.ui_selection_x][config.ui_selection_y]
    return selected_option

def press_to_continue(key, target_key = "enter"):
    while key != target_key:
        key = get_keypress()
    audio.ui_confirm()

def set_selection_options(target_list):
    global ui_selection_options
    result = []
    num_x = len(target_list)
    num_y = len(max(target_list, key = len))
    max_selection_y = None
    for x in range(num_x):
        result.append([])
        for y in range(num_y):
            entry = None
            if y < len(target_list[x]):
                entry = target_list[x][y]
                if config.ui_selection_x == x:
                    max_selection_y = y
            result[x].append(entry)
    ui_selection_options = result
    config.ui_selection_y = min(max_selection_y, config.ui_selection_y)
    config.ui_selection_current = ui_selection_options[config.ui_selection_x][config.ui_selection_y]

def ui_selection_y_prev():
    if config.ui_selection_y > 0:
        found = config.ui_selection_y - 1
        if ui_selection_options[config.ui_selection_x][found] is None:
            found = None
            for num in range(config.ui_selection_y - 1, -1, -1):
                if ui_selection_options[config.ui_selection_x][num] is not None:
                    found = num
                    break
        if found is not None:
            audio.ui_sel()
            config.ui_selection_y = found
            while config.ui_selection_x > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x -= 1
            while config.ui_selection_x < len(ui_selection_options) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x += 1

def ui_selection_y_next():
    if config.ui_selection_y < len(ui_selection_options[config.ui_selection_x])-1:
        found = config.ui_selection_y + 1
        if ui_selection_options[config.ui_selection_x][found] is None:
            found = None
            for num in range(config.ui_selection_y + 1, len(ui_selection_options[config.ui_selection_x])):
                if ui_selection_options[config.ui_selection_x][num] is not None:
                    found = num
                    break
        if found is not None:
            config.ui_selection_y = found
            audio.ui_sel()
            while config.ui_selection_x > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x -= 1
            while config.ui_selection_x < len(ui_selection_options) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x += 1

def ui_selection_x_prev():
    if config.ui_selection_x > 0:
        found = None
        for num in range(config.ui_selection_x - 1, -1, -1):
            if len(utils.list_none_filter(ui_selection_options[num])) > 0:
                found = num
                break
        if found is not None:
            audio.ui_sel()
            config.ui_selection_x = found
            while config.ui_selection_y > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y -= 1
            while config.ui_selection_y < len(ui_selection_options[config.ui_selection_x]) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y += 1

def ui_selection_x_next():
    if config.ui_selection_x < len(ui_selection_options)-1:
        found = None
        for num in range(config.ui_selection_x + 1, len(ui_selection_options)):
            if len(utils.list_none_filter(ui_selection_options[num])) > 0:
                found = num
                break
        if found is not None:
            audio.ui_sel()
            config.ui_selection_x = found
            while config.ui_selection_y > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y -= 1
            while config.ui_selection_y < len(ui_selection_options[config.ui_selection_x]) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y += 1

def ui_log_scroll_up():
    config.ui_log_scroll_pos += 1

def ui_log_scroll_down():
    config.ui_log_scroll_pos -= 1

def ui_log_or_selection_up():
    if config.ui_selection_y == 0:
        ui_log_scroll_up()
    else:
        ui_selection_y_prev()

def ui_log_or_selection_down():
    if config.ui_selection_y == 0 and config.ui_log_scroll_pos > 0:
        ui_log_scroll_down()
    else:
        ui_selection_y_next()

def ui_log_or_selection_left():
    if config.ui_log_scroll_pos == 0:
        ui_selection_x_prev()
def ui_log_or_selection_right():
    if config.ui_log_scroll_pos == 0:
        ui_selection_x_next()

def ui_selection_none():
    global ui_selection_options
    ui_selection_options = None
    config.ui_selection_x = 0
    config.ui_selection_y = 0
    config.ui_log_scroll_pos = 0
    config.ui_selection_current = None

def change_mode(new_mode):
    config.trigger_animation(config.ANIMATION_CHANGE_MODE)
    config.previous_mode = config.mode
    config.mode = new_mode
    ui_selection_none()
    if config.mode == config.MODE_MAIN_MENU:
        audio.music_change_type(audio.MUSIC_TYPE_MAIN_MENU)
    elif config.mode == config.MODE_CUTSCENE or config.mode == config.MODE_GAME:
        audio.music_change_type(audio.MUSIC_TYPE_GAME)

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
    rooms = json.load(open('resources/data/rooms.json','r')) 
    cutscenes = json.load(open('resources/data/cutscenes.json','r')) 
    interactables = json.load(open('resources/data/interactables.json','r')) 
    portals = json.load(open('resources/data/portals.json','r')) 
    statuses = json.load(open('resources/data/statuses.json','r')) 
    items = json.load(open('resources/data/items.json','r')) 
    log_list = ["You start the game"]
    inventory_list = []
    active_cutscene = "1"
    active_room = "1"
    current_position = "c"
    config.add_debug_log("Initializing new game")
    change_mode(config.MODE_CUTSCENE)

def ui_selection_option_change_scale_inc(current_value, settings):
    max_value = settings[1]
    inc_value = settings[2]
    current_value += inc_value
    audio.ui_sel()
    return min(current_value, max_value)

def ui_selection_option_change_scale_dec(current_value, settings):
    min_value = settings[0]
    inc_value = settings[2]
    current_value -= inc_value
    audio.ui_sel()
    return max(current_value, min_value)

def ui_selection_option_change_multi_prev(current_value, target_list):
    index_value = target_list.index(current_value)
    if index_value > 0:
        current_value = target_list[index_value - 1]
    audio.ui_sel()
    return current_value

def ui_selection_option_change_multi_next(current_value, target_list):
    max_value = len(target_list) - 1
    index_value = target_list.index(current_value)
    if index_value < max_value:
        current_value = target_list[index_value + 1]
    audio.ui_sel()
    return current_value

def ui_selection_option_change_toggle(current_value):
    audio.ui_sel()
    return not current_value