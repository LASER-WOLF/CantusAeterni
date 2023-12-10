# PROJECT
import audio
import config
import system
import utils
import windows

# SET VARS
debug_input_char = None

def run():
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            window_log(),
            window_lower(),
        ])
    ]

def input(key, mod = None):
    global debug_input_char
    debug_input_char = key
    selected_option = config.ui_selection_current
    if key == 'escape' or key == 'mouse3':
        audio.ui_back()
        system.change_mode(config.previous_mode)
    elif key == 'up' and (mod == 'shift' or mod == 'scroll_center'):
        config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST, config.UI_TAGS['scroll_center_up'])
        system.ui_scroll_center_up()
    elif key == 'down' and (mod == 'shift' or mod == 'scroll_center'):
        config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORTEST, config.UI_TAGS['scroll_center_down'])
        system.ui_scroll_center_down()
    elif key == 'up' or (key == 'up' and mod == 'scroll_log'):
        system.ui_log_scroll_up()
    elif key == 'down' or (key == 'down' and mod == 'scroll_log'):
        system.ui_log_scroll_down()

def window_center():
    lines = []
    justnum = 40
    lines.append('Color palette: '.ljust(justnum) + '"' + config.settings['palette'] + '"')
    lines.append('Foreground: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['foreground']) + '        ' + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['foreground']))
    lines.append('Red: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['red']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('Green: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['green']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('Yellow: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['yellow']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_yellow']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['yellow']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_yellow']))
    lines.append('Blue: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['blue']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_blue']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['blue']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_blue']))
    lines.append('Magenta: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['magenta']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_magenta']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['magenta']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_magenta']))
    lines.append('Cyan: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['cyan']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_cyan']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['cyan']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_cyan']))
    lines.append('White: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['white']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_white']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['white']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_white']))
    lines.append('Black: '.ljust(justnum) + utils.add_tag(' NORMAL ', config.TAGS['black']) + utils.add_tag(' BRIGHT ', config.TAGS['bright_black']) + utils.add_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['black']) + ' ' + utils.add_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_black']))
    lines.append("")
    lines.append('Last input: '.ljust(justnum) + '"' + str(debug_input_char)  + '"')
    lines.append('Music status: '.ljust(justnum) + 'Playing: ' + str(audio.music_status()) + ' | Volume: ' + str(config.settings['music_volume']) + ' | Mode: ' + str(audio.music_type) + ' | Title: ' + str(audio.music_title))
    lines.append('')
    lines.append('Statistics:')
    lines.append('Turn #: '.ljust(justnum) + str(config.game['turn']))
    lines.append('Health: '.ljust(justnum) + str(config.player['health_points'])  + ' (' + str(config.player['health_stage']) +')')
    lines.append('Times player has moved: '.ljust(justnum) + str(config.stats['times_moved']))
    lines.append('Times player has entered portal: '.ljust(justnum) + str(config.stats['portals_entered']))
    lines.append('Number of NPCs player has killed: '.ljust(justnum) + str(config.stats['npcs_killed']))
    lines.append('Times player has attacked: '.ljust(justnum) + str(config.stats['times_player_attack']))
    lines.append('Times player has attacked ranged: '.ljust(justnum) + str(config.stats['times_player_attack_ranged']))
    lines.append('Times player has missed: '.ljust(justnum) + str(config.stats['times_player_missed']))
    lines.append('Times player has been attacked: '.ljust(justnum) + str(config.stats['times_npc_attack']))
    lines.append('Times player has been attacked ranged: '.ljust(justnum) + str(config.stats['times_npc_attack_ranged']))
    lines.append('Times attacks has missed player: '.ljust(justnum) + str(config.stats['times_npc_missed']))
    lines.append('Damage player has dealt: '.ljust(justnum) + str(config.stats['damage_dealt']))
    lines.append('Damage player has defended: '.ljust(justnum) + str(config.stats['damage_defended']))
    lines.append('Damage player has received: '.ljust(justnum) + str(config.stats['damage_received']))
    lines.append('Health poits player has healed: '.ljust(justnum) + str(config.stats['health_healed']))
    lines.append('Number of items player has consumed: '.ljust(justnum) + str(config.stats['items_consumed']))
    lines.append('')
    lines.append('Flags:')
    lines.append('show_battle_num: '.ljust(justnum) + str(config.flags['show_battle_num']))
    lines.append('show_player_hp: '.ljust(justnum) + str(config.flags['show_player_hp']))
    lines.append('show_npc_hp: '.ljust(justnum) + str(config.flags['show_npc_hp']))
    lines.append('hide_minimap: '.ljust(justnum) + str(config.flags['hide_minimap']))
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_log():
    lines = []
    lines.extend(windows.log_content(config.debug_log_list, False))
    return windows.Content(windows.WINDOW_LOG, lines)

def window_lower():
    lines = [windows.press_to_go_back_text()]
    return windows.Content(windows.WINDOW_LOWER, lines, min_height = 0)