# PROJECT
import audio
import config
import system
import windows

def run():
    system.set_selection_options(selection_options())
    return windows.combine([
        windows.window_upper(),
        window_center(),
        window_lower(),
    ])

def input(key):
    selected_option = system.get_selected_option()
    if(key == 'up'):
        system.ui_selection_y_prev()
    elif(key == 'down'):
        system.ui_selection_y_next()
    elif(key == 'escape' or (key == 'return' and selected_option.name == "back")):
        audio.ui_back()
        system.change_mode(config.previous_mode)

def selection_options():
    result = [[
        system.SelectionOption("back", "GO BACK")
    ]]
    return result

def window_center():
    lines = []
    lines.append('MUSIC BY:')
    lines.append('Lory Werths'.upper())
    lines.append('mandolingals.tripod.com')
    lines.append('')
    lines.append('FONTS FROM:')
    lines.append('The Ultimate Oldschool PC Font Pack'.upper())
    lines.append('int10h.org/oldschool-pc-fonts/')
    lines.append('')
    lines.append('COLOR SCHEMES FROM:')
    lines.append('Gogh color scheme collection'.upper())
    lines.append('github.com/Gogh-Co/Gogh')
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options)
    selection_options_display[0].insert(0, 'SELECT OPTION:')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks))