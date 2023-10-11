# PROJECT
import audio
import config
import system
import windows

# SET VARS
cutscene = None

def run():
    system.run_queued_actions()
    return windows.combine([
        windows.window_upper(),
        window_center(),
        window_lower(),
    ])

def input(key):
    if key == 'return' or key == 'mouse1':
        audio.ui_confirm()
        for line in cutscene['on_exit']:
            system.queue_action(line)

def window_center():
    lines = load_cutscene(system.active_cutscene)
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_lower():
    lines = [windows.press_to_continue_text()]
    return windows.Content(windows.WINDOW_LOWER, lines, min_height = 0)

def load_cutscene(cutscene_id):
    global cutscene
    result = []
    if(config.settings['debug_mode']):
        result.append("DEBUG: Running cutscene " + str(cutscene_id))
    cutscene = system.cutscenes[cutscene_id]
    for line in cutscene['on_enter']:
        system.execute_action(line)
    for line in cutscene['text']:
        result.append(line)
    return result