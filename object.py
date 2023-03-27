import pygame
import json
import time
import random
import math
from gamesetting import *
from pygame.locals import *
from utility import *


class ingameObject(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)

        # set object's name
        self.name = name

        # set position of object
        self.x = x
        self.y = y

    # make sprite
    def set_sprite(self):

        # set trainer's sprite
        self.file_path = './data/spriteimg.json'
        with open(self.file_path, 'r') as file:
            self.json = json.load(file)

        for name, img_url in self.json.items():
            if name == self.name:
                image = img_url

        self.image = pygame.image.load(image).convert_alpha()

    # draw a sprite

    def draw(self, alpha=255):

        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    # draw rectangle
    def get_rect(self):
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Naebaemon(ingameObject):

    def __init__(self, name, level, x, y):
        super().__init__(name, x, y)

        # load naebaemon list
        file_path = './data/naebaemonList.json'

        with open(file_path, 'r') as file:
            self.json = json.load(file)

        # set level of naebaemon
        self.level = level

        # set base stat
        for species in self.json:
            if species['name'] == self.name:
                self.current_hp = species['base_stat']['hp'] + self.level
                self.max_hp = species['base_stat']['hp'] + self.level
                self.current_mp = species['base_stat']['mp'] + self.level
                self.max_mp = species['base_stat']['mp'] + self.level
                self.attack = species['base_stat']['attack']
                self.defense = species['base_stat']['defense']
                self.sattack = species['base_stat']['s.attack']
                self.speed = species['base_stat']['speed']

        # set sprite size
        self.size = 150

        # set sprite to front
        self.set_sprite('front_img')

        # 남은 포션의 수
        self.num_potions = 3

    # attack the other

    def perform_attack(self, theother):

        display_message(f'{self.name}이(가) 공격했다.')

        # pause 2second
        time.sleep(1)

        # calculate the damage
        damage = (2 * self.level + 10) / 10 * \
            self.attack / theother.defense * round(random.uniform(0.6, 1.4), 2)

        # critical heat
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5

        # integerize the damage
        damage = math.floor(damage)
        print(f"데미지 출력 {damage}")

        # take damage to the other
        theother.take_damage(damage)

    # attack the other

    def perform_skill(self, theother, skill):

        display_message(f'{self.name}이(가) {skill.name}을(를) 사용했다.')

        # pause 2second
        time.sleep(2)

        # calculate the damage
        damage = (2 * self.level + 10) / 250 * \
            self.attack / theother.defense * skill.power

        # critical heat
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5

        # integerize the damage
        damage = math.floor(damage)

        # take damage to the other
        theother.take_damage(damage)

    # the other takes damage
    def take_damage(self, damage):

        self.current_hp -= damage
        # hp should be above zero
        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):

        # 포션이 남았는지 체크
        if self.num_potions > 0:

            # 30 hp를 추가한다 하지만 max hp를 넘을 순 없음
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

            # 포션 수를 감소시킨다
            self.num_potions -= 1

    # make sprite
    def set_sprite(self, side):

        # set trainer's sprite
        self.file_path = './data/naebaemonList.json'

        with open(self.file_path, 'r') as file:
            self.json = json.load(file)

        for i in self.json:
            if i['name'] == self.name:
                image = i[side]

        self.image = pygame.image.load(image).convert_alpha()

        # scale of sprite
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(
            self.image, (new_width, new_height))

    # set 기술
    def set_skill(self):  # c

        self.skill = []

    # draw a sprite

    def draw(self, alpha=255):

        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    # draw a hp
    def draw_hp(self):
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, red, bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, green, bar)

        # draw hp text
        font = pygame.font.Font(default_font, 16)
        text = font.render(
            f'HP: {self.current_hp} / {self.max_hp}', True, black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        game.blit(text, text_rect)

    # draw rectangle
    def get_rect(self):
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Trainer(ingameObject):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        # set sprite size
        self.size = 200

    # make sprite
    def set_sprite(self):

        # set trainer's sprite
        file_path = './data/spriteimg.json'
        with open(file_path, 'r') as file:
            self.json = json.load(file)

        for name, img_url in self.json.items():
            if name == self.name:
                image = img_url

        self.image = pygame.image.load(image).convert_alpha()

        # scale of sprite
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(
            self.image, (new_width, new_height))

    def draw(self, alpha=255):

        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    # draw rectangle
    def get_rect(self):
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Skill():
    def __init__(self):

        # set Skills from skills.json
        file_path = './data/skills.json'
        with open(file_path, 'r') as file:
            self.json = json.load(file)

        self.name = self.json
