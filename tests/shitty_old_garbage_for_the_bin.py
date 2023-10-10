          '''
          combo = ""
          prev_fg = None
          prev_bg = None
          prev_other = None
          prev_end = 0
                      if match_fg == prev_fg and match_bg == 'bg' and match_other == prev_other:
              
              
              spaces_num = match.start() - prev_end
              prev_end = match.end()
              for n in range(spaces_num):
                combo += " "
              combo += match.group(1)
              render_line = font.render(color_line, False, config.palette[name])
              screen.blit(render_line, (offset_x, pos_y))
            else:
            prev_fg = match_fg
            prev_bg = match_bg
            prev_other = match_other
          '''


"""
def move_north():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['y'] > -1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']-1})[0], True)
        
def move_south():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['y'] < 1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x'], 'y': pos['y']+1})[0], True)
        
def move_west():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['x'] > -1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']-1, 'y': pos['y']})[0], True)

def move_east():
    global current_position
    pos = DIRECTION_TO_COORD[current_position]
    if pos['x'] < 1:
        change_position(utils.dict_key_by_value(DIRECTION_TO_COORD, {'x': pos['x']+1, 'y': pos['y']})[0], True)
"""