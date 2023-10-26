# PROJECT
import audio
import config
import system
import windows

def run():
    system.set_selection_options(selection_options())
    return [
        windows.main([
            windows.window_upper(),
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
            config.export_settings()
            system.change_mode(config.previous_mode)
        elif(selected_option.s_type == "toggle" and (key == "return" or key == "left" or key == "right")):
            if selected_option.name == "debug_mode":
                config.settings['debug_mode'] = system.ui_selection_option_change_toggle(config.settings['debug_mode'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "debug_on_start":
                config.settings['debug_on_start'] = system.ui_selection_option_change_toggle(config.settings['debug_on_start'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "debug_log_to_file":
                config.settings['debug_log_to_file'] = system.ui_selection_option_change_toggle(config.settings['debug_log_to_file'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "debug_error_log_to_file":
                config.settings['debug_error_log_to_file'] = system.ui_selection_option_change_toggle(config.settings['debug_error_log_to_file'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "enable_minimap":
                config.settings['enable_minimap'] = system.ui_selection_option_change_toggle(config.settings['enable_minimap'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "enable_music":
                config.settings['enable_music'] = system.ui_selection_option_change_toggle(config.settings['enable_music'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                if config.settings['enable_music']:
                    audio.music_play()
                else:
                    audio.music_stop()
            elif selected_option.name == "enable_sound":
                config.settings['enable_sound'] = system.ui_selection_option_change_toggle(config.settings['enable_sound'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "enable_sound_ui":
                config.settings['enable_sound_ui'] = system.ui_selection_option_change_toggle(config.settings['enable_sound_ui'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "enable_mouse":
                config.settings['enable_mouse'] = system.ui_selection_option_change_toggle(config.settings['enable_mouse'])
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
        elif(selected_option.s_type == "scale"):
            if selected_option.name == "master_volume":
                if key == "left":
                    config.settings['master_volume'] = round((system.ui_selection_option_change_scale_dec(config.settings['master_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_master_volume(config.settings['master_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['master_volume'] = round((system.ui_selection_option_change_scale_inc(config.settings['master_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_master_volume(config.settings['master_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "music_volume":
                if key == "left":
                    config.settings['music_volume'] = round((system.ui_selection_option_change_scale_dec(config.settings['music_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_music_volume(config.settings['music_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['music_volume'] = round((system.ui_selection_option_change_scale_inc(config.settings['music_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_music_volume(config.settings['music_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "sound_volume":
                if key == "left":
                    config.settings['sound_volume'] = round((system.ui_selection_option_change_scale_dec(config.settings['sound_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_sound_volume(config.settings['sound_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['sound_volume'] = round((system.ui_selection_option_change_scale_inc(config.settings['sound_volume'] * 10, selected_option.s_options) / 10), 1)
                    audio.change_sound_volume(config.settings['sound_volume'])
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
        elif(selected_option.s_type == "multi"):
            if selected_option.name == "window_mode":
                if key == "left":
                    config.settings['window_mode'] = system.ui_selection_option_change_multi_prev(config.settings['window_mode'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['window_mode'] = system.ui_selection_option_change_multi_next(config.settings['window_mode'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "font":
                if key == "left":
                    config.settings['font'] = system.ui_selection_option_change_multi_prev(config.settings['font'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['font'] = system.ui_selection_option_change_multi_next(config.settings['font'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "palette":
                if key == "left":
                    config.settings['palette'] = system.ui_selection_option_change_multi_prev(config.settings['palette'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['palette'] = system.ui_selection_option_change_multi_next(config.settings['palette'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "resolution":
                if key == "left":
                    resolution = system.ui_selection_option_change_multi_prev((config.settings['screen_width'], config.settings['screen_height']), selected_option.s_options)
                    config.settings['screen_width'] = resolution[0]
                    config.settings['screen_height'] = resolution[1]
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    resolution = system.ui_selection_option_change_multi_next((config.settings['screen_width'], config.settings['screen_height']), selected_option.s_options)
                    config.settings['screen_width'] = resolution[0]
                    config.settings['screen_height'] = resolution[1]
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
            elif selected_option.name == "debug_info_screen":
                if key == "left":
                    config.settings['debug_info_screen'] = system.ui_selection_option_change_multi_prev(config.settings['debug_info_screen'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)
                elif key == "right":
                    config.settings['debug_info_screen'] = system.ui_selection_option_change_multi_next(config.settings['debug_info_screen'], selected_option.s_options)
                    config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST)

def selection_options():
    result = [[]]
    result[0].append(system.SelectionOption("window_mode", "SCREEN, WINDOW MODE:", str(config.settings['window_mode']).upper(), "multi", [config.WINDOW_MODE_NORMAL, config.WINDOW_MODE_FULLSCREEN]))
    if config.settings['window_mode'] == config.WINDOW_MODE_NORMAL:
        result[0].append(system.SelectionOption("resolution", "SCREEN, RESOLUTION (WINDOWED):", str(config.settings['screen_width']) + "x" + str(config.settings['screen_height']), "multi", config.RESOLUTIONS))
    result[0].append(system.SelectionOption("font", "SCREEN, FONT:", str(config.settings['font']).upper(), "multi", list(config.FONTS.keys())))
    result[0].append(system.SelectionOption("palette", "SCREEN, COLOR PALETTE:", str(config.settings['palette']).upper(), "multi", list(config.PALETTES.keys())))
    result[0].append(system.SelectionOption("enable_mouse", "SYSTEM, ENABLE MOUSE:", str(config.settings['enable_mouse']).upper(), "toggle"))
    result[0].append(system.SelectionOption("enable_minimap", "OTHER, ENABLE MINIMAP:", str(config.settings['enable_minimap']).upper(), "toggle"))
    result[0].append(system.SelectionOption("enable_music", "AUDIO, ENABLE MUSIC:", str(config.settings['enable_music']).upper(), "toggle"))
    result[0].append(system.SelectionOption("enable_sound", "AUDIO, ENABLE SOUND:", str(config.settings['enable_sound']).upper(), "toggle"))
    if config.settings['enable_sound']:
        result[0].append(system.SelectionOption("enable_sound_ui", "AUDIO, ENABLE UI SOUND:", str(config.settings['enable_sound_ui']).upper(), "toggle"))
    result[0].append(system.SelectionOption("master_volume", "AUDIO, MASTER VOLUME:", str(round(config.settings['master_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_music']:
        result[0].append(system.SelectionOption("music_volume", "AUDIO, MUSIC VOLUME:", str(round(config.settings['music_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_sound']:
        result[0].append(system.SelectionOption("sound_volume", "AUDIO, SOUND VOLUME:", str(round(config.settings['sound_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    result[0].append(system.SelectionOption("debug_mode", "DEBUG, ENABLE DEBUG MODE:", str(config.settings['debug_mode']).upper(), "toggle"))
    if config.settings['debug_mode']:
        result[0].append(system.SelectionOption("debug_on_start", "DEBUG, DEBUG SCREEN ON START:", str(config.settings['debug_on_start']).upper(), "toggle"))
        result[0].append(system.SelectionOption("debug_log_to_file", "DEBUG, DEBUG LOG TO FILE:", str(config.settings['debug_log_to_file']).upper(), "toggle"))
        result[0].append(system.SelectionOption("debug_error_log_to_file", "DEBUG, ERROR LOG TO FILE:", str(config.settings['debug_error_log_to_file']).upper(), "toggle"))
        result[0].append(system.SelectionOption("debug_info_screen", "DEBUG, SHOW SCREEN INFO:", str(config.settings['debug_info_screen']).upper(), "multi", ['full', 'compact', 'hide']))
    result[0].append(system.SelectionOption("back", "GO BACK"))
    return result

def window_lower():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display_modifiable(system.ui_selection_options)
    #selection_options_display[0].insert(0, 'SELECT OPTION:')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_LOWER, windows.combine_blocks(ui_blocks))