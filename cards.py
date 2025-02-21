import pygame
import pygame.font
from pygame.sprite import Sprite
from input_field import Field
import FontSize
class Card(Sprite):
    def __init__(self, mg_game, image_pass='sprites/blank.png', text='test', tags=[-1], id=-1):
        super().__init__()
        self.game = mg_game
        self.settings = mg_game.settings
        self.screen = mg_game.screen
        self.text = text
        self.id = id
        self.image_pass = image_pass
        self.tags = tags


        self.next = None
        self.prev = None
        self.first = self
        self.level = 0

        self.bg_colour = (255, 255, 255)
        self.image = pygame.transform.scale(pygame.image.load(image_pass), self.settings.card_image_size)
        self.image_rect = self.image.get_rect()
        self.font_size = self.settings.font_size

        self.font = pygame.font.SysFont(None, self.font_size)
        self.text_color = (0, 0, 0)

        self.prep_msg(text)
        self.face = pygame.Surface(self.settings.card_size)

        self.make_card()
        self.rect = self.face.get_rect()

    def init_i_field(self):
        self.input_field = Field(self.game, self)
    def __copy__(self):
        card = Card(self.game, self.image_pass, self.text, self.tags, self.id)
        card.init_i_field()
        return card
    def set_first(self, card):
        self.first = card
        if self.prev:
            self.prev.set_first(card)

    def prep_msg(self, text):
        width, height = self.settings.card_size
        height -= self.settings.card_image_size[1]
        font_size = FontSize.get_font_size(self.font)
        lines = []
        line = ''
        words = text.split(' ')
        s_len = 0
        len_max = width
        for word in words:
            word_len = 0
            for symbol in word:
                word_len += font_size[symbol]
            s_len += word_len + font_size[' ']
            if s_len <= len_max:
                line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
                s_len = word_len + font_size[' ']
                if s_len > len_max:
                    self.font_size -= 1
                    self.font = pygame.font.SysFont(None, self.font_size)
                    self.prep_msg(text)
                    return None
        line = line[:-1]
        lines.append(line)
        self.msg_image = pygame.Surface((width, height))
        self.msg_image.fill(self.bg_colour)
        self.text_image = pygame.Surface((width, len(lines)*(font_size['height']+4)))
        self.text_image.fill(self.bg_colour)
        i = 0
        for line in lines:
            line_image = self.font.render(line, True, self.text_color)
            line_image_rect = line_image.get_rect()
            line_image_rect.topleft = (0, i * (font_size['height'] + 4))
            line_image_rect.centerx = width // 2
            self.text_image.blit(line_image, line_image_rect)

            i += 1
        self.text_image_rect = self.text_image.get_rect()
        if height < self.text_image_rect.size[1]:
            self.font_size -= 1
            self.font = pygame.font.SysFont(None, self.font_size)
            self.prep_msg(text)
        self.msg_image_rect = self.msg_image.get_rect()
        self.text_image_rect.center = self.msg_image_rect.center
        self.msg_image.blit(self.text_image, self.text_image_rect)
        # self.msg_image = self.font.render(text, True, self.text_color)
        # self.msg_image_rect = self.msg_image.get_rect()

    def render(self):
        self.screen.blit(self.face, self.rect)
        if self.prev:
            self.prev.render()

    def get_chosen(self):
        self.game.chosen = self
        if self.next:
            self.next.prev = None
            self.next.rect.height = self.settings.card_size[1]
            self.next = None
            self.set_first(self)
        self.get_chosed_scale()

    def get_unchosen(self):
        self.get_unchosed_scale()
        self.make_card()
        self.game.check_i_field_collision(self)
        self.game.check_card_collision(self)
        # self.game.check_receiver_collision(self)

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

    def set_screen(self, screen):
        self.screen = screen
        if self.prev:
            self.prev.set_screen(screen)
    def update(self) -> None:
        if self.next:
            self.rect.left = self.next.rect.left
            self.rect.top = self.next.rect.top + 20
        elif self.game.chosen != self:
            for collision in pygame.sprite.spritecollide(self, self.game.decks, 0):
                if collision and collision != self.game.chosen and collision != self:
                    x = self.rect.center[0] - collision.rect.center[0]
                    y = self.rect.center[1] - collision.rect.center[1]
                    l = (x ** 2 + y ** 2) ** (1 / 2)
                    nx = x / l
                    ny = y / l
                    self.rect.left += nx*12
                    self.rect.top += ny*12
            # for collision in pygame.sprite.spritecollide(self, self.game.receivers, 0):
            #     if collision and collision != self.game.chosen and collision != self:
            #         x = self.rect.center[0] - collision.rect.center[0]
            #         y = self.rect.center[1] - collision.rect.center[1]
            #         if x == 0 and y == 0:
            #             x = 1
            #         l = (x ** 2 + y ** 2) ** (1 / 2)
            #         nx = x / l
            #         ny = y / l
            #         self.rect.left += nx*12
            #         self.rect.top += ny*12

            for collision in pygame.sprite.spritecollide(self, self.game.cards, 0):
                if collision and \
                        collision != self.game.chosen and \
                        collision != self and \
                        collision.first != self.game.chosen:

                    x = self.rect.center[0] - collision.rect.center[0]
                    y = self.rect.center[1] - collision.rect.center[1]
                    if x == 0 and y == 0:
                        x = 1
                    l = (x**2 + y**2)**(1/2)
                    nx = x/l
                    ny = y/l
                    self.rect.left += nx*12
                    self.rect.top += ny*12
                    collision.rect.left -= nx*12
                    collision.rect.top -= ny*12

