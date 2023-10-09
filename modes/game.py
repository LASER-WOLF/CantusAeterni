# PROJECT
import audio
import config
import system
import utils
import windows

# SET VARS
room = None

def run():
    global room
    room = system.rooms[system.active_room]
    system.set_selection_options(selection_options())
    system.run_queued_actions()
    return windows.combine([
        windows.window_upper(),
        window_center(),
        window_log(),
        window_lower(),
    ])

def input(key):
    selected_option = system.get_selected_option()
    if(key == 'up'):
        system.ui_log_or_selection_up()
    elif(key == 'down'):
        system.ui_log_or_selection_down()
    elif(key == 'left'):
        system.ui_log_or_selection_left()
    elif(key == 'right'):
        system.ui_log_or_selection_right()
    elif(key == 'return'):
        if selected_option.name == "pre_quit_prompt":
            audio.ui_confirm()
            system.pre_quit_prompt()
        elif selected_option.name == "restart_game_prompt":
            audio.ui_confirm()
            system.restart_game_prompt()
            if system.ui_pre_quit_prompt:
                system.pre_quit_prompt()
        elif selected_option.name == "quit_game_prompt":
            audio.ui_confirm()
            system.quit_game_prompt()
            if system.ui_pre_quit_prompt:
                system.pre_quit_prompt()
        elif selected_option.name == "restart_game":
            audio.ui_back()
            system.restart_game()
        elif selected_option.name == "quit_game":
            system.quit_game()
        elif selected_option.name == "help":
            audio.ui_confirm()
            system.change_mode(config.MODE_HELP)
        elif selected_option.name == "settings":
            audio.ui_confirm()
            system.change_mode(config.MODE_SETTINGS)
        elif selected_option.name == "debug":
            audio.ui_confirm()
            system.change_mode(config.MODE_DEBUG)
        elif selected_option.name == "map":
            audio.ui_confirm()
            system.change_mode(config.MODE_MAP)
        elif selected_option.name == "move":
            audio.ui_confirm()
            system.change_position(selected_option.link, True)
        elif selected_option.name == "examine":
            audio.ui_confirm()
            examine(selected_option.link)
        elif selected_option.name == "portal":
            audio.ui_confirm()
            enter_portal(selected_option.link)

def selection_options():
    result = []
    if system.ui_pre_quit_prompt:
        result.append([
        system.SelectionOption("restart_game_prompt", "RETURN TO TITLE SCREEN"),
        system.SelectionOption("quit_game_prompt", "QUIT GAME"),
        system.SelectionOption("pre_quit_prompt", "CANCEL"),
        ])
    elif system.ui_quit_prompt:
        result.append([
        system.SelectionOption("quit_game", "YES"),
        system.SelectionOption("quit_game_prompt", "NO"),
        ])
    elif system.ui_restart_prompt:
        result.append([
        system.SelectionOption("restart_game", "YES"),
        system.SelectionOption("restart_game_prompt", "NO"),
        ])
    else:
        result.append(check_move_options())
        result.append(check_interact_options())
        result.append([
            system.SelectionOption("map", "MAP"),
        ])
        result.append([
            system.SelectionOption("debug", "DEBUG SCREEN"),
            system.SelectionOption("settings", "SETTINGS"),
            system.SelectionOption("help", "HELP"),
            system.SelectionOption("pre_quit_prompt", "QUIT"),
        ])
    return result

def window_center():
    lines = []
    lines.extend(show_active_status())
    lines.append("")
    lines.extend(load_room(system.active_room))
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options)
    if system.ui_pre_quit_prompt:
        selection_options_display[0].insert(0, 'SELECT ACTION:')
    elif system.ui_quit_prompt or system.ui_restart_prompt:
        selection_options_display[0].insert(0, 'ARE YOU SURE?')
    else:
        if config.settings['enable_minimap']:
            ui_blocks.append(windows.block_minimap(room, system.current_position))
        option_titles = ["MOVE TO:", "INTERACT WITH:", "OTHER:", "SYSTEM:"]
        selection_options_display = windows.format_selection_options_display_add_titles(selection_options_display, option_titles)
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks))

def window_log():
    lines = []
    lines.extend(windows.log_content(system.log_list))
    return windows.Content(windows.WINDOW_LOG, lines)

