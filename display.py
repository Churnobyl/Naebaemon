import pygame
from gamesetting import *
from object import *
from utility import *
from pygame_animatedgif import AnimatedGifSprite
import sys

# load script
file_path = './data/scripts.json'

with open(file_path, 'r') as file:
    script = json.load(file)

# load naebaemon
file_path = './data/naebaemonList.json'

with open(file_path, 'r') as file:
    naebaemon_list = json.load(file)


# game intro
def game_intro():

    clock = pygame.time.Clock()
    clock.tick(20)
    gifFrameList = loadGIF('./assets/img/gameintro.gif')
    animated_sprite = AnimatedSpriteObject(
        game.get_width() // 2, 512, gifFrameList)
    all_sprites = pygame.sprite.Group(animated_sprite)

    # background music
    sound = pygame.mixer.Sound("./assets/bgm/01. gameintro.mp3")
    sound.set_volume(0.6)
    sound.play(-1)

    run = True
    while run:
        # set x2 speed
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                sound.stop()
                game_status = 'start game'
                return game_status

        all_sprites.update()
        all_sprites.draw(game)
        pygame.display.flip()


def start_game():

    # 일어나기
    game.fill(black)

    index = 0
    index_max = len(script['0']['script'])

    run = True
    while run:
        if index < index_max:
            display_message(script['0']['script'][index])
        else:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                index += 1

    # 규박사 생성
    professorkyu = Trainer('규박사', 140, 0)
    game.fill(white)

    # 규박사 사이즈 조정
    professorkyu.size = 200

    professorkyu.set_sprite()
    professorkyu.draw()
    pygame.display.update()

    # background music
    sound = pygame.mixer.Sound("./assets/bgm/02. talk.mp3")
    sound.set_volume(0.5)
    sound.play(-1)

    index = 0
    index_max = len(script['1']['script'])

    run = True
    while run:
        if index < index_max:
            display_message(script['1']['script'][index])
        else:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                index += 1

    game_status = 'select naebaemon'
    return game_status, sound


def select_naebaemon(first, second, third):

    first_naebaemons = [first, second, third]
    game_status = select_naebaemon
    check_select = True
    while check_select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_status = 'quit'
                return game_status
            else:
                # select first naebaemon
                game.fill(white)

                # draw naebaemon
                first.draw()
                second.draw()
                third.draw()

                # draw boxes when the mouse hovering
                mouse_cursor = pygame.mouse.get_pos()
                for naebaemon in first_naebaemons:
                    if naebaemon.get_rect().collidepoint(mouse_cursor):
                        pygame.draw.rect(game, black, naebaemon.get_rect(), 2)

                        # detect mouse click
                        if event.type == MOUSEBUTTONDOWN:
                            # 마우스 클릭 좌표
                            mouse_click = event.pos

                            # 포켓몬이 클릭되었는지 확인
                            for i in range(len(first_naebaemons)):

                                if first_naebaemons[i].get_rect().collidepoint(mouse_click):

                                    # 플레이어와 라이벌 포켓몬 선택
                                    player_naebaemon = first_naebaemons[i]
                                    rival_naebaemon = first_naebaemons[(
                                        i + 1) % len(first_naebaemons)]

                                    game_status = 'selected'
                                    return player_naebaemon, rival_naebaemon, game_status

                pygame.display.update()


def selected(player_naebaemon, rival_naebaemon, sound):

    # hp바의 좌표
    player_naebaemon.hp_x = 275
    player_naebaemon.hp_y = 250
    rival_naebaemon.hp_x = 50
    rival_naebaemon.hp_y = 50

    # 선택된 내배몬 보여주기
    game.fill(white)
    player_naebaemon.draw()
    pygame.display.update()

    index = 0
    index_max = len(script['2']['script'])

    run = True
    while run:
        if index < index_max:
            if index == 0:
                display_message(script['2']['script']
                                [index].format(player_naebaemon.name))
            elif index == 1:
                script_desc = ''
                for species in naebaemon_list:
                    if species['name'] == player_naebaemon.name:
                        script_desc = species['description']

                display_message(script['2']['script']
                                [index].format(script_desc))
            elif index == 2:
                display_message(script['2']['script']
                                [index].format(player_naebaemon.name))
            else:
                display_message(script['2']['script'][index])

        else:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                index += 1

    sound.stop()

    game_status = 'prebattle'
    return game_status


def prebattle(player, other):

    # position of naebaemon
    player.x = 20
    player.y = 150
    other.x = 300
    other.y = 0

    # resize the sprites
    player.size = 200
    other.size = 200
    player.set_sprite('back_img')
    other.set_sprite('front_img')

    # background music
    sound = pygame.mixer.Sound("./assets/bgm/03. battle.mp3")
    sound.set_volume(0.6)
    sound.play(-1)

    # rival sends out their naebaemon
    game.fill(white)
    pygame.display.update()
    time.sleep(3)
    alpha = 0
    while alpha < 255:

        other.draw(alpha)
        display_message(f'라이벌이 {other.name}을 내보냈다!')
        alpha += math.log(2)

        pygame.display.update()

    # pause for 2 second
    time.sleep(2)

    # player sends out their naebaemon
    alpha = 0
    while alpha < 255:

        game.fill(white)
        other.draw()
        player.draw(alpha)
        display_message(f'가라 {player.name}!')
        alpha += math.log(2)

        pygame.display.update()

    # draw hp bars
    player.draw_hp()
    other.draw_hp()

    pygame.display.update()

    # whose turn is first?
    if other.speed * round(random.uniform(0.9, 1), 2) > player.speed:
        game_status = 'rival turn'
        return game_status, sound
    else:
        game_status = 'player turn'
        return game_status, sound


# player phase
def player_turn(player, other):

    game.fill(white)

    player.draw()
    other.draw()
    player.draw_hp()
    other.draw_hp()

    # make buttons
    attack_button = create_button(
        246, 75, 10, 350, 128, 387, '일반공격')  # width, height, left, top
    skill_button = create_button(246, 75, 256, 350, 379, 387, '스킬')
    potion_button = create_button(
        246, 75, 10, 425, 128, 462, f'핫식스: {player.num_potions}')
    runaway_button = create_button(246, 75, 256, 425, 379, 462, '떠넘기기')

    # black border
    pygame.draw.rect(game, black, (10, 350, 492, 150), 3)

    pygame.display.update()

    return attack_button, skill_button, potion_button, runaway_button


# rival phase
def rival_turn(player, other):
    game.fill(white)
    player.draw()
    other.draw()
    player.draw_hp()
    other.draw_hp()

    # 디스플레이 박스를 비우고 공격전에 2초 멈춤
    display_message('')
    time.sleep(1)

    other.perform_attack(player)

    if player.current_hp == 0:
        game_status = 'player fainted'
    else:
        game_status = 'player turn'

    pygame.display.update()

    return player.current_hp, game_status


# player normal attack


def player_attack(player, other):
    a = time.time()
    # calculate attack possibility
    possibility = (player.speed / other.speed) * \
        round(random.uniform(0.95, 1), 2)
    if possibility > 0.9:
        player.perform_attack(other)
    elif possibility > 0.7:
        if round(random.uniform(0, 1), 2) >= 0.5:
            player.perform_attack(other)
        else:
            display_message(f"{other.name}은(는) 회피했다.")

    b = time.time()

    if other.current_hp == 0:
        game_status = 'rival fainted'
    else:
        game_status = 'rival turn'

    c = time.time()

    print("player attack 1 {:.10f}".format(b-a))
    print("player attack 2 {:.10f}".format(c-b))

    return other.current_hp, game_status


def rival_fainted(player, other, sound):
    sound.stop()

    alpha = 255

    while alpha > 0:

        game.fill(white)
        player.draw_hp()
        other.draw_hp()
        player.draw()
        other.draw(alpha)

        display_message(f"{other.name}은(는) 쓰러졌다")

        alpha -= math.log(2)
        pygame.display.update()

    display_message(script['3']['script'][0])

    # background music
    sound = pygame.mixer.Sound("./assets/bgm/04. victory.mp3")
    sound.set_volume(0.5)
    sound.play(-1)

    time.sleep(3)

    # quit
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()


def player_fainted(player, other, sound):

    alpha = 255

    while alpha > 0:

        game.fill(white)
        player.draw_hp()
        other.draw_hp()
        player.draw(alpha)
        other.draw()

        display_message(f"{player.name}은(는) 쓰러졌다")

        alpha -= math.log(2)
        pygame.display.update()

    display_message(f"눈 앞이 캄캄해졌다")
    pygame.display.update()
    time.sleep(3)
    game.fill(black)
    pygame.display.update()
    time.sleep(2)

    sound.stop()
    game_status = 'intro'
    return game_status
