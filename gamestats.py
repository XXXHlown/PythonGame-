class GameStats():
    #跟踪统计游戏信息
    def __init__(self, ai_settings):
        #初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏活动状态
        self.game_active = False
        #最高得分，任何情况下都不重置
        self.high_score = 0

    #初始化随游戏进行变化的统计信息
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
