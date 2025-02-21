import pygame


def get_font_size(font):
    font_map = {}
    alphabet = ' абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ,.:?!-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\"'
    for symbol in alphabet:
        width = pygame.font.Font.size(font, symbol)[0]
        height = pygame.font.Font.size(font, symbol)[1]
        font_map[symbol] = width
    font_map['height'] = height
    return font_map

def scale_line(text, font_style, width, size, text_color):
    font = pygame.font.SysFont(font_style, size)
    line_image = font.render(text, True, text_color)
    if line_image.get_width() > width:
        return scale_line(text, font_style, width, size - 1, text_color)
    else:
        return line_image