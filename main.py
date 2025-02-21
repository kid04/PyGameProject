import pygame
import sys
from settings import Settings
import cards
import texts
import deck



class MyGame:
    def __init__(self):
        pygame.init()
        self.camera = pygame.math.Vector2((0, 0))
        self.camera_moving = False
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.cards = pygame.sprite.Group()
        self.decks = pygame.sprite.Group()
        self.card_dict, self.input_field_dict = texts.card_dict(self)
        for card in self.card_dict.values():
            card.init_i_field()

        time_deck = deck.Deck(self, [self.card_dict['time'].__copy__() for i in range(3)], image_pass='sprites/time_back.bmp',
                              pos=(1100, 700))
        self.decks.add(time_deck)
        letter_card = self.card_dict['letter']
        letter_card.rect.center = (600, 400)
        self.cards.add(letter_card)

        self.i_field = None
        self.chosen = None
        self.chosen_offset = (0, 0)

    def run_game(self):
        while True:
            self._check_events()

            if self.chosen:
                self.chosen.rect.center = pygame.mouse.get_pos()[0]+self.chosen_offset[0], pygame.mouse.get_pos()[1]+self.chosen_offset[1]
            if self.camera_moving:
                self.move_camera(pygame.mouse.get_pos())
            self.cards.update()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if self._check_card_take(mouse_pos):
                        pass
                    elif self._check_deck_draw(mouse_pos):
                        pass
                elif event.button == 3:
                    if self._check_input_field(mouse_pos):
                        pass
                    elif event.button == 3 and not self.camera_moving:
                        self.camera = pygame.mouse.get_pos()
                        self.camera_moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.chosen:
                        self.release()
                if event.button == 3:
                    self.camera_moving = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.i_field:
                        self.i_field.commit()

    def release(self):
        self.chosen.get_unchosen()
        self.chosen = None
        self.chosen_offset = (0, 0)

    def check_card_collision(self, card):
        for collide in pygame.sprite.spritecollide(card, self.cards, False):
            if card.stack(collide):
                break

    def check_i_field_collision(self, card):
        if self.i_field:
            if pygame.Rect.colliderect(card.rect, self.i_field):
                self.i_field.Collide(card)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for deck in self.decks.sprites():
            deck.render()
        for card in self.cards.sprites():
            card.render()
        if self.i_field:
            self.i_field.render()



        if self.chosen:
            self.chosen.render()
        pygame.display.flip()

    def _check_card_take(self, mouse_pos):
        if self.i_field:
            if self.i_field.rect.collidepoint(mouse_pos):
                self.card_taken(self.i_field)
                return True
        for sprite in self.cards:
            if sprite.rect.collidepoint(mouse_pos):
                self.card_taken(sprite)
                return True


        return False

    def card_taken(self, card):
        card.get_chosen()

    def move_camera(self, mouse_pos):
        for card in self.cards:
            card.rect.x += mouse_pos[0] - self.camera[0]
            card.rect.y += mouse_pos[1] - self.camera[1]
        for deck in self.decks:
            deck.rect.x += mouse_pos[0] - self.camera[0]
            deck.rect.y += mouse_pos[1] - self.camera[1]
        if self.i_field:
            self.i_field.rect.x += mouse_pos[0] - self.camera[0]
            self.i_field.rect.y += mouse_pos[1] - self.camera[1]
        self.camera = mouse_pos

    def _check_deck_draw(self, mouse_pos):
        for sprite in self.decks:
            if sprite.rect.collidepoint(mouse_pos):
                sprite.onClick()
                return True
        return False

    def check_receiver_collision(self, card):
        for collide in pygame.sprite.spritecollide(card, self.receivers, False):
            collide.receive(card)
            break

    def _check_input_field(self, mouse_pos):
        if self.i_field:
            if self.i_field.rect.collidepoint(mouse_pos):
                self.i_field.close()
        for sprite in self.cards:
            if sprite.rect.collidepoint(mouse_pos) and sprite.input_field:
                if self.i_field:
                    self.i_field.close()
                self.i_field = sprite.input_field
                self.i_field.rect.topleft = sprite.rect.topleft
                self.i_field.rect.x -= self.settings.input_field_size[0] + self.settings.card_size[0]
                return True
        return False


if __name__ == '__main__':

    mg = MyGame()

    mg.run_game()
