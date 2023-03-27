import pygame
from gamesetting import *
from object import *
from display import *
from game import *

# pygame start
pygame.init()

# game setting
pygame.display.set_caption(game_title)
pygame.display.set_icon(favicon)


# first naebaemon
level = 30
python = Naebaemon('Python', level, 25, 150)
sql = Naebaemon('SQL', level, 175, 150)
javascript = Naebaemon('JavaScript', level, 325, 150)
first_naebaemons = [python, sql, javascript]

# selected naebaemon
player_naebaemon = None
rival_naebaemon = None


# game loop
game_status = 'intro'

while game_status != 'quit':
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            game_status == 'quit'

        # detect mouse click
        if event.type == MOUSEBUTTONDOWN:

            # coordinate of mouse click
            mouse_click = event.pos

            # select naebaemon
            if game_status == 'select naebaemon':

                # check naebaemon clicked
                for i in range(len(first_naebaemons)):

                    if first_naebaemons[i].get_rect().collidepoint(mouse_click):

                        # player and rival naebaemon picked
                        player_naebaemon = first_naebaemons[i]
                        rival_naebaemon = first_naebaemons[(
                            i + 1) % len(first_naebaemons)]

                        # rival naebaemon level up
                        rival_naebaemon.level = int(
                            rival_naebaemon.level * 5)

        # player turn
        if game_status == 'player turn':
            attack_button, skill_button, potion_button, runaway_button = player_turn(
                player_naebaemon, rival_naebaemon)
            if event.type == MOUSEBUTTONDOWN:
                # coordinate of mouse click
                mouse_click = event.pos

                # 공격버튼 클릭됐는지 확인
                if attack_button.collidepoint(mouse_click):
                    game_status = 'player attack'

                # 포션 클릭됐는지 확인
                if potion_button.collidepoint(mouse_click):

                    # if potion not left, then return to player turn
                    if player_naebaemon.num_potions == 0:
                        display_message('남은 에너지 드링크가 없습니다')
                        time.sleep(2)
                        game_status = 'player turn'
                    else:
                        player_naebaemon.use_potion()
                        display_message(
                            f'{player_naebaemon.name}는 에너지 드링크를 사용했다')
                        time.sleep(2)
                        game_status = 'rival turn'

        # game intro
        if game_status == 'intro':
            game_status = game_intro()

            # naebaemon reset
            level = 30
            python = Naebaemon('Python', level, 25, 150)
            sql = Naebaemon('SQL', level, 175, 150)
            javascript = Naebaemon('JavaScript', level, 325, 150)

        # game start
        if game_status == 'start game':
            # 스타트 게임 끝난 후 naebaemon선택으로 넘어감
            game_status, sound = start_game()

        # rival attack
        if game_status == 'rival turn':
            player_naebaemon.current_hp, game_status = rival_turn(
                player_naebaemon, rival_naebaemon)

        # player attack
        if game_status == 'player attack':
            rival_naebaemon.current_hp, game_status = player_attack(
                player_naebaemon, rival_naebaemon)

        # select naebaemon
        if game_status == 'select naebaemon':
            player_naebaemon, rival_naebaemon, game_status = select_naebaemon(
                python, sql, javascript)

        # selected one of the naebaemon
        if game_status == 'selected':
            game_status = selected(player_naebaemon, rival_naebaemon, sound)

        # draw battle scene
        if game_status == 'prebattle':
            game_status, sound = prebattle(player_naebaemon, rival_naebaemon)

        if game_status == 'rival fainted':
            game_status = rival_fainted(
                player_naebaemon, rival_naebaemon, sound)

        if game_status == 'player fainted':
            game_status = player_fainted(
                player_naebaemon, rival_naebaemon, sound)


pygame.quit()
