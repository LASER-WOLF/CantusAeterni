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
    def __init__(self, name, display_name, link = None, s_type = None, s_options = None, link_secondary = None):
        self.name = name
        self.display_name = display_name
        self.link = link
        self.s_type = s_type
        self.s_options = s_options
        self.link_secondary = link_secondary

# SET VARS
queue_list = []
ui_selection_options = None
ui_pre_quit_prompt = False
ui_restart_prompt = False
ui_quit_prompt = False
main_content = None
popup_content = None

def initialize_new_game():
    global rooms
    global cutscenes
    global interactables
    global portals
    global statuses
    global items
    global npcs
    global dialogues
    global log_list
    global dialogue_log
    global inventory_list
    global active_cutscene
    global active_room
    global active_npcs
    global current_position
    global current_target
    rooms = json.load(open('resources/data/rooms.json','r')) 
    cutscenes = json.load(open('resources/data/cutscenes.json','r')) 
    interactables = json.load(open('resources/data/interactables.json','r')) 
    portals = json.load(open('resources/data/portals.json','r')) 
    statuses = json.load(open('resources/data/statuses.json','r')) 
    items = json.load(open('resources/data/items.json','r')) 
    npcs = json.load(open('resources/data/npcs.json','r')) 
    dialogues = json.load(open('resources/data/dialogues.json','r')) 
    log_list = [(0, "You start the game.")]
    dialogue_log = []
    inventory_list = []
    active_cutscene = '1'
    active_room = config.START_ROOM
    active_npcs = None
    current_position = config.START_POSITION
    current_target = None
    config.initialize_new_game()
    change_mode(config.MODE_CUTSCENE)

def end_turn(action):
    if action == 'portal':
        config.trigger_animation('change_room', 'fx_change_room')
    else:
        config.trigger_animation('fade')
    hp_old = config.player['health_points']
    if action != 'portal':
        npc_behaviour()
    if config.player['health_points'] > 0:
        dmg_from_statuses()
        dmg_from_wounds()
    hp_new = config.player['health_points']
    hp_diff = hp_old - hp_new
    if hp_diff > 0:
        config.trigger_animation('take_damage', 'fx_npc_hit')
    elif action == 'move':
        audio.sound_play('fx_move')
    elif action == 'pickup':
        audio.sound_play('fx_pick_up_item')
    elif action == 'portal_blocked':
        audio.sound_play('ui_back')
    config.game['turn'] += 1
    config.ui_scroll_zero()

def change_mode(new_mode):
    global main_content
    global popup_content
    ui_selection_none()
    config.ui_scroll_zero()
    main_content = None
    popup_content = None
    config.trigger_animation('fade')
    config.previous_mode = config.mode
    config.mode = new_mode
    if config.mode == config.MODE_MAIN_MENU:
        audio.music_change_type(audio.MUSIC_TYPE_MAIN_MENU)
    elif config.mode == config.MODE_CUTSCENE or config.mode == config.MODE_GAME:
        audio.music_change_type(audio.MUSIC_TYPE_GAME)

def change_mode_previous():
    audio.sound_play('ui_back', 'ui')
    change_mode(config.previous_mode)
    return True

def set_popup_content(lines, options = None, centered = False, play_animation = True, border_color = None, fg_color = None, bg_color = None):
    global popup_content
    if play_animation:
        config.trigger_animation('fade_popup')
    config.ui_selection_x_prev = config.ui_selection_x
    config.ui_selection_y_prev = config.ui_selection_y
    config.ui_selection_x = 0
    config.ui_selection_y = 0
    popup_content = {
        'lines': lines,
        'options': options,
        'centered': centered,
        'border_color': border_color,
        'fg_color': fg_color,
        'bg_color': bg_color,
    }

def unset_popup_content(play_animation = True):
    global popup_content
    if play_animation:
        config.trigger_animation('fade')
    config.ui_selection_x = config.ui_selection_x_prev
    config.ui_selection_y = config.ui_selection_y_prev
    popup_content = None
    ui_selection_options = None

def add_log(item):
    global log_list
    list_entry = (config.game['turn'], utils.format_color_tags(item))
    log_list.append(list_entry)

def add_dialogue_log(entry):
    global dialogue_log
    dialogue_log.append(entry)

def activate_flag(flag, activate = True):
    if flag in config.flags:
        config.flags[flag] = activate

def deactivate_flag(flag):
    activate_flag(flag, False)

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

