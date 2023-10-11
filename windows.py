# BUILT-IN
import math
import re

# PROJECT
import config
import utils

class Content:
    def __init__(self, w_type, lines = None, line_color = None, fill = None, fill_color = None, centered_horizontal = False, centered_vertical = False, min_height = None):
        self.w_type = w_type
        self.lines = lines
        self.line_color = line_color
        self.fill = fill
        self.fill_color = fill_color
        self.centered_horizontal = centered_horizontal
        self.centered_vertical = centered_vertical
        self.min_height = min_height

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

# SET CONSTANTS, TAGS
TAG_COLOR_FG = config.TAGS['foreground']
TAG_COLOR_BG = config.TAGS['background']
TAG_COLOR_DARK = config.TAGS['bright_black']
TAG_COLOR_UI_BG_SEL_FG = TAG_COLOR_BG
TAG_COLOR_UI_BG_SEL_BG = TAG_COLOR_FG
TAG_COLOR_UI_SEL_FG = TAG_COLOR_FG
TAG_COLOR_TITLE_SCREEN = config.TAGS['bright_cyan']
TAG_COLOR_INTERACTABLE = config.TAGS['bright_green']
TAG_COLOR_PORTAL = config.TAGS['bright_cyan']
TAG_COLOR_DIRECTION = config.TAGS['bright_blue']
TAG_COLOR_STATUS = config.TAGS['bright_magenta']
TAG_COLOR_SCROLLBAR_BG = config.TAGS['bright_white']
TAG_COLOR_MAP_INACTIVE = TAG_COLOR_DARK
TAG_COLOR_MAP_SELECTED = TAG_COLOR_FG

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
}
FILL_PATTERN_COLORS = {
    'rygma': [
        config.TAGS['red'],
        config.TAGS['yellow'],
        config.TAGS['green'],
        config.TAGS['magenta'],
        config.TAGS['cyan'],
    ]
}

