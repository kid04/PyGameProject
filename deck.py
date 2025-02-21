import pygame
import random
from pygame.sprite import Sprite


class Deck(Sprite):
    def __init__(self, game, card_list, image_pass='sprites/cardback.bmp', pos=(0, 0)):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.transform.scale(pygame.image.load(image_pass), self.settings.card_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.settings = game.settings

        self.card_list = card_list
        self.library = self.card_list.copy()

    def shuffle(self):
        print('Shuffled!')
        self.library = []
        for card in self.card_list:
            self.library.append(card.__copy__())
        random.shuffle(self.library)

    def deal(self):
        card = self.library.pop()
        self.game.cards.add(card)
        self.game.card_taken(card)
        if len(self.library) == 0:
            self.shuffle()

    def render(self):
        self.screen.blit(self.image, self.rect)

    def onClick(self):
        self.deal()

    def get_chosed_scale(self):
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width * 1.5,
                                                         self.image.get_rect().height * 1.5))

class TimeDeck(Deck):
    def __init__(self):
        super().__init__()
