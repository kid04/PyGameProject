import pygame
import sys
from settings import Settings
import cards


class MyGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.cards = pygame.sprite.Group()
        self.cards.add(cards.Card(self, text='card1'))
        self.cards.add(cards.Card(self, text='card2'))
        self.cards.add(cards.Card(self, text='card3'))
        self.cards.add(cards.Card(self, text='card4'))

        self.chosen = None

    def run_game(self):
        while True:
            self._check_events()

            if self.chosen:
                self.chosen.rect.center = pygame.mouse.get_pos()
            self.cards.update()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_card_take(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.chosen:
                    self.release_card()

    def release_card(self):
        self.chosen.get_unchosed_scale()
        self.chosen.make_card()
        self.check_card_collision(self.chosen)
        self.chosen = None

    def check_card_collision(self, card):
        for collide in pygame.sprite.spritecollide(card, self.cards, False):
            if card.stack(collide):
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for card in self.cards.sprites():
            card.render()
        if self.chosen:
            self.chosen.render()

        pygame.display.flip()

    def _check_card_take(self, mouse_pos):
        for sprite in self.cards:
            if sprite.rect.collidepoint(mouse_pos):
                self.card_taken(sprite)
                break

    def card_taken(self, card):
        card.get_chosen()
        self.chosen = card


if __name__ == '__main__':

    mg = MyGame()
    mg.run_game()
