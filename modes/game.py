# PROJECT
import audio
import config
import system
import random
import utils
import windows

# SET VARS
room_id = None
room = None
npcs = None

def set_room():
    global room_id
    global room
    global npcs
    room_id = system.active_room
    room = system.rooms[room_id]
    npcs = {}
    for npc_id, npc in system.npcs.items():
        if npc['disabled'] == False and npc['room'] == room_id:
            npcs[npc_id] = npc

def run():
    set_room()
    system.run_queued_actions()
    layers = []
    # MAIN LAYER
    if system.main_content is None or system.popup_content is None:
        system.set_selection_options(selection_options())
        system.main_content = windows.main([
                windows.window_upper(),
                window_center(),
                window_log(),
                window_lower(),
            ])
    layers.append(
        system.main_content
    )
    # CHECK IF DEAD
    if config.game['game_over'] is False and config.player['health_points'] <= 0:
        system.player_death()
    # POPUP LAYER
    if system.popup_content is not None:
        system.set_selection_options(system.popup_content['options'])
        layers.append(
            windows.popup(system.popup_content['lines'], options = system.ui_selection_options, centered = system.popup_content['centered'])
        )

    return layers

def action_attack(link):
    player_attack_npc(link)
    system.end_turn('attack', npcs)

def action_attack_ranged(link):
    player_attack_npc(link, ranged = True)
    system.end_turn('attack_ranged', npcs)

def action_portal(link):
    block_action = False
    blocking_npc = None
    for npc in npcs.values():
        if npc['hostile'] is True:
            if npc['position'] == system.current_position:
                block_action = random.choice([False, True, True, True])
            elif npc['ranged'] is True:
                block_action = random.choice([False, True])
            if block_action is True:
                blocking_npc = npc
                break
    if block_action is False:
        enter_portal(link)
        system.end_turn('portal', npcs)
    else:
        system.add_log(system.format_npc_log_text('<name> blocks you from leaving.', blocking_npc))
        system.end_turn('portal_blocked', npcs)

def action_move(link):
    system.player_change_position(link, logging = True)
    system.end_turn('move', npcs)

def action_pickup(link):
    add_to_inventory(link)
    system.end_turn('pickup', npcs)

def input_popup(key, mod = None):
    selected_option = config.ui_selection_current
    if selected_option is None:
        if key == 'return' or key == 'mouse1':
            config.trigger_animation(config.ANIMATION_UI_SELECTION_FG)
            audio.ui_confirm()
            config.trigger_animation(config.ANIMATION_FADE)
            system.unset_popup_content()
    else:
        if(key == 'up'):
            system.ui_selection_y_prev()
        elif(key == 'down'):
            system.ui_selection_y_next()
        elif not config.game['game_over'] and (key == 'escape' or key == 'mouse3' or (key == 'return' and selected_option.name == 'examine-cancel')):
            if key == 'return' and selected_option.name == 'examine-cancel':
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
            audio.ui_back()
            config.trigger_animation(config.ANIMATION_FADE)
            system.unset_popup_content()
        elif key == 'return':
            if selected_option.name == "examine-confirm":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                examine_confirm(selected_option.link)
                system.unset_popup_content()
            elif selected_option.name == "restart_game":
                ui_action_restart_game()
            elif selected_option.name == "quit_game":
                system.quit_game()


def ui_action_restart_game():
    audio.ui_back()
    config.trigger_animation(config.ANIMATION_UI_SELECTION)
    system.restart_game()

