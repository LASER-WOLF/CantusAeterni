# BUILT-IN
import math
import os
import re
import time

# THIRD-PARTY
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# PROJECT
import audio
import config
import modes.cutscene
import modes.debug
import modes.game
import modes.help
import modes.inventory
import modes.main_menu
import modes.map
import modes.settings
import utils

# SET CONSTANTS
TARGET_FRAMERATE = 30
MAIN_TITLE = "Cantus Aeterni"
ICON = pygame.image.load('resources/img/icon.png')

# SET VARS
screen_width_full = None
screen_height_full = None
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
offset_x = None
offset_y = None

def initialize():
    global screen_width_full
    global screen_height_full
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # PYGAME SETUP
    pygame.init()
    display_info = pygame.display.Info()
    screen_width_full = display_info.current_w
    screen_height_full = display_info.current_h
    setup_screen()
    setup_font()
    config.trigger_animation(config.ANIMATION_BOOT)
    if config.settings['debug_mode'] and config.settings['debug_on_start']:
        config.mode = config.MODE_DEBUG
    else:
        config.mode = config.MODE_MAIN_MENU

def setup_screen():
    global screen
    global screen_width
    global screen_height
    global window_mode
    screen_width = config.settings['screen_width']
    screen_height = config.settings['screen_height']
    window_mode = config.settings['window_mode']
    if window_mode == config.WINDOW_MODE_NORMAL:
        screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        screen_width = screen_width_full
        screen_height = screen_height_full
        if window_mode == config.WINDOW_MODE_BORDERLESS:
            screen = pygame.display.set_mode((screen_width_full, screen_height_full), pygame.NOFRAME)
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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

