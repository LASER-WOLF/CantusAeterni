# PROJECT
import audio
import config
import system
import utils
import windows

def run():
    return [
        windows.main([
            windows.window_upper(),
            window_center(),
            window_log(),
            windows.window_lower_back(),
        ])
    ]

def input(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if key in config.controls['back']:
        valid_input = system.change_mode_previous()
    elif key in config.controls['scroll_center_up'] or (key in config.controls['up'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_minus('center')
    elif key in config.controls['scroll_center_down'] or (key in config.controls['down'] and (mod in config.controls['mod_scroll_center'])):
        valid_input = system.ui_scroll_plus('center')
    elif key in config.controls['scroll_log_up'] or key in config.controls['up']:
        valid_input = system.ui_scroll_plus('log')
    elif key in config.controls['scroll_log_down'] or key in config.controls['down']:
        valid_input = system.ui_scroll_minus('log')
    return True

def window_center():
    justnum = 40
    lines = []
    lines.append('Color palette: '.ljust(justnum) + '"' + config.settings['palette'] + '"')
    lines.append('Foreground: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['foreground']) + '        ' + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['foreground']))
    lines.append('Red: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['red']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('Green: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['green']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_red']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['red']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_red']))
    lines.append('Yellow: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['yellow']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_yellow']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['yellow']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_yellow']))
    lines.append('Blue: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['blue']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_blue']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['blue']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_blue']))
    lines.append('Magenta: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['magenta']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_magenta']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['magenta']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_magenta']))
    lines.append('Cyan: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['cyan']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_cyan']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['cyan']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_cyan']))
    lines.append('White: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['white']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_white']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['white']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_white']))
    lines.append('Black: '.ljust(justnum) + utils.add_text_tag(' NORMAL ', config.TAGS['black']) + utils.add_text_tag(' BRIGHT ', config.TAGS['bright_black']) + utils.add_text_tag(' NORMAL ', fg = config.TAGS['background'], bg = config.TAGS['black']) + ' ' + utils.add_text_tag(' BRIGHT ', fg = config.TAGS['background'], bg = config.TAGS['bright_black']))
    lines.append("")
    lines.append('Last input device: '.ljust(justnum) + str(config.last_input_device))
    lines.append('Last input: '.ljust(justnum) + str(config.last_input))
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
    return windows.Content(windows.WINDOW_CENTER, lines)

def window_log():
    return windows.Content(windows.WINDOW_LOG, windows.log_content(config.debug_log_list, False))