# PROJECT
import config
import system
import utils
import windows

# SET VARS
input_combo = ''

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
    # CHECK FOR SECRET DEBUG MODE ACTIVATION
    global input_combo
    if key == 'return' or key in config.controls['back']:
        if input_combo == config.INPUT_COMBO_DEBUG_MODE:
            config.settings['debug_mode'] = not config.settings['debug_mode']
            config.export_settings()
            valid_input = True
            text = 'DEBUG MODE '
            if config.settings['debug_mode'] is True:
                text += 'ENABLED'
            else:
                text += 'DISABLED'
            print(text)
        input_combo = ''
    elif key.isalnum():
        input_combo += key
    # CHECK INPUT
    if key in config.controls['back']:
        valid_input = system.change_mode_previous()
    elif key in config.controls['scroll_center_up'] or (key in config.controls['up'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_minus('center')
    elif key in config.controls['scroll_center_down'] or (key in config.controls['down'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_plus('center')
    return valid_input

def window_center():
    lines = [
        'VERSION:',
        'v' + config.VERSION_NUMBER,
        '',
        'DEBUG MODE:',
        'Toggle activation of debug mode by typing "debug mode" followed by enter when in the help screen.',
        '',
        'SKILLS:',
        '- Weapon expertise -',
        'Determines the chance to successfully hit your enemy with a melee weapon',
        'Experience with weapon usage increases expertise over time. Maximum 3 levels of expertise can be gained from prolonged usage alone.',
        'Another level of expertise can be gained from reading an educational book on the subject.',
        'One level of expertise can also be gained through teachings from a learned master.',
        '',
        '- Ranged weapon expertise -',
        'Determines the chance to successfully hit your enemy with a ranged weapon',
        'Experience with ranged weapon usage increases expertise over time. Maximum 3 levels of expertise can be gained from prolonged usage alone.',
        'Another level of expertise can be gained from reading an educational book on the subject.',
        'One level of expertise can also be gained through teachings from a learned master.',
        '',
        'MUSIC:',
        'Lory Werths',
        utils.format_link('mandolingals.tripod.com', 'https://mandolingals.tripod.com/'),
        '',
        'SOUNDS:',
        '100 Retro RPG UI Sound Effects',
        utils.format_link('leohpaz.itch.io', 'https://leohpaz.itch.io/'),
        '',
        'FONTS:',
        'The Ultimate Oldschool PC Font Pack',
        utils.format_link('int10h.org/oldschool-pc-fonts/', 'https://int10h.org/oldschool-pc-fonts/'),
        '',
        'COLOR SCHEMES:',
        'Gogh color scheme collection',
        utils.format_link('github.com/Gogh-Co/Gogh', 'https://github.com/Gogh-Co/Gogh'),
    ]
    return windows.Content(windows.WINDOW_CENTER, lines)