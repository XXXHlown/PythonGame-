class Settings():
    '''存储外星人的所有类'''
    def __init__(self):
        #初始化设置
        #静态
        #屏幕设置
        self.screen_width=1500
        self.screen_height=800
        self.bg_color=(230,230,230)
        #飞船设置
        self.ship_limit = 3 #飞船数量
        #子弹设置
        self.bullet_height = 15
        self.bullet_color = 144,238,144
        self.bullets_allowed = 100 #限制子弹数
        #外星人设置
        self.alien_drop_speed = 10 # 下降速度
        #记分板设置
        self.sb_bg_color = 0,0,0
        #加快游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        #初始化各种随游戏进程改变的属性
        self.initialize_dynamic_settings()

    #改变属性
    def initialize_dynamic_settings(self):
        #子弹宽度        
        self.bullet_width = 300
        self.ship_speed_factor = 4
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 5 # 水平速度
        #外星人移动
        self.fleet_direction = 1 # 1表示右移，-1表示左移
        #外星人分值
        self.alien_points = 50

    #加快速度
    def increase_speed(self):
        if self.ship_speed_factor < 18 :
            self.ship_speed_factor *= (self.speedup_scale+0.08)
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_width +=10
        self.alien_points = int(self.alien_points * self.score_scale)