def input_main(key, mod = None):
    selected_option = config.ui_selection_current
    if key == 'up' and (mod == 'shift' or mod == 'scroll_center'):
        config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST, config.UI_TAGS['scroll_center_up'])
        system.ui_scroll_center_up()
    elif key == 'down' and (mod == 'shift' or mod == 'scroll_center'):
        config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST, config.UI_TAGS['scroll_center_down'])
        system.ui_scroll_center_down()
    elif key == 'up' and mod == 'scroll_log':
        system.ui_log_scroll_up()
    elif key == 'down' and mod == 'scroll_log':
        system.ui_log_scroll_down()
    elif selected_option is not None:
        if(key == 'up'):
            system.ui_log_or_selection_up()
        elif(key == 'down'):
            system.ui_log_or_selection_down()
        elif(key == 'left'):
            system.ui_log_or_selection_left()
        elif(key == 'right'):
            system.ui_log_or_selection_right()
        elif(key == 'escape' or key == 'mouse3'):
            if config.ui_scroll_log > 0:
                config.ui_scroll_log = 0
            elif system.ui_pre_quit_prompt:
                audio.ui_back()
                system.pre_quit_prompt()
            elif system.ui_restart_prompt:
                audio.ui_back()
                system.restart_game_prompt()
            elif system.ui_quit_prompt:
                audio.ui_back()
                system.quit_game_prompt()
        elif(key == 'return' and config.ui_scroll_log == 0):
            if selected_option.name == "pre_quit_prompt":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                if system.ui_pre_quit_prompt:
                    audio.ui_back()
                else:
                    audio.ui_confirm()
                system.pre_quit_prompt()
            elif selected_option.name == "restart_game_prompt":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                if system.ui_pre_quit_prompt:
                    system.pre_quit_prompt()
                    audio.ui_confirm()
                else:
                    audio.ui_back()
                system.restart_game_prompt()
            elif selected_option.name == "quit_game_prompt":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                if system.ui_pre_quit_prompt:
                    system.pre_quit_prompt()
                    audio.ui_confirm()
                else:
                    audio.ui_back()
                system.quit_game_prompt()
            elif selected_option.name == "restart_game":
                ui_action_restart_game()
            elif selected_option.name == "quit_game":
                system.quit_game()
            elif selected_option.name == "help":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_HELP)
            elif selected_option.name == "settings":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_SETTINGS)
            elif selected_option.name == "debug":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_DEBUG)
            elif selected_option.name == "inventory":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_INVENTORY)
            elif selected_option.name == "map":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_MAP)
            elif selected_option.name == "move":
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORT)
                action_move(selected_option.link)
            elif selected_option.name == "examine":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                examine(selected_option.link)
            elif selected_option.name == "portal":
                config.trigger_animation(config.ANIMATION_UI_SELECTION_LONG)
                action_portal(selected_option.link)
            elif selected_option.name == "attack":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                action_attack(selected_option.link)
            elif selected_option.name == "attack_ranged":
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                action_attack_ranged(selected_option.link)

def input(key, mod = None):
    if system.popup_content:
        input_popup(key, mod)
    else:
        input_main(key, mod)

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
            system.SelectionOption("inventory", "INVENTORY"),
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
    if config.player['health_status']:
        lines.append(config.player['health_status'])
    if config.player['health_points'] > 0:
        lines.extend(show_active_status())
        if lines:
            lines.append("")
        lines.extend(load_room())
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options, min_size_list = [50])
    if system.ui_pre_quit_prompt:
        selection_options_display[0].insert(0, 'SELECT ACTION:')
    elif system.ui_quit_prompt or system.ui_restart_prompt:
        selection_options_display[0].insert(0, 'ARE YOU SURE?')
    else:
        if config.flags['hide_minimap'] is False:
            ui_blocks.append(windows.block_minimap(room, npcs, system.current_position, check_move_options(True)))
        option_titles = ["MOVE / WAIT:", "INTERACT:", "OTHER:", "SYSTEM:"]
        selection_options_display = windows.format_selection_options_display_add_titles(selection_options_display, option_titles)
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks, r_align = 2))

def window_log():
    lines = []
    lines.extend(windows.log_content(system.log_list))
    return windows.Content(windows.WINDOW_LOG, lines)

