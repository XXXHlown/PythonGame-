import pygame.font
from pygame.sprite import Group
from ship import Ship

#计分板
class ScoreBoard():
    #初始化涉及得分的属性
    def __init__(self,ai_settings,screen,stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        #字体设置
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        #初始得分图像,文本转图像
        self.prep_score()
        #显示最高分i
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    #得分文本转化为图像
    def prep_score(self):
        #将得分以逗号分开
        rounded_score = int (round(self.stats.score,-1))
        score_str = "Score"+"{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,
                                            self.ai_settings.sb_bg_color)
        #将得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 20
    #得分文本转化为图像
    def prep_high_score(self):
        #将得分以逗号分开
        high_score = int (round(self.stats.score,-1))
        high_score_str = "Highest Score:"+"{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,
                                            self.ai_settings.sb_bg_color)
        #将最高得分放在右上角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.screen_rect.top

    #显示等级
    def prep_level(self):
        self.level_image = self.font.render(('Level:'+str(self.stats.level)),True,
                                            self.text_color,self.ai_settings.sb_bg_color)
        #等级放在左上角
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left
        self.level_rect.top = self.screen_rect.top

    #显示剩余飞船
    def prep_ships(self):
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = self.level_rect.right +ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    #屏幕显示得分
    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        #绘制飞船
        self.ships.draw(self.screen)