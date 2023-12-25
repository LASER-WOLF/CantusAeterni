# BUILT-IN
import math
import os
import re
import webbrowser

# THIRD-PARTY
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# PROJECT
import audio
import config
import modes.character
import modes.cutscene
import modes.debug
import modes.game
import modes.help
import modes.main_menu
import modes.map
import modes.settings
import utils

# SET CONSTANTS
MAIN_TITLE = "Cantus Aeterni"
ICON = pygame.image.load(config.FOLDER_NAME_RESOURCES + '/' + config.FOLDER_NAME_IMAGES + '/icon.png')
TARGET_FRAMERATE = 30
COLOR_KEY = (255,0,255)
CHAR_FADE1 = '░'
CHAR_FADE2 = '▒'
CHAR_FADE3 = '▓'
CHAR_DOT = '.'

# SET VARS
screen = None
screen_width = None
screen_height = None
window_mode = None
font_name = None
font = None
font_underline = None
font_strikethrough = None
font_width = None
font_height = None
palette_name = None
offset_x = None
offset_y = None
joysticks = {}
surfaces = {
    'main': None,
    'popup': None,
    'animation': None,
    'ui_animation': None,
}
pre_rendered_surfaces = {
}

def debug_print(message):
    timestamp = pygame.time.get_ticks()
    if config.settings['debug_print']:
        print(f'{timestamp:010d} | {message}')

def initialize():
    debug_print('Main initialization')
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # PYGAME SETUP
    pygame.init()
    display_info = pygame.display.Info()
    config.screen_width_full = display_info.current_w
    config.screen_height_full = display_info.current_h
    setup_screen()
    setup_font()
    setup_palette()
    joystick_init()
    config.trigger_animation('boot', 'boot')
    config.mode = config.MODE_MAIN_MENU

def setup_screen():
    global screen
    global screen_width
    global screen_height
    global window_mode
    global surfaces
    screen_width = min(config.settings['screen_width'], config.screen_width_full)
    screen_height = min(config.settings['screen_height'], config.screen_height_full)
    window_mode = config.settings['window_mode']
    if window_mode == config.WINDOW_MODE_NORMAL:
        screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        screen_width = config.screen_width_full
        screen_height = config.screen_height_full
        if window_mode == config.WINDOW_MODE_BORDERLESS:
            screen = pygame.display.set_mode((config.screen_width_full, config.screen_height_full), pygame.NOFRAME)
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for key in surfaces:
        if key != 'animation':
            surface = pygame.Surface((screen_width, screen_height))
            surface.set_colorkey(COLOR_KEY)
            surfaces[key] = surface
    debug_print('Setting up screen: (' + window_mode + ') ' +str(screen_width) + 'x' + str(screen_height))
    if config.screen_width_full < config.RESOLUTION_MIN[0] or config.screen_height_full < config.RESOLUTION_MIN[1]:
        config.raise_system_error('resolution')
    pygame.display.set_caption(MAIN_TITLE)
    pygame.display.set_icon(ICON)
    setup_cursor()

def setup_cursor():
    custom_cursor = (
    "      xxx       ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "xxxxxxx.xxxxxxx ",
    "x.............x ",
    "xxxxxxx.xxxxxxx ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "      x.x       ",
    "      xxx       ",
    "                ")
    cursor = pygame.cursors.compile(custom_cursor, black='x', white='.', xor='o')
    pygame.mouse.set_cursor((16, 16), (8, 8), *cursor)

def setup_font():
    global font_name
    global font
    global font_underline
    global font_strikethrough
    global font_width
    global font_height
    global offset_x
    global offset_y
    font_name = config.settings['font']
    font = pygame.font.Font("resources/font/" + config.FONTS[font_name] + '.ttf', 16)
    font_underline = pygame.font.Font("resources/font/" + config.FONTS[font_name] + '.ttf', 16)
    font_underline.set_underline(True)
    font_strikethrough = pygame.font.Font("resources/font/" + config.FONTS[font_name] + '.ttf', 16)
    font_strikethrough.set_underline(True)
    font_size = font.size('A')
    font_width = font_size[0]
    font_height = font_size[1]
    size_x_raw = screen_width / font_width
    offset_x = math.floor((font_width * math.modf(size_x_raw)[0]) / 2)
    config.size_x = math.floor(size_x_raw)
    size_y_raw = screen_height / font_height
    offset_y = math.floor((font_height * math.modf(size_y_raw)[0]) / 2)
    config.size_y = math.floor(size_y_raw)
    debug_print('Setting up font: (' + str(font_width) + 'x' + str(font_height) + ') ' + font_name + ' ('+ str(config.size_x) + 'x' + str(config.size_y) + ' characters on screen)')

def setup_palette():
    global palette_name
    palette_name = config.settings['palette']
    pre_render_surfaces()

def pre_render_surfaces():
    pre_rendered_surfaces['fade1_fg'] = pre_render_frame(CHAR_FADE1, 'foreground')
    pre_rendered_surfaces['fade1_bg'] = pre_render_frame(CHAR_FADE1, 'background')
    pre_rendered_surfaces['fade2_fg'] = pre_render_frame(CHAR_FADE2, 'foreground')
    pre_rendered_surfaces['fade2_bg'] = pre_render_frame(CHAR_FADE2, 'background')
    pre_rendered_surfaces['fade3_fg'] = pre_render_frame(CHAR_FADE3, 'foreground')
    pre_rendered_surfaces['fade3_bg'] = pre_render_frame(CHAR_FADE3, 'background')
    pre_rendered_surfaces['dot_white'] = pre_render_frame(CHAR_DOT, 'white')
    pre_rendered_surfaces['boot1'] = pre_render_frame(CHAR_DOT, 'foreground', 'background', '....BOOTING')
    pre_rendered_surfaces['boot2'] = pre_render_frame(CHAR_DOT, 'foreground', 'background', 'BOOTING')

def pre_render_frame(fg_char, fg_color, bg_color = None, fg_text = None):
    surface = pygame.Surface((screen_width, screen_height))
    surface.set_colorkey(COLOR_KEY)
    if bg_color is not None:
        surface.fill(config.PALETTES[palette_name][bg_color])
    else:
        surface.fill(COLOR_KEY)
    for num in range(config.size_y):
        pos_y = offset_y + (num * font_height)
        line_text = fg_char * config.size_x
        if fg_text is not None:
            line_text = fg_text + (fg_char * (config.size_x - len(fg_text)))
        render_line = font.render(line_text, False, config.PALETTES[palette_name][fg_color])
        surface.blit(render_line, (offset_x, pos_y))
    return surface

def joystick_init():
    for num in range(pygame.joystick.get_count()):
        joystick_add(pygame.joystick.Joystick(num))

def joystick_add(joy, timestamp = 0):
    joy_id = joy.get_instance_id()
    joysticks[joy_id] = {
        'joy': joy,
        'timestamp': timestamp,
        'axis_values': {}
    }
    joy_axes = joy.get_numaxes()
    for axis_num in range(joy_axes):
        joysticks[joy_id]['axis_values'][axis_num] = None
    debug_print('Joystick device added: (' + str(joy.get_instance_id()) + ') ' + str(joy.get_name()))

def joystick_remove(joy_id):
    joy = joysticks.pop(joy_id)['joy']
    debug_print('Joystick device removed: (' + str(joy_id) + ') ' + str(joy.get_name()))

