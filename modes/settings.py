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
            window_center(),
            window_lower(),
        ])
    ]

def input(key, mod = None):
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
            elif selected_option.name == "enable_music_now_playing":
                config.settings['enable_music_now_playing'] = system.ui_selection_option_change_toggle(config.settings['enable_music_now_playing'])
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
    result[0].append(system.SelectionOption("window_mode", "Screen | Window mode:", str(config.settings['window_mode']).capitalize(), "multi", [config.WINDOW_MODE_NORMAL, config.WINDOW_MODE_FULLSCREEN]))
    if config.settings['window_mode'] == config.WINDOW_MODE_NORMAL:
        result[0].append(system.SelectionOption("resolution", "Screen | Resolution (windowed):", str(config.settings['screen_width']) + "x" + str(config.settings['screen_height']), "multi", config.RESOLUTIONS))
    result[0].append(system.SelectionOption("font", "Screen | Font:", str(config.settings['font']), "multi", list(config.FONTS.keys())))
    result[0].append(system.SelectionOption("palette", "Screen | Color palette:", str(config.settings['palette']), "multi", list(config.PALETTES.keys())))
    result[0].append(system.SelectionOption("enable_mouse", "System | Enable mouse:", str(config.settings['enable_mouse']).capitalize(), "toggle"))
    result[0].append(system.SelectionOption("enable_music", "Audio | Enable music:", str(config.settings['enable_music']).capitalize(), "toggle"))
    result[0].append(system.SelectionOption("enable_sound", "Audio | Enable sound:", str(config.settings['enable_sound']).capitalize(), "toggle"))
    if config.settings['enable_sound']:
        result[0].append(system.SelectionOption("enable_sound_ui", "Audio | Enable UI sound:", str(config.settings['enable_sound_ui']).capitalize(), "toggle"))
    result[0].append(system.SelectionOption("master_volume", "Audio | Master volume:", str(round(config.settings['master_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_music']:
        result[0].append(system.SelectionOption("music_volume", "Audio | Music volume:", str(round(config.settings['music_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_sound']:
        result[0].append(system.SelectionOption("sound_volume", "Audio | Sound volume:", str(round(config.settings['sound_volume'] * 10)).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_music']:
        result[0].append(system.SelectionOption("enable_music_now_playing", "Audio | Show title of music track:", str(config.settings['enable_music_now_playing']).capitalize(), "toggle"))
    result[0].append(system.SelectionOption("debug_mode", "Debug | Enable debug mode:", str(config.settings['debug_mode']).capitalize(), "toggle"))
    if config.settings['debug_mode']:
        result[0].append(system.SelectionOption("debug_on_start", "Debug | Debug screen on start:", str(config.settings['debug_on_start']).capitalize(), "toggle"))
        result[0].append(system.SelectionOption("debug_log_to_file", "Debug | Debug log to file:", str(config.settings['debug_log_to_file']).capitalize(), "toggle"))
        result[0].append(system.SelectionOption("debug_error_log_to_file", "Debug | Error log to file:", str(config.settings['debug_error_log_to_file']).capitalize(), "toggle"))
        result[0].append(system.SelectionOption("debug_info_screen", "Debug | Show screen info:", str(config.settings['debug_info_screen']).capitalize(), "multi", ['full', 'compact', 'hide']))
    #result[0].append(system.SelectionOption("back", "GO BACK"))
    return result

def window_center():
    ui_blocks = []
    selection_options_display = windows.format_selection_options_display_modifiable(system.ui_selection_options)
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_CENTER, windows.combine_blocks(ui_blocks))

def window_lower():
    lines = [windows.press_to_go_back_text()]
    return windows.Content(windows.WINDOW_LOWER, lines, min_height = 0)