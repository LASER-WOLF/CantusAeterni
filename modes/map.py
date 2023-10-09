# MAP TILES
MAP_TILES = {
    'empty_top': "ƒƒƒ",
    'empty_low': "ƒƒƒ",
    'visited_top': config.COLOR_MAP_INACTIVE + "┌─┐" + config.COLOR_DEFAULT,
    'visited_low': config.COLOR_MAP_INACTIVE + "└─┘" + config.COLOR_DEFAULT,
    'selected_top': config.COLOR_MAP_SELECTED + "╔═╗" + config.COLOR_DEFAULT,
    'selected_low': config.COLOR_MAP_SELECTED + "╚═╝" + config.COLOR_DEFAULT,
    'active_top': config.COLOR_MAP_SELECTED + "┌|┐" + config.COLOR_DEFAULT,
    'active_low': config.COLOR_MAP_SELECTED + "└─┘" + config.COLOR_DEFAULT,
    'active_selected_top': config.COLOR_MAP_SELECTED + "╔|╗" + config.COLOR_DEFAULT,
    'active_selected_low': config.COLOR_MAP_SELECTED + "╚═╝" + config.COLOR_DEFAULT,
}

def input_map(key, selected_option = None):
    if(key == "up"):
        ui_selection_y_prev()
    elif(key == "down"):
        ui_selection_y_next()
    elif(key == "left"):
        ui_selection_x_prev()
    elif(key == "right"):
        ui_selection_x_next()
    elif(key == "escape"):
        audio.sound_ui("ui_back")
        change_mode(previous_mode)

def center_window_map():
    lines = []
    lines.extend(map_window_content())
    return WindowContent(WINDOW_CENTER, lines, None, FILL_PATTERNS['dots1'], None, True, True)

def lower_window_map():
    lines = [press_to_go_back_text()]
    return WindowContent(WINDOW_LOWER, lines, min_height = 0)

def map_portal_check(portal_check_dict = {'selected_room': '1', 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}}):
    selected_room_root = portal_check_dict['selected_room']
    current_coords_root = portal_check_dict['current_coords']
    portal_check_dict['checked_rooms'][selected_room_root] = portal_check_dict['current_coords']
    for portal in rooms[selected_room_root]['portal']:
        if portal['disabled'] == False:
            next_room = portals[portal['link']]['link2']
            next_dir = portals[portal['link']]['dir']
            next_portal_pos = portals[portal['link']]['pos2']
            if next_room == selected_room_root:
                next_room = portals[portal['link']]['link1']
                next_dir = DIRECTION_REVERSE[next_dir]
                next_portal_pos = portals[portal['link']]['pos1']
            if not next_room in portal_check_dict['checked_rooms'] and rooms[next_room]['visited'][next_portal_pos]:
                next_coords = {'x': current_coords_root['x'] + DIRECTION_TO_COORD[next_dir]['x'], 'y': current_coords_root['y'] + DIRECTION_TO_COORD[next_dir]['y']}
                portal_check_dict['selected_room'] = next_room
                portal_check_dict['current_coords'] = next_coords
                portal_check_dict = map_portal_check(portal_check_dict)
    return portal_check_dict

def selection_options_map(known_rooms, max_x, max_y):
    global ui_selection_options
    global ui_selection_y
    global ui_selection_x
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
                if found_room == active_room and not ui_selection_options:
                    ui_selection_x = x
                    ui_selection_y = y
            else:
                result[x].append(None)
    ui_selection_options = result

def make_map(known_rooms, max_x, max_y):
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
                selected_room = ui_selection_options[ui_selection_x][ui_selection_y]
                if found_room == active_room:
                    if found_room == selected_room:
                        map_line_top += MAP_TILES['active_selected_top']
                        map_line_low += MAP_TILES['active_selected_low']
                    else:
                        map_line_top += MAP_TILES['active_top']
                        map_line_low += MAP_TILES['active_low']
                elif found_room == selected_room:
                    map_line_top += MAP_TILES['selected_top']
                    map_line_low += MAP_TILES['selected_low']
                else:
                    map_line_top += MAP_TILES['visited_top']
                    map_line_low += MAP_TILES['visited_low']
            else:
                map_line_top += MAP_TILES['empty_top']
                map_line_low += MAP_TILES['empty_low']
        result.append(map_line_top)
        result.append(map_line_low)
    return result

def map_window_content():
    known_rooms = map_portal_check({'selected_room': active_room, 'current_coords': {'x': 0, 'y': 0}, 'checked_rooms': {}})['checked_rooms']
    #known_rooms_sorted = sorted(known_rooms.items(), key=lambda room: (room[1]['y'], room[1]['x']))
    zero_x = min(coord['x'] for coord in known_rooms.values())
    zero_y = min(coord['y'] for coord in known_rooms.values())
    for room in known_rooms.values():
        room['x'] += abs(zero_x)
        room['y'] += abs(zero_y)
    max_x = max(coord['x'] for coord in known_rooms.values())+1
    max_y = max(coord['y'] for coord in known_rooms.values())+1
    selection_options_map(known_rooms, max_x, max_y)
    result = make_map(known_rooms, max_x, max_y)
    if config.settings['debug_mode']:
        result.append("DEBUG: " + str(ui_selection_options[ui_selection_x][ui_selection_y]))
    return result