class GameStats:
    '统计游戏信息'

    def __init__(self, game):

        self.setting = game.setting

        self.reset_stats()

        self.high_score = 0

        self.game_active = False
        self.level = 1

    def reset_stats(self):

        self.ships_left = self.setting.ship_limit
        self.score = 0