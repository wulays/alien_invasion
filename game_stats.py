class GameStats:
    '统计游戏信息'

    def __init__(self, game):

        self.setting = game.setting

        self.reset_stats()

        self.game_active = False

    def reset_stats(self):

        self.ships_left = self.setting.ship_limit