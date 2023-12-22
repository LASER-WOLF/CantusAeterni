# BUILT-IN
import re

# PROJECT
import audio
import config
import utils

class Content:
    def __init__(self, w_type = None, lines = None, line_color = None, fill = None, fill_color = None, centered_horizontal = False, centered_vertical = False, min_height = None, selection_scroll = False):
        self.w_type = w_type
        self.lines = lines
        self.line_color = line_color
        self.fill = fill
        self.fill_color = fill_color
        self.centered_horizontal = centered_horizontal
        self.centered_vertical = centered_vertical
        self.min_height = min_height
        self.selection_scroll = selection_scroll

class Line:
    def __init__(self, content, color = None, fill = None, fill_color = None, centered = False):
        self.content = content
        self.color = color
        self.fill = fill
        self.fill_color = fill_color
        self.centered = centered

# SET CONSTANTS
WINDOW_UPPER = "upper"
WINDOW_CENTER = "center"
WINDOW_LOWER = "lower"
WINDOW_LOG = "log"

# SET CONSTANTS, FILL
FILL_PATTERNS = {
    'dots1': [
        "  .",
        ".  "
    ],
    'dots2': [
        "      ",
        " '    ",
        "      ",
        "      ",
        "    ` ",
        "      ",
    ],
    'crosses1': [
        " ┼    ",
        "      ",
        "    ┼ ",
    ],
    'floral1': [
        " .'    ",
        "       ",
        "    `. ",
    ],
    'arrows1': [
        " »    ",
        "    « ",
    ],
    'stars1': [
        "     *  ",
        "      -    ",
        "    *     ",
        "    -      ",
        "  *   ",
        "       - ",
        "      * ",
        "  -       ",
        " *      ",
        " -    ",
    ],
    'fade1': [
        "░",
    ],
}
FILL_PATTERN_COLORS = {
    'rygmc': [
        'red',
        'yellow',
        'green',
        'magenta',
        'cyan',
    ]
}