# SET CONSTANTS, MINIMAP
MINIMAP_TILES = {  
    'undiscovered_top': utils.add_tag("     ", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_mid': utils.add_tag("  -  ", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_low': utils.add_tag("     ", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_top_upper_left': utils.add_tag("┌─   ", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_top_upper_right': utils.add_tag("   ─┐", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_bottom_lower_left': utils.add_tag("└─   ", TAG_COLOR_MAP_INACTIVE),
    'undiscovered_bottom_lower_right': utils.add_tag("   ─┘", TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_top': utils.add_tag("╔═══╗", TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_mid': utils.add_tag("║ - ║", TAG_COLOR_MAP_INACTIVE),
    'selected_undiscovered_low': utils.add_tag("╚═══╝", TAG_COLOR_MAP_INACTIVE),
    'visited_top': utils.add_tag("┌───┐", TAG_COLOR_MAP_INACTIVE),
    'visited_mid': utils.add_tag("│   │", TAG_COLOR_MAP_INACTIVE),
    'visited_low': utils.add_tag("└───┘", TAG_COLOR_MAP_INACTIVE),
    'selected_visited_top': utils.add_tag("╔═══╗", TAG_COLOR_MAP_INACTIVE),
    'selected_visited_mid': utils.add_tag("║   ║", TAG_COLOR_MAP_INACTIVE),
    'selected_visited_low': utils.add_tag("╚═══╝", TAG_COLOR_MAP_INACTIVE),
    'current_top': utils.add_tag("┌───┐", TAG_COLOR_MAP_SELECTED),
    'current_mid': utils.add_tag("│YOU│", TAG_COLOR_MAP_SELECTED),
    'current_low': utils.add_tag("└───┘", TAG_COLOR_MAP_SELECTED),
    'selected_current_top': utils.add_tag("╔═══╗", TAG_COLOR_MAP_SELECTED),
    'selected_current_mid': utils.add_tag("║YOU║", TAG_COLOR_MAP_SELECTED),
    'selected_current_low': utils.add_tag("╚═══╝", TAG_COLOR_MAP_SELECTED),
    'portal_top': utils.add_tag("┌───┐", TAG_COLOR_PORTAL),
    'portal_mid': utils.add_tag("│ P │", TAG_COLOR_PORTAL),
    'portal_low': utils.add_tag("└───┘", TAG_COLOR_PORTAL),
    'selected_portal_top': utils.add_tag("╔═══╗", TAG_COLOR_PORTAL),
    'selected_portal_mid': utils.add_tag("║ P ║", TAG_COLOR_PORTAL),
    'selected_portal_low': utils.add_tag("╚═══╝", TAG_COLOR_PORTAL),
    'portal_current_top': utils.add_tag("┌───┐", TAG_COLOR_PORTAL),
    'portal_current_mid': utils.add_tag("│", TAG_COLOR_PORTAL) + utils.add_tag("YOU", TAG_COLOR_MAP_SELECTED) + utils.add_tag("│", TAG_COLOR_PORTAL),
    'portal_current_low': utils.add_tag("└───┘", TAG_COLOR_PORTAL),
    'selected_portal_current_top': utils.add_tag("╔═══╗", TAG_COLOR_PORTAL),
    'selected_portal_current_mid': utils.add_tag("║", TAG_COLOR_PORTAL) + utils.add_tag("YOU", TAG_COLOR_MAP_SELECTED) + utils.add_tag("║", TAG_COLOR_PORTAL),
    'selected_portal_current_low': utils.add_tag("╚═══╝", TAG_COLOR_PORTAL),
    'interactable_top': utils.add_tag("┌───┐", TAG_COLOR_INTERACTABLE),
    'interactable_mid': utils.add_tag("│ E │", TAG_COLOR_INTERACTABLE),
    'interactable_low': utils.add_tag("└───┘", TAG_COLOR_INTERACTABLE),
    'selected_interactable_top': utils.add_tag("╔═══╗", TAG_COLOR_INTERACTABLE),
    'selected_interactable_mid': utils.add_tag("║ E ║", TAG_COLOR_INTERACTABLE),
    'selected_interactable_low': utils.add_tag("╚═══╝", TAG_COLOR_INTERACTABLE),
    'interactable_current_top': utils.add_tag("┌───┐", TAG_COLOR_INTERACTABLE),
    'interactable_current_mid': utils.add_tag("│", TAG_COLOR_INTERACTABLE) + utils.add_tag("YOU", TAG_COLOR_MAP_SELECTED) + utils.add_tag("│", TAG_COLOR_INTERACTABLE),
    'interactable_current_low': utils.add_tag("└───┘", TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_top': utils.add_tag("╔═══╗", TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_mid': utils.add_tag("║", TAG_COLOR_INTERACTABLE) + utils.add_tag("YOU", TAG_COLOR_MAP_SELECTED) + utils.add_tag("║", TAG_COLOR_INTERACTABLE),
    'selected_interactable_current_low': utils.add_tag("╚═══╝", TAG_COLOR_INTERACTABLE),
}

def combine(target_list):
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
    return result

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

def center(content, padding_top = 0, padding_bottom = 0):
    if padding_bottom > 0:
        padding_bottom += 1
    padding = padding_top + padding_bottom
    lines = []
    # INIT FILL
    fill, fill_list, fill_num = fill_init(content.fill)
    fill_color, fill_color_list, fill_color_num = fill_init(content.fill_color)
    # CENTER CONTENT
    num_empty = 0
    if content.centered_vertical:
        while num_empty < ((config.size_y - padding) - len(content.lines)) / 2:
            lines.append(Line("", None, fill, fill_color))
            # INCREMENT FILL
            fill, fill_num = utils.increment_list_loop(fill_list, fill_num)
            fill_color, fill_color_num = utils.increment_list_loop(fill_color_list, fill_color_num)
            num_empty += 1
    # CONTENT
    num = 0
    for num, line in enumerate(content.lines):
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
    while num == 0 or num == 1 or num < min_height:
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

def make_line(line, line_color = None, fill = None, fill_color = None, align = "l", margin = 2):
    line_without_tags = utils.remove_tag(line)
    line_length = len(line_without_tags)
    centered_start = int((config.size_x - line_length) / 2)
    # FILL SETUP
    if fill:
        fill_length = len(fill)
        if not fill_color:
            fill_color = TAG_COLOR_DARK
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
    # LINE COLOR
    if line_color:
        line_set_color(line_formatted, line_color)
    # FORMAT FILL
    fill_formatted = None
    if fill:
        fill_formatted = ""
        for n in range(int(config.size_x / fill_length)):
            fill_formatted += fill
        fill_formatted = (fill_formatted, fill_color)
    return (line_formatted, fill_formatted)

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
    return Line("", fill = "-", fill_color = TAG_COLOR_FG)

def fill_init(fill):
    fill_list = fill
    fill_num = 0
    if fill:
        fill = fill_list[fill_num]
    return fill, fill_list, fill_num

def format_selection_options_display(target_list, min_size = 10, r_align = None):
    pre_line = "> "
    pre_line_empty = " "
    result = []
    for x, option_list in enumerate(target_list):
        just_num = min_size
        if utils.list_none_filter(option_list):
            just_num = utils.list_longest_entry_length(utils.remove_tag_list([item.display_name for item in utils.list_none_filter(option_list)])) + 2
        just_num = max(min_size, just_num)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ""
            if len(utils.list_none_filter(option_list)) == 0 and y == 0:
                entry = pre_line_empty + "(EMPTY)"
            if option_entry:
                entry = option_entry.display_name
                if x == config.ui_selection_x and y == config.ui_selection_y and config.ui_log_scroll_pos == 0:
                    entry = utils.add_tag(pre_line + entry, TAG_COLOR_UI_SEL_FG)
                else:
                    entry = pre_line_empty + entry
            entry_formatted = entry.ljust(just_num)
            if r_align is not None:
                if x >= r_align:
                    entry_formatted = entry.rjust(just_num)
            entry_formatted = utils.add_ui_tag(entry_formatted, x, y, config.UI_TAGS['return'])
            result[x].append(entry_formatted)
    return result
    
def format_selection_options_display_modifiable(target_list, min_size_name = 60, min_size_value = 20, name_link_padding = 20):
    pre_line = "> "
    pre_line_empty = " "
    result = []
    for x, option_list in enumerate(target_list):
        just_num_name = utils.list_longest_entry_length(utils.remove_tag_list([item.display_name for item in utils.list_none_filter(option_list)])) + 2 + name_link_padding
        just_num_name = max (min_size_name, just_num_name)
        just_num_link = utils.list_longest_entry_length(utils.remove_tag_list(utils.list_none_filter([item.link for item in utils.list_none_filter(option_list)])))
        just_num_link = max (min_size_value, just_num_link)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ""
            if option_entry:
                entry_name = option_entry.display_name
                entry_link = option_entry.link
                if x == config.ui_selection_x and y == config.ui_selection_y:
                    entry_name = utils.add_tag(pre_line + entry_name, TAG_COLOR_UI_SEL_FG)
                else:
                    entry_name = pre_line_empty + entry_name
                entry = fill_empty_space(entry_name, just_num_name - len(utils.remove_tag(entry_name)))
                if entry_link is not None:
                    entry_link = fill_empty_space(entry_link, just_num_link - len(utils.remove_tag(entry_link)), " ")
                    entry = utils.add_ui_tag(entry, x, y)
                    entry_link = utils.add_ui_tag(entry_link, x, y)
                    sel_ind_l = utils.add_ui_tag('< ', x, y, config.UI_TAGS['left'])
                    sel_ind_r = utils.add_ui_tag(' >', x, y, config.UI_TAGS['right'])
                    if x == config.ui_selection_x and y == config.ui_selection_y:
                        entry_link = utils.add_tag(entry_link, other=config.TAGS['underline'])
                    entry_link = sel_ind_l + entry_link + sel_ind_r
                    entry += entry_link
                else:
                    entry = utils.add_ui_tag(entry, x, y, config.UI_TAGS['return'])
            entry = fill_empty_space(entry, (just_num_name + just_num_link + 4) - len(utils.remove_tag(entry)))
            result[x].append(entry)
    return result

def format_selection_options_display_bg(target_list, centered = False, min_size = 10):
    padding_size = 2
    padding = fill_empty_space("", padding_size, " ")
    padding_fill = fill_empty_space("", padding_size)
    result = []
    for x, option_list in enumerate(target_list):
        just_num = max(min_size, utils.list_longest_entry_length(utils.remove_tag_list([item.display_name for item in utils.list_none_filter(option_list)])) + padding_size + padding_size)
        result.append([])
        for y, option_entry in enumerate(option_list):
            entry = ""
            if option_entry:
                entry = option_entry.display_name
                if x == config.ui_selection_x and y == config.ui_selection_y:
                    entry = padding + entry + padding
                    entry = fill_empty_space(entry, just_num - len(utils.remove_tag(entry)), " ", centered)
                    entry = utils.add_tag(entry, fg = TAG_COLOR_UI_BG_SEL_FG, bg = TAG_COLOR_UI_BG_SEL_BG)
                else:
                    entry = padding_fill + entry + padding_fill
                    entry = fill_empty_space(entry, just_num - len(utils.remove_tag(entry)), centered = centered)
            entry = utils.add_ui_tag(entry, x, y, config.UI_TAGS['return'])
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
        content.append("NAME")
        content.append("LVL 4")
        content.append("HP 20 / 20")
    elif config.mode == config.MODE_MAP:
        content.append("MAP")
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

def combine_blocks(blocks, margin_size = 4, r_align = None):
    margin = fill_empty_space("", margin_size)
    lines = []
    height = utils.list_longest_entry_length([utils.remove_tag_list(utils.list_none_filter(single_block)) for single_block in utils.list_none_filter(blocks)])
    block_length = []
    for block in blocks:
        just_num = utils.list_longest_entry_length(utils.remove_tag_list(utils.list_none_filter(block)))
        block_length.append(just_num)
    if r_align is not None:
        l_length = sum(block_length[:r_align:])
        r_length = sum(block_length[r_align::])
        fill_length = (config.size_x - (l_length + r_length)) - (margin_size * len(blocks))
    line_align = False
    for block_num, block in enumerate(blocks):
        fill_space = 0
        if r_align is not None:
            if block_num == r_align:
                fill_space = fill_length
                line_align = True
        for line_num in range(height):
            line = ""
            if line_num < len(block):
                if block[line_num]:
                    line = block[line_num]
            if line_num < height:
                line = fill_empty_space(line, block_length[block_num] + fill_space - len(utils.remove_tag(line)), r_align = line_align)
                if block_num == 0:
                    lines.append(line)
                else:
                    lines[line_num] += margin + line
    return lines

def block_minimap(room, position = None):
    lines = []
    lines.append("MEMORY (LOCAL):".ljust(15))
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
            if config.ui_selection_current is not None:
                if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                    tile_top = MINIMAP_TILES['selected_undiscovered_top']
                    tile_mid = MINIMAP_TILES['selected_undiscovered_mid']
                    tile_low = MINIMAP_TILES['selected_undiscovered_low']
            if room['visited'][pos]:
                tile_top = MINIMAP_TILES['visited_top']
                tile_mid = MINIMAP_TILES['visited_mid']
                tile_low = MINIMAP_TILES['visited_low']
                if config.ui_selection_current is not None:
                    if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                        tile_top = MINIMAP_TILES['selected_visited_top']
                        tile_mid = MINIMAP_TILES['selected_visited_mid']
                        tile_low = MINIMAP_TILES['selected_visited_low']
                if pos == position:
                    tile_top = MINIMAP_TILES['current_top']
                    tile_mid = MINIMAP_TILES['current_mid']
                    tile_low = MINIMAP_TILES['current_low']
                    if config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_current_top']
                            tile_mid = MINIMAP_TILES['selected_current_mid']
                            tile_low = MINIMAP_TILES['selected_current_low']
            for portal in room['portal']:
                if portal['position'] == pos and portal['disabled'] == False and room['visited'][pos]:
                    tile_top = MINIMAP_TILES['portal_top']
                    tile_mid = MINIMAP_TILES['portal_mid']
                    tile_low = MINIMAP_TILES['portal_low']
                    if config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_portal_top']
                            tile_mid = MINIMAP_TILES['selected_portal_mid']
                            tile_low = MINIMAP_TILES['selected_portal_low']
                    if pos == position:
                        tile_top = MINIMAP_TILES['portal_current_top']
                        tile_mid = MINIMAP_TILES['portal_current_mid']
                        tile_low = MINIMAP_TILES['portal_current_low']
                        if config.ui_selection_current is not None:
                            if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                tile_top = MINIMAP_TILES['selected_portal_current_top']
                                tile_mid = MINIMAP_TILES['selected_portal_current_mid']
                                tile_low = MINIMAP_TILES['selected_portal_current_low']
            for interactable in room['interactable']:
                if interactable['position'] == pos and interactable['disabled'] == False and room['visited'][pos]:
                    tile_top = MINIMAP_TILES['interactable_top']
                    tile_mid = MINIMAP_TILES['interactable_mid']
                    tile_low = MINIMAP_TILES['interactable_low']
                    if config.ui_selection_current is not None:
                        if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                            tile_top = MINIMAP_TILES['selected_interactable_top']
                            tile_mid = MINIMAP_TILES['selected_interactable_mid']
                            tile_low = MINIMAP_TILES['selected_interactable_low']
                    if pos == position:
                        tile_top = MINIMAP_TILES['interactable_current_top']
                        tile_mid = MINIMAP_TILES['interactable_current_mid']
                        tile_low = MINIMAP_TILES['interactable_current_low']
                        if config.ui_selection_current is not None:
                            if config.ui_selection_current.name == 'move' and config.ui_selection_current.link == pos:
                                tile_top = MINIMAP_TILES['selected_interactable_current_top']
                                tile_mid = MINIMAP_TILES['selected_interactable_current_mid']
                                tile_low = MINIMAP_TILES['selected_interactable_current_low']
            line_top += tile_top
            line_mid += tile_mid
            line_low += tile_low
        lines.append(line_top)
        lines.append(line_mid)
        lines.append(line_low)
    return lines

def make_scrollbar(scrollbar_window_height, scroll_pos, scroll_max):
    scrollbar_style_line = "│"
    scrollbar_style_body_top = utils.add_tag(" ", bg = TAG_COLOR_SCROLLBAR_BG)
    scrollbar_style_body_mid = utils.add_tag(" ", bg = TAG_COLOR_SCROLLBAR_BG)
    scrollbar_style_body_low = utils.add_tag(" ", bg = TAG_COLOR_SCROLLBAR_BG)
    lines = []
    scrollbar_pos = 0
    scrollbar_size = 1
    if scroll_pos > 0 and scroll_max > 0:
        scrollbar_pos = int(scrollbar_window_height - (scrollbar_window_height * scroll_pos/scroll_max))+1
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
    return lines

def log_content(target_list, max_num_lines = 10):
    result = []
    target_list_len = len(target_list)
    max_scroll_num = max(0, target_list_len-max_num_lines)
    config.ui_log_scroll_pos = max(0, config.ui_log_scroll_pos)
    config.ui_log_scroll_pos = min(max_scroll_num, config.ui_log_scroll_pos)
    ui_log_start_pos = -abs(max_num_lines + config.ui_log_scroll_pos)
    ui_log_end_pos = -abs(config.ui_log_scroll_pos)
    if ui_log_end_pos == 0:
        ui_log_end_pos = None
    target_list_shortened = target_list[ui_log_start_pos:ui_log_end_pos]
    scrollbar = make_scrollbar(max_num_lines, config.ui_log_scroll_pos, max_scroll_num)
    num = len(target_list_shortened)
    while num < max_num_lines:
        result.append(scrollbar[num-1] + "")
        num += 1
    for num, line in enumerate(target_list_shortened):
        result.append(scrollbar[num] + " " + line)
    return result

def format_status(text):
    return utils.add_tag(text, fg = TAG_COLOR_STATUS)

def format_interactable(text):
    return utils.add_tag(text, fg = TAG_COLOR_INTERACTABLE)

def format_direction(text):
    return utils.add_tag(text, fg = TAG_COLOR_DIRECTION)

def format_portal(text):
    return utils.add_tag(text, fg = TAG_COLOR_PORTAL)

def format_color_tags(content):
    content = re.sub("<i>(.*?)</i>", format_interactable(r"\1"), content)
    content = re.sub("<s>(.*?)</s>", format_status(r"\1"), content)
    content = re.sub("<d>(.*?)</d>", format_direction(r"\1"), content)
    content = re.sub("<p>(.*?)</p>", format_portal(r"\1"), content)
    return content

def format_position_text(abr):
    position_string = ""
    if abr in utils.DIRECTION_ABR:
        position_string = format_direction(utils.DIRECTION_ABR[abr])
        if abr != "c":
            position_string += " side"
    else:
        position_string = "INVALID"
    return position_string

def press_to_continue_text(target_key = "enter"):
    text ='PRESS [' + target_key.upper() + ']'
    if config.settings['enable_mouse']:
        text += ' OR [MOUSE LEFT]'
    text += ' TO CONTINUE'
    return text

def press_to_go_back_text(target_key = "esc"):
    text ='PRESS [' + target_key.upper() + ']'
    if config.settings['enable_mouse']:
        text += ' OR [MOUSE RIGHT]'
    text += ' TO GO BACK'
    return text

def line_set_color_multi(target_list, target_color):
    result = []
    for line in target_list:
        result.append(line_set_color(line, target_color))
    return result

def line_set_color(target_line, target_color):
    return utils.add_tag(target_line, target_color)

def fill_empty_space(line, length, char = " ", centered = False, r_align = False):
    for n in range(length):
        if r_align or (centered and n < length / 2):
            line = char + line
        else:
            line += char
    return line

def fill_empty_space_centered(line, length, char = None):
    return fill_empty_space(line, length, char, True)