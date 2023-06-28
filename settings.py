class Settings:
    '''存储设置'''

    def __init__(self):
        '''初始化设置'''

        # 屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        self.FULL_SCREEN = False

        # 子弹
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.ship_limit = 3
