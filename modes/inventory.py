# PROJECT
import audio
import config
import system
import utils
import windows

def run():
    layers = []
    # MAIN LAYER
    if system.main_content is None or system.popup_content is None:
        system.main_content = windows.main([
                windows.window_upper(),
                window_center(),
                window_lower(),
            ])
    layers.append(
        system.main_content
    )
    # POPUP LAYER
    if system.popup_content is not None:
        system.set_selection_options(system.popup_content['options'])
        layers.append(
            windows.popup(system.popup_content['lines'], options = system.ui_selection_options, centered = system.popup_content['centered'])
        )
    return layers


def input_popup(key, mod = None):
    selected_option = config.ui_selection_current
    if selected_option is None:
        if key == 'return' or key == 'mouse1':
            config.trigger_animation(config.ANIMATION_UI_SELECTION_FG)
            audio.ui_confirm()
            config.trigger_animation(config.ANIMATION_FADE)
            system.unset_popup_content()
    else:
        if key == 'up':
            system.ui_selection_y_prev()
        elif key == 'down':
            system.ui_selection_y_next()
        elif key == 'escape' or key == 'mouse3' or (key == 'return' and selected_option.name == 'cancel'):
            if key == 'return' and selected_option.name == 'cancel':
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
            audio.ui_back()
            config.trigger_animation(config.ANIMATION_FADE)
            system.unset_popup_content()
        elif key == 'return':
            if selected_option.name == "equip":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                equip(selected_option.link)
            elif selected_option.name == "unequip":
                audio.ui_back()
                config.trigger_animation(config.ANIMATION_UI_SELECTION)
                unequip(selected_option.link)
                config.trigger_animation(config.ANIMATION_FADE)
                system.unset_popup_content()

def input_main(key, mod = None):
    selected_option = config.ui_selection_current
    if key == 'escape' or key == 'mouse3':
        audio.ui_back()
        system.change_mode(config.previous_mode)
    elif selected_option is not None:
        if key == 'up':
            system.ui_selection_y_prev()
        elif key == 'down':
            system.ui_selection_y_next()
        elif(key == 'left'):
            system.ui_selection_x_prev()
        elif(key == 'right'):
            system.ui_selection_x_next()
        elif key == 'return':
            if selected_option.name == "item":
                audio.ui_confirm()
                config.trigger_animation(config.ANIMATION_UI_SELECTION_SHORT)
                examine(selected_option.link)

def input(key, mod = None):
    if system.popup_content:
        input_popup(key, mod)
    else:
        input_main(key, mod)

def window_center():
    ui_blocks = []
    sel_options = [[],[]]
    for item_type, item_id in config.equipment.items():
        if item_id is None:
            sel_options[0].append(None)
        else:
            item = system.items[item_id]
            sel_options[0].append(system.SelectionOption("item", item['name'].upper(), item_id))
    if not config.rings:
        sel_options[0].append(None)
    else:
        for item_id in config.rings:
            item = system.items[item_id]
            sel_options[0].append(system.SelectionOption("item", item['name'].upper(), item_id))
    if system.inventory_list:
        for item_id in system.inventory_list:
            item = system.items[item_id]
            sel_options[1].append(system.SelectionOption("item", item['name'].upper(), item_id))
    system.set_selection_options(sel_options)
    equipment_just_num = 30
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options, min_size = equipment_just_num)
    for num, (item_type, item_id) in enumerate(config.equipment.items()):
        item_content = selection_options_display[0][num]
        if item_id is None:
            item_content = '(NONE)'.ljust(equipment_just_num)
        selection_options_display[0][num] = (utils.format_item_type(item_type).upper() + ':').ljust(20) + ' ' + item_content
    if not config.rings:
        selection_options_display[0].insert(len(config.equipment), '(NONE)')
    selection_options_display[0].insert(len(config.equipment), 'EQUIPPED RINGS:')
    selection_options_display[0].insert(len(config.equipment), '')
    selection_options_display[0].insert(0, 'EQUIPPED ARMOR / WEAPONS:')
    selection_options_display[1].insert(0, 'ITEMS:')
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_CENTER, windows.combine_blocks(ui_blocks))

