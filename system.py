# BUILT-IN
import datetime
import json
import time
import random

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
main_content = None
popup_content = None

def end_turn(action, npcs = None):
    if action == 'portal':
        audio.fx_change_room()
        config.trigger_animation(config.ANIMATION_CHANGE_ROOM)
    else:
        config.trigger_animation(config.ANIMATION_FADE)
    hp_old = config.player['health_points']
    if npcs:
        npc_behaviour(npcs)
    if config.player['health_points'] > 0:
        dmg_from_statuses()
        dmg_from_wounds()
    hp_new = config.player['health_points']
    hp_diff = hp_old - hp_new
    if hp_diff > 0:
        config.trigger_animation(config.ANIMATION_TAKE_DAMAGE)
        audio.fx_npc_hit()
    elif action == 'move':
        audio.fx_move()
    elif action == 'pickup':
        audio.fx_pick_up_item()
    update_health_status()
    config.game['turn'] += 1
    config.ui_scroll_log = 0
    config.ui_scroll_center = 0

def update_health_status():
    health_stage = 0
    if config.player['health_points'] <= 0:
        health_stage = 8
    elif config.player['health_points'] < 10:
        health_stage = 7
    elif config.player['health_points'] < 26:
        health_stage = 6
    elif config.player['health_points'] < 42:
        health_stage = 5
    elif config.player['health_points'] < 58:
        health_stage = 4
    elif config.player['health_points'] < 74:
        health_stage = 3
    elif config.player['health_points'] < 90:
        health_stage = 2
    elif config.player['health_points'] < 100:
        health_stage = 1
    if config.player['health_stage'] != health_stage:
        if health_stage == 0:
            config.player['health_status'] = None
        else:
            health_status = random.choice(config.health_stages[health_stage])
            health_status = utils.format_health(health_stage, health_status)
            if health_stage > config.player['health_stage'] and config.player['health_points'] > 0:
                add_log(health_status)
            config.player['health_status'] = health_status
        config.player['health_stage'] = health_stage

def npc_check_move(npc):
    move = False
    if not npc['immobile']:
        move = random_chance(npc['speed'])
    return move

def dmg_from_statuses():
    for status in statuses.values():
        if status['active'] and status['damage']:
            player_take_damage(randomize_damage(status['damage']), status['damage_name'], status['game_over_text'])

def dmg_from_wounds():
    if config.player['health_stage'] == 6 or config.player['health_stage'] == 7:
        if random_chance(config.player['health_stage'] - 4):
            player_take_damage(randomize_damage(1), 'wounds', 'You died from wounds.')

def random_chance(level):
    random_options = [False, False, False, False, True]
    if level == 2:
        random_options = [False, False, True]
    if level == 3:
        random_options = [False, True]
    if level == 4:
        random_options = [False, True, True, True]
    if level == 5:
        random_options = [True]
    if level == 0:
        random_options = [False]
    return random.choice(random_options)

def npc_behaviour(npcs):
    for npc_id, npc in npcs.items():
        if npc['room'] == active_room and config.player['health_points'] > 0:
            if npc['hostile'] is True:
                if npc['ranged'] and npc['position'] != current_position:
                    npc_action_attack_player(npc, ranged = True)
                else:
                    if npc['position'] == current_position:
                        npc_action_attack_player(npc)
                    else:
                        if npc_check_move(npc):
                            npc_move_to_player(npc)
            elif npc['always_moving'] is True:
                if npc_check_move(npc):
                    npc_move_random(npc)

def npc_action_move(npc, link):
    npc_change_position(link, npc)

def format_npc_log_text(text, npc):
    text = text.replace('<pos>', utils.format_position_text_room(npc['position'], rooms[active_room]['noun']))
    text = text.replace('<name>', utils.format_log_npc(npc['name'], npc['proper_noun']))
    if npc['proper_noun'] is False:
        text = text.capitalize()
    return text

def player_take_damage(dmg, dmg_source, game_over_text = None):
    if dmg > 0 and config.player['health_points'] > 0:
        old_hp = config.player['health_points']
        new_hp = max(0, old_hp - dmg)
        diff = old_hp - new_hp
        dmg_num_txt = 'damage'
        if diff < 5:
            dmg_num_txt = 'minor damage'
        elif diff > 20:
            dmg_num_txt = 'major damage'
        elif diff > 40:
            dmg_num_txt = 'a colossal amount of damage'
        damage_text = 'take ' + utils.format_log_damage(dmg_num_txt)
        if config.flags['show_hp_num']:
            s = ''
            if dmg != 1:
                s = 's'
            damage_text = 'lose ' + utils.format_log_damage(str(diff) + ' health point' + s)
        add_log('You ' + damage_text + ' from ' + dmg_source +'.')
        config.player['health_points'] = new_hp
        if new_hp <= 0:
            add_log('You die from ' + dmg_source + '.')
            if game_over_text:
                config.game['game_over_text'] = game_over_text

