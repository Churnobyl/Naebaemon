import pygame

"""set variables"""

# game size
game_width = 512  # 화면 너비
game_height = 512  # 화면 높이
size = (game_width, game_height)
game = pygame.display.set_mode(size)  # pygame 화면 사이즈 결정

# game desciption
game_title = 'NaeBaemon'
favicon = pygame.image.load("./assets/img/nbm.png")

# game color
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
gold = (218, 165, 32)
green = (0, 200, 0)
red = (200, 0, 0)

# 폰트
default_font = 'gsc.ttf'
