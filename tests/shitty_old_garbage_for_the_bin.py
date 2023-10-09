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