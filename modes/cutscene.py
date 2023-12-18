# PROJECT
import config
import system
import windows

# SET VARS
cutscene = None

def run():
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            windows.window_lower_continue()
        ])
    ]

def input(key, mod = None):
    valid_input = False
    if key in config.controls['action']:
        valid_input = True
        config.trigger_animation(config.ANIMATION_UI_CONTINUE_DEFAULT, 'ui_confirm', 'ui')
        for line in cutscene['on_exit']:
            system.execute_action(line)
    return valid_input

def window_center():
    return windows.Content(windows.WINDOW_CENTER, load_cutscene(system.active_cutscene))

def load_cutscene(cutscene_id):
    global cutscene
    cutscene = system.cutscenes[cutscene_id]
    config.add_debug_log('Running cutscene -> ' + str(cutscene_id))
    result = []
    if(config.settings['debug_mode']):
        result.append("DEBUG: Running cutscene " + str(cutscene_id))
    for line in cutscene['on_enter']:
        system.execute_action(line)
    for line in cutscene['text']:
        result.append(line)
    return result