def run():
    current_animation = None
    animation_frame = 0
    animation_fps = None
    animation_control = (False, False)
    animation_control_playing = False
    animation_control_stopping = False
    instant_quit = False
    mouse_time_inactive = 0
    ui_options = []
    get_input = False
    clock = pygame.time.Clock()
    while config.run_game:
        # HIDE / SHOW MOUSE CURSOR
        if mouse_time_inactive == 0 and config.settings['enable_mouse']:
            pygame.mouse.set_visible(True)
        elif mouse_time_inactive > 2000 or not config.settings['enable_mouse']:
            pygame.mouse.set_visible(False)
        mouse_time_inactive += clock.get_time()
        # CHECK ANIMATION QUEUE
        if config.animation_queue and current_animation is None:
            current_animation = config.animation_queue.pop(0)
            config.refresh_content = False
            animation_control_playing = True
            get_input = False
        # REFRESH SCREEN
        if config.refresh_screen and config.refresh_content:
            # RE-ENABLE USER INPUT (AFTER ANIMATION)
            if current_animation is None:
                get_input = True
            screen.fill(config.PALETTES[config.settings['palette']]['background'])
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
            elif config.mode == config.MODE_INVENTORY:
                screen_content = modes.inventory.run()
            elif config.mode == config.MODE_CUTSCENE:
                screen_content = modes.cutscene.run()
            elif config.mode == config.MODE_GAME:
                screen_content = modes.game.run()
            elif config.mode == config.MODE_MAP:
                screen_content = modes.map.run()
            for layer_num, content_layer in enumerate(screen_content):
                ui_options = []
                layer_type = content_layer[0]
                layer_lines = content_layer[1]
                layer_fg_color = content_layer[2]
                layer_bg_color = content_layer[3]
                if layer_fg_color is None:
                    layer_fg_color = 'foreground'
                start_x = 0
                start_y = 0
                fill_start_x = 0
                fill_start_y = 0
                #if layer_num > 0:
                if layer_type == config.LAYER_TYPE_POPUP:
                    # FADE OUT PREVIOUS LAYERS
                    for num in range(config.size_y):
                        pos_y = offset_y + (num * font_height)
                        bg_line = '▒' * config.size_x
                        render_line = font.render(bg_line, False, config.PALETTES[config.settings['palette']]['background'])
                        screen.blit(render_line, (offset_x + start_x, start_y + pos_y))
                    # MAKE BOX
                    layer_size_y = len(layer_lines) * font_height
                    layer_size_x = utils.list_longest_entry_length([utils.remove_tag(line[0][0]) for line in layer_lines]) * font_width
                    centered_x = ((config.size_x * font_width) / 2) - (layer_size_x / 2)
                    centered_y = ((config.size_y * font_height) / 2) - (layer_size_y / 2)
                    popup_rect = pygame.Rect(offset_x + centered_x + (font_width / 2), offset_y + centered_y + (font_height / 2), layer_size_x - font_width, layer_size_y - font_height)
                    screen.fill(config.PALETTES[config.settings['palette']][layer_bg_color], popup_rect)
                    start_x = centered_x
                    start_y = centered_y
                    fill_start_x = start_x + (font_width / 2)
                    fill_start_y = start_y + (font_height / 2)
                # CHECK LINES
                for num in range(config.size_y):
                    pos_y = offset_y + (num * font_height)
                    # LINE
                    if len(layer_lines) > num:
                        line = layer_lines[num][0][0]
                        line_color = layer_lines[num][0][1]
                        fill_line = layer_lines[num][1][0]
                        fill_color = layer_lines[num][1][1]
                        if line_color is None:
                            line_color = layer_fg_color
                        if fill_color is None:
                            fill_color = 'bright_black'
                        clean_line = utils.remove_tag(line)
                        # RENDER FILL
                        if fill_line:
                            render_fill_line = font.render(fill_line, False, config.PALETTES[config.settings['palette']][fill_color])
                            screen.blit(render_fill_line, (offset_x + fill_start_x, fill_start_y + pos_y))
                        # RENDER LINE
                        if clean_line.strip():
                            render_line = font.render(clean_line, False, config.PALETTES[config.settings['palette']][line_color])
                            screen.blit(render_line, (offset_x + start_x, start_y + pos_y))
                        # FIND UI TAGS
                        tag_search = re.finditer('<ui=(.{2}):(.{2}):(.{2})>(.*?)</ui>', utils.remove_text_tag(line))
                        for tag_num, match in enumerate(tag_search):
                            match_x = match.group(1)
                            match_y = match.group(2)
                            match_action = match.group(3)
                            match_text = match.group(4)
                            start_adj = 18 * tag_num
                            match_start = match.start() - start_adj
                            ui_option_x = offset_x + start_x + ((match_start) * font_width)
                            ui_option_y = pos_y + start_y
                            ui_option_size_x = font_width * len(match_text)
                            ui_option_size_y = font_height
                            ui_option_rect = pygame.Rect(ui_option_x, ui_option_y, ui_option_size_x, ui_option_size_y)
                            ui_option = (match_text, ui_option_rect,(int(match_x), int(match_y)), match_action)
                            ui_options.append(ui_option)
                        # FIND TEXT TAGS
                        tag_search = re.finditer('<text=(.{2}):(.{2}):(.{2})>(.*?)</text>',  utils.remove_ui_tag(line))
                        for tag_num, match in enumerate(tag_search):
                            match_fg = match.group(1)
                            match_bg = match.group(2)
                            match_other = match.group(3)
                            match_text = match.group(4)
                            start_adj = 22 * tag_num
                            match_start = match.start() - start_adj
                            # SET OTHER
                            tag_line_font = None
                            if match_other == 'ul':
                                tag_line_font = font_underline
                            elif match_other == 'st':
                                tag_line_font = font_strikethrough
                            else:
                                tag_line_font = font
                            # SET FG COLOR
                            tag_line_render = tag_line_font.render(match_text, False, config.PALETTES[config.settings['palette']][config.TAGS_REVERSE[match_fg]])
                            # SET BG COLOR
                            if match_bg != 'bg':
                                tag_line_bg = pygame.Surface(tag_line_render.get_size())
                                tag_line_bg.fill(config.PALETTES[config.settings['palette']][config.TAGS_REVERSE[match_bg]])
                                tag_line_bg.blit(tag_line_render, (0, 0))
                                tag_line_render = tag_line_bg
                            # RENDER TAGGED TEXT
                            screen.blit(tag_line_render, (offset_x + start_x + ((match_start) * font_width), start_y + pos_y))
        # PLAY ANIMATION
        if current_animation is not None:
            # UI ANIMATIONS
            if current_animation[0] == config.ANIMATION_UI_SELECTION_SHORTEST:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1], length = 1)
            elif current_animation[0] == config.ANIMATION_UI_SELECTION_SHORT:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1], length = 3)
            elif current_animation[0] == config.ANIMATION_UI_SELECTION:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1])
            elif current_animation[0] == config.ANIMATION_UI_SELECTION_LONG:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1], length = 7)
            elif current_animation[0] == config.ANIMATION_UI_SELECTION_LONG:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1], length = 7)
            elif current_animation[0] == config.ANIMATION_UI_SELECTION_FG:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = ui_animation(animation_frame, ui_options, current_animation[1], color_hl = False)
            # BOOT ANIMATION
            elif current_animation[0] == config.ANIMATION_BOOT:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = boot_animation(animation_frame)
            # PLAY FADE ANIMATION
            elif current_animation[0] == config.ANIMATION_FADE:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = fade_animation(animation_frame)
            # PLAY FADE POPUP ANIMATION
            elif current_animation[0] == config.ANIMATION_FADE_POPUP:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = fade_popup_animation(animation_frame)
            # PLAY CHANGE ROOM ANIMATION
            elif current_animation[0] == config.ANIMATION_CHANGE_ROOM:
                animation_frame, animation_control_stopping, animation_fps, config.refresh_content = change_room_animation(animation_frame)
        # UPDATE DISPLAY
        if config.refresh_screen:
            pygame.display.flip()
            config.refresh_screen = False
        # DEBUG LINE
        if config.settings['debug_mode'] and config.settings['debug_info_screen'] != 'hide' and config.mode != config.MODE_BOOT_SCREEN:
                debug_pos_y = offset_y + ((config.size_y - 1) * font_height)
                fps = int(clock.get_fps())
                debug_line = '  '
                if config.settings['debug_info_screen'] == 'full' or (current_animation is None and config.mode == config.MODE_DEBUG):
                    debug_line += 'RESOLUTION: ' + str(screen_width) + 'x' + str(screen_height) + ' | SIZE: ' + str(config.size_x) + 'x' + str(config.size_y) + ' | OFFSET: ' + 'X=' + str(offset_x) + ' Y=' + str(offset_y) + ' | FONT: ' + font_name + ' (' + str(font_width) + 'x' + str(font_height) + ') | MOUSE: ' + str(pygame.mouse.get_pos()[0]).zfill(4) + 'x' + str(pygame.mouse.get_pos()[1]).zfill(4) + ' | '
                debug_line += 'FPS: ' + str(fps).zfill(2) + '  '
                debug_rect = (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y, screen_width - offset_x, font_height)
                screen.fill(config.PALETTES[config.settings['palette']]['red'], debug_rect)
                debug_render_line = font.render(debug_line, False, config.PALETTES[config.settings['palette']]['bright_white'])
                screen.blit(debug_render_line, (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y))
                if not config.refresh_screen:
                    pygame.display.update(debug_rect)
        # CHECK EVENTS      
        got_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instant_quit = True
                config.run_game = False
            elif event.type == audio.MUSIC_END and config.settings['enable_music']:
                audio.music_play()
            # MOUSE / KEYBOARD INPUT
            if get_input and not got_input:
                key = None
                if config.settings['enable_mouse'] and (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
                    mouse_time_inactive = 0
                    mouse_action = None
                    for option in ui_options:
                        if option[1].collidepoint(pygame.mouse.get_pos()):
                            sel_x = option[2][0]
                            sel_y = option[2][1]
                            if config.ui_selection_x != sel_x or config.ui_selection_y != sel_y:
                                audio.ui_sel()
                                config.ui_selection_x = sel_x
                                config.ui_selection_y = sel_y
                                config.refresh_screen = True
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_button = event.button
                                if mouse_button == 1:
                                    mouse_action = option[3]
                                    if mouse_action == '00':
                                        key = None
                                    elif mouse_action == '01':
                                        key = 'return'
                                    elif mouse_action == '<-':
                                        key = 'left'
                                    elif mouse_action == '->':
                                        key = 'right'
                    if event.type == pygame.MOUSEBUTTONDOWN and mouse_action is None:
                        mouse_button = event.button
                        key = 'mouse' + str(mouse_button)
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                if key is not None:
                    config.refresh_screen = True
                    got_input = True
                    if config.mode == config.MODE_MAIN_MENU:
                        modes.main_menu.input(key)
                    elif config.mode == config.MODE_DEBUG:
                        modes.debug.input(key)
                    elif config.mode == config.MODE_SETTINGS:
                        modes.settings.input(key)
                    elif config.mode == config.MODE_HELP:
                        modes.help.input(key)
                    elif config.mode == config.MODE_INVENTORY:
                        modes.inventory.input(key)
                    elif config.mode == config.MODE_CUTSCENE:
                        modes.cutscene.input(key)
                    elif config.mode == config.MODE_GAME:
                        modes.game.input(key)
                    elif config.mode == config.MODE_MAP:
                        modes.map.input(key)
        # CHANGE WINDOW MODE / RESOLUTION
        if window_mode != config.settings['window_mode'] or (window_mode == config.WINDOW_MODE_NORMAL and (screen_width != config.settings['screen_width'] or screen_height != config.settings['screen_height'])):
            pygame.display.quit()
            pygame.display.init()
            setup_screen()
            setup_font()
        # CHANGE FONT
        elif font_name != config.settings['font']:
            setup_font()
        # CHECK IF ANIMATION NEEDS NEW FRAME
        if animation_control_playing:
            pygame.time.delay(int(1000 / animation_fps))
            config.refresh_screen = True
        # STOP ANIMATION
        if animation_control_stopping:
            animation_control_playing = animation_control_stopping = False
            current_animation = None
            config.refresh_content = True
        # WAIT
        clock.tick(TARGET_FRAMERATE)
    # QUIT
    audio.music_stop()
    if not instant_quit:
        quit_animation()
    pygame.quit()

def ui_animation(frame, ui_options, ui_sel, length = 5, color_hl = True):
    anim_fps = 8
    ANIMATION_FRAMES = []
    for num in range(length):
        ANIMATION_FRAMES.append('T')
    ui_text = None
    ui_rect = None
    for option in ui_options:
        sel_x = option[2][0]
        sel_y = option[2][1]
        if ui_sel[0] == sel_x and ui_sel[1] == sel_y:
            ui_text = option[0]
            ui_rect = option[1]
            anim_line = ''
            color = 'foreground'
            if color_hl:
                color = 'bright_white'
            if frame == 1 or frame == 3 or frame == 5:
                color = 'background'
            if ANIMATION_FRAMES[frame] == 'T':
                anim_line = ui_text
            else:
                for char_num in range (int(ui_rect.width / font_width)):
                    anim_line += ANIMATION_FRAMES[frame]
            anim_render_line = font.render(anim_line, False, config.PALETTES[config.settings['palette']][color])
            screen.blit(anim_render_line, ui_rect)
    frame += 1
    if frame >= len(ANIMATION_FRAMES):
        frame = 0
        return (frame, True, anim_fps, True)
    else:
        return (frame, False, anim_fps, False)

def boot_animation(frame):
    anim_fps = 8
    BOOT_ANIMATION_FRAMES = [
    ('.', '....BOOTING'),
    ('.', 'BOOTING'),
    ('░', ''),
    ('░', ''),
    ]
    color = 'foreground'
    if frame >= 3:
        color = 'black'
    if frame <= 1:
        screen.fill(config.PALETTES[config.settings['palette']]['background'])
    if frame == 0:
        if config.settings['enable_sound']:
            audio.sound_play('boot')
    for line_num in range(config.size_y):
        pos_y = offset_y + (line_num * font_height)
        line = BOOT_ANIMATION_FRAMES[frame][1]
        for char_num in range(config.size_x - len(line)):
            line += BOOT_ANIMATION_FRAMES[frame][0]
        render_line = font.render(line, False, config.PALETTES[config.settings['palette']][color])
        screen.blit(render_line, (offset_x, pos_y))
    frame += 1
    if frame >= len(BOOT_ANIMATION_FRAMES):
        frame = 0
        return (frame, True, anim_fps, True)
    elif frame > 0:
        return (frame, False, anim_fps, True)
    else:
        return (frame, False, anim_fps, False)

def fade_animation(frame):
    anim_fps = 16
    ANIMATION_FRAMES = [
    '░',
    '▒',
    '░',
    ]
    for line_num in range(config.size_y):
        pos_y = offset_y + (line_num * font_height)
        line = ''
        for char_num in range(config.size_x):
            line += ANIMATION_FRAMES[frame]
        render_line = font.render(line, False, config.PALETTES[config.settings['palette']]['background'])
        screen.blit(render_line, (offset_x, pos_y))
    frame += 1
    if frame >= len(ANIMATION_FRAMES):
        frame = 0
        return (frame, True, anim_fps, True)
    elif frame > 1:
        return (frame, False, anim_fps, True)
    else:
        return (frame, False, anim_fps, False)

def fade_popup_animation(frame):
    anim_fps = 8
    ANIMATION_FRAMES = [
    '░',
    '▒',
    ]
    for line_num in range(config.size_y):
        pos_y = offset_y + (line_num * font_height)
        line = ''
        for char_num in range(config.size_x):
            line += ANIMATION_FRAMES[frame]
        render_line = font.render(line, False, config.PALETTES[config.settings['palette']]['background'])
        screen.blit(render_line, (offset_x, pos_y))
    frame += 1
    if frame >= len(ANIMATION_FRAMES):
        frame = 0
        return (frame, True, anim_fps, True)
    else:
        return (frame, False, anim_fps, True)

def change_room_animation(frame):
    anim_fps = 8
    ANIMATION_FRAMES = [
    '░',
    '▒',
    '▓',
    '▒',
    '░',
    ]
    for line_num in range(config.size_y):
        pos_y = offset_y + (line_num * font_height)
        line = ''
        for char_num in range(config.size_x):
            line += ANIMATION_FRAMES[frame]
        render_line = font.render(line, False, config.PALETTES[config.settings['palette']]['background'])
        screen.blit(render_line, (offset_x, pos_y))
    frame += 1
    if frame >= len(ANIMATION_FRAMES):
        frame = 0
        return (frame, True, anim_fps, True)
    elif frame > 2:
        return (frame, False, anim_fps, True)
    else:
        return (frame, False, anim_fps, False)

def quit_animation():
    anim_fps = 160
    ANIMATION_FRAMES = [
    ('.', '....................QUITTING'),
    ('▒', ''),
    ('▓', ''),
    ('░', ''),
    ]
    color = 'foreground'
    for num, frame in enumerate(ANIMATION_FRAMES):
        if num == 0:
            if config.settings['enable_sound']:
                audio.sound_play('ui_back')
        elif num == 2:
            color = 'black'
        else:
            color = 'background'
        for line_num in range(config.size_y):
            pos_y = offset_y + (line_num * font_height)
            line = frame[1]
            for char_num in range(config.size_x - len(line)):
                line += frame[0]
            render_line = font.render(line, False, config.PALETTES[config.settings['palette']][color])
            screen.blit(render_line, (offset_x, pos_y))
            pygame.display.flip()
            pygame.time.delay(int(1000 / anim_fps))
    pygame.time.delay(750)

if __name__ == "__main__":
        config.initialize()
        initialize()
        audio.initialize()
        run()