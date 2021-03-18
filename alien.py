import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #创建外星人类
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings= ai_settings
        self.image = pygame.image.load("C:\\Users\\HP\\Desktop\\Alient\\alien1.png")
        #设置外星人的rect
        self.rect = self.image.get_rect()
        #初始位置左上角附近，有一个图像的边距
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 
        #小数外星人的准确位置
        self.x = float(self.rect.x)

    def check_edge(self):
        #检测边缘，触碰边缘返回True
        a = self.screen.get_rect()
        if self.rect.right >= a.right :
            return True
        elif self.rect.left <= 0 :
            return True
        
    def update(self):
        self.x += (self.ai_settings.alien_speed_factor*
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        #指定位置绘制外星人
        self.screen.blit(self.image,self.rect)

