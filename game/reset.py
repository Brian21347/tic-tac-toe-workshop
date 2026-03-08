import pygame
from collections.abc import Callable


class ResetButton(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, get_position: Callable[[], tuple[int, int]]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.get_position = get_position
        self.rect.center = self.get_position()
    
    def check_mouse_collide(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            return True
        return False
    
    def update(self):
        self.rect.center = self.get_position()
