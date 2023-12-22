# PROJECT
import audio
import config
import system
import utils
import windows

# SET VARS
init_done = False
equipment_changed = None
item_consumed = None

def init():
    global init_done
    global equipments_changed
    global drinks_consumed
    global foods_consumed
    global books_consumed
    init_done = True
    equipments_changed = 0
    drinks_consumed = 0
    foods_consumed = 0
    books_consumed = 0

def run():
    if init_done is False:
        init()
    layers = []
    # MAIN LAYER
    if system.main_content is None or system.popup_content is None:
        system.main_content = windows.main([
                windows.window_upper(),
                window_center(),
                windows.window_lower_back(),
            ])
    layers.append(
        system.main_content
    )
    # POPUP LAYER
    if system.popup_content is not None:
        system.set_selection_options(system.popup_content['options'])
        layers.append(
            windows.popup(system.popup_content['lines'], options = system.ui_selection_options, title = system.popup_content['title'], image = system.popup_content['image'], centered = system.popup_content['centered'])
        )
    return layers

def exit_inventory_screen():
    if equipments_changed > 0:
        system.add_log('You change your equipment.')
    system.run_queued_actions()
    if equipments_changed > 0 or (drinks_consumed + foods_consumed + books_consumed) > 0:
        global init_done
        init_done = False
        system.end_turn('inventory')
    return system.change_mode_previous()