def execute_action(action):
    if action['type'] == 'enter_room':
        enter_room(action['link'])
    elif action['type'] == 'change_position':
        player_change_position(action['link'])
    elif action['type'] == 'activate_status':
        activate_status(action['link'])
    elif action['type'] == 'deactivate_status':
        deactivate_status(action['link'])
    elif action['type'] == 'activate_flag':
        activate_flag(action['link'])
    elif action['type'] == 'deactivate_flag':
        deactivate_flag(action['link'])
    elif action['type'] == 'change_mode':
        change_mode(action['link'])
    elif action['type'] == 'npc_set_hostile':
        npc_set_hostile(action['link'])
    elif action['type'] == 'npc_set_friendly':
        npc_set_friendly(action['link'])
    elif action['type'] == 'npc_unlock_secret_name':
        npc_unlock_secret_name(action['link'])
    elif action['type'] == 'heal_player':
        heal_player(action['link'])
    config.add_debug_log("Action: " + action['type'] + " -> " + str(action['link']))

def queue_action(action):
    queue_list.append(action)

def run_queued_actions():
    while queue_list:
        action = queue_list.pop(0)
        execute_action(action)

def quit_game():
    config.run_game = False

def restart_game():
    global ui_restart_prompt
    ui_restart_prompt = False
    change_mode(config.MODE_MAIN_MENU)

def pre_quit_prompt():
    global ui_pre_quit_prompt
    ui_selection_none()
    config.ui_scroll_zero()
    ui_pre_quit_prompt = not ui_pre_quit_prompt

def quit_game_prompt():
    global ui_quit_prompt
    ui_selection_none()
    config.ui_scroll_zero()
    ui_quit_prompt = not ui_quit_prompt

def restart_game_prompt():
    global ui_restart_prompt
    ui_selection_none()
    config.ui_scroll_zero()
    ui_restart_prompt = not ui_restart_prompt

def ui_selection_none():
    global ui_selection_options
    ui_selection_options = None
    config.ui_selection_x = 0
    config.ui_selection_y = 0
    config.ui_selection_current = None

def prev_selection_none():
    config.ui_selection_x_prev = 0
    config.ui_selection_y_prev = 0

def set_selection_options(target_list):
    global ui_selection_options
    if target_list is None:
        ui_selection_none()
    else:
        result = []
        num_x = len(target_list)
        num_y = len(max(target_list, key = len))
        min_selection_y = None
        max_selection_y = None
        for x in range(num_x):
            result.append([])
            for y in range(num_y):
                entry = None
                if y < len(target_list[x]):
                    entry = target_list[x][y]
                    if config.ui_selection_x == x and entry is not None:
                        max_selection_y = y
                        if min_selection_y is None:
                            min_selection_y = y
                result[x].append(entry)
        ui_selection_options = result
        if max_selection_y is None and num_x > 1:
            if config.ui_selection_x > 0:
                ui_selection_x_prev()
            else:
                ui_selection_x_next()
        else:
            config.ui_selection_y = min(max_selection_y, max(min_selection_y, config.ui_selection_y))
        config.ui_selection_current = ui_selection_options[config.ui_selection_x][config.ui_selection_y]

def ui_selection_y_prev():
    valid_input = False
    if config.ui_selection_y > 0:
        found = config.ui_selection_y - 1
        if ui_selection_options[config.ui_selection_x][found] is None:
            found = None
            for num in range(config.ui_selection_y - 1, -1, -1):
                if ui_selection_options[config.ui_selection_x][num] is not None:
                    found = num
                    break
        if found is not None:
            valid_input = True
            audio.sound_play('ui_sel', 'ui')
            config.ui_selection_y = found
            while config.ui_selection_x > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x -= 1
            while config.ui_selection_x < len(ui_selection_options) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x += 1
    return valid_input

def ui_selection_y_next():
    valid_input = False
    if config.ui_selection_y < len(ui_selection_options[config.ui_selection_x])-1:
        found = config.ui_selection_y + 1
        if ui_selection_options[config.ui_selection_x][found] is None:
            found = None
            for num in range(config.ui_selection_y + 1, len(ui_selection_options[config.ui_selection_x])):
                if ui_selection_options[config.ui_selection_x][num] is not None:
                    found = num
                    break
        if found is not None:
            valid_input = True
            audio.sound_play('ui_sel', 'ui')
            config.ui_selection_y = found
            while config.ui_selection_x > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x -= 1
            while config.ui_selection_x < len(ui_selection_options) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_x += 1
    return valid_input

