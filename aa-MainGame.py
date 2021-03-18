import sys
import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from gamestats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
      # 初始化游戏并创建一个屏幕对象
    pygame.init()
    pygame.mixer.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    background = pygame.image.load('C:\\Users\\HP\\Desktop\\Alient\\background.jpg')
    pygame.display.set_caption("Alien Invasion",'C:\\Users\\HP\\Desktop\\Alient\\icon.png')
    # 音乐初始化
    file='C:\\Users\\HP\\Desktop\\Alient\\Itro Kontinuum - Alive.mp3'
    #加载音乐文件
    pygame.mixer.music.load(file)
    # 开始播放音乐流
    pygame.mixer.music.play()
    #创建play按钮
    play_button = Button(ai_settings,screen,"PLAY")
    #创建飞船
    ship=Ship(ai_settings,screen)
    #创建子弹的编组
    bullets = Group()
    #创建外星人编组
    aliens = Group()
    #创建外星人群
    gf.creat_fleet(ai_settings,screen,ship,aliens)
    #创建统计信息实例
    stats = GameStats(ai_settings)
    #创建记分牌
    sb = ScoreBoard(ai_settings,screen,stats)
      # 开始游戏的主循环
    while True:
        #绘制背景
        screen.blit(background,(0,0))
          # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,
                      aliens,bullets)
        if stats.game_active:
            pygame.mixer.music.stop()
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