def run():
    debug_print('Running main loop')
    current_animation = None
    anim_frame = 0
    anim_fps = None
    anim_fps_timestamp = None
    anim_ctrl_playing = False
    anim_ctrl_stopping = False
    anim_block_refresh_content = True
    anim_load_frame = True
    instant_quit = False
    mouse_time_inactive = 0
    get_input = False
    refresh_screen = True
    refresh_content = True
    popup_window_active = False
    screen_content = None
    ui_options = []
    ui_windows = []
    clock = pygame.time.Clock()
    # MAIN LOOP
    while config.run_game:
        timestamp = pygame.time.get_ticks()
        # CHECK ANIMATION QUEUE
        if config.animation_queue and current_animation is None:
            current_animation = config.animation_queue.pop(0)
            debug_print('Running animation: ' + str(current_animation))
            refresh_screen = True
            anim_block_refresh_content = True
            anim_ctrl_playing = True
            anim_frame = 0
            anim_fps_timestamp = timestamp
            anim_load_frame = True
            get_input = False
            if current_animation[1][0] is not None:
                audio.sound_play(current_animation[1][0], current_animation[1][1])
        # CHECK IF DISPLAY / FONT / PALETTE SETTINGS CHANGED
        if anim_ctrl_playing is False:
            # CHANGE WINDOW MODE / RESOLUTION
            if config.display_changed:
                config.display_changed = False
                pygame.display.quit()
                pygame.display.init()
                setup_screen()
                setup_font()
                setup_palette()
            # CHANGE FONT
            elif config.font_changed:
                config.font_changed = False
                setup_font()
                setup_palette()
            # CHANGE PALETTE
            elif config.palette_changed:
                config.palette_changed = False
                setup_palette()
        # HIDE / SHOW MOUSE CURSOR
        if mouse_time_inactive == 0 and config.settings['enable_mouse']:
            pygame.mouse.set_visible(True)
        elif mouse_time_inactive > 2000 or not config.settings['enable_mouse']:
            pygame.mouse.set_visible(False)
        mouse_time_inactive += clock.get_time()
        # REFRESH CONTENT
        if refresh_content and anim_block_refresh_content is False:
            debug_print('Refreshing screen content')
            refresh_screen = True
            refresh_content = False
            popup_window_active = False
            # GET SCREEN CONTENT
            screen_content = []
            if config.mode == config.MODE_MAIN_MENU:
                screen_content = modes.main_menu.run()
            elif config.mode == config.MODE_DEBUG:
                screen_content = modes.debug.run()
            elif config.mode == config.MODE_SETTINGS:
                screen_content = modes.settings.run()
            elif config.mode == config.MODE_HELP:
                screen_content = modes.help.run()
            elif config.mode == config.MODE_CUTSCENE:
                screen_content = modes.cutscene.run()
            elif config.mode == config.MODE_GAME:
                screen_content = modes.game.run()
            elif config.mode == config.MODE_MAP:
                screen_content = modes.map.run()
            elif config.mode == config.MODE_CHARACTER:
                screen_content = modes.character.run()
            # ITERATE THROUGH CONTENT LAYERS
            for layer_num, content_layer in enumerate(screen_content):
                layer_type = content_layer[0]
                layer_fg_color = content_layer[2]
                layer_bg_color = content_layer[3]
                if layer_fg_color is None:
                    layer_fg_color = config.DEFAULT_FG_COLOR
                layer_lines = []
                ui_options = []
                ui_windows = []
                # ITERATE THROUGH WINDOWS
                if layer_type == config.LAYER_TYPE_MAIN:
                    window_start_y = offset_y
                    for window_name, window_lines in content_layer[1]:
                        window_size_y = len(window_lines) * font_height
                        layer_lines.extend(window_lines)
                        window_rect = pygame.Rect(0, window_start_y, screen_width, window_size_y)
                        window_entry = (window_name, window_rect)
                        ui_windows.append(window_entry)
                        window_start_y += window_size_y
                elif layer_type == config.LAYER_TYPE_POPUP:
                    layer_lines = content_layer[1]
                start_x = 0
                start_y = 0
                surfaces[layer_type].fill(COLOR_KEY)
                # DRAW BACKGROUND FOR POPUP WINDOW
                if layer_type == config.LAYER_TYPE_POPUP:
                    popup_window_active = True
                    popup_offset_y = 0
                    total_line_offset = sum([line[1] for line in layer_lines])
                    # MAKE BOX
                    layer_size_y = (len(layer_lines) - total_line_offset) * font_height
                    layer_size_x = utils.list_longest_entry_length([utils.remove_all_tags(line[0]) for line in layer_lines]) * font_width
                    centered_x = ((config.size_x * font_width) / 2) - (layer_size_x / 2)
                    centered_y = ((config.size_y * font_height) / 2) - (layer_size_y / 2)
                    border_offset_x = 2
                    border_offset_y = 6
                    popup_rect = pygame.Rect(offset_x + centered_x + border_offset_x, offset_y + centered_y + border_offset_y, (layer_size_x - font_width) + (border_offset_x * 2) , (layer_size_y - font_height) + (border_offset_y / 2))
                    ui_windows.append(('popup', popup_rect))
                    if config.settings['visual_enable_popup_window_shadow']:
                        shadow_rect = popup_rect.move(16,16)
                        surfaces[layer_type].fill(config.PALETTES[palette_name]['black'], shadow_rect)
                    surfaces[layer_type].fill(config.PALETTES[palette_name][layer_bg_color], popup_rect)
                    start_x = centered_x
                    start_y = centered_y
                    # RENDER FILL
                    fill_start_x = start_x + border_offset_x
                    fill_start_y = start_y + border_offset_y
                    fill_line = content_layer[4][0]
                    fill_color = content_layer[4][1]
                    if fill_line:
                        for num in range(math.ceil(popup_rect[3] / font_height)):
                            pos_y = offset_y + (num * font_height)
                            line_end_y = (num + 1) * font_height
                            line_overflow_y = line_end_y - popup_rect[3]
                            crop_area = (0,0, popup_rect[2], max(0, font_height - line_overflow_y))
                            if fill_color is None:
                                fill_color = config.DEFAULT_FILL_COLOR
                            render_fill_line = font.render(fill_line, False, config.PALETTES[palette_name][fill_color])
                            surfaces[layer_type].blit(render_fill_line, (offset_x + fill_start_x, fill_start_y + pos_y), crop_area)
                # CHECK LINES IN LAYER
                for num in range(config.size_y):
                    pos_y = offset_y + (num * font_height)
                    # LINE
                    if len(layer_lines) > num:
                        line = None
                        line_color = layer_fg_color
                        # MAIN WINDOW SETUP
                        if layer_type == config.LAYER_TYPE_MAIN:
                            line = layer_lines[num][0][0]
                            if layer_lines[num][0][1] is not None:
                                line_color = layer_lines[num][0][1]
                            # RENDER FILL
                            fill_line = layer_lines[num][1][0]
                            fill_color = layer_lines[num][1][1]
                            if fill_line:
                                if fill_color is None:
                                    fill_color = config.DEFAULT_FILL_COLOR
                                render_fill_line = font.render(fill_line, False, config.PALETTES[palette_name][fill_color])
                                surfaces[layer_type].blit(render_fill_line, (offset_x + start_x, start_y + pos_y))
                        # POPUP WINDOW SETUP
                        elif layer_type == config.LAYER_TYPE_POPUP:
                            line = layer_lines[num][0]
                            line_offset = layer_lines[num][1]
                            if line_offset > 0:
                                popup_offset_y += int(line_offset * font_height)
                            pos_y -= popup_offset_y
                        # RENDER LINE
                        clean_line = utils.remove_all_tags(line)
                        if clean_line.strip():
                            render_line = font.render(clean_line, False, config.PALETTES[palette_name][line_color])
                            surfaces[layer_type].blit(render_line, (offset_x + start_x, start_y + pos_y))
                        # FIND UI TAGS
                        tag_search = re.finditer('<ui=(.{4}):(.*?)>(.*?)</ui>', utils.remove_text_tags(line), flags = re.IGNORECASE)
                        start_adj = 0
                        for tag_num, match in enumerate(tag_search):
                            match_type = match.group(1).lower()
                            match_data = match.group(2).lower()
                            match_text = match.group(3)
                            match_start = match.start() - start_adj
                            start_adj += 15 + len(match_data)
                            ui_option_x = offset_x + start_x + ((match_start) * font_width)
                            ui_option_y = pos_y + start_y
                            ui_option_size_x = font_width * len(match_text)
                            ui_option_size_y = font_height
                            ui_option_rect = pygame.Rect(ui_option_x, ui_option_y, ui_option_size_x, ui_option_size_y)
                            ui_option = (match_text, ui_option_rect, match_type, match_data)
                            ui_options.append(ui_option)
                        # FIND TEXT TAGS
                        tag_search = re.finditer('<text=(.{2}):(.{2}):(.{2})>(.*?)</text>',  utils.remove_ui_tags(line), flags = re.IGNORECASE)
                        for tag_num, match in enumerate(tag_search):
                            match_fg = match.group(1).lower()
                            match_bg = match.group(2).lower()
                            match_other = match.group(3).lower()
                            match_text = match.group(4)
                            start_adj = 22 * tag_num
                            match_start = match.start() - start_adj
                            # SET OTHER
                            tag_line_font = None
                            if match_other == config.TAGS['underline']:
                                tag_line_font = font_underline
                            elif match_other == config.TAGS['strikethrough']:
                                tag_line_font = font_strikethrough
                            else:
                                tag_line_font = font
                            # SET FG COLOR
                            tag_line_render = tag_line_font.render(match_text, False, config.PALETTES[palette_name][config.TAGS_REVERSE[match_fg]])
                            # SET BG COLOR
                            if match_bg != 'bg':
                                tag_line_bg = pygame.Surface(tag_line_render.get_size())
                                tag_line_bg.fill(config.PALETTES[palette_name][config.TAGS_REVERSE[match_bg]])
                                tag_line_bg.blit(tag_line_render, (0, 0))
                                tag_line_render = tag_line_bg
                            # RENDER TAGGED TEXT
                            surfaces[layer_type].blit(tag_line_render, (offset_x + start_x + ((match_start) * font_width), start_y + pos_y))
        # PLAY ANIMATION
        if current_animation is not None and anim_load_frame is True:
            anim_load_frame = False
            # OTHER ANIMATIONS
            if current_animation[0] in config.ANIMATIONS:
                anim_fps = config.ANIMATIONS[current_animation[0]]['fps']
                surfaces['animation'] = pre_rendered_surfaces[config.ANIMATIONS[current_animation[0]]['frames'][anim_frame]]
                if anim_frame >= config.ANIMATIONS[current_animation[0]]['block_until_frame']:
                    anim_block_refresh_content = False
                if (anim_frame + 1) >= len(config.ANIMATIONS[current_animation[0]]['frames']):
                    anim_ctrl_stopping = True
            # UI ANIMATIONS
            elif current_animation[0] in config.ANIMATIONS_UI:
                anim_fps = config.ANIMATIONS_UI[current_animation[0]]['fps']
                anim_block_refresh_content = True
                if (anim_frame + 1) >= config.ANIMATIONS_UI[current_animation[0]]['length']:
                    anim_ctrl_stopping = True
                surfaces['ui_animation'].fill(COLOR_KEY)
                animation_type = current_animation[2][0]
                animation_data = current_animation[2][1]
                for option in ui_options:
                    option_found = False
                    option_type = option[2]
                    option_data = option[3]
                    if option_type == config.UI_TAGS['continue'] and animation_data == config.UI_TAGS['continue']:
                        option_found = True
                    elif animation_data == option_data:
                        if animation_type == option_type:
                            option_found = True
                        elif animation_type == 'sel' and (option_type == config.UI_TAGS['none'] or option_type == config.UI_TAGS['action'] or option_type == config.UI_TAGS['left'] or option_type == config.UI_TAGS['right']):
                            option_found = True
                    if option_found is True:
                        ui_text = option[0]
                        ui_rect = option[1]
                        color = config.TAGS_REVERSE[config.TAG_COLOR_UI_SEL_FG]
                        if config.ANIMATIONS_UI[current_animation[0]]['highlight']:
                            color = config.TAGS_REVERSE[config.TAG_COLOR_UI_SEL_HL]
                        if anim_frame % 2:
                            color = config.TAGS_REVERSE[config.TAG_COLOR_BG]
                        anim_line = ui_text
                        anim_render_line = font.render(anim_line, False, config.PALETTES[palette_name][color])
                        surfaces['ui_animation'].blit(anim_render_line, ui_rect)
                surfaces['animation'] = surfaces['ui_animation']
        # UPDATE DISPLAY
        if refresh_screen:
            screen.fill(config.PALETTES[palette_name]['background'])
            screen.blit(surfaces['main'], (0,0))
            if popup_window_active:
                screen.blit(pre_rendered_surfaces['fade2_bg'], (0,0))
                screen.blit(surfaces['popup'], (0,0))
            if anim_ctrl_playing:
                screen.blit(surfaces['animation'], (0,0))
            pygame.display.flip()
            refresh_screen = False
        # DEBUG LINE
        if config.settings['debug_mode'] and config.settings['debug_info_screen'] != 'hide' and config.mode != config.MODE_BOOT_SCREEN:
                debug_pos_y = offset_y + ((config.size_y - 1) * font_height)
                fps = round(clock.get_fps())
                debug_line = '  '
                if config.settings['debug_info_screen'] == 'full' or (config.mode == config.MODE_DEBUG):
                    debug_line += 'RESOLUTION: ' + str(screen_width) + 'x' + str(screen_height) + ' | SIZE: ' + str(config.size_x) + 'x' + str(config.size_y) + ' | FONT: ' + font_name + ' (' + str(font_width) + 'x' + str(font_height) + ') | MOUSE: ' + str(pygame.mouse.get_pos()[0]).zfill(4) + 'x' + str(pygame.mouse.get_pos()[1]).zfill(4) + ' | '
                debug_line += 'FPS: ' + str(fps).zfill(2) + '  '
                debug_rect = (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y, screen_width - offset_x, font_height)
                screen.fill(config.PALETTES[palette_name]['red'], debug_rect)
                debug_render_line = font.render(debug_line, False, config.PALETTES[palette_name]['bright_white'])
                screen.blit(debug_render_line, (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y))
                pygame.display.update(debug_rect)
        # CHECK EVENTS      
        got_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instant_quit = True
                config.run_game = False
            elif event.type == audio.MUSIC_END and config.settings['enable_music']:
                audio.music_play()
            # JOYSTICK ADDED
            elif event.type == pygame.JOYDEVICEADDED:
                joystick_add(pygame.joystick.Joystick(event.device_index), timestamp)
            # JOYSTICK REMOVED
            elif event.type == pygame.JOYDEVICEREMOVED:
                joystick_remove(event.instance_id)
            # MOUSE / KEYBOARD INPUT
            if get_input and not got_input:
                key = None
                mod = None
                # MOUSE INPUT
                if config.settings['enable_mouse'] and (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
                    mouse_time_inactive = 0
                    mouse_button = None
                    mouse_on_ui_option = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_button = event.button
                        config.last_input_device = 'mouse'
                        debug_print('Mouse button pressed: ' + str(mouse_button))
                    for window in ui_windows:
                        if window[1].collidepoint(pygame.mouse.get_pos()):
                            window_name = window[0]
                            scroll_dir = None
                            if mouse_button == 4:
                                scroll_dir = 'down'
                            elif mouse_button == 5:
                                scroll_dir = 'up'
                            if scroll_dir is not None:
                                key = 'mouse_scroll_' + window_name + '_' + scroll_dir
                    for option in ui_options:
                        if option[1].collidepoint(pygame.mouse.get_pos()):
                            option_type = option[2]
                            option_data = option[3]
                            if option_type == config.UI_TAGS['none'] or option_type == config.UI_TAGS['action'] or option_type == config.UI_TAGS['left'] or option_type == config.UI_TAGS['right']:
                                option_data = option_data.split('-')
                                sel_x = int(option_data[0])
                                sel_y = int(option_data[1])
                                if config.ui_selection_x != sel_x or config.ui_selection_y != sel_y:
                                    audio.sound_play('ui_sel', 'ui')
                                    config.ui_selection_x = sel_x
                                    config.ui_selection_y = sel_y
                                    config.ui_scroll['log']['pos'] = 0
                                    refresh_content = True
                                    mouse_button = None
                                elif mouse_button == 1:
                                    if option_type == config.UI_TAGS['action']:
                                        key = 'mouse_action'
                                    elif option_type == config.UI_TAGS['left']:
                                        key = 'mouse_left'
                                    elif option_type == config.UI_TAGS['right']:
                                        key = 'mouse_right'
                            elif option_type == config.UI_TAGS['back'] and mouse_button == 1:
                                key = 'mouse_back'
                            elif option_type == config.UI_TAGS['scroll'] and mouse_button == 1:
                                if option_data == config.UI_TAGS['data_center_up']:
                                    key = 'mouse_scroll_center_up'
                                elif option_data == config.UI_TAGS['data_center_down']:
                                    key = 'mouse_scroll_center_down'
                                elif option_data == config.UI_TAGS['data_log_up']:
                                    key = 'mouse_scroll_log_up'
                                elif option_data == config.UI_TAGS['data_log_down']:
                                    key = 'mouse_scroll_log_down'
                            elif option_type == config.UI_TAGS['link'] and mouse_button == 1:
                                webbrowser.get().open_new_tab(option_data)
                                debug_print('Opening web page: ' + option_data)
                    if mouse_button is not None and key is None:
                        mouse_val = None
                        if mouse_button == 1 and config.ui_selection_current is None:
                            mouse_val = 'action'
                        elif mouse_button == 3:
                            mouse_val = 'back'
                        if mouse_val is not None:
                            key = 'mouse_' + mouse_val
                # KEYBOARD INPUT
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == 'left shift' or key == 'left ctrl' or key == 'left alt' or key == 'right shift' or key == 'right ctrl' or key == 'right alt':
                        key = None
                    elif key:
                        if event.mod & pygame.KMOD_SHIFT:
                            mod = 'shift'
                        elif event.mod & pygame.KMOD_CTRL:
                            mod = 'ctrl'
                        elif event.mod & pygame.KMOD_ALT:
                            mod = 'alt'
                        keyboard_button_debug_message = key
                        if mod is not None:
                            keyboard_button_debug_message = mod + ' + ' + keyboard_button_debug_message
                        config.last_input_device = 'keyboard'
                        debug_print('Keyboard button pressed: ' + keyboard_button_debug_message)
                # JOYSTICK INPUT
                elif config.settings['enable_joystick'] and (event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION or event.type == pygame.JOYAXISMOTION):
                    config.last_input_device = 'joystick'
                    joy_id = event.instance_id
                    if event.type == pygame.JOYBUTTONDOWN:
                        key = 'joy_' + str(event.button)
                        debug_print('Joystick button pressed: (' + str(joy_id) + ') ' + str(key))
                    elif event.type == pygame.JOYHATMOTION:
                        hat_val = None
                        if event.value[1] == -1:
                            hat_val = 'hat_down'
                        elif event.value[1] == 1:
                            hat_val = 'hat_up'
                        elif event.value[0] == -1:
                            hat_val = 'hat_left'
                        elif event.value[0] == 1:
                            hat_val = 'hat_right'
                        if hat_val is not None:
                            key = 'joy_' + hat_val
                            debug_print('Joystick hat pressed: (' + str(joy_id) + ') ' + str(key))
                    elif event.type == pygame.JOYAXISMOTION:
                        axis_val = None
                        if event.value < -0.4:
                            axis_val = 'neg'
                        elif event.value > 0.4:
                            axis_val = 'pos'
                        else:
                            joysticks[joy_id]['axis_values'][event.axis] = None
                        if axis_val is not None:
                            if axis_val != joysticks[joy_id]['axis_values'][event.axis]:
                                joysticks[joy_id]['axis_values'][event.axis] = axis_val
                                key = 'joy_axis_' + str(event.axis) + '_' + axis_val
                                debug_print('Joystick axis pressed: (' + str(joy_id) + ') ' + str(key) + ' (' + str(event.value) + ')')
                # HANDLE INPUT
                if key is not None:
                    got_input = True
                    config.last_input = (key, mod)
                    if config.mode == config.MODE_MAIN_MENU:
                        refresh_content = modes.main_menu.input(key, mod)
                    elif config.mode == config.MODE_DEBUG:
                        refresh_content = modes.debug.input(key, mod)
                    elif config.mode == config.MODE_SETTINGS:
                        refresh_content = modes.settings.input(key, mod)
                    elif config.mode == config.MODE_HELP:
                        refresh_content = modes.help.input(key, mod)
                    elif config.mode == config.MODE_CUTSCENE:
                        refresh_content = modes.cutscene.input(key, mod)
                    elif config.mode == config.MODE_GAME:
                        refresh_content = modes.game.input(key, mod)
                    elif config.mode == config.MODE_MAP:
                        refresh_content = modes.map.input(key, mod)
                    elif config.mode == config.MODE_CHARACTER:
                        refresh_content = modes.character.input(key, mod)
        # CHECK IF ANIMATION FRAME IS FINISHED
        if anim_ctrl_playing and timestamp - anim_fps_timestamp >= int(1000 / anim_fps):
            refresh_screen = True
            # STOP ANIMATION
            if anim_ctrl_stopping:
                anim_ctrl_playing = anim_ctrl_stopping = False
                refresh_screen = True
                current_animation = None
                anim_block_refresh_content = False
                get_input = True
            # LOAD NEXT FRAME
            else:
                anim_fps_timestamp = timestamp
                anim_frame += 1
                anim_load_frame = True
        # WAIT
        clock.tick(TARGET_FRAMERATE)
    # QUIT
    audio.music_stop()
    # SYSTEM ERROR SCREEN
    if config.system_error is not None:
        error_lines = []
        error_lines.append('ERROR!')
        if config.system_error == 'resolution':
            error_lines.append('RESOLUTION NOT SUPPORTED!')
            error_lines.append('MINIMUM SUPPORTED RESOLUTION IS ' + str(config.RESOLUTION_MIN[0]) + 'x' + str(config.RESOLUTION_MIN[1]))
        error_lines.append('')
        error_lines.append('PRESS ANY KEY TO QUIT GAME')
        screen.fill(config.PALETTES[palette_name]['background'])
        for num, line in enumerate(error_lines):
            pos_y = offset_y + (num * font_height) + font_height
            render_line = font.render('  ' + line, False, config.PALETTES[palette_name]['foreground'])
            screen.blit(render_line, (offset_x, pos_y))
        pygame.display.flip()
        run_system_error = True
        while run_system_error:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_system_error = False
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key is not None:
                        run_system_error = False
            clock.tick(TARGET_FRAMERATE)
    # QUIT ANIMATION
    elif not instant_quit:
        quit_animation()
    pygame.quit()

def boot_animation():
    start_timestamp = pygame.time.get_ticks()
    # SET FPS
    anim_fps = TARGET_FRAMERATE
    speed_multiplier = round(config.size_x * 0.04)
    # SET COLORS
    fg_color = 'foreground'
    bg_color = 'background'
    bar_color = 'bright_white'
    title_fg_color = 'bright_white'
    title_bg_color = 'red'
    # SET POSITIONS / SIZES
    title_line_start_line = 1
    info_lines_start_line = title_line_start_line + 2
    x_margin = round(config.size_x * 0.2)
    bar_length = config.size_x - (x_margin * 2)
    bar_pos_y = offset_y + ((config.size_y - 2) * font_height)
    # RENDER BG
    screen.fill(config.PALETTES[palette_name]['background'])
    screen.blit(pre_rendered_surfaces['dot_white'], (0, 0))
    # RENDER TITLE LINE
    title_pos_y = offset_y + (title_line_start_line * font_height)
    title_rect = (offset_x + (x_margin * font_width), title_pos_y, ((bar_length + 2) * font_width), font_height)
    screen.fill(config.PALETTES[palette_name][title_bg_color], title_rect)
    title_line_render = font.render(MAIN_TITLE.upper() + ' v' + str(config.VERSION_NUMBER), False, config.PALETTES[palette_name][title_fg_color])
    screen.blit(title_line_render, (offset_x + (x_margin * font_width), title_pos_y))
    # RENDER INFO LINES
    lines = [
    str(screen_width) + 'x' + str(screen_height) + ' ' + window_mode.upper() + ' RENDERING MODE (' + str(len(config.PALETTES[palette_name])) + ' COLORS)',
    str(config.size_x) + 'x' + str(config.size_y) + ' CHARACTERS ' + '(' + str(font_width) + 'x' + str(font_height) + ') ' + font_name.upper(),
    'TARGET FRAMERATE: ' + str(TARGET_FRAMERATE),
    ]
    for line_num, line in enumerate(lines):
        pos_y = offset_y + ((line_num + info_lines_start_line) * font_height)
        render_line = font.render(line, False, config.PALETTES[palette_name][fg_color])
        line_render_bg = pygame.Surface(render_line.get_size())
        line_render_bg.fill(config.PALETTES[palette_name][bg_color])
        line_render_bg.blit(render_line, (0, 0))
        screen.blit(line_render_bg, (offset_x + (x_margin * font_width), pos_y))
    # RENDER LOADING BAR TEXT
    loading_text_line = 'STARTING GAME'
    loading_text_render_line = font.render(loading_text_line, False, config.PALETTES[palette_name][fg_color])
    loading_text_line_render_bg = pygame.Surface(loading_text_render_line.get_size())
    loading_text_line_render_bg.fill(config.PALETTES[palette_name][bg_color])
    loading_text_line_render_bg.blit(loading_text_render_line, (0, 0))
    screen.blit(loading_text_line_render_bg, (offset_x + (x_margin * font_width), bar_pos_y - font_height))
    # RENDER LOADING BAR ENDS
    render_bar_ends = font.render('[' + ' ' * bar_length + ']', False, config.PALETTES[palette_name][fg_color])
    screen.blit(render_bar_ends, (offset_x + (x_margin * font_width), bar_pos_y))
    # RENDER LOADING BAR
    for char_num in range(0, bar_length, speed_multiplier):
        num_to_add = min(speed_multiplier, bar_length - (char_num))
        # BAR LINES
        pos_x = offset_x + (char_num * font_width) + ((x_margin + 1) * font_width)
        line = '#' * num_to_add
        render_line = font.render(line, False, config.PALETTES[palette_name][bar_color])
        screen.blit(render_line, (pos_x, bar_pos_y))
        # PERCENTAGE
        percent_num = round(100 * ((char_num + num_to_add) / bar_length))
        percent_line = str(percent_num).zfill(3) + '%'
        percent_pos_x = screen_width - (len(percent_line) * font_width) - offset_x - (x_margin * font_width) + (2 * font_width)
        percent_render_line = font.render(percent_line, False, config.PALETTES[palette_name][fg_color])
        percent_render_bg = pygame.Surface(percent_render_line.get_size())
        percent_render_bg.fill(config.PALETTES[palette_name][bg_color])
        percent_render_bg.blit(percent_render_line, (0, 0))
        screen.blit(percent_render_bg, (percent_pos_x, bar_pos_y - font_height))
        # UPDATE DISPLAY
        pygame.display.flip()
        pygame.time.delay(int(1000 / anim_fps))
    end_timestamp = pygame.time.get_ticks()
    debug_print('Running boot animation with speed multiplier ' + str(speed_multiplier) + ' in ' + str(end_timestamp - start_timestamp) + 'ms')

def quit_animation():
    start_timestamp = pygame.time.get_ticks()
    audio.sound_play('ui_back')
    anim_fps = TARGET_FRAMERATE
    speed_multiplier = round(config.size_y * 0.06)
    animation_frames = [
    (CHAR_DOT, '....................QUITTING'),
    (CHAR_FADE2, ''),
    (CHAR_FADE3, ''),
    (CHAR_FADE1, ''),
    ]
    for num, frame in enumerate(animation_frames):
        color = 'background'
        if num == 0:
            color = 'foreground'
        elif num == 1:
            color = 'white'
        elif num == 2:
            color = 'black'
        for line_num in range(0, config.size_y, speed_multiplier):
            line = frame[1]
            for char_num in range(config.size_x - len(line)):
                line += frame[0]
            for num in  range(speed_multiplier):
                pos_y = offset_y + ((line_num + num) * font_height)
                if line_num + num < config.size_y:
                    render_line = font.render(line, False, config.PALETTES[palette_name][color])
                    screen.blit(render_line, (offset_x, pos_y))
            pygame.display.flip()
            pygame.time.delay(int(1000 / anim_fps))
    pygame.time.delay(250)
    end_timestamp = pygame.time.get_ticks()
    debug_print('Running quit animation with speed multiplier ' + str(speed_multiplier) + ' in ' + str(end_timestamp - start_timestamp) + 'ms')

if __name__ == "__main__":
    config.initialize()
    initialize()
    if config.settings['visual_enable_extended_boot_animation']:
        boot_animation()
    audio.initialize()
    run()