def ui_selection_x_prev():
    valid_input = False
    if config.ui_selection_x > 0:
        found = None
        for num in range(config.ui_selection_x - 1, -1, -1):
            if len(utils.list_none_filter(ui_selection_options[num])) > 0:
                found = num
                break
        if found is not None:
            valid_input = True
            audio.sound_play('ui_sel', 'ui')
            config.ui_selection_x = found
            while config.ui_selection_y > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y -= 1
            while config.ui_selection_y < len(ui_selection_options[config.ui_selection_x]) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y += 1
    return valid_input

def ui_selection_x_next():
    valid_input = False
    if config.ui_selection_x < len(ui_selection_options)-1:
        found = None
        for num in range(config.ui_selection_x + 1, len(ui_selection_options)):
            if len(utils.list_none_filter(ui_selection_options[num])) > 0:
                found = num
                break
        if found is not None:
            valid_input = True
            audio.sound_play('ui_sel', 'ui')
            config.ui_selection_x = found
            while config.ui_selection_y > 0 and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y -= 1
            while config.ui_selection_y < len(ui_selection_options[config.ui_selection_x]) and ui_selection_options[config.ui_selection_x][config.ui_selection_y] is None:
                config.ui_selection_y += 1
    return valid_input

def ui_selection_up():
    return ui_selection_y_prev()

def ui_selection_down():
    return ui_selection_y_next()

def ui_selection_left():
    return ui_selection_x_prev()

def ui_selection_right():
    return ui_selection_x_next()

def ui_scroll_minus(scroll_name):
    if config.ui_scroll[scroll_name]['pos'] > 0:
        config.ui_scroll[scroll_name]['pos'] -= 1
        if scroll_name == 'center':
            config.trigger_animation('ui_sel_1', animation_type = config.UI_TAGS['scroll'], animation_data = config.UI_TAGS['data_center_up'])
        elif scroll_name == 'log' and config.settings['visual_scroll_log_arrows']:
            config.trigger_animation('ui_sel_1', animation_type = config.UI_TAGS['scroll'], animation_data = config.UI_TAGS['data_log_down'])
        return True
    return False

def ui_scroll_plus(scroll_name):
    if config.ui_scroll[scroll_name]['pos'] < config.ui_scroll[scroll_name]['max']:
        config.ui_scroll[scroll_name]['pos'] += 1
        if scroll_name == 'center':
            config.trigger_animation('ui_sel_1', animation_type = config.UI_TAGS['scroll'], animation_data = config.UI_TAGS['data_center_down'])
        elif scroll_name == 'log' and config.settings['visual_scroll_log_arrows']:
            config.trigger_animation('ui_sel_1', animation_type = config.UI_TAGS['scroll'], animation_data = config.UI_TAGS['data_log_up'])
        return True
    return False

def ui_selection_up_or_scroll_plus(scroll_name):
    if config.ui_selection_y == 0:
        return ui_scroll_plus(scroll_name)
    else:
        return ui_selection_up()

def ui_selection_down_or_scroll_minus(scroll_name):
    if config.ui_selection_y == 0 and config.ui_scroll[scroll_name]['pos'] > 0:
        return ui_scroll_minus(scroll_name)
    else:
        return ui_selection_down()

def ui_selection_left_or_scroll(scroll_name):
    if config.ui_scroll[scroll_name]['pos'] == 0:
        return ui_selection_left()
    return False

def ui_selection_right_or_scroll(scroll_name):
    if config.ui_scroll[scroll_name]['pos'] == 0:
        return ui_selection_right()
    return False

def ui_selection_option_change_scale_plus(current_value, settings):
    max_value = settings[1]
    inc_value = settings[2]
    current_value += inc_value
    return min(current_value, max_value)

def ui_selection_option_change_scale_minus(current_value, settings):
    min_value = settings[0]
    inc_value = settings[2]
    current_value -= inc_value
    return max(current_value, min_value)

def ui_selection_option_change_scale(current_value, settings, plus_value = True):
    if plus_value is True:
        return ui_selection_option_change_scale_plus(current_value, settings)
    else:
        return ui_selection_option_change_scale_minus(current_value, settings)

def ui_selection_option_change_multi_prev(current_value, target_list):
    index_value = target_list.index(current_value)
    if index_value > 0:
        current_value = target_list[index_value - 1]
    return current_value

def ui_selection_option_change_multi_next(current_value, target_list):
    max_value = len(target_list) - 1
    index_value = target_list.index(current_value)
    if index_value < max_value:
        current_value = target_list[index_value + 1]
    return current_value