def window_lower():
    lines = [windows.press_to_go_back_text()]
    return windows.Content(windows.WINDOW_LOWER, lines, min_height = 0)

def examine(item_id):
    item = system.items[item_id]
    item_equipped = item_id in config.rings or item_id in config.equipment.values()
    item_equippable = item['type'] == 'ring' or item['type'] in config.equipment
    popup_lines = []
    popup_options = [[]]
    popup_lines.append(item['name'].upper())
    popup_lines.append('Type: ' + utils.format_item_type(item['type']).capitalize())
    if item['type'] == 'attack' or item['type'] == 'attack_ranged':
        damage_num = utils.format_damage_num(item['damage'])
        popup_lines.append('Damage: ' + damage_num.capitalize())
    elif item['type'] == 'upper_body' or item['type'] == 'lower_body' or item['type'] == 'head' or item['type'] == 'feet' or item['type'] == 'hands' or item['type'] == 'shield':
        defence_num = utils.format_defence_num(item['defence'])
        popup_lines.append('Defence: ' + defence_num.capitalize())
    if item_equippable and item['on_equip']:
        text_powers = 'This item is infused with magicks'
        if item['identified'] is True:
            if item['text_identified'] is not None:
                text_powers = item['text_identified']
        else:
            text_powers = 'This item seems to be infused with some mysterious magicks'
            if item['text_unidentified'] is not None:
                text_powers = item['text_unidentified']
        popup_lines.append('* ' + text_powers + ' *')
    for line in item['text']:
        popup_lines.append(utils.format_color_tags(line))
    if item_equipped:
        popup_options[0].append(system.SelectionOption("unequip", 'Unequip item', item_id))
    elif item_equippable:
        popup_options[0].append(system.SelectionOption("equip", 'Equip item', item_id))
    popup_options[0].append(system.SelectionOption("cancel", 'Go back'))
    system.set_popup_content(popup_lines, popup_options)

def equip(item_id):
    item = system.items[item_id]
    if item['type'] in config.equipment and config.equipment[item['type']] is not None:
        unequip(config.equipment[item['type']])
    item['identified'] = True
    if item['type'] == 'ring':
        config.rings.append(item_id)
    else:
        config.equipment[item['type']] = item_id
    system.inventory_list.remove(item_id)
    popup_lines = []
    equip_text = ''
    if item['type'] == 'ring':
        equip_text = 'You put the ' + item['name'] + ' on your finger.'
    elif item['type'] == 'head':
        equip_text = 'You put the ' + item['name'] + ' on your head.'
    elif item['type'] == 'upper_body':
        equip_text = 'You put the ' + item['name'] + ' on your upper body.'
    elif item['type'] == 'lower_body':
        equip_text = 'You put the ' + item['name'] + ' on your lower body.'
    elif item['type'] == 'hands':
        equip_text = 'You put the ' + item['name'] + ' on your hands.'
    elif item['type'] == 'feet':
        equip_text = 'You put the ' + item['name'] + ' on your feet.'
    elif item['type'] == 'attack':
        equip_text = 'You take the ' + item['name'] + ' as your active weapon.'
    elif item['type'] == 'attack_ranged':
        equip_text = 'You take the ' + item['name'] + ' as your active ranged weapon.'
    elif item['type'] == 'shield':
        equip_text = 'You take the ' + item['name'] + ' as your active shield.'
    popup_lines.append(equip_text)
    if item['on_equip_text']:
        for line in item['on_equip_text']:
            popup_lines.append(line)
    for action in item['on_equip']:
        system.execute_action(action)
    system.set_popup_content(popup_lines)

def unequip(item_id):
    item = system.items[item_id]
    if item['type'] == 'ring':
        config.rings.remove(item_id)
    else:
        config.equipment[item['type']] = None
    for action in item['on_unequip']:
        system.execute_action(action)
    system.inventory_list.append(item_id)
