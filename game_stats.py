class GameStats:
    '统计游戏信息'

    def __init__(self, game):

        self.setting = game.setting
        self.game_active = True

        self.reset_stats()

    def reset_stats(self):

        self.ships_left = self.setting.ship_limit