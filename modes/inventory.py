# PROJECT
import audio
import config
import system
import windows

def run():
    system.set_selection_options(selection_options())
    return [
        windows.combine([
            windows.window_upper(),
            window_center(),
            window_lower(),
        ])
    ]

def input(key):
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if(key == 'up'):
            system.ui_selection_y_prev()
        elif(key == 'down'):
            system.ui_selection_y_next()
        elif(key == 'escape' or key == 'mouse3' or (key == 'return' and selected_option.name == "back")):
            if key == 'return' and selected_option.name == 'back':
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
            audio.ui_back()
            system.change_mode(config.previous_mode)

def selection_options():
    result = [[
        system.SelectionOption("back", "GO BACK")
    ]]
    return result

def window_center():
    lines = []
    if not system.inventory_list:
        lines.append('(EMPTY)')
    for item_id in system.inventory_list:
        item = system.items[item_id]
        lines.append(' - ' + item['name'].upper() + ' ∙ ' + item['text'].upper())
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options)
    selection_options_display[0].insert(0, 'SELECT OPTION:')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks))