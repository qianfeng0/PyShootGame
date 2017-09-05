
import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
SHOOT_FREQUENCY = 20

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, down_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.down_image = down_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_cnt = 0

    def move(self):
        self.rect.top += self.speed

    def transToDown(self):
        self.image = self.down_image
        self.down_cnt = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, init_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = plane_img

        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos

        self.speed = 6

        self.bullets = pygame.sprite.Group()
        self.shoot_frequency = SHOOT_FREQUENCY

    def shoot(self, bullet_img):
        if (self.shoot_frequency >= SHOOT_FREQUENCY):
            bullet = Bullet(bullet_img, self.rect.midtop)
            self.bullets.add(bullet)
            self.shoot_frequency = 0
        self.shoot_frequency += 1

    def moveUp(self):
        self.rect.top -= self.speed
        if self.rect.top <= 0:
            self.rect.top = 0

    def moveDown(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height

    def moveLeft(self):
        self.rect.left -= self.speed
        if (self.rect.left < 0):
            self.rect.left = 0

    def moveRight(self):
        self.rect.left += self.speed
        if self.rect.left > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
