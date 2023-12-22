# BUILT-IN
import random

# PROJECT
import audio
import config
import system
import utils
import windows

# SET VARS
room_id = None
room = None

def set_room():
    global room_id
    global room
    if room_id != system.active_room:
        room_id = system.active_room
        room = system.rooms[room_id]
        config.add_debug_log('Loading room -> ' + str(room_id))
    system.update_active_npcs()

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
            windows.popup(system.popup_content['lines'], options = system.ui_selection_options, title = system.popup_content['title'], image = system.popup_content['image'], centered = system.popup_content['centered'], border_color = system.popup_content['border_color'], fg_color = system.popup_content['fg_color'], bg_color = system.popup_content['bg_color'])
        )
    return layers

def ui_action_restart_game():
    config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_back')
    system.restart_game()

def input_popup(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if key in config.controls['scroll_center_up'] or (key in config.controls['up'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_minus('center')
    elif key in config.controls['scroll_center_down'] or (key in config.controls['down'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_plus('center')
    elif selected_option is None:
        if key in config.controls['action']:
            valid_input = True
            config.trigger_animation(config.ANIMATION_UI_CONTINUE_DEFAULT, 'ui_confirm', 'ui', animation_data = config.UI_TAGS['continue'])
            system.unset_popup_content()
    else:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up()
        elif key in config.controls['down']:
            valid_input = system.ui_selection_down()
        elif not config.game['game_over'] and (key in config.controls['back'] or (key in config.controls['action'] and selected_option.name == 'examine-cancel')):
            valid_input = True
            if key in config.controls['action'] and selected_option.name == 'examine-cancel':
                config.trigger_animation(config.ANIMATION_UI_DEFAULT)
            audio.sound_play('ui_back', 'ui')
            system.unset_popup_content()
        elif key in config.controls['action']:
            valid_input = True
            if selected_option.name == "examine-confirm":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                examine_confirm(selected_option.link)
                system.unset_popup_content(play_animation = False)
            elif selected_option.name == "restart_game":
                ui_action_restart_game()
            elif selected_option.name == "quit_game":
                system.quit_game()
            elif selected_option.name == "dialogue_response":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                dialogue_response(selected_option.link)
    return valid_input

def input_main(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if key in config.controls['scroll_center_up'] or (key in config.controls['up'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_minus('center')
    elif key in config.controls['scroll_center_down'] or (key in config.controls['down'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_plus('center')
    elif key in config.controls['scroll_log_up']:
        valid_input = system.ui_scroll_plus('log')
    elif key in config.controls['scroll_log_down']:
        valid_input = system.ui_scroll_minus('log')
    elif selected_option is not None:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up_or_scroll_plus('log')
        elif key in config.controls['down']:
            valid_input = system.ui_selection_down_or_scroll_minus('log')
        elif key in config.controls['left']:
            valid_input = system.ui_selection_left_or_scroll('log', True)
        elif key in config.controls['right']:
            valid_input = system.ui_selection_right_or_scroll('log', True)
        elif key in config.controls['back']:
            if config.ui_scroll['log']['pos'] > 0:
                valid_input = True
                config.ui_scroll['log']['pos'] = 0
            elif system.ui_pre_quit_prompt:
                valid_input = True
                audio.sound_play('ui_back', 'ui')
                system.pre_quit_prompt()
                system.ui_selection_retrieve()
            elif system.ui_restart_prompt:
                valid_input = True
                audio.sound_play('ui_back', 'ui')
                system.restart_game_prompt()
                system.ui_selection_retrieve()
            elif system.ui_quit_prompt:
                valid_input = True
                audio.sound_play('ui_back', 'ui')
                system.quit_game_prompt()
                system.ui_selection_retrieve()
        elif key in config.controls['action'] and config.ui_scroll['log']['pos'] == 0:
            valid_input = True
            if selected_option.name == "pre_quit_prompt":
                config.trigger_animation('ui_sel_5')
                if system.ui_pre_quit_prompt:
                    audio.sound_play('ui_back', 'ui')
                    system.ui_selection_retrieve()
                else:
                    audio.sound_play('ui_confirm', 'ui')
                    system.ui_selection_store()
                    system.ui_selection_none()
                system.pre_quit_prompt()
            elif selected_option.name == "restart_game_prompt":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT)
                if system.ui_pre_quit_prompt:
                    system.pre_quit_prompt()
                    audio.sound_play('ui_confirm', 'ui')
                    system.ui_selection_none()
                else:
                    audio.sound_play('ui_back', 'ui')
                    system.ui_selection_retrieve()
                system.restart_game_prompt()
            elif selected_option.name == "quit_game_prompt":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT)
                if system.ui_pre_quit_prompt:
                    system.pre_quit_prompt()
                    audio.sound_play('ui_confirm', 'ui')
                    system.ui_selection_none()
                else:
                    audio.sound_play('ui_back', 'ui')
                    system.ui_selection_retrieve()
                system.quit_game_prompt()
            elif selected_option.name == "restart_game":
                ui_action_restart_game()
            elif selected_option.name == "quit_game":
                system.quit_game()
            elif selected_option.name == "help":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                system.change_mode(config.MODE_HELP)
            elif selected_option.name == "settings":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                system.change_mode(config.MODE_SETTINGS)
            elif selected_option.name == "debug":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                system.change_mode(config.MODE_DEBUG)
            elif selected_option.name == "map":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                system.change_mode(config.MODE_MAP)
            elif selected_option.name == "character":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                system.change_mode(config.MODE_CHARACTER)
            elif selected_option.name == "move":
                config.trigger_animation('ui_sel_1')
                action_move(selected_option.link)
            elif selected_option.name == "examine":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                examine(selected_option.link, selected_option.display_name)
            elif selected_option.name == "portal":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                action_portal(selected_option.link)
            elif selected_option.name == "attack":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                action_attack(selected_option.link[0], selected_option.link[1])
            elif selected_option.name == "attack_ranged":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                action_attack_ranged(selected_option.link[0], selected_option.link[1])
            elif selected_option.name == "dialogue_load":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                dialogue_load(selected_option.link[0], selected_option.link[1], selected_option.link[2])
            elif selected_option.name == "dialogue_fail":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                dialogue_fail(selected_option.link)
    return valid_input

def input(key, mod = None):
    if system.popup_content:
        return input_popup(key, mod)
    else:
        return input_main(key, mod)

def selection_options():
    result = []
    if system.ui_pre_quit_prompt:
        result.append([
        system.SelectionOption("restart_game_prompt", "Return to title screen"),
        system.SelectionOption("quit_game_prompt", "Quit game"),
        system.SelectionOption("pre_quit_prompt", "Cancel"),
        ])
    elif system.ui_quit_prompt:
        result.append([
        system.SelectionOption("quit_game", "Yes"),
        system.SelectionOption("quit_game_prompt", "No"),
        ])
    elif system.ui_restart_prompt:
        result.append([
        system.SelectionOption("restart_game", "Yes"),
        system.SelectionOption("restart_game_prompt", "No"),
        ])
    else:
        result.append(check_move_options())
        result.append(check_interact_options())
        result.append([
            system.SelectionOption("character", "Character"),
            system.SelectionOption("map", "Map"),
            system.SelectionOption("debug", "Debug screen"),
            system.SelectionOption("settings", "Settings"),
            system.SelectionOption("help", "Help"),
            system.SelectionOption("pre_quit_prompt", "Quit"),
        ])
    return result

def window_center():
    lines = []
    if config.player['health_status']:
        lines.append(config.player['health_status'])
    if config.player['health_points'] > 0:
        lines.extend(show_active_status())
        if lines:
            lines.append('')
        lines.extend(load_room())
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_log():
    return windows.Content(windows.WINDOW_LOG, windows.log_content(system.log_list))

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options, min_size_list = [50], append_empty = False)
    if system.ui_pre_quit_prompt:
        selection_options_display[0].insert(0, 'SELECT ACTION:')
    elif system.ui_quit_prompt or system.ui_restart_prompt:
        selection_options_display[0].insert(0, 'ARE YOU SURE?')
    else:
        if config.game_settings['show_minimap']:
            ui_blocks.append(windows.block_minimap(room, system.active_npcs, system.current_position, check_move_options(True)))
        option_titles = ["MOVE OR WAIT:", "INTERACT:", "OTHER:"]
        selection_options_display = windows.format_selection_options_display_add_titles(selection_options_display, option_titles)
        selection_options_display[2].insert(3, 'SYSTEM:')
        selection_options_display[2].insert(3, '')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks, r_align = 2))

def npc_block_player():
    block_action = False
    blocking_npc = None
    for npc in system.active_npcs.values():
        if npc['hostile'] is True and npc['dead'] is False:
            if npc['position'] == system.current_position:
                block_action = random.choice([False, True, True, True])
            #elif npc['ranged'] is True:
            #    block_action = random.choice([False, True])
            if block_action is True:
                blocking_npc = npc
                break
    return (block_action, blocking_npc)

def action_move(link):
    block_action, blocking_npc = npc_block_player()
    if block_action is False:
        system.player_change_position(link, logging = True)
        system.end_turn('move', link, 'success')
        config.add_to_stats('times_moved', 1)
    else:
        system.add_log(system.format_npc_log_text('<name> blocks you from moving.', blocking_npc))
        system.end_turn('move', link, 'blocked')

def action_portal(link):
    block_action, blocking_npc = npc_block_player()
    if block_action is False:
        enter_portal(link)
        system.end_turn('portal', link, 'success')
        config.add_to_stats('portals_entered', 1)
    else:
        system.add_log(system.format_npc_log_text('<name> blocks you from leaving.', blocking_npc))
        system.end_turn('portal', link, 'blocked')

def action_attack(npc_id, npc):
    system.end_turn('attack', npc_id, player_attack_npc(npc))
    config.add_to_stats('times_player_attack', 1)

def action_attack_ranged(npc_id, npc):
    system.end_turn('attack_ranged', npc_id, player_attack_npc(npc, ranged = True))
    config.add_to_stats('times_player_attack_ranged', 1)

def action_pickup(link):
    add_to_inventory(link)
    system.end_turn('pickup', link, 'success')

def check_move_options(minimap_mode = False):
    result = []
    result_minimap = {}
    wait_text = 'Wait at the current position'
    result.append(system.SelectionOption("move", wait_text, system.current_position))
    result_minimap[system.current_position] = 0
    num = 1
    for pos, text in utils.DIRECTION_ABR.items():
        pos_coord = utils.DIRECTION_TO_COORD[pos]
        current_pos_coord = utils.DIRECTION_TO_COORD[system.current_position]
        if system.current_position != pos and abs(pos_coord['x'] - current_pos_coord['x']) <= 1 and abs(pos_coord['y'] - current_pos_coord['y']) <= 1:
            position_text = 'Move to the ' + text
            if pos != "c":
                position_text += " side"
            position_text += " of the " + room['noun']
            result.append(system.SelectionOption("move", position_text, pos))
            result_minimap[pos] = num
            num += 1
    if minimap_mode:
        return result_minimap
    else:
        return result

def check_interact_options():
    result = []
    for npc_id, npc in system.active_npcs.items():
        if npc['hostile'] is True and npc['dead'] is False:
            if npc['position'] == system.current_position:
                dialogue_text = 'Try to start a conversation with ' + utils.format_npc_name(npc, False)
                if npc['dialogue_hostile'] is not None:
                    result.append(system.SelectionOption("dialogue_load", dialogue_text, (npc['dialogue_hostile'], dialogue_text, npc_id)))
                else:
                    result.append(system.SelectionOption("dialogue_fail", dialogue_text, npc_id))
                attack_text = 'Attack'
                if config.equipped_weapons['attack'] is None:
                    attack_text = 'Swing your fists at'
                elif system.items[config.equipped_weapons['attack']]['interact_text'] is not None:
                    attack_text = system.items[config.equipped_weapons['attack']]['interact_text']
                result.append(system.SelectionOption("attack", attack_text + ' ' + utils.format_npc_name(npc, False), (npc_id,  npc)))
            elif npc['position'] != system.current_position and config.equipped_weapons['attack_ranged'] is not None:
                attack_text = 'Shoot at'
                if system.items[config.equipped_weapons['attack_ranged']]['interact_text'] is not None:
                    attack_text = system.items[config.equipped_weapons['attack_ranged']]['interact_text']
                result.append(system.SelectionOption("attack_ranged", attack_text + ' ' + utils.format_npc_name(npc, False), (npc_id,  npc)))
        elif npc['position'] == system.current_position and npc['dialogue'] is not None and npc['dead'] is False:
            dialogue_text = 'Start a conversation with ' + utils.format_npc_name(npc, False)
            result.append(system.SelectionOption("dialogue_load", dialogue_text, (npc['dialogue'], dialogue_text, npc_id)))
    for entry in room['interactable']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("examine", entry['content'], entry['link']))
    for entry in room['portal']:
        if entry['position'] == system.current_position and not entry['disabled']:
            result.append(system.SelectionOption("portal", entry['content'], entry['link']))
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
    for npc in system.active_npcs.values():
        sense_text_list = []
        if not position_mode and npc['position'] != system.current_position:
            if npc['dead']:
                if sense == 'sight':
                    if npc['sight_far_dead'] is not None:
                        sense_text_list.append(npc['sight_far_dead'])
                    else:
                        sense_text_list.append('You see the dead body of <name> at the <pos>.')
                elif sense == 'smell' and npc['smell_far_dead'] is not None:
                    sense_text_list.append(npc['smell_far_dead'])
            else:
                if npc[sense + '_far_always'] is not None:
                    sense_text_list.append(npc[sense + '_far_always'])
                if npc['hostile'] is True and npc[sense + '_far_hostile'] is not None:
                    sense_text_list.append(npc[sense + '_far_hostile'])
                elif npc['hostile'] is False and npc[sense + '_far_friendly'] is not None:
                    sense_text_list.append(npc[sense + '_far_friendly'])
        elif position_mode and npc['position'] == system.current_position:
            if npc['dead']:
                if sense == 'sight':
                    if npc['sight_near_dead'] is not None:
                        sense_text_list.append(npc['sight_near_dead'])
                    else:
                        sense_text_list.append('You see the dead body of <name> in front of you.')
                elif sense == 'smell' and npc['smell_near_dead'] is not None:
                    sense_text_list.append(npc['smell_near_dead'])
            else:
                if npc[sense + '_near_always'] is not None:
                    sense_text_list.append(npc[sense + '_near_always'])
                if npc['hostile'] is True and npc[sense + '_near_hostile'] is not None:
                    sense_text_list.append(npc[sense + '_near_hostile'])
                if npc['hostile'] is False and npc[sense + '_near_friendly'] is not None:
                    sense_text_list.append(npc[sense + '_near_friendly'])
        for line in sense_text_list:
            result.append(sense_text + utils.format_color_tags(system.format_npc_log_text(line, npc)))
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

def examine(link, popup_title):
    interactable = system.interactables[link]
    popup_lines = []
    popup_options = None
    for line in interactable['examine_text']:
        popup_lines.append(utils.format_color_tags(line))
    if interactable['examine_options']:
        popup_options = [[]]
        for line in interactable['examine_options']:
            popup_options[0].append(system.SelectionOption("examine-" + line['type'], line['text'], link))
    system.set_popup_content(popup_lines, popup_options, title = popup_title)

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
    elif interactable['type'] == "portal":
        enable_event_portal(interactable['link'])
        system.add_log("You have discovered " + interactable['log_text'])
        action_portal(interactable['link'])
        system.ui_selection_popup_prev_none()
    for line in interactable['on_interact']:
        execute_action(line)

def player_attack_npc(npc, ranged = False):
    result = 'hit'
    attack_text = config.PLAYER_ATTACK_TEXT
    miss_text = config.NPC_DODGE_TEXT
    player_miss_text = npc['player_attack_miss_text']
    killed_text = 'You have murdered <name>.'
    skill_name = 'attack_unarmed'
    attack_skill = config.player['skill_level_attack_unarmed']
    damage = config.player['damage_unarmed']
    on_attack = None
    player_attack_text = None
    if config.equipped_weapons['attack'] is not None:
        skill_name = 'attack'
        attack_skill = config.player['skill_level_attack']
        damage = system.items[config.equipped_weapons['attack']]['damage']
        on_attack = system.items[config.equipped_weapons['attack']]['on_attack']
        player_attack_text = system.items[config.equipped_weapons['attack']]['attack_text']
    if ranged:
        skill_name = 'attack_ranged'
        attack_text = config.PLAYER_ATTACK_TEXT_RANGED
        killed_text = 'You have murdered <name> from a distance.'
        attack_skill = config.player['skill_level_attack_ranged']
        damage = system.items[config.equipped_weapons['attack_ranged']]['damage']
        on_attack = system.items[config.equipped_weapons['attack_ranged']]['on_attack']
        player_attack_text = system.items[config.equipped_weapons['attack_ranged']]['attack_text']
    hit = utils.random_chance(attack_skill)
    if player_miss_text and random.choice([False, True]):
        miss_text = player_miss_text
    if player_attack_text and random.choice([False, True]):
        attack_text = player_attack_text
    miss_text = random.choice(miss_text)
    miss_text = system.format_npc_log_text(miss_text, npc)
    attack_text = random.choice(attack_text)
    attack_text = system.format_npc_log_text(attack_text, npc)
    if not hit:
        hit = utils.random_chance_luck_combat(config.player['luck'])
        if hit:
            config.add_to_stats('times_player_attack_luck', 1)
    system.add_log(attack_text)
    if hit:
        system.npc_take_damage(utils.randomize_damage(damage), 'the attack', npc, killed_text)
        if skill_name != 'attack_unarmed':
            system.add_skill_experience(skill_name)
        if npc['health_points'] <= 0:
            result = 'kill'
        if npc['health_points'] > 0 and on_attack:
            for action in on_attack:
              system.execute_action(action)
    else:
        config.add_to_stats('times_player_missed', 1)
        system.add_log(miss_text)
        result = 'miss'
    return result

def dialogue_load(dialogue_id, popup_title = None, npc_id = None):
    dialogue_start = False
    if npc_id is not None:
        npc = system.npcs[npc_id]
        system.current_target = (npc_id, npc, npc['hostile'])
        dialogue_start = True
    else:
        npc = system.current_target[1]
    dialogue = system.dialogues[dialogue_id]
    popup_lines = []
    popup_options = [[]]
    if popup_title is None:
        popup_title = 'In conversation with ' + utils.format_npc_name(npc, False)
    if dialogue_start:
        system.add_dialogue_log('Started conversation with ' + utils.format_npc_name(npc))
    for line in dialogue['text']:
        dialogue_line = utils.format_color_tags(line)
        dialogue_line = system.format_npc_log_text(dialogue_line, npc, colored = False)
        popup_lines.append(dialogue_line)
        system.add_dialogue_log(dialogue_line)
    for response in dialogue['responses']:
        popup_options[0].append(system.SelectionOption('dialogue_response', response['text'], response))
    system.set_popup_content(popup_lines, popup_options, selection_memory = dialogue_start, title = popup_title)
    for action in dialogue['on_load']:
        handle_dialogue_action(action)

def dialogue_unload():
    system.unset_popup_content(play_animation = False)
    npc_id = system.current_target[0] 
    npc = system.current_target[1]
    hostile = system.current_target[2]
    system.add_log(system.format_npc_log_text('You have a conversation with <name>', npc))
    if hostile != npc['hostile']:
        hostile_text = 'hostile'
        if npc['hostile'] is False:
            hostile_text = 'friendly'
        hostile_log_text = system.format_npc_log_text('<name> becomes ' + hostile_text + '.', npc)
        system.add_log(hostile_log_text)
        system.add_dialogue_log(hostile_log_text)
    system.current_target = None
    system.end_turn('dialogue', npc_id, 'success')

def dialogue_fail(npc_id):
    npc = system.npcs[npc_id]
    system.add_log(system.format_npc_log_text('<name> is not interested in having a conversation.', npc))
    system.end_turn('dialogue', npc_id, 'failure')

def dialogue_response(link):
    system.add_dialogue_log('You responded: ' + link['text'])
    for action in link['on_response']:
        handle_dialogue_action(action)
    if link['next'] is None:
        dialogue_unload()
    else:
        dialogue_load(link['next'], link['text'])

def handle_dialogue_action(action):
    dialogue_action = action.copy()
    if dialogue_action['link'] is None:
        dialogue_action['link'] = system.current_target[0]
    system.execute_action(dialogue_action)