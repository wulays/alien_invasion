import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    '''管理游戏资源和行为'''

    def __init__(self):
        '''初始化游戏资源'''
        pygame.init()
        pygame.display.set_caption('外星入侵大游戏')

        self.setting = Settings()

        if self.setting.FULL_SCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.setting.screen_width = self.screen.get_rect().width
            self.setting.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))

        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        # 飞船
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, 'Play')


    def run_game(self):
        '''开始游戏'''

        while True:
            # 监听用户键盘和鼠标事件
            self._check_events()

            if self.stats.game_active:
                # 更新飞船
                self.ship.updata()
                self._update_bullets()

                # 更新外星人
                self._update_aliens()

            # 更新屏幕
            self._updata_screen()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):

            self.setting.initialize_dynamic_setting()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

    # 处理键盘按下
    def _check_keydown_events(self, event):
        # 向右移动
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        # 向左移动
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True
        # 按Q推出
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    # 处理键盘松开
    def _check_keyup_events(self, event):
        # 向右停止
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        # 向左停止
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False


    def _updata_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _fire_bullet(self):

        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if(collisions):
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()



    def _create_fleet(self):

        alien = Alien(self)

        alien_width, alien_height = alien.rect.size

        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        available_space_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):

        self.aliens.update()
        self._check_fleet_edges()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):

        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
 
if __name__ == '__main__':
    # 创建游戏示例并运行
    game = AlienInvasion()
    game.run_game()
