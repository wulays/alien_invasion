import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''宇宙飞船'''

    def __init__(self, game):
        '''初始化飞船和飞船位置'''

        super().__init__()

        self.setting = game.setting

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # 加载飞船图像
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘飞船，都放置于屏幕底部
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动飞船
        self.move_right = False
        self.move_left = False

        self.x = float(self.rect.x)

    def blitme(self):
        '''指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def updata(self):

        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        elif self.move_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed

        self.rect.x = self.x

    def center_ship(self):

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)