def check_move_options(minimap_mode = False):
    result = []
    result_minimap = {}
    result.append(system.SelectionOption("move", 'WAIT AT THE CURRENT POSITION', system.current_position))
    result_minimap[system.current_position] = 0
    num = 1
    for pos, text in utils.DIRECTION_ABR.items():
        pos_coord = utils.DIRECTION_TO_COORD[pos]
        current_pos_coord = utils.DIRECTION_TO_COORD[system.current_position]
        if system.current_position != pos and abs(pos_coord['x'] - current_pos_coord['x']) <= 1 and abs(pos_coord['y'] - current_pos_coord['y']) <= 1:
            text = 'MOVE TO THE ' + text
            position_text = text.upper()
            if pos != "c":
                position_text += " SIDE"
            position_text += " OF THE " + room['noun'].upper()
            result.append(system.SelectionOption("move", position_text, pos))
            result_minimap[pos] = num
            num += 1
    if minimap_mode:
        return result_minimap
    else:
        return result

def check_interact_options():
    result = []
    for npc in npcs.values():
        if npc['hostile'] is True:
            if npc['position'] == system.current_position:
                result.append(system.SelectionOption("attack", "(ATTACK) " + npc['name'].upper(), npc))
            elif npc['position'] != system.current_position and config.equipment['attack_ranged'] is not None:
                result.append(system.SelectionOption("attack_ranged", "(RANGED ATTACK) " + npc['name'].upper(), npc))
        elif npc['position'] == system.current_position:
            result.append(system.SelectionOption("talk", "(TALK) " + npc['name'].upper(), npc))
    for entry in room['interactable']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("examine", "(EXAMINE) " + entry['content'].upper(), entry['link']))
    for entry in room['portal']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("portal", "(TRAVEL) " + entry['content'].upper(), entry['link']))
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

def load_room():
    result = []
    if(config.settings['debug_mode']):
        result.append("DEBUG: You are in room " + str(room_id))
    result.append(room['location'])
    result.extend(sense_sight())
    result.extend(sense_sound())
    result.extend(sense_smell())
    result.append("")
    result.append("You are positioned at the " + utils.format_position_text_room(system.current_position, room['noun']) + '.')
    result.extend(sense_sight(True))
    result.extend(sense_sound(True))
    result.extend(sense_smell(True))
    return result

def show_active_status():
    result = []
    for status in system.statuses.values():
        if (status['active']):
            result.append(utils.format_color_tags(status['text']))
    return result

def sense_scan(sense, sense_text, position_mode = False):
    result = []
    for line in room[sense]:
        if not line['disabled']:
            content = utils.format_color_tags(line['content'])
            if not position_mode and (line['position'] == "" or (line['position'][0] == "-" and line['position'][1:] != system.current_position)):
                result.append(sense_text + content)
            elif (position_mode and line['position'] == system.current_position):
                result.append(sense_text + content)
    for npc in npcs.values():
        sense_text_list = []
        if not position_mode and npc['position'] != system.current_position:
            sense_text_list.append(npc[sense + '_far_always'])
            if npc['hostile']:
                sense_text_list.append(npc[sense + '_far_hostile'])
            else:
                sense_text_list.append(npc[sense + '_far_friendly'])
        elif position_mode and npc['position'] == system.current_position:
            sense_text_list.append(npc[sense + '_near_always'])
            if npc['hostile']:
                sense_text_list.append(npc[sense + '_near_hostile'])
            else:
                sense_text_list.append(npc[sense + '_near_friendly'])
        for line in sense_text_list:
            if line:
                content = line.replace('<pos>', utils.format_position_text_room(npc['position'], room['noun']))
                content = content.replace('<name>', utils.format_npc(npc['name']))
                content = utils.format_color_tags(content)
                result.append(sense_text + content)
    return result

def sense_sight(position_mode = False):
    result = []
    sense_text = "You look around: "
    if position_mode:
        sense_text = "You inspect your immediate surroundings: "
    if not system.statuses['blind']['active']:
        result.extend(sense_scan("sight", sense_text, position_mode))
    if not result:
        result.append(sense_text + "You see nothing.")
    return result

