import pygame
import random
from pygame.sprite import Sprite



class Deck(Sprite):
    def __init__(self, game, card_list):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.card_list = card_list

    def shuffle(self):
        random.shuffle(self.card_list)

    def deal(self):
        return self.card_list.pop()
