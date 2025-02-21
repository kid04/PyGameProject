import pygame
import cards
from pygame.sprite import Sprite

class Receiver(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.image = pygame.image.load('sprites/cardback.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = (600, 400)

    def receive(self, card):
        card_received = self._rec_receive(card)
        number = 0
        for card in card_received:
            number += int(card.text.replace('card', ''))
            self.game.cards.remove(card)
        card = cards.Card(self.game, text=f'card{number}')
        card.rect.center = self.rect.center
        self.game.cards.add(card)

    def _rec_receive(self, card):
        cards_received = []
        if card.prev:
            cards_received = self._rec_receive(card.prev)
        cards_received.append(card)
        return cards_received

    def render(self):
        self.screen.blit(self.image, self.rect)