def input_popup(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if selected_option is None:
        if key in config.controls['action']:
            valid_input = True
            config.trigger_animation(config.ANIMATION_UI_CONTINUE_DEFAULT, 'ui_confirm', 'ui', animation_data = config.UI_TAGS['continue'])
            system.unset_popup_content()
    else:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up()
        elif key in config.controls['down']:
           valid_input = system.ui_selection_down()
        elif key in config.controls['back'] or (key in config.controls['action'] and selected_option.name == 'cancel'):
            valid_input = True
            if key in config.controls['action'] and selected_option.name == 'cancel':
                config.trigger_animation(config.ANIMATION_UI_DEFAULT)
            audio.sound_play('ui_back', 'ui')
            system.unset_popup_content()
        elif key in config.controls['action']:
            valid_input = True
            if selected_option.name == "equip":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                equip(selected_option.link)
            elif selected_option.name == "unequip":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                unequip(selected_option.link)
                system.unset_popup_content()
            elif selected_option.name == "consume":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                consume(selected_option.link)
    return valid_input

def input_main(key, mod = None):
    valid_input = False
    selected_option = config.ui_selection_current
    if key in config.controls['back']:
        valid_input = exit_inventory_screen()
    elif selected_option is not None:
        if key in config.controls['up']:
            valid_input = system.ui_selection_up()
        elif key in config.controls['down']:
            valid_input = system.ui_selection_down()
        elif key in config.controls['left']:
            valid_input = system.ui_selection_left(True)
        elif key in config.controls['right']:
            valid_input = system.ui_selection_right(True)
        elif key in config.controls['action']:
            valid_input = True
            if selected_option.name == "item":
                config.trigger_animation(config.ANIMATION_UI_DEFAULT, 'ui_confirm', 'ui')
                examine(selected_option.link)
    return valid_input

def input(key, mod = None):
    if system.popup_content:
        return input_popup(key, mod)
    else:
        return input_main(key, mod)

def window_center():
    ui_blocks = []
    just_num = 30
    equipment_merged = config.equipped_armor | config.equipped_weapons
    empty_text = utils.add_text_tag('Nothing', fg = config.TAG_COLOR_UI_INACTIVE)
    # COMBAT STATUS
    combat_status = []
    damage = config.player['damage_unarmed']
    if config.equipped_weapons['attack'] is not None:
        damage = system.items[config.equipped_weapons['attack']]['damage']
    damage = utils.format_damage_num(damage)
    damage_ranged = 0
    if config.equipped_weapons['attack_ranged'] is not None:
        damage_ranged = system.items[config.equipped_weapons['attack_ranged']]['damage']
    damage_ranged = utils.format_damage_num(damage_ranged)
    defence = utils.format_defence_num(system.check_player_defence(), 6)
    attack_skill = utils.format_skill_num(config.player['skill_level_attack'])
    attack_skill_ranged = utils.format_skill_num(config.player['skill_level_attack_ranged'])
    combat_status.append('COMBAT STATUS:')
    combat_status.append((' ' + config.SKILL_NAMES['attack'].capitalize() + ': ').ljust(just_num) + str(attack_skill))
    combat_status.append((' ' + config.SKILL_NAMES['attack_ranged'].capitalize() + ': ').ljust(just_num) + str(attack_skill_ranged))
    combat_status.append(' Attack damage: '.ljust(just_num) + str(damage))
    combat_status.append(' Ranged attack damage: '.ljust(just_num) + str(damage_ranged))
    combat_status.append(' Defence: '.ljust(just_num) + str(defence))
    combat_status.append('')
    sel_options = [[],[]]
    # EQUIPPED ARMOR / WEAPONS
    for item_type, item_id in equipment_merged.items():
        if item_id is None:
            sel_options[0].append(None)
        else:
            item = system.items[item_id]
            sel_options[0].append(system.SelectionOption("item", utils.format_item_name(item['name'], item['type']), item_id))
    # EQUIPPED RINGS
    if not config.equipped_rings:
        sel_options[0].append(None)
    else:
        for item_id in config.equipped_rings:
            item = system.items[item_id]
            sel_options[0].append(system.SelectionOption("item", utils.format_item_name(item['name'], item['type']), item_id))
    # ITEMS IN INVENTORY
    item_sel_options = []
    for item_id in system.inventory_list:
        sort_num = 0
        item = system.items[item_id]
        if item['type'] == 'book':
            sort_num = 0
        elif item['type'] == 'ring':
            sort_num = 1
        elif item['type'] in config.equipped_armor:
            sort_num = 2
        elif item['type'] in config.equipped_weapons:
            sort_num = 3
        elif item['type'] in config.item_type_consumable:
            sort_num = 4
        elif item['type'] == 'key':
            sort_num = 5
        item_sel_options.append((sort_num, item['type'], item['name'], item_id))
    for sort_num, item_type, item_name, item_id in sorted(item_sel_options):
        sel_options[1].append(system.SelectionOption("item", utils.format_item_name(item_name, item_type, type_abr = True), item_id))
    # FORMAT SELECTION OPTIONS
    system.set_selection_options(sel_options)
    selection_options_display = windows.format_selection_options_display(system.ui_selection_options)
    # FORMAT EQUIPPED ITEMS
    for num, (item_type, item_id) in enumerate(equipment_merged.items()):
        item_content = selection_options_display[0][num]
        if item_id is None:
            item_content = ' ' + empty_text
        selection_options_display[0][num] = (' ' + utils.format_item_type(item_type, colored = False) + ':').ljust(just_num - 2) + ' ' + item_content
    # FORMAT RINGS
    if not config.equipped_rings:
        selection_options_display[0].insert(len(equipment_merged), ' ' + empty_text)
    selection_options_display[0].insert(len(equipment_merged), 'EQUIPPED RINGS:')
    selection_options_display[0].insert(len(equipment_merged), '')
    # ADD TITLES AND MERGE COMBAT STATS
    selection_options_display[0].insert(len(config.equipped_armor), 'EQUIPPED WEAPONS:')
    selection_options_display[0].insert(len(config.equipped_armor), '')
    selection_options_display[0].insert(0, 'EQUIPPED ARMOR:')
    selection_options_display[1].insert(0, 'ITEMS:')
    selection_options_display[0] = combat_status + selection_options_display[0]
    ui_blocks.extend(selection_options_display)
    return windows.Content(windows.WINDOW_CENTER, windows.combine_blocks(ui_blocks, min_size_list = [60]))

def examine(item_id):
    item = system.items[item_id]
    item_equipped = item_id in config.equipped_rings or item_id in config.equipped_armor.values() or item_id in config.equipped_weapons.values()
    item_equippable = item['type'] == 'ring' or item['type'] in config.equipped_armor or item['type'] in config.equipped_weapons
    popup_lines = []
    popup_options = [[]]
    popup_title = item['name'].upper()
    popup_lines.append('Type: ' + utils.format_item_type(item['type']))
    if item['type'] == 'attack' or item['type'] == 'attack_ranged':
        damage_num = utils.format_damage_num(item['damage'])
        popup_lines.append('Damage: ' + damage_num)
    elif item['type'] == 'upper_body' or item['type'] == 'lower_body' or item['type'] == 'head' or item['type'] == 'feet' or item['type'] == 'hands' or item['type'] == 'shield':
        defence_num = utils.format_defence_num(item['defence'])
        popup_lines.append('Defence: ' + defence_num)
        if item['defence'] > 0:
            popup_lines.append('* This item grants you defence against damage in combat *')
    if item_equippable and item['on_equip']:
        text_powers = 'This item is infused with magicks'
        if item['identified'] is True:
            if item['text_identified'] is not None:
                text_powers = item['text_identified']
        else:
            text_powers = 'This item seems to be infused with some mysterious magicks'
            if item['text_unidentified'] is not None:
                text_powers = item['text_unidentified']
        text_powers = utils.add_text_tag('* ' + text_powers + ' *', fg = config.TAG_COLOR_ITEM_MAGICAL)
        popup_lines.append(text_powers)
    for line in item['text']:
        popup_lines.append(utils.format_color_tags(line))
    if item_equipped:
        popup_options[0].append(system.SelectionOption("unequip", 'Unequip item', item_id))
    elif item_equippable:
        popup_options[0].append(system.SelectionOption("equip", 'Equip item', item_id))
    elif item['type'] in config.item_type_consumable:
        consume_text = 'Consume'
        if item['type'] == 'drink':
            consume_text = 'Drink'
        elif item['type'] == 'food':
            consume_text = 'Eat'
        consume_text += ' item'
        if item['consume_text']:
            consume_text = item['consume_text']
        popup_options[0].append(system.SelectionOption("consume", consume_text, item_id))
    popup_options[0].append(system.SelectionOption("cancel", 'Go back'))
    system.set_popup_content(popup_lines, popup_options, title = popup_title)

def handle_item_action(action):
    system.execute_action(action)

def equip(item_id):
    global equipments_changed
    equipments_changed += 1
    item = system.items[item_id]
    if item['type'] in config.equipped_armor and config.equipped_armor[item['type']] is not None:
        unequip(config.equipped_armor[item['type']])
    elif item['type'] in config.equipped_weapons and config.equipped_weapons[item['type']] is not None:
        unequip(config.equipped_weapons[item['type']])
    item['identified'] = True
    if item['type'] == 'ring':
        config.equipped_rings.append(item_id)
    elif item['type'] in config.equipped_armor:
        config.equipped_armor[item['type']] = item_id
    elif item['type'] in config.equipped_weapons:
        config.equipped_weapons[item['type']] = item_id
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
        handle_item_action(action)
    system.set_popup_content(popup_lines, selection_memory = False)

def unequip(item_id):
    global equipments_changed
    equipments_changed += 1
    item = system.items[item_id]
    if item['type'] == 'ring':
        config.equipped_rings.remove(item_id)
    elif item['type'] in config.equipped_armor:
        config.equipped_armor[item['type']] = None
    elif item['type'] in config.equipped_weapons:
        config.equipped_weapons[item['type']] = None
    for action in item['on_unequip']:
        handle_item_action(action)
    system.inventory_list.append(item_id)

def consume(item_id):
    global drinks_consumed
    global foods_consumed
    global books_consumed
    item = system.items[item_id]
    system.inventory_list.remove(item_id)
    consume_type = 'consume'
    if item['type'] == 'drink':
        consume_type = 'drink'
        config.add_to_stats('drinks_consumed', 1)
        drinks_consumed += 1
    elif item['type'] == 'food':
        consume_type = 'eat'
        config.add_to_stats('foods_consumed', 1)
        foods_consumed += 1
    elif item['type'] == 'book':
        consume_type = 'read'
        config.add_to_stats('books_consumed', 1)
        books_consumed += 1
    consume_text = 'You ' + consume_type + ' the ' + item['name'] + '.'
    system.add_log(consume_text)
    popup_lines = []
    popup_lines.append(consume_text)
    if item['on_consume_text']:
        for line in item['on_consume_text']:
            popup_lines.append(line)
    for action in item['on_consume']:
        handle_item_action(action)
    system.set_popup_content(popup_lines, selection_memory = False)