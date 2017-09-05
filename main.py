import pygame
import sys
import random

import role

def init_player():
    plane_img = pygame.Surface([50, 50])
    plane_img.fill(pygame.Color(100, 100, 100, 100))
    player = role.Player(plane_img, [role.SCREEN_WIDTH / 2, role.SCREEN_HEIGHT / 2])
    return player

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((480, 800))
    pygame.display.set_caption('飞机大战')

    text_font = pygame.font.Font(None, 36)

    background = pygame.Surface([480,800])
    background.fill(pygame.Color(200, 200, 200))
    
    bullet_img = pygame.Surface([10,10])
    bullet_img.fill(pygame.Color(100, 100, 100))

    enemy_img = pygame.Surface([30, 30])
    enemy_img.fill(pygame.Color(100, 100, 100))

    enemy_down_img = pygame.Surface([30, 30])
    enemy_down_img.fill(pygame.Color(255, 0, 0))

    player = init_player()
    enemies = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()
    enemy_frequency = 0
    score = 0

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.shoot(bullet_img)

        #生成敌机
        if enemy_frequency >= 50:
            enemy_frequency = 0
            enemy_pos = [random.randint(0, role.SCREEN_WIDTH - enemy_img.get_width()), 0]
            enemies.add(role.Enemy(enemy_img, enemy_down_img, enemy_pos))
        enemy_frequency += 1

        # 移动子弹
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        ##移动敌机
        for enemy in enemies:
            enemy.move()
            if enemy.rect.top > role.SCREEN_HEIGHT:
                enemies.remove(enemy)

        #移动玩家
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            player.moveUp()
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            player.moveDown()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            player.moveLeft()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            player.moveRight()
        
        #击落
        temp_enemies_down = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
        score += len(temp_enemies_down) * 10
        for enemy_down in temp_enemies_down:
            enemy_down.transToDown()
            enemies_down.add(enemy_down)

        #绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))

        #绘制FPS
        fps_text = text_font.render(str(int(clock.get_fps())), True, (128, 128, 128))
        fps_rect = fps_text.get_rect()
        fps_rect.topleft = [10,10]
        screen.blit(fps_text, fps_rect)

        #绘制分数
        score_text = text_font.render(str(int(score)), True, (128, 128, 128))
        score_rect = score_text.get_rect()
        score_rect.midbottom = [240,700]
        screen.blit(score_text, score_rect)

        #绘制子弹
        player.bullets.draw(screen)

        #绘制玩家
        screen.blit(player.image, player.rect)

        #绘制敌机
        enemies.draw(screen)

        for enemy_down in enemies_down:
            if enemy_down.down_cnt > 7:
                enemies_down.remove(enemy_down)
            enemy_down.down_cnt += 1
        
        enemies_down.draw(screen)

        pygame.display.update()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
