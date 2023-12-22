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
            windows.window_lower_back(),
        ])
    ]

def input(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up_scrollable('center')
        elif key in config.controls['down']:
            valid_input = system.ui_selection_down_scrollable('center')
        elif key in config.controls['back']:
            config.export_settings()
            valid_input = system.change_mode_previous()
        # "TOGGLE" TYPE SETTINGS
        elif selected_option.s_type == "toggle" and (key in config.controls['left'] or key in config.controls['right']):
            valid_input = True
            config.trigger_animation('ui_sel_1', 'ui_sel', 'ui')
            config.settings[selected_option.name] = system.ui_selection_option_change_toggle(config.settings[selected_option.name])
            if selected_option.name == 'enable_music':
                if config.settings['enable_music']:
                    audio.music_play()
                else:
                    audio.music_stop()
        # "SCALE" TYPE SETTINGS
        elif selected_option.s_type == "scale" and (key in config.controls['left'] or key in config.controls['right']):
            plus_value = True
            if key in config.controls['left']:
                plus_value = False
            new_value = system.ui_selection_option_change_scale(config.settings[selected_option.name], selected_option.s_options, plus_value)
            if config.settings[selected_option.name] != new_value:
                config.settings[selected_option.name] = new_value
                config.trigger_animation('ui_sel_1', 'ui_sel', 'ui')
                valid_input = True
                if selected_option.name == 'master_volume':
                    audio.change_master_volume(new_value)
                elif selected_option.name == 'music_volume':
                    audio.change_music_volume(new_value)
                elif selected_option.name == 'sound_volume':
                    audio.change_sound_volume(new_value)
        # "MULTI" TYPE SETTINGS
        elif selected_option.s_type == "multi" and (key in config.controls['left'] or key in config.controls['right']):
            next_value = True
            if key in config.controls['left']:
                next_value = False
            if selected_option.name == 'resolution':
                new_value = system.ui_selection_option_change_multi((config.settings['screen_width'], config.settings['screen_height']), selected_option.s_options, next_value)
                if (config.settings['screen_width'], config.settings['screen_height']) != new_value and config.screen_width_full >= new_value[0] and config.screen_height_full >= new_value[1]:
                    config.settings['screen_width'] = new_value[0]
                    config.settings['screen_height'] = new_value[1]
                    config.trigger_animation('ui_sel_1', 'ui_sel', 'ui')
                    config.display_changed = True
                    valid_input = True
            else:
                new_value = system.ui_selection_option_change_multi(config.settings[selected_option.name], selected_option.s_options, next_value)
                if config.settings[selected_option.name] != new_value:
                    config.settings[selected_option.name] = new_value
                    config.trigger_animation('ui_sel_1', 'ui_sel', 'ui')
                    valid_input = True
                    if selected_option.name == 'window_mode':
                        config.display_changed = True
                    elif selected_option.name == 'aspect_ratio':
                        config.display_changed = True
                        config.settings['screen_width'] = config.RESOLUTIONS[config.settings['aspect_ratio']][0][0]
                        config.settings['screen_height'] = config.RESOLUTIONS[config.settings['aspect_ratio']][0][1]
                    elif selected_option.name == 'font':
                        config.font_changed = True
                    elif selected_option.name == 'palette':
                        config.palette_changed = True
    return valid_input

def selection_options():
    result = []
    result.append(system.SelectionOption("window_mode", "Screen | Window mode:", str(config.settings['window_mode']).capitalize(), "multi", [config.WINDOW_MODE_NORMAL, config.WINDOW_MODE_FULLSCREEN]))
    if config.settings['window_mode'] == config.WINDOW_MODE_NORMAL:
        result.append(system.SelectionOption("aspect_ratio", "Screen | Windowed mode, aspect ratio:", str(config.settings['aspect_ratio']), "multi", list(config.RESOLUTIONS.keys())))
        result.append(system.SelectionOption("resolution", "Screen | Windowed mode, resolution:", str(config.settings['screen_width']) + "x" + str(config.settings['screen_height']), "multi", [resolution for resolution in config.RESOLUTIONS[config.settings['aspect_ratio']] if resolution[0] <= config.screen_width_full and resolution[1] <= config.screen_height_full]))
    result.append(system.SelectionOption("font", "Screen | Font:", str(config.settings['font']), "multi", list(config.FONTS.keys())))
    result.append(system.SelectionOption("palette", "Screen | Color palette:", str(config.settings['palette']), "multi", list(config.PALETTES.keys())))
    result.append(system.SelectionOption("enable_mouse", "System | Enable mouse:", str(config.settings['enable_mouse']).capitalize(), "toggle"))
    result.append(system.SelectionOption("enable_joystick", "System | Enable joystick:", str(config.settings['enable_joystick']).capitalize(), "toggle"))
    result.append(system.SelectionOption("enable_music", "Audio | Enable music:", str(config.settings['enable_music']).capitalize(), "toggle"))
    result.append(system.SelectionOption("enable_sound", "Audio | Enable sound:", str(config.settings['enable_sound']).capitalize(), "toggle"))
    if config.settings['enable_sound']:
        result.append(system.SelectionOption("enable_sound_ui", "Audio | Enable UI sound:", str(config.settings['enable_sound_ui']).capitalize(), "toggle"))
    result.append(system.SelectionOption("master_volume", "Audio | Master volume:", str(config.settings['master_volume']).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_music']:
        result.append(system.SelectionOption("music_volume", "Audio | Music volume:", str(config.settings['music_volume']).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_sound']:
        result.append(system.SelectionOption("sound_volume", "Audio | Sound volume:", str(config.settings['sound_volume']).zfill(2) + " / 10", "scale", (0, 10, 1)))
    if config.settings['enable_music']:
        result.append(system.SelectionOption("enable_music_now_playing", "Audio | Show title of music track:", str(config.settings['enable_music_now_playing']).capitalize(), "toggle"))
    if config.settings['debug_mode']:
        result.append(system.SelectionOption("debug_mode", "Debug | Enable debug mode:", str(config.settings['debug_mode']).capitalize(), "toggle"))
        result.append(system.SelectionOption("debug_print", "Debug | Print detailed debug messages:", str(config.settings['debug_print']).capitalize(), "toggle"))
        result.append(system.SelectionOption("debug_log_to_file", "Debug | Debug log to file:", str(config.settings['debug_log_to_file']).capitalize(), "toggle"))
        result.append(system.SelectionOption("debug_error_log_to_file", "Debug | Error log to file:", str(config.settings['debug_error_log_to_file']).capitalize(), "toggle"))
        result.append(system.SelectionOption("debug_info_screen", "Debug | Show screen info:", str(config.settings['debug_info_screen']).capitalize(), "multi", ['hide', 'compact', 'full']))
        result.append(system.SelectionOption("visual_enable_extended_boot_animation", "Visual | Enable extended boot animation:", str(config.settings['visual_enable_extended_boot_animation']).capitalize(), "toggle"))
        result.append(system.SelectionOption("visual_enable_popup_window_shadow", "Visual | Popup window, enable window shadow:", str(config.settings['visual_enable_popup_window_shadow']).capitalize(), "toggle"))
        result.append(system.SelectionOption("visual_enable_popup_fill", "Visual | Popup window, enable background fill:", str(config.settings['visual_enable_popup_fill']).capitalize(), "toggle"))
        result.append(system.SelectionOption("visual_enable_scroll_log_arrows", "Visual | Enable arrows on log window scrollbar:", str(config.settings['visual_enable_scroll_log_arrows']).capitalize(), "toggle"))
    return [result]

def window_center():
    return windows.Content(windows.WINDOW_CENTER, windows.format_selection_options_display_modifiable(system.ui_selection_options)[0], selection_scroll = True)