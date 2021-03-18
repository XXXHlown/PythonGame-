#响应事件的所有函数
import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
    
#响应按键
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        #向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #向左
        ship.moving_left = True
    #开火！按空格
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    #设置退出游戏快捷键-q
    elif event.key == pygame.K_q:
        sys.exit()
    
#响应松开
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

#响应按键与鼠标事件
def check_events(ai_settings,screen,stats,sb,play_button,ship,
                 aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,
                              aliens,bullets,mouse_x,mouse_y)

#单击play开始，重置游戏
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,
                      aliens,bullets,mouse_x,mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置速度
        ai_settings.initialize_dynamic_settings()
        #隐藏鼠标光标
        pygame.mouse.set_visible(False)
        #重置统计信息
        stats.game_active = True
        stats.reset_stats()
        #重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_ships()
        #清空子弹和外星人编组
        aliens.empty()
        bullets.empty()
        #创建新外星人并居中
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


#更换屏幕图像，并且换到新屏幕
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    #screen.fill(ai_settings.bg_color)
    #飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #飞船出现
    ship.blitme()
    #外星人出现
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()
       
#开火！创建新子弹，限制子弹数
def fire_bullets(ai_settings,screen,ship,bullets):

        if len(bullets)<ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            #将其加入B ullets 的Group中
            bullets.add(new_bullet)

#更新子弹位置
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets): 
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #中弹检测
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
    
#检查是否有子弹击中了外星人，如果是的话则同时删除两者
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    #计分增加
    if collisions :
        for aliens in collisions.values(): #确保每个外星人都被计数
            stats.score +=ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    #检查外星人数量，如果全部被消灭则清空所有子弹重建一组外星人
    if len(aliens)==0:
        bullets.empty()
        ai_settings.increase_speed() #加快游戏节奏
        #提高等级
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)
 
#计算每行容纳的外星人数
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width-2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

#计算屏幕能容纳多少行外星人
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height-
                         (1*alien_height)-ship_height)
    number_rows = int(available_space_y/(1 * alien_height))
    return number_rows

#创建一个外星人加入当行
def creat_alien(ai_settings,screen,aliens,alien_num,row_num):
    alien = Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x = alien_width * 0.75+ 2 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height * 1 + 1 * alien.rect.height * row_num
    aliens.add(alien)

#创建外星人群
def creat_fleet(ai_settings,screen,ship,aliens):
    #先创建一个，再计算能容纳多少个,多少行
    alien = Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建多行外星人
    print(number_rows)
    for row_num in range(number_rows):
        for alien_num in range(number_aliens_x):
            creat_alien(ai_settings,screen,aliens,alien_num,row_num)
    
#外星人到达边缘时采取措施
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break

#将外星人整群下移并改变方向
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1

#更新所有外星人的位置
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人与飞船间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

#检测是否到达底端并处理
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    a = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= a.bottom:
            #像撞到飞船一样
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

#响应外星人与飞船撞击
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    if stats.ships_left > 0:
        #将ship_left减1
        stats.ships_left -= 1
        #更新记分牌
        sb.prep_ships()
        #清空外星人与子弹
        aliens.empty()
        bullets.empty()
        #重建一群外星人，飞船重新归位
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #游戏暂停
        sleep(0.5)
    else:
        stats.game_active = False
        #重新显示光标
        pygame.mouse.set_visible(True)

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    