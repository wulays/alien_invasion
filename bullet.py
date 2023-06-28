import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '管理飞船发射的子弹'

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.setting = game.setting
        self.color = self.setting.bullet_color

        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):

        self.y -= self.setting.bullet_speed

        self.rect.y = self.y

    def draw_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)