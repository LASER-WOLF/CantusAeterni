import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import math
import pygame

def main():
  MAIN_TITLE = "Cantus Aeterni"
  SCREEN_WIDTH = 1600
  SCREEN_HEIGHT = 900
  FRAMERATE = 12
  WINDOW_MODE_NORMAL = 'normal'
  WINDOW_MODE_FULLSCREEN = 'fullscren'
  WINDOW_MODE_BORDERLESS = 'borderless_fullscren'

  FONTS = {
    'IBM PS/55 re.': 'Px437_IBM_PS-55_re',
    'Cordata PPC-400': 'Px437_Cordata_PPC-400',
    'ToshibaTxL1': 'Px437_ToshibaTxL1_8x16',
    'NEC APC III': 'Px437_NEC_APC3_8x16',
  }

  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  GRAY = (200, 200, 200)
  WHITE = (255, 255, 255)

  COLOR_BACKGROUND = BLACK
  COLOR_DEFAULT = WHITE

  currrent_window_mode = WINDOW_MODE_NORMAL
  current_font = FONTS['NEC APC III']

  pygame.init()
  clock = pygame.time.Clock()

  os.environ['SDL_VIDEO_CENTERED'] = '1'
  display_info = pygame.display.Info()
  screen_height_full = display_info.current_h
  screen_width_full = display_info.current_w

  if currrent_window_mode == WINDOW_MODE_FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  elif currrent_window_mode == WINDOW_MODE_BORDERLESS:
    screen = pygame.display.set_mode((screen_width_full, screen_height_full), pygame.NOFRAME)
  else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  pygame.display.set_caption(MAIN_TITLE)

  font = pygame.font.Font("font/" + current_font + '.ttf', 16)
  font_size = font.size('A')
  font_width = font_size[0]
  font_height = font_size[1]

  size_x_raw = SCREEN_WIDTH / font_width
  offset_x = math.floor((font_width * math.modf(size_x_raw)[0]) / 2)
  size_x = math.floor(size_x_raw)

  size_y_raw = SCREEN_HEIGHT / font_height
  offset_y = math.floor((font_height * math.modf(size_y_raw)[0]) / 2)
  size_y = math.floor(size_y_raw)

  FILL_CHAR = "ƒ"
  def fill_empty_space(line, length, char = None, centered = False):
    if not char:
      char = FILL_CHAR
    for n in range(length):
      if centered and n < length / 2:
        line = char + line
      else:
        line += char
    return line

  play_test_animation = False
  TEST_ANIMATION_FRAMES = [
    '░',
    '▒',
    '▓',
    '█',
  ]
  TEST_ANIMATION_FRAMERATE = 4
  FRAME_HOLD = FRAMERATE / TEST_ANIMATION_FRAMERATE
  test_current_frame = 0
  current_frame_hold = 0

  run = True
  while run:
    screen.fill(COLOR_BACKGROUND)

    #for num, pos_y in enumerate(range(offset_y, SCREEN_HEIGHT - font_height - offset_y, font_height)):
    for num in range(size_y):
      pos_y = offset_y + (num * font_height)
      line = 'LINE #' + str(num + 1) + ' AT Y: ' + str(pos_y)
      if num == 0:
        fps = int(clock.get_fps())
        line = 'RESOLUTION: ' + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT) + ' | SIZE: ' + str(size_x) + 'x' + str(size_y) + ' | OFFSET: ' + 'X=' + str(offset_x) + ' Y=' + str(offset_y) + ' | FONT: ' + current_font + ' (' + str(font_size[0]) + 'x' + str(font_size[1]) + ') | FPS: ' + str(fps)
      line = fill_empty_space(line, size_x - len(line))
      render_line = font.render(line, False, COLOR_DEFAULT)
      screen.blit(render_line, (offset_x, pos_y))

    if play_test_animation:
      current_frame_hold += 1
      if current_frame_hold >= FRAME_HOLD:
        current_frame_hold = 0
        test_current_frame += 1
        if test_current_frame >= len(TEST_ANIMATION_FRAMES):
          test_current_frame = 0
      for num in range(size_y):
        pos_y = offset_y + (num * font_height)
        line = ''
        line = fill_empty_space(line, size_x - len(line), TEST_ANIMATION_FRAMES[test_current_frame])
        render_line = font.render(line, False, COLOR_BACKGROUND)
        screen.blit(render_line, (offset_x, pos_y))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
              run = False
          elif event.key == pygame.K_t:
              play_test_animation = not play_test_animation

    pygame.display.flip()
    clock.tick(FRAMERATE)

  pygame.quit()

if __name__=="__main__":
    main()