def ui_selection_option_change_multi(current_value, target_list, next_value = True):
    if next_value is True:
        return ui_selection_option_change_multi_next(current_value, target_list)
    else:
        return ui_selection_option_change_multi_prev(current_value, target_list)

def ui_selection_option_change_toggle(current_value):
    return not current_value

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

def update_active_npcs():
    global active_npcs
    active_npcs = {}
    for npc_id, npc in npcs.items():
        if npc['disabled'] == False and npc['room'] == active_room:
            active_npcs[npc_id] = npc

def format_npc_log_text(text, npc, colored = True):
    text = text.replace('<pos>', utils.format_position_text_room(npc['position'], rooms[active_room]['noun']))
    text = text.replace('<name>', utils.format_npc_name(npc, colored = colored))
    text = text.replace('<name_default>', utils.format_npc_name(npc, colored = colored, force_default = True))
    text = text.replace('<name_secret>', utils.format_npc_name(npc, colored = colored, force_secret = True))
    text = text.replace('<pronoun_sub>', utils.format_npc_pronoun(npc, 'subject'))
    text = text.replace('<pronoun_obj>', utils.format_npc_pronoun(npc, 'object'))
    text = text.replace('<pronoun_pos>', utils.format_npc_pronoun(npc, 'possesive'))
    text = text.replace('<pronoun_ref>', utils.format_npc_pronoun(npc, 'reflexive'))
    text = utils.capitalize(text)
    return text

def npc_behaviour():
    for npc_id, npc in active_npcs.items():
        if npc['disabled'] is False and npc['room'] == active_room and config.player['health_points'] > 0:
            if npc['hostile'] is True:
                if npc['ranged'] and npc['position'] != current_position:
                    npc_action_attack_player(npc, ranged = True)
                    config.add_to_stats('times_npc_attack', 1)
                else:
                    if npc['position'] == current_position:
                        npc_action_attack_player(npc)
                        config.add_to_stats('times_npc_attack_ranged', 1)
                    else:
                        if npc_check_move(npc):
                            npc_move_to_player(npc)
            elif npc['always_moving'] is True:
                if npc_check_move(npc):
                    npc_move_random(npc)

def npc_set_hostile(npc_id, hostile = True):
    npc = npcs[npc_id]
    npc['hostile'] = hostile

def npc_set_friendly(npc_id):
    npc_set_hostile(npc_id, False)

def npc_unlock_secret_name(npc_id):
    npc = npcs[npc_id]
    npc['secret_name_unlocked'] = True

def npc_check_move(npc):
    move = False
    if not npc['immobile']:
        move = utils.random_chance(npc['speed'])
    return move

def npc_action_move(npc, link):
    npc_change_position(link, npc)

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

def npc_action_attack_player(npc, ranged = False):
    attack_text = config.NPC_ATTACK_TEXT
    miss_text = config.PLAYER_DODGE_TEXT
    npc_miss_text = npc['npc_attack_miss_text']
    killed_text = '<name> murdered you.'
    attack_skill = npc['attack_skill']
    npc_attack_text = npc['attack_text']
    npc_game_over_text = npc['game_over_text']
    damage = npc['damage']
    on_attack = npc['on_attack']
    if ranged:
        attack_text = '<name> attacks you from a distance.'
        npc_miss_text = npc['npc_attack_miss_text_ranged']
        game_over_text = '<name> killed you from a distance.'
        attack_skill = npc['attack_skill_ranged']
        npc_attack_text = npc['attack_text_ranged']
        if npc['game_over_text_ranged']:
            npc_game_over_text = npc['game_over_text_ranged']
        damage = npc['damage_ranged']
        on_attack = npc['on_attack_ranged']
    hit = utils.random_chance(attack_skill)
    if npc_game_over_text:
        game_over_text = random.choice(npc_game_over_text)
    if npc_miss_text and random.choice([False, True]):
        miss_text = npc_miss_text
    attack_text = random.choice(npc_attack_text)
    miss_text = random.choice(miss_text)
    attack_text = format_npc_log_text(attack_text, npc)
    game_over_text = format_npc_log_text(game_over_text, npc)
    add_log(attack_text)
    if hit:
        damage_num = utils.randomize_damage(damage)
        defence_num = utils.randomize_damage(check_player_defence())
        if defence_num >= damage_num:
            add_log('Your equipment protect you from the attack and you sustain no damage.')
        else:
            player_take_damage(damage_num, 'the attack', game_over_text, defence_num = defence_num)
            if config.player['health_points'] > 0 and on_attack:
                for action in on_attack:
                  execute_action(action)
    else:
        config.add_to_stats('times_npc_missed', 1)
        add_log(miss_text)

