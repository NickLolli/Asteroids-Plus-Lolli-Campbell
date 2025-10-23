import pygame
from config import *

class Button(object):

    def __init__(self, position, size, color, text, image_path=None):
        self.image_path = image_path  # remember if this button uses an image
        self.base_color = color       # store the base color
        self.hover_color = (0, 200, 200)  


        # image
        self.image = pygame.Surface(size)
        self.input_text = text
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, size)
        else:
            if color:
                self.image.fill(color)
            else:
                pass

        self.rect = pygame.Rect((0,0), size)
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        if text:
           
            self.text = self.font.render(self.input_text, False, WHITE)
            #text = font.render(text, False, (BLACK))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.rect.center

            self.image.blit(self.text, self.text_rect)
        else:
            pass

        # set after centering text
        self.rect.topleft = position

    def draw(self, screen, color):
        # use stored colors and avoid filling over image based buttons
        is_hover = self.rect.collidepoint(pygame.mouse.get_pos())

        if self.image_path:
            # For image buttons, just change text color on hover (no fill)
            text_color = BLACK if is_hover else WHITE
            # Re-render text and blit on top of the image
            self.text = self.font.render(self.input_text, False, text_color)
            # Reset base image (scaled) each frame to avoid text ghosting
            base_img = pygame.image.load(self.image_path)
            base_img = pygame.transform.scale(base_img, self.rect.size)
            self.image = base_img
            self.image.blit(self.text, self.text_rect)
        else:
            # For color buttons, fill with cyan base or hover cyan
            fill_color = self.hover_color if is_hover else self.base_color
            self.image.fill(fill_color)
            text_color = BLACK if is_hover else WHITE
            self.text = self.font.render(self.input_text, False, text_color)
            self.image.blit(self.text, self.text_rect)

        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)