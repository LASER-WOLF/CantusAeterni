# PROJECT
import audio
import config
import system
import utils
import windows

def run():
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
    if key in config.controls['back']:
        valid_input = system.change_mode_previous()
    return valid_input

def window_center():
    lines = [
        'Music by:',
        'Lory Werths',
        utils.add_ui_tag_link('mandolingals.tripod.com', 'https://mandolingals.tripod.com/'),
        '',
        'Sounds from:',
        '100 Retro RPG UI Sound Effects',
        utils.add_ui_tag_link('leohpaz.itch.io', 'https://leohpaz.itch.io/'),
        '',
        'Fonts from:',
        'The Ultimate Oldschool PC Font Pack',
        utils.add_ui_tag_link('int10h.org/oldschool-pc-fonts/', 'https://int10h.org/oldschool-pc-fonts/'),
        '',
        'Color schemes from:',
        'Gogh color scheme collection',
        utils.add_ui_tag_link('github.com/Gogh-Co/Gogh', 'https://github.com/Gogh-Co/Gogh'),
    ]
    return windows.Content(windows.WINDOW_CENTER, lines)