def check_move_options():
    result = []
    for pos, text in utils.DIRECTION_ABR.items():
        if system.current_position == pos:
            text = 'WAIT AT ' + text
        position_text = text.upper()
        if pos != "c":
            position_text += " SIDE"
        position_text += " OF " + room['noun'].upper()
        result.append(system.SelectionOption("move", position_text, pos))
    return result

def check_interact_options():
    result = []
    for entry in room['interactable']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("examine", "(EXAMINE) " + entry['content'].upper(), entry['link']))
    for entry in room['portal']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("portal", "(EXIT) " + entry['content'].upper(), entry['link']))
    return result

def enable_event(link, category, disable = False):
    num = 0
    for room in system.rooms.values():
        for line in room[category]:
                if line['link'] == link:
                    line['disabled'] = disable
                    num += 1
    if num > 0:
        disable_text = "enabled"
        if disable:
            disable_text = "disabled"
        config.add_debug_log("Change event (" + str(num) + "): " + category + ":" + link + " -> " + disable_text)

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

def load_room(room_id):
    result = []
    if(config.settings['debug_mode']):
        result.append("DEBUG: You are in room " + str(room_id))
    result.append(room['location'])
    result.extend(sense_sight(room_id))
    result.extend(sense_sound(room_id))
    result.extend(sense_smell(room_id))
    result.append("")
    result.append("You are positioned at the " + windows.format_position_text(system.current_position) + " of the " + room['noun'] + ".")
    result.extend(sense_sight(room_id, True))
    result.extend(sense_sound(room_id, True))
    result.extend(sense_smell(room_id, True))
    return result

def show_active_status():
    result = []
    for status in system.statuses.values():
        if (status['active']):
            result.append(windows.format_status(status['text']))
    return result

def sense_scan(sense, sense_text, room_id, position_mode = False):
    result = []
    for line in room[sense]:
        if not line['disabled']:
            content = windows.format_color_tags(line['content'])
            if not position_mode and (line['position'] == "" or (line['position'][0] == "-" and line['position'][1:] != system.current_position)):
                result.append(sense_text + content)
            elif (position_mode and line['position'] == system.current_position):
                result.append(sense_text + content)
    return result

def sense_sight(room_id, position_mode = False):
    result = []
    sense_text = "You look around: "
    if position_mode:
        sense_text = "You inspect your immediate surroundings: "
    if not system.statuses['blind']['active']:
        result.extend(sense_scan("sight", sense_text, room_id, position_mode))
    if not result:
        result.append(sense_text + "You see nothing.")
    return result

def sense_sound(room_id, position_mode = False):
    result = []
    sense_text = "You focus on your sense of hearing: "
    if position_mode:
        sense_text = "You focus on the sounds in you immediate proximity: "
    if not system.statuses['deaf']['active']:
        result.extend(sense_scan("sound", sense_text, room_id, position_mode))
    if system.statuses['blind']['active'] and not result:
        result.append(sense_text + "You don't hear anything.")
    return result
    
def sense_smell(room_id, position_mode = False):
    result = []
    sense_text = "You focus on your sense of smell: "
    if position_mode:
        sense_text = "You focus on the smells in you immediate proximity: "
    if not system.statuses['anosmic']['active']:
        result.extend(sense_scan("smell", sense_text, room_id, position_mode))
    if system.statuses['blind']['active'] and not result:
        result.append(sense_text + "You don't smell anything.")
    return result
"""
def move_north():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['y'] > -1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']-1})[0], True)
        
def move_south():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['y'] < 1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']+1})[0], True)
        
def move_west():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['x'] > -1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']-1, 'y': pos['y']})[0], True)

def move_east():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['x'] < 1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']+1, 'y': pos['y']})[0], True)
"""

def examine(link):
    interactable = system.interactables[link]
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
        system.add_log("You have discovered: " + interactable['text'])
    for line in interactable['on_interact']:
        execute_action(line)

def enter_portal(link):
    portal = system.portals[link]
    target_room = None
    target_pos = None
    if portal['link1'] == system.active_room:
        target_room = portal['link2']
        target_pos = portal['pos2']
        system.add_log(portal['text1to2'])
    else:
        target_room = portal['link1']
        target_pos = portal['pos1']
        system.add_log(portal['text2to1'])
    system.enter_room(target_room)
    system.change_position(target_pos)
    for line in portal['on_interact']:
        system.execute_action(line)

def add_to_inventory(item):
    global inventory_list
    inventory_list.append(item)