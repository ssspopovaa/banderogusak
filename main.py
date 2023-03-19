import pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

COLOR_WHITE = 255, 255, 255
COLOR_BLACK = 0, 0, 0
COLOR_RED = 255, 0, 0
COLOR_GREEN = 0, 255, 0

screen = width, height = 800, 600

mainSurface = pygame.display.set_mode(screen)

ball = pygame.Surface((20,20))
ball.fill(COLOR_WHITE)
ballRect = ball.get_rect()
ballSpeed = 5

def creteEnemy():
    enemy = pygame.Surface((20,20))
    enemy.fill(COLOR_RED)
    enemyRect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemySpeed = random.randint(2, 5)

    return [enemy, enemyRect, enemySpeed]

def creteBonus():
    bonus = pygame.Surface((20,20))
    bonus.fill(COLOR_GREEN)
    bonusRect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonusSpeed = random.randint(2, 5)

    return [bonus, bonusRect, bonusSpeed]

CREATE_ENEMY = pygame.USEREVENT +1
CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 5000)

enemies = []
bonuses = []

isActive = True
while isActive:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            isActive = False
        if event.type == CREATE_ENEMY:
            enemies.append(creteEnemy())
        if event.type == CREATE_BONUS:
            bonuses.append(creteBonus())

    pressedKeys = pygame.key.get_pressed()

    mainSurface.fill(COLOR_BLACK)
    mainSurface.blit(ball, ballRect)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        mainSurface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ballRect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        mainSurface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))
        if ballRect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))

    if pressedKeys[K_DOWN] and ballRect.bottom < height:
        ballRect = ballRect.move(0, ballSpeed)
    if pressedKeys[K_UP] and ballRect.top > 0:
        ballRect = ballRect.move(0, -ballSpeed)
    if pressedKeys[K_RIGHT] and ballRect.right < width:
        ballRect = ballRect.move(ballSpeed, 0)
    if pressedKeys[K_LEFT] and ballRect.left > 0:
        ballRect = ballRect.move(-ballSpeed, 0)

    pygame.display.flip()
