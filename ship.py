import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship,self).__init__()
        #初始化飞船大小与初始位置
        self.screen=screen
        self.ai_settings=ai_settings
        #加载飞船图像并获取其外接矩形,处理矩形更简单
        self.image=pygame.image.load('C:\\Users\\HP\\Desktop\\Alient\\ship6.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        #将每艘新飞船放在底部
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        #在飞船属性center中增加小数值，方便修改速度
        self.center = float(self.rect.centerx)
        #添加飞船移动标志，可以按住方向键移动
        self.moving_right = False
        self.moving_left =False

    def update(self):
        #根据移动调整飞船位置,限制屏幕活动范围
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center+=self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0 :
            self.center-=self.ai_settings.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx =self.center

    def center_ship(self):
        #飞船居中
        self.center = self.screen_rect.centerx

    def blitme(self):
        #指定位置绘制飞船
        self.screen.blit(self.image,self.rect)