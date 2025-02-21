import pygame
from pygame.sprite import Sprite
import texts
import FontSize
import math

class Field(Sprite):
    def __init__(self, game, source):
        self.game = game
        self.source = source
        self.id = self.source.id
        self.input, self.input_cards = game.input_field_dict.get(self.id, ({}, {}))
        self.input_rects = {}

        self.bg_colour = (255, 255, 255)
        self.text_colour = (0, 0, 0)
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.width, self.height = self.settings.input_field_size

        self.font = pygame.font.SysFont(None, 24)
        self.prep_msg()
        self.prep_input(self.input)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.input_image_rect = self.input_image.get_rect()
        self.input_image_rect.topleft = (self.surface.get_size()[0] // 2, 3)

    def render(self):

        self.surface.fill(self.bg_colour)
        self.surface.blit(self.msg_image, (3, 3))
        if self.input:
            self.prep_input(self.input)
        # if len(self.input_cards) > 0:
        #     for card in self.input_cards:
        #         self.input_image.blit(self.input_cards[card].face, self.input_rects[card])
        self.surface.blit(self.input_image, self.input_image_rect)

        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.rect.size[0], self.rect.size[1]), 2)
        self.screen.blit(self.surface, self.rect)

    def update_surface(self):

        if self.rect:
            pos = self.rect.topleft
        else:
            pos = (0, 0)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.input_image_rect = self.input_image.get_rect()
        self.input_image_rect.topleft = (self.surface.get_size()[0] // 2, 3)
        self.rect.topleft = pos

    def update_height(self):
        self.height = max(self.input_image_rect.height, self.msg_image_rect.height, self.settings.input_field_size[1])
        self.update_surface()


    def prep_msg(self):
        self.text_id = self.id
        for card in self.input_cards.values():
            self.text_id *= card.id
        if self.id == self.text_id:
            text = texts.input_texts[self.id]
        else:
            text = texts.spoiler_texts.get(self.text_id, texts.input_texts[self.id])
        font_size = FontSize.get_font_size(self.font)
        lines = []
        line = ''
        words = text.split(' ')
        s_len = 0
        len_max = self.width / 2 - 6

        for word in words:
            word_len = 0
            for symbol in word:
                word_len += font_size[symbol]
            if word_len > 0:
                s_len += word_len + font_size[' ']
                if s_len <= len_max:
                    line += word + ' '
                else:
                    lines.append(line)
                    line = word + ' '
                    s_len = word_len + font_size[' ']
            else:
                lines.append(line)
                line = ''
                s_len = 0
        lines.append(line)
        self.msg_image = pygame.Surface((self.width//2, len(lines)*(font_size['height']+4) + 15))
        self.msg_image.fill(self.bg_colour)
        i = 0
        for line in lines:
            line_image = self.font.render(line, True, self.text_colour)
            self.msg_image.blit(line_image, (0, i*(font_size['height']+4)))
            i += 1
        self.msg_image_rect = self.msg_image.get_rect()
        if self.height < self.msg_image_rect.size[1]:
            self.update_height()


    def get_chosen(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos

        x = x - self.rect.x - self.input_image_rect.x
        y -= self.rect.y
        for slot in self.input_cards:
            print(self.input_cards[slot].rect.center)
        for slot in self.input_cards:

            if self.input_cards[slot].rect.collidepoint(x, y):
                card = self.input_cards[slot]
                self.game.cards.add(card)
                card.get_chosen()
                self.input_cards.pop(slot, None)
                self.prep_msg()
                self.update_height()
                return True

        self.game.chosen_offset = (self.rect.center[0] - mouse_pos[0], self.rect.center[1] - mouse_pos[1])
        self.game.chosen = self
    def get_unchosen(self):
        pass

    def close(self):
        self.game.i_field = None

        for card in self.input_cards.values():
            print(card.rect.topleft, self.rect.topleft)
            self.game.cards.add(card)
            card.rect.x += self.rect.x + self.width // 2
            card.rect.y += self.rect.y
        self.input_cards.clear()
    def prep_input(self, input):
        font_size = FontSize.get_font_size(self.font)
        card_size = self.settings.card_size
        width = self.width // 2 - 6
        card_in_line_max = width // card_size[0]
        card_in_line = card_in_line_max
        lines = math.ceil(len(input) / card_in_line)
        height = lines * (font_size['height'] + card_size[1] + 15)

        self.input_image = pygame.Surface((self.width, height))
        self.input_image.fill(self.bg_colour)
        i = 0
        for pack in input:
            if i + card_in_line_max >= len(input):
                if len(input) % card_in_line_max != 0:
                    card_in_line = len(input) % card_in_line_max
            x = self.width // 4 // card_in_line + (i % card_in_line) * self.width // 2 // card_in_line
            y = (i // card_in_line) * (font_size['height'] + card_size[1] + 15)
            #line_image = self.font.render(pack, True, self.text_colour)
            line_image = FontSize.scale_line(pack, None, width // card_in_line, 24, (0, 0, 0))


            l_rect = line_image.get_rect()
            l_rect.centerx = x
            l_rect.y = y
            self.input_image.blit(line_image, l_rect)

            rect = pygame.rect.Rect(0, 0, card_size[0], card_size[1])
            rect.centerx = x
            rect.y = y+font_size['height'] + 5
            pygame.draw.rect(self.input_image, (255, 0, 255), rect, 2)
            self.input_rects[pack] = rect
            i += 1



        if self.input_image.get_rect().height > self.height:
            self.update_height()
            #self.height = self.input_image.get_rect().height

    def Collide(self, card):
        card_center = card.rect.center
        card.rect.left, card.rect.top = card.rect.left - self.rect.left - self.rect.size[0]//2, card.rect.top - self.rect.top
        for slot in self.input:
            if pygame.Rect.colliderect(card.rect, self.input_rects[slot]) and len(set(card.tags) & set(self.input[slot])) > 0 and not self.input_cards.get(slot, False):

                self.input_cards[slot] = card
                self.game.cards.remove(card)
                if self.game.chosen == card:
                    self.game.chosen = None
                card.rect.center = self.input_rects[slot].center
                self.prep_msg()
                return True
        card.rect.center = card_center

    def commit(self):
        for card in self.input_cards.values():
            self.id *= card.id
            if self.game.input_field_dict.get(self.id, False):
                self.prep_msg()
                print(self.game.input_field_dict[self.id])
                self.input, self.input_cards = self.game.input_field_dict.get(self.id, ({}, {}))
                self.prep_input(self.input)
                for card in self.input_cards:
                    self.input_cards[card].rect.center = self.input_rects[card].center
