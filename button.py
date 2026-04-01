import random
import time
import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, color_on, color_off, sound, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Store color and sound properties
        self.color_on  = color_on
        self.color_off = color_off
        self.sound     = sound

        self.image = pygame.Surface((230, 230))
        self.image.fill(self.color_off)
        self.rect  = self.image.get_rect()

        # Assign x, y coordinates to the top-left of the sprite
        self.rect.topleft = (x, y)

        self.clicked = False

    # ------------------------------------------------------------------
    # Draws button sprite onto the pygame window
    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # ------------------------------------------------------------------
    # Returns True if the mouse position is inside this button's rect
    # ------------------------------------------------------------------
    def selected(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    # ------------------------------------------------------------------
    # Illuminates the button, plays its sound, then resets to off-color
    # ------------------------------------------------------------------
    def update(self, screen):
        # Light up the button
        self.image.fill(self.color_on)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Play the associated sound
        self.sound.play()

        pygame.display.update()

        # Wait 500 ms then restore the off-color
        self.image.fill(self.color_off)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.wait(500)
        pygame.display.update()
