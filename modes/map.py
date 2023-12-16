# PROJECT
import audio
import config
import system
import utils
import windows

# SET CONSTANTS, MAP TILES
MAP_TILES = {
    'empty_top': "   ",
    'empty_low': "   ",
    'visited_top': utils.add_text_tag("┌─┐", config.TAG_COLOR_MAP_INACTIVE),
    'visited_low': utils.add_text_tag("└─┘", config.TAG_COLOR_MAP_INACTIVE),
    'selected_top': utils.add_text_tag("╔═╗", config.TAG_COLOR_MAP_SELECTED),
    'selected_low': utils.add_text_tag("╚═╝", config.TAG_COLOR_MAP_SELECTED),
    'active_top': utils.add_text_tag("┌↓┐", config.TAG_COLOR_MAP_SELECTED),
    'active_low': utils.add_text_tag("└─┘", config.TAG_COLOR_MAP_SELECTED),
    'active_selected_top': utils.add_text_tag("╔↓╗", config.TAG_COLOR_MAP_SELECTED),
    'active_selected_low': utils.add_text_tag("╚═╝", config.TAG_COLOR_MAP_SELECTED),
}

# SET VARS
known_rooms = None
max_x = 0
max_y = 0

def check_rooms():
    global known_rooms
    global max_x
    global max_y
    known_rooms = portal_check({'selected_room': system.active_room, 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}})['checked_rooms']
    zero_x = min(coord['x'] for coord in known_rooms.values())
    zero_y = min(coord['y'] for coord in known_rooms.values())
    for room in known_rooms.values():
        room['x'] += abs(zero_x)
        room['y'] += abs(zero_y)
    max_x = max(coord['x'] for coord in known_rooms.values())+1
    max_y = max(coord['y'] for coord in known_rooms.values())+1

def run():
    check_rooms()
    system.set_selection_options(selection_options())
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            windows.window_lower_back(),
        ])
    ]

def input(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up()
        elif key in config.controls['down']:
            valid_input = system.ui_selection_down()
        elif key in config.controls['left']:
            valid_input = system.ui_selection_left()
        elif key in config.controls['right']:
            valid_input = system.ui_selection_right()
        elif key in config.controls['back'] :
            valid_input = system.change_mode_previous()
    return valid_input

def selection_options():
    result = []
    for x in range(max_x):
        result.append([])
        for y in range(max_y):
            if {'x': x, 'y': y} in known_rooms.values():
                found_rooms = utils.dict_key_by_value(known_rooms, {'x': x, 'y': y})
                found_room = found_rooms[0]
                result[x].append(found_room)
                if len(found_rooms) > 1:
                    add_debug_log("Multiple rooms with same coordinates " + "(ID: " + str(found_rooms) + ")", True)
                if found_room == system.active_room and system.ui_selection_options is None:
                    config.ui_selection_x = x
                    config.ui_selection_y = y
            else:
                result[x].append(None)
    return result

def window_center():
    lines = []
    lines.extend(map_content())
    lines.append('')
    lines.append('')
    lines.append('')
    lines.append(system.rooms[system.ui_selection_options[config.ui_selection_x][config.ui_selection_y]]['noun'].upper())
    if config.settings['debug_mode']:
        lines.append("DEBUG: " + str(system.ui_selection_options[config.ui_selection_x][config.ui_selection_y]))
    #lines.extend(windows.block_minimap(system.rooms[config.ui_selection_current], system.current_position))
    return windows.Content(windows.WINDOW_CENTER, lines, None, windows.FILL_PATTERNS['dots1'],None, True, True)

def portal_check(portal_check_dict):
    selected_room_root = portal_check_dict['selected_room']
    current_coords_root = portal_check_dict['current_coords']
    portal_check_dict['checked_rooms'][selected_room_root] = portal_check_dict['current_coords']
    for portal in system.rooms[selected_room_root]['portal']:
        if portal['disabled'] == False:
            portal_link = system.portals[portal['link']]
            next_room = portal_link['link2']
            next_dir = portal_link['dir']
            next_portal_pos = portal_link['pos2']
            if next_room == selected_room_root:
                next_room = portal_link['link1']
                next_dir = utils.DIRECTION_REVERSE[next_dir]
                next_portal_pos = portal_link['pos1']
            if not next_room in portal_check_dict['checked_rooms'] and system.rooms[next_room]['visited'][next_portal_pos]:
                next_coords = {'x': current_coords_root['x'] + utils.DIRECTION_TO_COORD[next_dir]['x'], 'y': current_coords_root['y'] + utils.DIRECTION_TO_COORD[next_dir]['y']}
                portal_check_dict['selected_room'] = next_room
                portal_check_dict['current_coords'] = next_coords
                portal_check_dict = portal_check(portal_check_dict)
    return portal_check_dict

def map_content():
    result = []
    for y in range(max_y):
        map_line_top = ""
        map_line_low = ""
        for x in range(max_x):
            if x > 0:
                map_line_top += " "
                map_line_low += " "
            if {'x': x, 'y': y} in known_rooms.values():
                found_rooms = utils.dict_key_by_value(known_rooms, {'x': x, 'y': y})
                found_room = found_rooms[0]
                selected_room = system.ui_selection_options[config.ui_selection_x][config.ui_selection_y]
                if found_room == system.active_room:
                    if found_room == selected_room:
                        map_line_top += utils.add_ui_tag_sel_none(MAP_TILES['active_selected_top'], x, y)
                        map_line_low += utils.add_ui_tag_sel_none(MAP_TILES['active_selected_low'], x, y)
                    else:
                        map_line_top += utils.add_ui_tag_sel_none(MAP_TILES['active_top'], x, y)
                        map_line_low += utils.add_ui_tag_sel_none(MAP_TILES['active_low'], x, y)
                elif found_room == selected_room:
                    map_line_top += utils.add_ui_tag_sel_none(MAP_TILES['selected_top'], x, y)
                    map_line_low += utils.add_ui_tag_sel_none(MAP_TILES['selected_low'], x, y)
                else:
                    map_line_top += utils.add_ui_tag_sel_none(MAP_TILES['visited_top'], x, y)
                    map_line_low += utils.add_ui_tag_sel_none(MAP_TILES['visited_low'], x, y)
            else:
                map_line_top += MAP_TILES['empty_top']
                map_line_low += MAP_TILES['empty_low']
        result.append(map_line_top)
        result.append(map_line_low)
    return result