def player_death():
    config.game['game_over'] = True
    popup_lines = []
    popup_lines.append('')
    popup_lines.append('         .:=%@@@@%=-.         ')
    popup_lines.append('       .#@@@@@@@@@@@@%.       ')
    popup_lines.append('      #@@@@@@@@@@@@@@@@#.     ')
    popup_lines.append('     %@@@@@@@@@@@@@@@@@@@     ')
    popup_lines.append('     %@*@@@@@@@@@@@@@@*@@     ')
    popup_lines.append('     %@%-%@%##%**#%@@=%@@     ')
    popup_lines.append('     .%%-+::-****:::+-%%:     ')
    popup_lines.append('      .*     :%@+     #.      ')
    popup_lines.append('      #@+-:=*%:.**+::+@#      ')
    popup_lines.append('      =#@+-+@%=:*@#:+%%=      ')
    popup_lines.append('        ++:#%@%@@%%-++        ')
    popup_lines.append('         + -:*-++-+ *:        ')
    popup_lines.append('         =:*=@*#%+#:=.        ')
    popup_lines.append('          -#@@@@@@#=          ')
    popup_lines.append('            """"""            ')
    popup_lines.append('')
    popup_lines.append('You have reached the end of your journey.')
    if config.game['game_over_text']:
        popup_lines.append(config.game['game_over_text'])
    popup_lines.append('You played for ' + str(config.game['turn']) + ' turns.')
    popup_options = [[
        SelectionOption('restart_game', 'Return to title screen'),
        SelectionOption('quit_game', 'Quit game')
    ]]
    set_popup_content(popup_lines, popup_options, centered = True, play_animation = False)

def randomize_damage(dmg):
    dmg_min = int(dmg * 0.75)
    dmg_max = int(dmg * 1.25)
    dmg_result = random.randrange(dmg_min, dmg_max + 1)
    return dmg_result

def npc_action_attack_player(npc, ranged = False):
    attack_text = npc['name'] + ' attacks you.'
    miss_text = config.dodge_text
    npc_miss_text = npc['attack_miss_text']
    game_over_text = '<name_log> killed you.'
    attack_skill = npc['attack_skill']
    npc_attack_text = npc['attack_text']
    npc_game_over_text = npc['game_over_text']
    damage = npc['damage']
    on_attack = npc['on_attack']
    if ranged:
        attack_text = npc['name'] + ' attacks you from a distance.'
        npc_miss_text = npc['attack_miss_text_ranged']
        game_over_text = '<name_log> killed you from a distance.'
        attack_skill = npc['attack_skill_ranged']
        npc_attack_text = npc['attack_text_ranged']
        if npc['game_over_text_ranged']:
            npc_game_over_text = npc['game_over_text_ranged']
        damage = npc['damage_ranged']
        on_attack = npc['on_attack_ranged']
    hit = random_chance(attack_skill)
    if npc_attack_text:
        attack_text = random.choice(npc_attack_text)
    if npc_game_over_text:
        game_over_text = random.choice(npc_game_over_text)
    if npc_miss_text and random.choice([False, True]):
        miss_text = npc_miss_text
    miss_text = random.choice(miss_text)
    attack_text = format_npc_log_text(attack_text, npc)
    game_over_text = format_npc_log_text(game_over_text, npc)
    add_log(attack_text)
    if hit:
        player_take_damage(randomize_damage(damage), 'the attack', game_over_text)
        if config.player['health_points'] > 0:
            for action in on_attack:
              execute_action(action)
    else:
        add_log(miss_text)

def npc_move_to_player(npc):
    move_options = []
    npc_pos = npc['position']
    npc_pos_coord = utils.DIRECTION_TO_COORD[npc_pos]
    player_pos_coord = utils.DIRECTION_TO_COORD[current_position]
    for pos, text in utils.DIRECTION_ABR.items():
        pos_coord = utils.DIRECTION_TO_COORD[pos]
        if npc_pos != pos and abs(pos_coord['x'] - npc_pos_coord['x']) <= 1 and abs(pos_coord['y'] - npc_pos_coord['y']) <= 1:
            score = abs(player_pos_coord['x'] - pos_coord['x']) + abs(player_pos_coord['y'] - pos_coord['y'])
            move_options.append((score, pos))
    new_position = sorted(move_options)[0][1]
    npc_action_move(npc, new_position)