def npc_take_damage(dmg, dmg_source, npc, killed_text):
    if dmg > 0 and npc['health_points'] > 0:
        old_hp = npc['health_points']
        new_hp = max(0, old_hp - dmg)
        diff = old_hp - new_hp
        config.add_to_stats('damage_dealt', diff)
        dmg_num_txt = 'damage'
        if diff < 5:
            dmg_num_txt = 'minor damage'
        elif diff > 40:
            dmg_num_txt = 'a colossal amount of damage'
        elif diff > 20:
            dmg_num_txt = 'major damage'
        damage_text = 'takes ' + utils.format_log_damage(dmg_num_txt)
        if config.flags['show_battle_num']:
            s = ''
            if dmg != 1:
                s = 's'
            damage_text = 'loses ' + utils.format_log_damage(str(diff) + ' health point' + s)
        add_log(format_npc_log_text('<name> ' + damage_text + ' from ' + dmg_source +'.', npc))
        npc['health_points'] = new_hp
        if new_hp <= 0:
            npc['disabled'] = True
            config.add_to_stats('npcs_killed', 1)
            add_log(format_npc_log_text('<name> dies from ' + dmg_source + '.', npc))
            if killed_text:
                add_log(format_npc_log_text(killed_text, npc))
                popup_lines = []
                popup_lines.append(format_npc_log_text(killed_text, npc))
                set_popup_content(popup_lines)
        update_npc_health_status(npc)

def player_take_damage(dmg, dmg_source, game_over_text = None, defence_num = 0):
    original_dmg = dmg
    dmg -= defence_num
    if dmg > 0 and config.player['health_points'] > 0:
        old_hp = config.player['health_points']
        new_hp = max(0, old_hp - dmg)
        diff = old_hp - new_hp
        config.add_to_stats('damage_received', diff)
        dmg_num_txt = 'damage'
        if diff < 5:
            dmg_num_txt = 'minor damage'
        elif diff > 40:
            dmg_num_txt = 'a colossal amount of damage'
        elif diff > 20:
            dmg_num_txt = 'major damage'
        damage_text = 'take ' + utils.format_log_damage(dmg_num_txt)
        if config.flags['show_battle_num']:
            s = ''
            if dmg != 1:
                s = 's'
            damage_text = 'lose ' + utils.format_log_damage(str(diff) + ' health point' + s)
        if defence_num > 0:
            config.add_to_stats('damage_defended', defence_num)
            defence_precent = int((defence_num / original_dmg) * 100)
            defence_text = 'a little bit'
            if defence_precent > 20:
                defence_text = 'some'
            elif defence_precent > 40:
                defence_text = 'a good amount'
            elif defence_precent > 60:
                defence_text = 'a very good amount'
            elif defence_precent > 80:
                defence_text = 'almost all'
            if config.flags['show_battle_num']:
                defence_text = str(defence_precent) + '%'
            add_log('Your equipment protects you from ' + defence_text + ' of the damage caused by ' + dmg_source + '.')
        add_log('You ' + damage_text + ' from ' + dmg_source +'.')
        config.player['health_points'] = new_hp
        if new_hp <= 0:
            add_log('You die from ' + dmg_source + '.')
            if game_over_text:
                config.game['game_over_text'] = game_over_text
        update_player_health_status()

def check_player_defence():
    defence_num = 0
    if config.equipped_armor['upper_body'] is not None:
        defence_num += items[config.equipped_armor['upper_body']]['defence']
    if config.equipped_armor['lower_body'] is not None:
        defence_num += items[config.equipped_armor['lower_body']]['defence']
    if config.equipped_armor['head'] is not None:
        defence_num += items[config.equipped_armor['head']]['defence']
    if config.equipped_armor['hands'] is not None:
        defence_num += items[config.equipped_armor['hands']]['defence']
    if config.equipped_armor['feet'] is not None:
        defence_num += items[config.equipped_armor['feet']]['defence']
    if config.equipped_armor['shield'] is not None:
        defence_num += items[config.equipped_armor['shield']]['defence']
    return defence_num

