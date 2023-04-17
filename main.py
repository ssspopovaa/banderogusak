import pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from os import listdir

pygame.init()

FPS = pygame.time.Clock()

COLOR_WHITE = 255, 255, 255
COLOR_BLACK = 0, 0, 0
COLOR_RED = 255, 0, 0
COLOR_GREEN = 0, 255, 0

screen = width, height = 1600, 900
font = pygame.font.SysFont('Verdana', 20)

mainSurface = pygame.display.set_mode(screen)

IMG_PATH = 'goose'
playerImages = [pygame.image.load(IMG_PATH + '/' + file).convert_alpha() for file in listdir(IMG_PATH)]

imageIndex = 0
player = playerImages[imageIndex]
playerRect = player.get_rect()
playerSpeed = 5

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bgSpeed = 2

bgEnd = pygame.transform.scale(pygame.image.load('background-end.png').convert(), screen)
fontEnd = pygame.font.SysFont('Verdana', 100)

def creteEnemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 35))
    enemyRect = pygame.Rect(width, random.randint(0, height - enemy.get_size()[1]), *enemy.get_size())
    enemySpeed = random.randint(3, 5)

    return [enemy, enemyRect, enemySpeed]

def creteBonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (50, 80))
    bonusRect = pygame.Rect(random.randint(0, width - bonus.get_size()[0]), 0, *bonus.get_size())
    bonusSpeed = 2

    return [bonus, bonusRect, bonusSpeed]

CREATE_ENEMY = pygame.USEREVENT +1
CREATE_BONUS = pygame.USEREVENT +2
ANIMATE_PLAYER = pygame.USEREVENT +3
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 5000)
pygame.time.set_timer(ANIMATE_PLAYER, 150)

enemies = []
bonuses = []
scores  = 0

isActive = True
isExit = True
while isExit:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            isActive = False
            isExit = False
        if event.type == CREATE_ENEMY and isActive :
            enemies.append(creteEnemy())
        if event.type == CREATE_BONUS and isActive :
            bonuses.append(creteBonus())
        if event.type == ANIMATE_PLAYER  and isActive:
            imageIndex += 1
            if imageIndex == len(playerImages):
                imageIndex = 0

            player = playerImages[imageIndex]

    pressedKeys = pygame.key.get_pressed()

    if isActive :
        bgX -= bgSpeed
        bgX2 -= bgSpeed

        if bgX < -bg.get_width():
            bgX = bg.get_width()
        if bgX2 < -bg.get_width():
            bgX2 = bg.get_width()
    
        mainSurface.blit(bg, (bgX, 0))
        mainSurface.blit(bg, (bgX2, 0))
    else:
        mainSurface.blit(bgEnd, (0, 0))
        mainSurface.blit(fontEnd.render('Your record: ' + str(scores), True, COLOR_RED), (width - 1150, 400))    


    mainSurface.blit(player, playerRect)
    mainSurface.blit(font.render('Score: ' + str(scores), True, COLOR_BLACK), (width - 100, 20))

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

# mainSurface.blit(bgEnd, (0, 0))