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
    pygame.init()
    display_info = pygame.display.Info()
    screen_width_full = display_info.current_w
    screen_height_full = display_info.current_h
    setup_screen()
    setup_font()
    config.current_animation = config.ANIMATION_BOOT
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
    animation_frame = 0
    animation_fps = None
    animation_control = (False, False)
    instant_quit = False
    clock = pygame.time.Clock()
    while config.run_game:
        # REFRESH SCREEN
        if config.refresh_screen and config.refresh_content:
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
            elif config.mode == config.MODE_CUTSCENE:
                screen_content = modes.cutscene.run()
            elif config.mode == config.MODE_GAME:
                screen_content = modes.game.run()
            elif config.mode == config.MODE_MAP:
                screen_content = modes.map.run()
            # CHECK LINES
            for num in range(config.size_y):
                pos_y = offset_y + (num * font_height)
                # LINE
                if len(screen_content) > num:
                    line = screen_content[num][0]
                    fill_line = screen_content[num][1]
                    # RENDER FILL
                    if fill_line:
                        render_fill_line = font.render(fill_line[0], False, config.PALETTES[config.settings['palette']][config.TAGS_REVERSE[fill_line[1]]])
                        screen.blit(render_fill_line, (offset_x, pos_y))
                    # RENDER LINE
                    clean_line = utils.remove_tag(line)
                    render_line = font.render(clean_line, False, config.PALETTES[config.settings['palette']]['foreground'])
                    screen.blit(render_line, (offset_x, pos_y))
                    # TAGS
                    tag_search = re.finditer('<text=(.{2}):(.{2}):(.{2})>(.*?)</text>', line)
                    for num, match in enumerate(tag_search):
                        match_fg = match.group(1)
                        match_bg = match.group(2)
                        match_other = match.group(3)
                        match_text = match.group(4)
                        start_adj = 22 * num
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
                        screen.blit(tag_line_render, (offset_x + ((match_start) * font_width), pos_y))
        # PLAY BOOT ANIMATION
        if config.current_animation == config.ANIMATION_BOOT:
            animation_frame, animation_control, animation_fps, config.refresh_content = boot_animation(animation_frame)
        # PLAY CHANGE MODE ANIMATION
        elif config.current_animation == config.ANIMATION_CHANGE_MODE:
            animation_frame, animation_control, animation_fps, config.refresh_content = change_mode_animation(animation_frame)
        # PLAY CHANGE ROOM ANIMATION
        elif config.current_animation == config.ANIMATION_CHANGE_ROOM:
            animation_frame, animation_control, animation_fps, config.refresh_content = change_room_animation(animation_frame)
        # UPDATE DISPLAY
        if config.refresh_screen:
            pygame.display.flip()
            config.refresh_screen = False
        # DEBUG LINE
        if config.settings['debug_mode'] and config.settings['debug_info_screen'] != 'hide' and config.mode != config.MODE_BOOT_SCREEN:
                debug_pos_y = offset_y + ((config.size_y - 1) * font_height)
                fps = int(clock.get_fps())
                debug_line = '  '
                if config.settings['debug_info_screen'] == 'full':
                    debug_line += 'RESOLUTION: ' + str(screen_width) + 'x' + str(screen_height) + ' | SIZE: ' + str(config.size_x) + 'x' + str(config.size_y) + ' | OFFSET: ' + 'X=' + str(offset_x) + ' Y=' + str(offset_y) + ' | FONT: ' + font_name + ' (' + str(font_width) + 'x' + str(font_height) + ') | '
                debug_line += 'FPS: ' + str(fps) + '  '
                debug_rect = (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y, screen_width - offset_x, font_height)
                screen.fill(config.PALETTES[config.settings['palette']]['red'], debug_rect)
                debug_render_line = font.render(debug_line, False, config.PALETTES[config.settings['palette']]['bright_white'])
                screen.blit(debug_render_line, (screen_width - (len(debug_line) * font_width) - offset_x, debug_pos_y))
                if not config.refresh_screen:
                    pygame.display.update(debug_rect)
        # CHECK EVENTS      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instant_quit = True
                config.run_game = False
            elif event.type == audio.MUSIC_END and config.settings['enable_music']:
                audio.music_play()
            elif event.type == pygame.KEYDOWN and not animation_control[0]:
                config.refresh_screen = True
                key = pygame.key.name(event.key)
                if config.mode == config.MODE_MAIN_MENU:
                    modes.main_menu.input(key)
                elif config.mode == config.MODE_DEBUG:
                    modes.debug.input(key)
                elif config.mode == config.MODE_SETTINGS:
                    modes.settings.input(key)
                elif config.mode == config.MODE_HELP:
                    modes.help.input(key)
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
        if animation_control[0]:
            pygame.time.delay(int(1000 / animation_fps))
            config.refresh_screen = True
        # STOP ANIMATION
        if animation_control[1]:
            animation_control = (False, False)
            config.current_animation = None
            config.refresh_content = True
        # WAIT
        clock.tick(TARGET_FRAMERATE)
    # QUIT
    audio.music_stop()
    if not instant_quit:
        quit_animation()
    pygame.quit()

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
        return (frame, (True, True), anim_fps, True)
    elif frame > 0:
        return (frame, (True, False), anim_fps, True)
    else:
        return (frame, (True, False), anim_fps, False)

def change_mode_animation(frame):
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
        return (frame, (True, True), anim_fps, True)
    elif frame > 1:
        return (frame, (True, False), anim_fps, True)
    else:
        return (frame, (True, False), anim_fps, False)

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
        return (frame, (True, True), anim_fps, True)
    elif frame > 1:
        return (frame, (True, False), anim_fps, True)
    else:
        return (frame, (True, False), anim_fps, False)

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