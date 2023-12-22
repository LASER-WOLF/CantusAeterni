# PROJECT
import config
import system
import windows

def run():
    system.set_selection_options(selection_options())
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            windows.window_lower_empty(),
        ])
    ]

def input(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up()
        elif key in config.controls['down'] :
            valid_input = system.ui_selection_down()
        elif key in config.controls['back']:
            if system.ui_quit_prompt:
                valid_input = True
                system.quit_game_prompt()
                config.trigger_animation('fade', 'ui_back', 'ui')
                system.ui_selection_retrieve()
        elif key in config.controls['action'] :
            valid_input = True
            if selected_option.name == "start":
                config.trigger_animation('ui_sel_7', 'ui_confirm_big', 'ui')
                system.initialize_new_game()
            elif selected_option.name == "settings":
                config.trigger_animation('ui_sel_5', 'ui_confirm', 'ui')
                system.change_mode(config.MODE_SETTINGS)
            elif selected_option.name == "debug":
                config.trigger_animation('ui_sel_5', 'ui_confirm', 'ui')
                system.change_mode(config.MODE_DEBUG)
            elif selected_option.name == "help":
                config.trigger_animation('ui_sel_5', 'ui_confirm', 'ui')
                system.change_mode(config.MODE_HELP)
            elif selected_option.name == "quit_game_prompt":
                config.trigger_animation('ui_sel_5', 'ui_confirm', 'ui')
                config.trigger_animation('fade')
                if system.ui_quit_prompt:
                    system.ui_selection_retrieve()
                else:
                    system.ui_selection_store()
                    system.ui_selection_none()
                system.quit_game_prompt()
            elif selected_option.name == "quit_game":
                system.quit_game()
    return valid_input

def selection_options():
    result = []
    if system.ui_quit_prompt:
        result.append(system.SelectionOption("quit_game", "YES"))
        result.append(system.SelectionOption("quit_game_prompt", "NO"))
    else:
        result.append(system.SelectionOption("start", "START GAME"))
        if config.settings['debug_mode']:
            result.append(system.SelectionOption("debug", "DEBUG SCREEN"))
        result.append(system.SelectionOption("settings", "SETTINGS"))
        result.append(system.SelectionOption("help", "HELP"))
        result.append(system.SelectionOption("quit_game_prompt", "QUIT"))
    return [result]

def window_center():
    lines = []
    if system.ui_quit_prompt:
        lines.append('ARE YOU SURE?')
    else:
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('      .g8"""bgd     db      `7MN.   `7MF\'MMP""MM""YMM `7MMF\'   `7MF\'.M"""bgd       ')
        lines.append('    .dP\'     `M    ;MM:       MMN.    M  P\'   MM   `7   MM       M ,MI    "Y       ' )
        lines.append('    dM\'       `   ,V^MM.      M YMb   M       MM        MM       M `MMb.           '  )
        lines.append('    MM           ,M  `MM      M  `MN. M       MM        MM       M   `YMMNq.       '   )
        lines.append('    MM.          AbmmmqMA     M   `MM.M       MM        MM       M .     `MM       '   )
        lines.append('    `Mb.     ,\' A\'     VML    M     YMM       MM        YM.     ,M Mb     dM       ' )
        lines.append('      `"bmmmd\'.AMA.   .AMMA..JML.    YM     .JMML.       `bmmmmd"\' P"Ybmmd"        ' )
        lines.append('                                                                                   '   )
        lines.append('      db      `7MM"""YMM MMP""MM""YMM `7MM"""YMM  `7MM"""Mq.  `7MN.   `7MF\'`7MMF\'  ' )
        lines.append('     ;MM:       MM    `7 P\'   MM   `7   MM    `7    MM   `MM.   MMN.    M    MM    '  )
        lines.append('    ,V^MM.      MM   d        MM        MM   d      MM   ,M9    M YMb   M    MM    '   )
        lines.append('   ,M  `MM      MMmmMM        MM        MMmmMM      MMmmdM9     M  `MN. M    MM    '   )
        lines.append('   AbmmmqMA     MM   Y  ,     MM        MM   Y  ,   MM  YM.     M   `MM.M    MM    '   )
        lines.append('  A\'     VML    MM     ,M     MM        MM     ,M   MM   `Mb.   M     YMM    MM    '  )
        lines.append('.AMA.   .AMMA..JMMmmmmMMM   .JMML.    .JMMmmmmMMM .JMML. .JMM..JML.    YM  .JMML.  '   )
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        lines = windows.line_set_color_multi(lines, config.TAG_COLOR_TITLE_SCREEN)
    lines.extend(windows.format_selection_options_display_bg_centered(system.ui_selection_options, min_size = 30)[0])
    return windows.Content(windows.WINDOW_CENTER, lines, None, windows.FILL_PATTERNS['dots2'], None, True, True)