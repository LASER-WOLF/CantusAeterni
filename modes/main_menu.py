# PROJECT
import audio
import config
import system
import windows

def run():
    system.set_selection_options(selection_options())
    return windows.combine([
        windows.window_upper(),
        window_center(),
        windows.window_lower_empty(),
    ])

def input(key):
    selected_option = config.ui_selection_current
    if selected_option is not None:
        if(key == 'up'):
            system.ui_selection_y_prev()
        elif(key == 'down'):
            system.ui_selection_y_next()
        elif(key == 'escape' or key == 'mouse3'):
            if system.ui_quit_prompt:
                audio.ui_back()
                system.quit_game_prompt()
                config.trigger_animation(config.ANIMATION_FADE)
        elif(key == 'return'):
            if selected_option.name == "start":
                audio.ui_confirm_big()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.initialize_new_game()
            elif selected_option.name == "settings":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_SETTINGS)
            elif selected_option.name == "debug":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_DEBUG)
            elif selected_option.name == "help":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                system.change_mode(config.MODE_HELP)
            elif selected_option.name == "quit_game_prompt":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                config.trigger_animation(config.ANIMATION_FADE)
                system.quit_game_prompt()
            elif selected_option.name == "quit_game":
                system.quit_game()

def selection_options():
    result = []
    if system.ui_quit_prompt:
        result.append([
        system.SelectionOption("quit_game", "YES"),
        system.SelectionOption("quit_game_prompt", "NO"),
        ])
    else:
        result.append([
        system.SelectionOption("start", "START GAME"),
        system.SelectionOption("debug", "DEBUG SCREEN"),
        system.SelectionOption("settings", "SETTINGS"),
        system.SelectionOption("help", "HELP"),
        system.SelectionOption("quit_game_prompt", "QUIT"),
        ])
    return result

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
        lines = windows.line_set_color_multi(lines, windows.TAG_COLOR_TITLE_SCREEN)
    lines.extend(windows.combine_blocks(windows.format_selection_options_display_bg_centered(system.ui_selection_options, 30)))
    return windows.Content(windows.WINDOW_CENTER, lines, None, windows.FILL_PATTERNS['dots2'], None, True, True)