# SET CONSTANTS, MINIMAP
MINIMAP_TILES = {  
    'undiscovered_top': utils.add_text_tag("     ", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_mid': utils.add_text_tag("  -  ", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_low': utils.add_text_tag("     ", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_top_upper_left': utils.add_text_tag("┌─   ", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_top_upper_right': utils.add_text_tag("   ─┐", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_bottom_lower_left': utils.add_text_tag("└─   ", config.TAG_COLOR_MAP_INACTIVE),
    'undiscovered_bottom_lower_right': utils.add_text_tag("   ─┘", config.TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_mid': utils.add_text_tag("║ - ║", config.TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_MAP_INACTIVE),
    'visited_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_MAP_INACTIVE),
    'visited_mid': utils.add_text_tag("│   │", config.TAG_COLOR_MAP_INACTIVE),
    'visited_low': utils.add_text_tag("└───┘", config.TAG_COLOR_MAP_INACTIVE),
    'selected_visited_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_MAP_INACTIVE),
    'selected_visited_mid': utils.add_text_tag("║   ║", config.TAG_COLOR_MAP_INACTIVE),
    'selected_visited_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_MAP_INACTIVE),
    'current_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_MAP_SELECTED),
    'current_mid': utils.add_text_tag("│YOU│", config.TAG_COLOR_MAP_SELECTED),
    'current_low': utils.add_text_tag("└───┘", config.TAG_COLOR_MAP_SELECTED),
    'selected_current_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_MAP_SELECTED),
    'selected_current_mid': utils.add_text_tag("║YOU║", config.TAG_COLOR_MAP_SELECTED),
    'selected_current_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_MAP_SELECTED),
    'portal_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_PORTAL),
    'portal_mid': utils.add_text_tag("││→││", config.TAG_COLOR_PORTAL),
    'portal_low': utils.add_text_tag("└───┘", config.TAG_COLOR_PORTAL),
    'selected_portal_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_PORTAL),
    'selected_portal_mid': utils.add_text_tag("║│→│║", config.TAG_COLOR_PORTAL),
    'selected_portal_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_PORTAL),
    'portal_current_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_PORTAL),
    'portal_current_mid': utils.add_text_tag("│", config.TAG_COLOR_PORTAL) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("│", config.TAG_COLOR_PORTAL),
    'portal_current_low': utils.add_text_tag("└───┘", config.TAG_COLOR_PORTAL),
    'selected_portal_current_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_PORTAL),
    'selected_portal_current_mid': utils.add_text_tag("║", config.TAG_COLOR_PORTAL) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("║", config.TAG_COLOR_PORTAL),
    'selected_portal_current_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_PORTAL),
    'interactable_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_INTERACTABLE),
    'interactable_mid': utils.add_text_tag("│???│", config.TAG_COLOR_INTERACTABLE),
    'interactable_low': utils.add_text_tag("└───┘", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_mid': utils.add_text_tag("║???║", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_INTERACTABLE),
    'interactable_current_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_INTERACTABLE),
    'interactable_current_mid': utils.add_text_tag("│", config.TAG_COLOR_INTERACTABLE) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("│", config.TAG_COLOR_INTERACTABLE),
    'interactable_current_low': utils.add_text_tag("└───┘", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_mid': utils.add_text_tag("║", config.TAG_COLOR_INTERACTABLE) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("║", config.TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_INTERACTABLE),
    'npc_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_NPC),
    'npc_mid': utils.add_text_tag("│NPC│", config.TAG_COLOR_NPC),
    'npc_low': utils.add_text_tag("└───┘", config.TAG_COLOR_NPC),
    'selected_npc_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_NPC),
    'selected_npc_mid': utils.add_text_tag("║NPC║", config.TAG_COLOR_NPC),
    'selected_npc_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_NPC),
    'npc_current_top': utils.add_text_tag("┌───┐", config.TAG_COLOR_NPC),
    'npc_current_mid': utils.add_text_tag("│", config.TAG_COLOR_NPC) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("│", config.TAG_COLOR_NPC),
    'npc_current_low': utils.add_text_tag("└───┘", config.TAG_COLOR_NPC),
    'selected_npc_current_top': utils.add_text_tag("╔═══╗", config.TAG_COLOR_NPC),
    'selected_npc_current_mid': utils.add_text_tag("║", config.TAG_COLOR_NPC) + utils.add_text_tag("YOU", config.TAG_COLOR_MAP_SELECTED) + utils.add_text_tag("║", config.TAG_COLOR_NPC),
    'selected_npc_current_low': utils.add_text_tag("╚═══╝", config.TAG_COLOR_NPC),
}

def main(target_list):
    # FIND UPPER AND LOWER WINDOWS
    size_upper = 0
    size_lower = 0
    content_upper = []
    content_lower = []
    for window in target_list:
        if window.w_type == WINDOW_UPPER:
            window_formatted = upper(window)
            content_upper.append(window_formatted)
            size_upper += len(window_formatted)
        elif window.w_type == WINDOW_LOWER:
            window_formatted = lower(window)
            content_lower.append(window_formatted)
            size_lower += len(window_formatted)
        elif window.w_type == WINDOW_LOG:
            window_formatted = log(window)
            content_lower.append(window_formatted)
            size_lower += len(window_formatted)
    # FIND CENTER WINDOW
    content_center = []
    for window in target_list:
        if window.w_type == WINDOW_CENTER:
            content_center.append(center(window, size_upper, size_lower))
    # COMBINE ALL WINDOWS
    result = make_lines_multi(content_upper + content_center + content_lower)
    return (config.LAYER_TYPE_MAIN, result, None, None)

def popup(content, options = None, title = None, image = None, fill = '░', fill_color = 'bright_black', fg_color = None, bg_color = None, border_color = None, centered = False, margin = 2, min_width = 36):
    if config.settings['visual_enable_popup_fill'] is False:
        fill = None
    if fg_color is None:
        fg_color = 'foreground'
    if bg_color is None:
        bg_color = 'black'
    if border_color is None:
        border_color = 'foreground'
    width = utils.list_longest_entry_length([utils.remove_all_tags(line) for line in content])
    max_width = config.size_x - (round(config.size_x * 0.2) + ((margin * 2) + 2))
    width = min(max(width, min_width), max_width)
    if image is not None:
        width = max(width, utils.list_longest_entry_length([utils.remove_all_tags(line) for line in image]))
    if title is not None:
        title_formatted = title.upper()
        if len(title_formatted) + 4 > max_width:
            title_formatted = title_formatted[:max_width - 7] + '...'
        title_formatted = '« ' + title_formatted +  ' »'
        width = max(width, len(title_formatted))
    # SELECTION OPTIONS
    content_options = []
    if options is None:
        press_to_contine_option = press_to_continue_text()
        content_options.append(press_to_contine_option)
    else:
        content_options.append('SELECT ACTION:')
        content_options.extend(format_selection_options_display(options, enable_justnum = False)[0])
    content_options = word_wrap(content_options, max_width)
    width = max(width, utils.list_longest_entry_length([utils.remove_all_tags(line) for line in content_options]))
    wrapped_lines = word_wrap(content, max_width)
    wrapped_lines = scrollable_content_center(wrapped_lines, config.size_y - round(config.size_y * 0.4) - len(content_options))
    # SET BACKGROUND AND BORDERS
    if fill:
        fill = fill_empty_space('', length = width + (margin * 2) + 2, char = fill)
    border_hor = fill_empty_space('', width + (margin * 2), '═', centered = centered)
    first_line = utils.add_text_tag('╔' + border_hor + '╗', config.TAGS[border_color])
    final_line = utils.add_text_tag('╚' + border_hor + '╝', config.TAGS[border_color])
    border_ver = utils.add_text_tag('║', config.TAGS[border_color])
    border_margin = fill_empty_space('', margin)
    border_left = border_ver + border_margin
    border_right = border_margin + border_ver
    # ADD VERTICAL SPACING
    content_combine = []
    spacing = 0.75
    spacer = ('', spacing, 'other')
    content_combine.append(('', 0, 'other'))
    if image is not None:
        for num, line in enumerate(image):
            offset = 0
            if num == 0:
                offset = spacing
            content_combine.append((line, offset, 'image'))
        content_combine.append(('', 0, 'other'))
    if title is not None:
        content_combine.append((title_formatted, spacing, 'title'))
        content_combine.append(('', 0, 'other'))
    for num, line in enumerate(wrapped_lines):
        offset = 0
        if num == 0:
            offset = spacing
        content_combine.append((line, offset, 'content'))
    content_combine.append(spacer)
    content_combine.append(('-' * width, 0,'other'))
    content_combine.append(spacer)
    for num, line in enumerate(content_options):
        content_combine.append((line, 0, 'options'))
    content_combine.append(spacer)
    # FORMAT FINAL CONTENT
    result = []
    result.append((first_line, 0))
    for num, (line, line_offset, line_type) in enumerate(content_combine):
        line_centered = False
        if line_type == 'content' or line_type == 'title' or line_type == 'image':
            line_centered = centered
        line_color = None
        line_without_tags = utils.remove_all_tags(line)
        line_formatted = border_left + fill_empty_space(line, width - len(line_without_tags), centered = line_centered) + border_right
        result.append((line_formatted, line_offset))
    result.append((final_line, 0))
    return (config.LAYER_TYPE_POPUP, result, fg_color, bg_color, (fill, fill_color))

def upper(content):
    lines = []
    # INIT FILL
    fill, fill_list, fill_num = fill_init(content.fill)
    fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
    # FIRST LINE EMPTY
    lines.append(Line("", None, fill, fill_color))
    # INCREMENT FILL
    fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
    fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
    # CONTENT
    if content.lines:
        for num, line in enumerate(content.lines):
            lines.append(Line(line, content.line_color, fill, fill_color))
            # INCREMENT FILL
            fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
            fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
    # EMPTY LINE
    else:
        lines.append(Line("", None, fill, fill_color))
    lines.append(seperator())
    return lines

def word_wrap(target_list, max_width, numbered_list = False, new_line_padding = False, line_prefix = None):
    def add_word(line, word):
        if line != '':
            line += ' '
        line += word
        return line, ''
    result = []
    for line_num, line in enumerate(target_list):
        if numbered_list is True:
            line_num = line[0]
            line = line[1]
        # WRAP LINE IF TOO LONG
        if len(utils.remove_all_tags(line)) > max_width:
            word = new_line = ''
            text_tag = text_tag_search = ui_tag = ui_tag_search = ui_tag_data = None
            text_tag_word_num = ui_tag_word_num = 0
            if line_prefix is not None:
                word = line_prefix
            for character_num, character in enumerate(line):
                line_count = 0
                word_finished = False
                # LOOK FOR TAGS
                if text_tag_search is None:
                    text_tag_search = re.search('<text=(.{2}):(.{2}):(.{2})>',  word)
                # TAG FOUND
                if text_tag_search is not None:
                    text_tag = (text_tag_search.string, '</text>')
                    text_tag_search_end = re.search('</text>',  word)
                    if text_tag_search_end:
                        text_tag = text_tag_search = None
                        text_tag_word_num = 0
                # LOOK FOR TAGS
                if ui_tag_search is None:
                    ui_tag_search = re.search('<ui=(.{4}):(.*?)>',  word)
                # TAG FOUND
                if ui_tag_search is not None:
                    ui_tag_data = ui_tag_search.group(2)
                    ui_tag = (ui_tag_search.string, '</ui>')
                    ui_tag_search_end = re.search('</ui>',  word)
                    if ui_tag_search_end:
                        ui_tag = ui_tag_search = ui_tag_data = None
                        ui_tag_word_num = 0
                # END OF WORD IF CHARACTER IS WHITESPACE
                if len(word) > 0 and character == ' ':
                    word_finished = True
                # ADD CHARACTER TO WORD
                else:
                    word += character
                # END OF WORD IF FINAL CHARACTER
                if (character_num + 1)  == len(line):
                    word_finished = True
                # ADD WORD TO LINE
                if word_finished is True:
                    if (len(utils.remove_all_tags(new_line + word)) + 1) <= max_width:
                        new_line, word = add_word(new_line, word)
                        if text_tag:
                            text_tag_word_num += 1
                        elif ui_tag:
                            ui_tag_word_num += 1
                    # MAKE NEW LINE WITH WORD
                    else:
                        if new_line_padding is True or (ui_tag and ui_tag_word_num > 0 and (str(config.ui_selection_x) + '-' + str(config.ui_selection_y)) == ui_tag_data):
                            word = '  ' + word
                        if text_tag and text_tag_word_num > 0:
                            new_line += text_tag[1]
                            word = text_tag[0] + word
                        if ui_tag and ui_tag_word_num > 0:
                            new_line += ui_tag[1]
                            word = ui_tag[0] + word
                        if numbered_list is True:
                            result.append((line_num, new_line))
                        else:
                            result.append(new_line)
                        new_line = word
                        word = ''
            # ADD LAST WORD TO LINE
            new_line, word = add_word(new_line, word)
            if new_line != '':
                if numbered_list is True:
                    result.append((line_num, new_line))
                else:
                    result.append(new_line)
        # DO NOTHING IF LINE LENGTH WITHIN MAX LENGTH
        else:
            if line_prefix is not None:
                line = line_prefix + line
            if numbered_list is True:
                result.append((line_num, line))
            else:
                result.append(line)
    return result

def scrollable_content_center(target_list, max_num_lines = 10, selection_scroll = False):
    result = []
    scroll_pos = config.ui_scroll['center']['pos']
    scroll_max = 0
    scroll_start_pos = 0
    scroll_end_pos = len(target_list)
    if len(target_list) > max_num_lines:
        scroll_pos_mod = 0
        scroll_max_mod = 0
        if selection_scroll is False:
            max_num_lines -= 1
            scroll_max_mod = 1
            if scroll_pos > 0:
                max_num_lines -= 1
                scroll_pos_mod = 1
        scroll_max = max(0, len(target_list) - max_num_lines - scroll_pos_mod - scroll_max_mod)
        scroll_pos = min(scroll_max, max(0, scroll_pos))
        if scroll_pos >= scroll_max and selection_scroll is False:
            max_num_lines += 1
        scroll_start_pos = scroll_pos + scroll_pos_mod
        scroll_end_pos = max_num_lines + scroll_pos + scroll_pos_mod
        target_list_shortened = target_list[scroll_start_pos:scroll_end_pos]
        text_up = "[SHIFT] + [UP]"
        if config.last_input_device == 'joystick':
            text_up = '[RIGHT STICK UP]'
        text_up = '▲ PRESS ' + text_up + ' TO SCROLL UP'
        text_down = "[SHIFT] + [DOWN]"
        if config.last_input_device == 'joystick':
            text_down = '[RIGHT STICK DOWN]'
        text_down = '▼ PRESS ' + text_down + ' TO SCROLL DOWN'
        if scroll_pos > 0 and selection_scroll is False:
            result.append(utils.add_ui_tag_scroll_center_up(text_up))
        for line in target_list_shortened:
            result.append(line)
        if scroll_pos < scroll_max and selection_scroll is False:
            result.append(utils.add_ui_tag_scroll_center_down(text_down))
    else:
        result = target_list
        scroll_pos = 0
    config.ui_scroll['center']['pos'] = scroll_pos
    config.ui_scroll['center']['max'] = scroll_max
    config.ui_scroll_start_pos = scroll_start_pos
    config.ui_scroll_end_pos = scroll_end_pos
    return result

def center(content, padding_top = 0, padding_bottom = 0):
    if padding_bottom > 0:
        padding_bottom += 1
    padding = padding_top + padding_bottom
    wrapped_lines = word_wrap(content.lines, config.size_x - 4)
    wrapped_lines = scrollable_content_center(wrapped_lines, config.size_y - padding, selection_scroll = content.selection_scroll)
    lines = []
    # INIT FILL
    fill, fill_list, fill_num = fill_init(content.fill)
    fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
    # CENTER CONTENT
    num_empty = 0
    if content.centered_vertical:
        while num_empty < ((config.size_y - padding) - len(wrapped_lines)) / 2:
            lines.append(Line("", None, fill, fill_color))
            # INCREMENT FILL
            fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
            fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
            num_empty += 1
    # CONTENT
    num = 0
    for num, line in enumerate(wrapped_lines):
        lines.append(Line(line, content.line_color, fill, fill_color, content.centered_horizontal))
        # INCREMENT FILL
        fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
        fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
    #EMPTY LINES BOTTOM
    while num + 1 + num_empty < config.size_y - padding:
        lines.append(Line("", None, fill, fill_color))
        # INCREMENT FILL
        fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
        fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
        num_empty += 1
    if padding_bottom > 0:
        lines.append(seperator())
    return lines

def lower(content):
    min_height = 10
    if content.min_height is not None:
        min_height = content.min_height
    lines = []
    # INIT FILL
    fill, fill_list, fill_num = fill_init(content.fill)
    fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
    # CONTENT
    num = 0
    if content.lines:
        for line in content.lines:
            lines.append(Line(line, content.line_color, fill, fill_color, content.centered_horizontal))
            num += 1
            # INCREMENT FILL
            fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
            fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
    # EMPTY LINES
    while num == 0 or num == 1 or num <= min_height:
        lines.append(Line("", None, fill, fill_color))
        num += 1
    return lines

def log(content):
    lines = []
    # INIT FILL
    fill, fill_list, fill_num = fill_init(content.fill)
    fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
    # CONTENT
    if content.lines:
        for num, line in enumerate(content.lines):
            lines.append(Line(line, content.line_color, fill, fill_color))
            # INCREMENT FILL
            fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
            fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
    lines.append(seperator())
    return lines

def format_fill(fill, width):
    result = None
    if fill:
        result = ""
        for n in range(int(width / len(fill))):
            result += fill
        result = result[:width]
    return result

def make_line(line, line_color = None, fill = None, fill_color = None, align = "l", margin = 2):
    line_without_tags = utils.remove_all_tags(line)
    line_length = len(line_without_tags)
    centered_start = int((config.size_x - line_length) / 2)
    line_formatted = ""
    num = 0
    # ADD LINE
    while num < config.size_x:
        if line_length > 0 and ((align == "l" and num == margin) or (align == "c" and num == centered_start) or (align == "r" and num == config.size_x - (line_length + margin))):
            num += line_length
            line_formatted += line
        else:
            line_formatted += " "
            num += 1
    # FORMAT FILL
    fill_formatted = format_fill(fill, config.size_x)
    return ((line_formatted, line_color), (fill_formatted, fill_color))

def make_line_centered(line, line_color = None, fill = None, fill_color = None):
    return make_line(line, line_color, fill, fill_color, "c")

def make_lines(target_list):
    result = []
    for line in target_list:
        if line.centered:
            result.append(make_line_centered(line.content, line.color, line.fill, line.fill_color))
        else:
            result.append(make_line(line.content, line.color, line.fill, line.fill_color))
    return result

def make_lines_multi(target_list):
    result = []
    for window in target_list:
        result.extend(make_lines(window))
    return result

def seperator():
    return Line("", fill = "-", fill_color = 'foreground')

def fill_init(fill):
    fill_list = fill
    fill_num = 0
    if fill:
        fill = fill_list[fill_num]
    return fill, fill_list, fill_num

def format_selection_options_display(target_list, min_size_list = None, min_size = 10, empty_text = None, enable_justnum = True, append_empty = True):
    if empty_text is None:
        empty_text = utils.add_text_tag('Nothing', fg = config.TAG_COLOR_UI_INACTIVE)
    pre_line = "> "
    pre_line_empty = " "
    result = []
    for x, option_list in enumerate(target_list):
        this_min_size = min_size
        if min_size_list is not None and len(min_size_list) > x:
            this_min_size = min_size_list[x]
        just_num = this_min_size
        if utils.list_none_filter(option_list):
            just_num = utils.list_longest_entry_length(utils.remove_all_tags_multi([item.display_name for item in utils.list_none_filter(option_list)])) + 2
        just_num = max(this_min_size, just_num)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ''
            if len(utils.list_none_filter(option_list)) == 0 and y == 0:
                entry = pre_line_empty + empty_text
            if option_entry:
                entry = option_entry.display_name
                if x == config.ui_selection_x and y == config.ui_selection_y and config.ui_scroll['log']['pos'] == 0:
                    entry = utils.add_ui_tag_sel_action(entry, x, y)
                    entry = pre_line + entry
                else:
                    entry = utils.add_ui_tag_sel_action(entry, x, y)
                    entry = pre_line_empty + entry
            if enable_justnum and (entry or append_empty):
                entry = fill_empty_space(entry, just_num - len(utils.remove_all_tags(entry)))
            if append_empty or entry:
                result[x].append(entry)
    return result
    
def format_selection_options_display_modifiable(target_list, min_size_name = 70, min_size_value = 20, name_link_padding = 10):
    pre_line = "> "
    pre_line_empty = " "
    result = []
    for x, option_list in enumerate(target_list):
        just_num_name = utils.list_longest_entry_length(utils.remove_all_tags_multi([item.display_name for item in utils.list_none_filter(option_list)])) + 2 + name_link_padding
        just_num_name = max(min_size_name, just_num_name)
        just_num_link = utils.list_longest_entry_length(utils.remove_all_tags_multi(utils.list_none_filter([item.link for item in utils.list_none_filter(option_list)])))
        just_num_link = max(min_size_value, just_num_link)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ""
            if option_entry:
                entry_name = option_entry.display_name
                entry_link = option_entry.link
                if x == config.ui_selection_x and y == config.ui_selection_y:
                    entry_name = utils.add_text_tag(pre_line + entry_name, config.TAG_COLOR_UI_SEL_FG)
                else:
                    entry_name = pre_line_empty + entry_name
                entry = fill_empty_space(entry_name, just_num_name - len(utils.remove_all_tags(entry_name)))
                if entry_link is not None:
                    entry_link = fill_empty_space(entry_link, just_num_link - len(utils.remove_all_tags(entry_link)), " ")
                    entry = utils.add_ui_tag_sel_none(entry, x, y)
                    entry_link = utils.add_ui_tag_sel_none(entry_link, x, y)
                    sel_ind_l = utils.add_ui_tag_sel_left('< ', x, y)
                    sel_ind_r = utils.add_ui_tag_sel_right(' >', x, y)
                    if x == config.ui_selection_x and y == config.ui_selection_y:
                        entry_link = utils.add_text_tag(entry_link, other=config.TAGS['underline'])
                    entry_link = sel_ind_l + entry_link + sel_ind_r
                    entry += entry_link
                else:
                    entry = utils.add_ui_tag_sel_action(entry, x, y)
            entry = fill_empty_space(entry, (just_num_name + just_num_link + 4) - len(utils.remove_all_tags(entry)))
            result[x].append(entry)
    return result

def format_selection_options_display_bg(target_list, centered = False, min_size = 10):
    padding_size = 2
    padding = fill_empty_space("", padding_size, " ")
    padding_fill = fill_empty_space("", padding_size)
    result = []
    for x, option_list in enumerate(target_list):
        just_num = max(min_size, utils.list_longest_entry_length(utils.remove_all_tags_multi([item.display_name for item in utils.list_none_filter(option_list)])) + padding_size + padding_size)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ""
            if option_entry:
                entry = option_entry.display_name
                if x == config.ui_selection_x and y == config.ui_selection_y:
                    entry = padding + entry + padding
                    entry = fill_empty_space(entry, just_num - len(utils.remove_all_tags(entry)), " ", centered)
                    entry = utils.add_text_tag(entry, fg = config.TAG_COLOR_UI_BG_SEL_FG, bg = config.TAG_COLOR_UI_BG_SEL_BG)
                else:
                    entry = padding_fill + entry + padding_fill
                    entry = fill_empty_space(entry, just_num - len(utils.remove_all_tags(entry)), centered = centered)
            entry = utils.add_ui_tag_sel_action(entry, x, y)
            result[x].append(entry)
    return result

def format_selection_options_display_bg_centered(target_list, min_size = 10):
    return format_selection_options_display_bg(target_list, True, min_size)

def format_selection_options_display_add_titles(target_list, titles_list):
        for num, column in enumerate(target_list):
            target_list[num].insert(0, titles_list[num])
        return target_list

def window_upper():
    content = []
    if config.settings['debug_mode']:
        if config.mode != config.MODE_DEBUG:
            content.append("DEBUG MODE")
    if config.mode == config.MODE_SETTINGS:
        content.append("SETTINGS")
    elif config.mode == config.MODE_DEBUG:
        content.append("DEBUG SCREEN")
    elif config.mode == config.MODE_HELP:
        content.append("HELP")
    elif config.mode == config.MODE_CUTSCENE or config.mode == config.MODE_GAME:
        content.append('ADVENTURE')
        if config.flags['show_player_hp']:
            content.append('HEALTH POINTS: ' + str(config.player['health_points']))
    elif config.mode == config.MODE_MAP:
        content.append("MAP")
    elif config.mode == config.MODE_CHARACTER:
        content.append("CHARACTER")
    if config.settings['enable_music'] and config.settings['enable_music_now_playing']:
        content.append('♫ NOW PLAYING: ' + str(audio.music_title).upper() + ' ♫')
    upper_window_string = ""
    for num, item in enumerate(content):
        if num != 0:
            upper_window_string += " | "
        upper_window_string += item
    lines = []
    lines.append(upper_window_string)
    return Content(WINDOW_UPPER, lines)

def window_lower_empty():
    return Content(WINDOW_LOWER, min_height = 0)

def window_lower_continue():
    return Content(WINDOW_LOWER, [press_to_continue_text()], min_height = 0)

def window_lower_back():
    return Content(WINDOW_LOWER, [press_to_go_back_text()], min_height = 0)

def combine_blocks(blocks, margin_size = 4, r_align = None, min_size_list = None):
    margin = fill_empty_space("", margin_size)
    lines = []
    height = utils.list_longest_entry_length([utils.remove_all_tags_multi(utils.list_none_filter(single_block)) for single_block in utils.list_none_filter(blocks)])
    block_length = []
    for block_num, block in enumerate(blocks):
        just_num = utils.list_longest_entry_length(utils.remove_all_tags_multi(utils.list_none_filter(block)))
        if min_size_list is not None and len(min_size_list) > block_num:
            just_num = max(min_size_list[block_num], just_num)
        block_length.append(just_num)
    if r_align is not None:
        l_length = sum(block_length[:r_align:])
        r_length = sum(block_length[r_align::])
        fill_length = (config.size_x - (l_length + r_length)) - (margin_size * len(blocks))
    for block_num, block in enumerate(blocks):
        fill_space = 0
        if r_align is not None:
            if block_num == r_align:
                fill_space = fill_length
        for line_num in range(height):
            line = ""
            if line_num < len(block):
                if block[line_num]:
                    line = block[line_num]
            if line_num < height:
                line = fill_empty_space(line, block_length[block_num] + fill_space - len(utils.remove_all_tags(line)))
                if block_num == 0:
                    lines.append(line)
                else:
                    lines[line_num] += margin + line
    return lines

def block_minimap(room, npcs = None, position = None, ui_tags = None):
    lines = []
    if config.mode == config.MODE_GAME:
        lines.append("MEMORY:".ljust(15))
    for y in range(3):
        line_top = ""
        line_mid = ""
        line_low = ""
        for x in range(3):
            pos = utils.coords_to_pos(x,y)
            tile_top = MINIMAP_TILES['undiscovered_top']
            tile_mid = MINIMAP_TILES['undiscovered_mid']
            tile_low = MINIMAP_TILES['undiscovered_low']
            if pos == 'nw':
                tile_top = MINIMAP_TILES['undiscovered_top_upper_left']
            elif pos == 'ne':
                tile_top = MINIMAP_TILES['undiscovered_top_upper_right']
            elif pos == 'sw':
                tile_low = MINIMAP_TILES['undiscovered_bottom_lower_left']
            elif pos == 'se':
                tile_low = MINIMAP_TILES['undiscovered_bottom_lower_right']
            if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                    tile_top = MINIMAP_TILES['selected_undiscovered_top']
                    tile_mid = MINIMAP_TILES['selected_undiscovered_mid']
                    tile_low = MINIMAP_TILES['selected_undiscovered_low']
            if room['visited'][pos]:
                tile_top = MINIMAP_TILES['visited_top']
                tile_mid = MINIMAP_TILES['visited_mid']
                tile_low = MINIMAP_TILES['visited_low']
                if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                    if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                        tile_top = MINIMAP_TILES['selected_visited_top']
                        tile_mid = MINIMAP_TILES['selected_visited_mid']
                        tile_low = MINIMAP_TILES['selected_visited_low']
                if pos == position:
                    tile_top = MINIMAP_TILES['current_top']
                    tile_mid = MINIMAP_TILES['current_mid']
                    tile_low = MINIMAP_TILES['current_low']
                    if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_current_top']
                            tile_mid = MINIMAP_TILES['selected_current_mid']
                            tile_low = MINIMAP_TILES['selected_current_low']
            for portal in room['portal']:
                if portal['position'] == pos and portal['disabled'] == False and room['visited'][pos]:
                    tile_top = MINIMAP_TILES['portal_top']
                    tile_mid = MINIMAP_TILES['portal_mid']
                    tile_low = MINIMAP_TILES['portal_low']
                    if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_portal_top']
                            tile_mid = MINIMAP_TILES['selected_portal_mid']
                            tile_low = MINIMAP_TILES['selected_portal_low']
                    if pos == position:
                        tile_top = MINIMAP_TILES['portal_current_top']
                        tile_mid = MINIMAP_TILES['portal_current_mid']
                        tile_low = MINIMAP_TILES['portal_current_low']
                        if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                            if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                tile_top = MINIMAP_TILES['selected_portal_current_top']
                                tile_mid = MINIMAP_TILES['selected_portal_current_mid']
                                tile_low = MINIMAP_TILES['selected_portal_current_low']
            for interactable in room['interactable']:
                if interactable['position'] == pos and interactable['disabled'] == False and room['visited'][pos]:
                    tile_top = MINIMAP_TILES['interactable_top']
                    tile_mid = MINIMAP_TILES['interactable_mid']
                    tile_low = MINIMAP_TILES['interactable_low']
                    if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_interactable_top']
                            tile_mid = MINIMAP_TILES['selected_interactable_mid']
                            tile_low = MINIMAP_TILES['selected_interactable_low']
                    if pos == position:
                        tile_top = MINIMAP_TILES['interactable_current_top']
                        tile_mid = MINIMAP_TILES['interactable_current_mid']
                        tile_low = MINIMAP_TILES['interactable_current_low']
                        if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                            if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                tile_top = MINIMAP_TILES['selected_interactable_current_top']
                                tile_mid = MINIMAP_TILES['selected_interactable_current_mid']
                                tile_low = MINIMAP_TILES['selected_interactable_current_low']
            if npcs:
                for npc in npcs.values():
                    if npc['position'] == pos and room['visited'][pos] and npc['dead'] is False:
                        tile_top = MINIMAP_TILES['npc_top']
                        tile_mid = MINIMAP_TILES['npc_mid']
                        tile_low = MINIMAP_TILES['npc_low']
                        if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                            if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                tile_top = MINIMAP_TILES['selected_npc_top']
                                tile_mid = MINIMAP_TILES['selected_npc_mid']
                                tile_low = MINIMAP_TILES['selected_npc_low']
                        if pos == position:
                            tile_top = MINIMAP_TILES['npc_current_top']
                            tile_mid = MINIMAP_TILES['npc_current_mid']
                            tile_low = MINIMAP_TILES['npc_current_low']
                            if config.mode == config.MODE_GAME and config.ui_selection_current is not None:
                                if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                    tile_top = MINIMAP_TILES['selected_npc_current_top']
                                    tile_mid = MINIMAP_TILES['selected_npc_current_mid']
                                    tile_low = MINIMAP_TILES['selected_npc_current_low']
            if ui_tags is not None and pos in ui_tags:
                tile_top = utils.add_ui_tag_sel_action(tile_top, 0, ui_tags[pos])
                tile_mid = utils.add_ui_tag_sel_action(tile_mid, 0, ui_tags[pos])
                tile_low = utils.add_ui_tag_sel_action(tile_low, 0, ui_tags[pos])
            line_top += tile_top
            line_mid += tile_mid
            line_low += tile_low
        lines.append(line_top)
        lines.append(line_mid)
        lines.append(line_low)
    return lines

def make_scrollbar(scrollbar_window_height, scroll_pos, scroll_max):
    scrollbar_style_line = "│"
    scrollbar_style_body_top = utils.add_text_tag(" ", bg = config.TAG_COLOR_SCROLLBAR_BG)
    scrollbar_style_body_mid = utils.add_text_tag(" ", bg = config.TAG_COLOR_SCROLLBAR_BG)
    scrollbar_style_body_low = utils.add_text_tag(" ", bg = config.TAG_COLOR_SCROLLBAR_BG)
    lines = []
    down_arrow = None
    if config.settings['visual_enable_scroll_log_arrows']:
        if scroll_max > 0:
            up_arrow = '▲'
            scrollbar_window_height -= 1
            if scroll_pos >= scroll_max:
                up_arrow = utils.add_text_tag(up_arrow, fg = config.TAG_COLOR_UI_INACTIVE)
            else:
                up_arrow = utils.add_ui_tag_scroll_log_up(up_arrow)
            lines.append(up_arrow)
        if scroll_pos > 0:
            scrollbar_window_height -= 1
            down_arrow = utils.add_ui_tag_scroll_log_down('▼')
    scrollbar_pos = 0
    scrollbar_size = 1
    if scroll_pos > 0 and scroll_max > 0:
        scrollbar_pos = int(scrollbar_window_height - (scrollbar_window_height * scroll_pos / scroll_max))+1
        if scrollbar_pos - scrollbar_size <= 1 and scroll_pos != scroll_max:
            scrollbar_pos = scrollbar_size + 1
    num = 0
    scrollbar_body_pos = 1
    while num < scrollbar_window_height:
        scrollbar = scrollbar_style_line
        if scrollbar_pos != 0:
            scrollbar_pos = min(scrollbar_pos, scrollbar_window_height - scrollbar_size)
            scrollbar_pos = max(scrollbar_pos, scrollbar_size + 1 )
            if num + 1 in range(scrollbar_pos-scrollbar_size, scrollbar_pos + scrollbar_size + 1):
                if scrollbar_body_pos == 1:
                    scrollbar = scrollbar_style_body_top
                elif scrollbar_body_pos == scrollbar_size + 1 + scrollbar_size:
                    scrollbar = scrollbar_style_body_low
                else:
                    scrollbar = scrollbar_style_body_mid
                scrollbar_body_pos += 1
        lines.append(scrollbar)
        num += 1
    if down_arrow:
        lines.append(down_arrow)
    return lines

def log_content(target_list, numbered_list = True, max_num_lines = 10,):
    wrapped_lines = word_wrap(target_list, config.size_x - 5, numbered_list = numbered_list, new_line_padding = True, line_prefix = '∙ ')
    result = []
    scroll_pos = config.ui_scroll['log']['pos']
    scroll_max = max(0, len(wrapped_lines) - max_num_lines)
    scroll_start_pos = -abs(max_num_lines + scroll_pos)
    scroll_end_pos = -abs(scroll_pos)
    if scroll_end_pos == 0:
        scroll_end_pos = None
    target_list_shortened = wrapped_lines[scroll_start_pos:scroll_end_pos]
    scrollbar = make_scrollbar(max_num_lines, scroll_pos, scroll_max)
    num = len(target_list_shortened)
    while num < max_num_lines:
        result.append(scrollbar[num-1] + "")
        num += 1
    for num, line in enumerate(target_list_shortened):
        log_line = line
        if numbered_list:
            log_num = line[0]
            log_line = line[1]
            if log_num < config.game['turn'] - 1:
                log_line = utils.add_text_tag(utils.remove_all_tags(log_line), fg = config.TAG_COLOR_LOG_OLD)
        result.append(scrollbar[num] + " " + log_line)
    config.ui_scroll['log']['pos'] = scroll_pos
    config.ui_scroll['log']['max'] = scroll_max
    return result

def press_to_continue_text():
    text = "[ENTER]"
    if config.settings['enable_mouse']:
        text += ' OR [LEFT MOUSE]'
    if config.last_input_device == 'joystick':
        text = '(A)'
    return utils.add_ui_tag_continue('PRESS ' + text + ' TO CONTINUE')

def press_to_go_back_text(target_key = "esc"):
    text ='[ESC]'
    if config.settings['enable_mouse']:
        text += ' OR [RIGHT MOUSE]'
    if config.last_input_device == 'joystick':
        text = '(B)'
    return utils.add_ui_tag_back('PRESS ' + text + ' TO GO BACK')

def line_set_color_multi(target_list, target_color):
    result = []
    for line in target_list:
        result.append(line_set_color(line, target_color))
    return result

def line_set_color(target_line, target_color):
    return utils.add_text_tag(target_line, target_color)

def fill_empty_space(line, length, char = " ", centered = False):
    for n in range(length):
        if centered and n < length / 2:
            line = char + line
        else:
            line += char
    return line

def fill_empty_space_centered(line, length, char = None):
    return fill_empty_space(line, length, char, True)