def heal_player(link):
    heal = link['health_points']
    heal_source = link['source']
    original_heal = heal
    old_hp = config.player['health_points']
    new_hp = min(config.player['health_points_max'], old_hp + heal)
    diff = new_hp - old_hp
    config.add_to_stats('health_healed', diff)
    heal_num_txt = 'health'
    if diff == 0:
        heal_num_txt = 'no health'
    elif diff < 5:
        heal_num_txt = 'minor health'
    elif diff > 40:
        heal_num_txt = 'a colossal amount of health'
    elif diff > 20:
        heal_num_txt = 'major health'
    heal_text = utils.format_log_heal(heal_num_txt)
    if config.flags['show_battle_num']:
        s = ''
        if heal != 1:
            s = 's'
        heal_text = utils.format_log_heal(str(diff) + ' health point' + s)
    add_log('You regain ' + heal_text + ' from ' + heal_source +'.')
    config.player['health_points'] = new_hp

def dmg_from_statuses():
    for status in statuses.values():
        if status['active'] and status['damage']:
            player_take_damage(utils.randomize_damage(status['damage']), status['damage_name'], utils.format_color_tags(status['game_over_text']))

def dmg_from_wounds():
    if config.player['health_stage'] == 6 or config.player['health_stage'] == 7:
        if utils.random_chance(config.player['health_stage'] - 4):
            player_take_damage(utils.randomize_damage(1), 'your wounds', 'You died from your wounds.')

def update_npc_health_status(npc):
    health_percent = int((npc['health_points'] / npc['health_points_max']) * 100)
    health_stage = 0
    if health_percent <= 0:
        health_stage = 4
    elif health_percent < 25:
        health_stage = 3
    elif health_percent < 50:
        health_stage = 2
    elif health_percent < 75:
        health_stage = 1
    if npc['health_stage'] != health_stage:
        if health_stage == 0:
            npc['health_status'] = None
        else:
            health_status = random.choice(config.NPC_HEALTH_STAGES[health_stage])
            health_status = utils.format_npc_health(health_stage, health_status)
            if health_stage > npc['health_stage'] and npc['health_points'] > 0:
                add_log(format_npc_log_text(health_status, npc))
            npc['health_status'] = health_status
        npc['health_stage'] = health_stage
    if config.flags['show_npc_hp']:
        s = ''
        if npc['health_points'] != 1:
            s = 's'
            add_log(format_npc_log_text('<name> has ' + npc['health_points'] + ' (' + health_percent + '%) health point' + s + ' left.', npc))

def update_player_health_status():
    health_percent = int((config.player['health_points'] / config.player['health_points_max']) * 100)
    health_stage = 0
    if health_percent <= 0:
        health_stage = 8
    elif health_percent < 10:
        health_stage = 7
    elif health_percent < 26:
        health_stage = 6
    elif health_percent < 42:
        health_stage = 5
    elif health_percent < 58:
        health_stage = 4
    elif health_percent < 74:
        health_stage = 3
    elif health_percent < 90:
        health_stage = 2
    elif health_percent < 100:
        health_stage = 1
    if config.player['health_stage'] != health_stage:
        if health_stage == 0:
            config.player['health_status'] = None
        else:
            health_status = random.choice(config.PLAYER_HEALTH_STAGES[health_stage])
            health_status = utils.format_player_health(health_stage, health_status)
            if health_stage > config.player['health_stage'] and config.player['health_points'] > 0:
                add_log(health_status)
            config.player['health_status'] = health_status
        config.player['health_stage'] = health_stage

def player_death():
    config.game['game_over'] = True
    popup_lines = []
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
    popup_lines.append('<vertical_spacer>')
    popup_lines.append('« YOU HAVE REACHED THE END OF YOUR JOURNEY »')
    popup_lines.append('<vertical_spacer>')
    if config.game['game_over_text']:
        popup_lines.append(config.game['game_over_text'])
    popup_lines.append('You played for ' + str(config.game['turn']) + ' turns.')
    if config.stats['npcs_killed'] > 0:
        popup_lines.append('You commited ' + str(config.stats['npcs_killed']) + ' murders.')
    '''
    popup_lines.append('')
    popup_lines.append('FINAL LOG ENTRIES:')
    final_log_entries = [entry for entry in log_list if entry[0] == config.game['turn'] - 1]
    for entry in final_log_entries:
        popup_lines.append('"' + entry[1] + '"')
    '''
    popup_options = [[
        SelectionOption('restart_game', 'Return to title screen'),
        SelectionOption('quit_game', 'Quit game')
    ]]
    set_popup_content(popup_lines, popup_options, centered = True, play_animation = False)