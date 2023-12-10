# PROJECT
import audio
import config
import system
import windows

def run():
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            window_lower(),
        ])
    ]

def input(key, mod = None):
    selected_option = config.ui_selection_current
    if key == 'escape' or key == 'mouse3':
        audio.ui_back()
        system.change_mode(config.previous_mode)

def window_center():
    lines = []
    lines.append('Music by:')
    lines.append('Lory Werths')
    lines.append('mandolingals.tripod.com')
    lines.append('')
    lines.append('Sounds from:')
    lines.append('100 Retro RPG UI Sound Effects')
    lines.append('leohpaz.itch.io')
    lines.append('')
    lines.append('Fonts from:')
    lines.append('The Ultimate Oldschool PC Font Pack')
    lines.append('int10h.org/oldschool-pc-fonts/')
    lines.append('')
    lines.append('Color schemes from:')
    lines.append('Gogh color scheme collection')
    lines.append('github.com/Gogh-Co/Gogh')
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    lines = [windows.press_to_go_back_text()]
    return windows.Content(windows.WINDOW_LOWER, lines, min_height = 0)