import pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

COLOR_WHITE = 255, 255, 255
COLOR_BLACK = 0, 0, 0
COLOR_RED = 255, 0, 0
COLOR_GREEN = 0, 255, 0

screen = width, height = 800, 600
font = pygame.font.SysFont('Verdana', 20)

mainSurface = pygame.display.set_mode(screen)

player = pygame.image.load('player.png').convert_alpha()
playerRect = player.get_rect()
playerSpeed = 5

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bgSpeed = 3


def creteEnemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 35))
    enemyRect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemySpeed = random.randint(2, 5)

    return [enemy, enemyRect, enemySpeed]

def creteBonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (50, 80))
    bonusRect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonusSpeed = random.randint(2, 5)

    return [bonus, bonusRect, bonusSpeed]

CREATE_ENEMY = pygame.USEREVENT +1
CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 5000)

enemies = []
bonuses = []
scores  = 0

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

    bgX -= bgSpeed
    bgX2 -= bgSpeed
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    mainSurface.blit(bg, (bgX, 0))
    mainSurface.blit(bg, (bgX2, 0))

    mainSurface.blit(player, playerRect)
    mainSurface.blit(font.render(str(scores), True, COLOR_BLACK), (width - 30, 20))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        mainSurface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if playerRect.colliderect(enemy[1]):
            isActive = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        mainSurface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))
        if playerRect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressedKeys[K_DOWN] and playerRect.bottom < height:
        playerRect = playerRect.move(0, playerSpeed)
    if pressedKeys[K_UP] and playerRect.top > 0:
        playerRect = playerRect.move(0, -playerSpeed)
    if pressedKeys[K_RIGHT] and playerRect.right < width:
        playerRect = playerRect.move(playerSpeed, 0)
    if pressedKeys[K_LEFT] and playerRect.left > 0:
        playerRect = playerRect.move(-playerSpeed, 0)

    pygame.display.flip()
