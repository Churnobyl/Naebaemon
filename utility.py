import pygame
import json
import time
import random
import math
from gamesetting import *
from pygame.locals import *
from PIL import Image, ImageSequence


# show message
def display_message(message):

    # white box with black border
    pygame.draw.rect(game, white, (10, 350, 492, 150))
    pygame.draw.rect(game, black, (10, 350, 492, 150), 3)

    # show text
    font = pygame.font.Font(default_font, 20)

    if len(message) > 34:
        message1 = message[:34]
        message2 = message[34:]

        text1 = font.render(message1, True, black)
        text2 = font.render(message2, True, black)

        text1_rect = text1.get_rect()
        text1_rect.x = 25
        text1_rect.y = 390

        text2_rect = text2.get_rect()
        text2_rect.x = 25
        text2_rect.y = 420

        game.blit(text1, text1_rect)
        game.blit(text2, text2_rect)

        pygame.display.update()
    else:
        text = font.render(message, True, black)
        text_rect = text.get_rect()
        text_rect.x = 25
        text_rect.y = 410
        game.blit(text, text_rect)

        pygame.display.update()


# make buttons
def create_button(width, height, left, top, text_cx, text_cy, label):

    # position of mouse cursor
    mouse_cursor = pygame.mouse.get_pos()

    button = Rect(left, top, width, height)

    # highlighting of button
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(game, gold, button)
    else:
        pygame.draw.rect(game, white, button)

    # add label to button
    font = pygame.font.Font(default_font, 24)
    text = font.render(f'{label}', True, black)
    text_rect = text.get_rect(center=(text_cx, text_cy))
    game.blit(text, text_rect)

    return button


# load gif and divide frame by frame
def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
    return frames


# move a image group
class AnimatedSpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, bottom, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(x, bottom))
        self.image_index = 0

    def update(self):
        self.image_index += 1
        self.image = self.images[self.image_index % len(self.images)]