def sense_sound(position_mode = False):
    result = []
    sense_text = "You focus on your sense of hearing: "
    if position_mode:
        sense_text = "You focus on the sounds in your immediate proximity: "
    if not system.statuses['deaf']['active']:
        result.extend(sense_scan("sound", sense_text, position_mode))
    if system.statuses['blind']['active'] and not result:
        result.append(sense_text + "You don't hear anything.")
    return result
    
def sense_smell(position_mode = False):
    result = []
    sense_text = "You focus on your sense of smell: "
    if position_mode:
        sense_text = "You focus on the smells in you immediate proximity: "
    if not system.statuses['anosmic']['active']:
        result.extend(sense_scan("smell", sense_text, position_mode))
    if system.statuses['blind']['active'] and not result:
        result.append(sense_text + "You don't smell anything.")
    return result

def enter_portal(link):
    portal = system.portals[link]
    target_room = None
    target_pos = None
    if portal['link1'] == room_id:
        target_room = portal['link2']
        target_pos = portal['pos2']
        system.add_log(portal['text1to2'])
    else:
        target_room = portal['link1']
        target_pos = portal['pos1']
        system.add_log(portal['text2to1'])
    system.enter_room(target_room)
    system.player_change_position(target_pos)
    for line in portal['on_interact']:
        system.execute_action(line)

def add_to_inventory(item):
    system.inventory_list.append(item)

def examine(link):
    interactable = system.interactables[link]
    popup_lines = []
    popup_options = None
    if interactable['examine_text']:
        for line in interactable['examine_text']:
            popup_lines.append(utils.format_color_tags(line))
        if interactable['examine_options']:
            popup_options = [[]]
            for line in interactable['examine_options']:
                popup_options[0].append(system.SelectionOption("examine-" + line['type'], line['text'], link))
    system.set_popup_content(popup_lines, popup_options)

def examine_confirm(link):
    interactable = system.interactables[link]
    disable_event_interactable(link)
    if interactable['enable']:
        enable_event_all(interactable['enable'])
    if interactable['disable']:
        disable_event_all(interactable['disable'])
    if interactable['type'] == "item":
        system.add_log("You pick up " + interactable['log_text'])
        action_pickup(interactable['link'])
    if interactable['type'] == "portal":
        enable_event_portal(interactable['link'])
        system.add_log("You have discovered " + interactable['log_text'])
        action_portal(interactable['link'])
        system.prev_selection_none()
    for line in interactable['on_interact']:
        execute_action(line)

def player_attack_npc(npc, ranged = False):
    attack_text = config.player_attack_text
    miss_text = config.npc_dodge_text
    player_miss_text = npc['player_attack_miss_text']
    killed_text = 'You have murdered <name>.'
    attack_skill = config.player['attack_skill']
    damage = config.player['damage_melee']
    on_attack = None
    player_attack_text = None
    if config.equipment['attack'] is not None:
        damage = system.items[config.equipment['attack']]['damage']
        on_attack = system.items[config.equipment['attack']]['on_attack']
        player_attack_text = system.items[config.equipment['attack']]['attack_text']
    if ranged:
        attack_text = config.player_attack_text_ranged
        killed_text = 'You have murdered <name> from a distance.'
        attack_skill = config.player['attack_skill_ranged']
        damage = system.items[config.equipment['attack_ranged']]['damage']
        on_attack = system.items[config.equipment['attack_ranged']]['on_attack']
        player_attack_text = system.items[config.equipment['attack_ranged']]['attack_text']
    hit = system.random_chance(attack_skill)
    if player_miss_text and random.choice([False, True]):
        miss_text = player_miss_text
    if player_attack_text and random.choice([False, True]):
        attack_text = player_attack_text
    miss_text = random.choice(miss_text)
    miss_text = system.format_npc_log_text(miss_text, npc)
    attack_text = random.choice(attack_text)
    attack_text = system.format_npc_log_text(attack_text, npc)
    system.add_log(attack_text)
    if hit:
        system.npc_take_damage(system.randomize_damage(damage), 'the attack', npc, killed_text)
        if npc['health_points'] > 0 and on_attack:
            for action in on_attack:
              system.execute_action(action)
    else:
        system.add_log(miss_text)