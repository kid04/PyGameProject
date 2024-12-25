import pygame
import pygame.font
from pygame.sprite import Sprite

class Card(Sprite):
    def __init__(self, mg_game, image_pass='sprites/blank.png', text='test'):
        super().__init__()
        self.settings = mg_game.settings
        self.screen = mg_game.screen
        self.text = text

        self.next = None
        self.prev = None
        self.first = self
        self.level = 0

        self.image = pygame.transform.scale(pygame.image.load(image_pass), self.settings.card_image_size)
        self.image_rect = self.image.get_rect()

        self.font = pygame.font.SysFont(None, 24)
        self.text_color = (0, 0, 0)

        self.prep_msg(text)
        self.face = pygame.Surface(self.settings.card_size)

        self.make_card()
        self.rect = self.face.get_rect()

    def set_first(self, card):
        self.first = card
        if self.prev:
            print(f"im {self.text} and my prev is {self.prev.text} and my first is {self.first.text}")
            self.prev.set_first(card)

    def prep_msg(self, msg):

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()

    def render(self):
        self.screen.blit(self.face, self.rect)
        if self.prev:
            self.prev.render()

    def get_chosen(self):
        if self.next:
            self.next.prev = None
            self.next.rect.height = self.settings.card_size[1]
            self.next = None
            self.set_first(self)
        self.get_chosed_scale()

    def get_chosed_scale(self):
        self.face = pygame.transform.scale(self.face, (self.face.get_rect().width * 1.5,
                                                       self.face.get_rect().height * 1.5))
        if self.prev:
            self.prev.get_chosed_scale()

    def get_unchosed_scale(self):
        self.face = pygame.transform.scale(self.face, self.settings.card_size)
        if self.prev:
            self.prev.get_unchosed_scale()

    def make_card(self):
        self.face.fill((255, 255, 255))
        face_size = self.face.get_size()
        self.image_rect.center = (face_size[0] / 2,
                                  self.settings.card_image_size[1] / 2)

        self.msg_image_rect.center = (face_size[0] / 2,
                                      (self.image.get_rect().height + face_size[1]) / 2)

        self.face.blit(self.image, self.image_rect)
        self.face.blit(self.msg_image, self.msg_image_rect)
        pygame.draw.rect(self.face, (0, 0, 0), (0, 0, face_size[0], face_size[1]), 2)

        if self.prev:
            self.prev.make_card()

    def stack(self, card):
        if card.first != self and card != self:
            if card.prev:
                self.stack(card.prev)
            else:
                self.next = card
                card.prev = self
                card.rect.height = 20

                if self.next.first:
                    self.set_first(self.next.first)
                else:
                    self.set_first(self.next)
                self.level = card.level + 1
            return True
        else:
            return False

    def update(self) -> None:
        if self.next:
            self.rect.left = self.next.rect.left
            self.rect.top = self.next.rect.top + 20