def npc_move_random(npc):
    move_options = []
    npc_pos = npc['position']
    npc_pos_coord = utils.DIRECTION_TO_COORD[npc_pos]
    for pos, text in utils.DIRECTION_ABR.items():
        pos_coord = utils.DIRECTION_TO_COORD[pos]
        if npc_pos != pos and abs(pos_coord['x'] - npc_pos_coord['x']) <= 1 and abs(pos_coord['y'] - npc_pos_coord['y']) <= 1:
            move_options.append(pos)
    new_position = random.choice(move_options)
    npc_action_move(npc, new_position)

def player_change_position(position, logging = False):
    global current_position
    ui_selection_none()
    rooms[active_room]['visited'][position] = True
    old_pos = current_position
    current_position = position
    if logging:
        change_position_logging('You', old_pos, position)

def npc_change_position(new_pos, npc, logging = True):
    old_pos = npc['position']
    npc['position'] = new_pos
    name = npc['name']
    if npc['name_log']:
        name = npc['name_log']
    if rooms[active_room]['visited'][old_pos] or rooms[active_room]['visited'][new_pos]:
        change_position_logging(name, old_pos, new_pos, plural = True)

def change_position_logging(name, old_pos, new_pos, plural = False):
    add_s = ''
    if plural:
        add_s = 's'
    wait = old_pos == new_pos
    action_text = 'move' + add_s + ' to'
    if wait:
        action_text = 'wait' + add_s + ' at'
    log_string = name + " " + action_text + " the " + '<d>' + utils.DIRECTION_ABR[new_pos] + '</d>'
    if new_pos != "c":
        log_string += " side"
    log_string += " of the " + rooms[active_room]['noun'] + '.'
    add_log(log_string)

def set_popup_content(lines, options = None, centered = False, play_animation = True):
    global popup_content
    if play_animation:
        config.trigger_animation(config.ANIMATION_FADE_POPUP)
    config.ui_selection_x_prev = config.ui_selection_x
    config.ui_selection_y_prev = config.ui_selection_y
    config.ui_selection_x = 0
    config.ui_selection_y = 0
    popup_content = {
        'lines': lines,
        'options': options,
        'centered': centered
    }

def unset_popup_content():
    global popup_content
    config.ui_selection_x = config.ui_selection_x_prev
    config.ui_selection_y = config.ui_selection_y_prev
    popup_content = None
    ui_selection_options = None

def prev_selection_none():
    config.ui_selection_x_prev = 0
    config.ui_selection_y_prev = 0

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
    if logging:
        add_log("You enter the " + rooms[active_room]['noun'])

def execute_action(action):
    if action['type'] == 'enter_room':
        enter_room(action['link'])
    elif action['type'] == 'change_position':
        player_change_position(action['link'])
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
    list_entry = (config.game['turn'], utils.format_color_tags(item))
    log_list.append(list_entry)

def press_to_continue(key, target_key = "enter"):
    while key != target_key:
        key = get_keypress()
    audio.ui_confirm()

def set_selection_options(target_list):
    global ui_selection_options
    if target_list is None:
        ui_selection_options = None
    else:
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
        if max_selection_y is None:
            if config.ui_selection_x > 0:
                ui_selection_x_prev()
            else:
                ui_selection_x_next()
        else:
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

def ui_scroll_center_down():
    config.ui_scroll_center += 1

def ui_scroll_center_up():
    if config.ui_scroll_center > 0:
        config.ui_scroll_center -= 1

def ui_log_scroll_up():
    config.ui_scroll_log += 1

def ui_log_scroll_down():
    config.ui_scroll_log -= 1

def ui_log_or_selection_up():
    if config.ui_selection_y == 0:
        ui_log_scroll_up()
    else:
        ui_selection_y_prev()

def ui_log_or_selection_down():
    if config.ui_selection_y == 0 and config.ui_scroll_log > 0:
        ui_log_scroll_down()
    else:
        ui_selection_y_next()

def ui_log_or_selection_left():
    if config.ui_scroll_log == 0:
        ui_selection_x_prev()
def ui_log_or_selection_right():
    if config.ui_scroll_log == 0:
        ui_selection_x_next()

def ui_selection_none():
    global ui_selection_options
    ui_selection_options = None
    config.ui_selection_x = 0
    config.ui_selection_y = 0
    config.ui_log_scroll_pos = 0
    config.ui_selection_current = None

def change_mode(new_mode):
    global main_content
    global popup_content
    ui_selection_none()
    main_content = None
    popup_content = None
    config.trigger_animation(config.ANIMATION_FADE)
    config.previous_mode = config.mode
    config.mode = new_mode
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
    global npcs
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
    npcs = json.load(open('resources/data/npcs.json','r')) 
    log_list = [(0, "You start the game.")]
    inventory_list = []
    active_cutscene = "1"
    active_room = "1"
    current_position = "c"
    config.initialize_new_game()
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