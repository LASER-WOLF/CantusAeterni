# PROJECT
import audio
import config
import system
import utils
import windows

# SET VARS
debug_input_char = None

def run():
    system.set_selection_options(selection_options())
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            window_log(),
            window_lower(),
        ])
    ]

def input(key, mod = None):
    global debug_input_char
    debug_input_char = key
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if(key == 'up'):
            system.ui_log_or_selection_up()
        elif(key == 'down'):
            system.ui_log_or_selection_down()
        elif(key == 'escape' or key == 'mouse3' or (key == 'return' and selected_option.name == "back"  and config.ui_scroll_log == 0)):
            if config.ui_scroll_log > 0:
                config.ui_scroll_log = 0
            else:
                if key == 'return' and selected_option.name == 'back':
                    config.trigger_animation(config.ANIMATION_UI_SELECTION)
                audio.ui_back()
                system.change_mode(config.previous_mode)
        elif(key == 'return' and config.ui_scroll_log == 0):
            config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            if selected_option.name == "music_next":
                audio.music_stop()

def selection_options():
    result = [[]]
    if config.settings['enable_music']:
        result[0].append(system.SelectionOption("music_next", "NEXT SONG"))
    result[0].append(system.SelectionOption("back", "GO BACK"))
    return result

def window_center():
    lines = []
    justnum = 20
    lines.append('COLOR PALETTE: '.ljust(justnum) + '"' + config.settings['palette'].upper() + '"')
    lines.append('FOREGROUND: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['foreground']) + '        ' + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['foreground']))
    lines.append('RED: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['red']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('GREEN: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['green']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('YELLOW: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['yellow']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_yellow']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['yellow']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_yellow']))
    lines.append('BLUE: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['blue']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_blue']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['blue']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_blue']))
    lines.append('MAGENTA: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['magenta']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_magenta']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['magenta']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_magenta']))
    lines.append('CYAN: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['cyan']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_cyan']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['cyan']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_cyan']))
    lines.append('WHITE: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['white']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_white']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['white']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_white']))
    lines.append('BLACK: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['black']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_black']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['black']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_black']))
    lines.append("")
    lines.append('LAST INPUT: '.ljust(justnum) + '"' + str(debug_input_char)  + '"')
    lines.append('TURN #: '.ljust(justnum) + str(config.game['turn']))
    lines.append('HEALTH: '.ljust(justnum) + str(config.player['health_points'])  + ' (' + str(config.player['health_stage']) +')')
    lines.append('')
    lines.append('MUSIC STATUS: '.ljust(justnum) + 'PLAYING: ' + str(audio.music_status()).upper() + ' | VOL: ' + str(config.settings['music_volume']) + ' | MODE: ' + str(audio.music_type).upper() + ' | TITLE: ' + str(audio.music_title).upper())
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_log():
    lines = []
    lines.extend(windows.log_content(config.debug_log_list, False))
    return windows.Content(windows.WINDOW_LOG, lines)

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options)
    selection_options_display[0].insert(0, 'SELECT OPTION:')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks))