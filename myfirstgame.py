import pygame
import random as r
import math as m
from pygame import mixer


# intializing pygame

pygame.init()

# creating window
screen = pygame.display.set_mode((700, 500))

# TITLE AND ICON
pygame.display.set_caption("DARK SPACE")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background_image.png")

#sound
mixer.music.load("bg_music.mp3")
mixer.music.play(-1)

#
player_Img = pygame.image.load("spaceship.png")
playerX = 330
playerY = 420
playerX_change = 0

# ENEMY
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
No_of_enemies = 7

for i in range(No_of_enemies):
    enemy_Img.append(pygame.image.load("ufo.png"))
    enemyX.append(r.randint(0, 653))
    enemyY.append(r.randint(20, 90))
    enemyX_change.append(0.2)
    enemyY_change.append(50)

# BULLET
bullet_Img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 420
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("Honey.ttf", 40)
testX = 6
testY = 6

# game over
over_font = pygame.font.Font("fire.otf", 2000)


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300 , 200))
    Gameover = mixer.Sound("gameover.wav")
    Gameover.play()



# DEFINING FUNCTION FOR DISPLAYING
def player(x, y):
    screen.blit(player_Img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_Img, (x + 5, y + 10))


def Collide(x1, x2, y1, y2):
    Distance = m.sqrt((m.pow(x1 - x2, 2)) + (m.pow(y1 - y2, 2)))

    if Distance < 27:
        return 1
    else:
        return 0


# creating loop
running = 1
while running:
    # BACKGROUND COLOR BY RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

        # if key is pressed check whether left or right key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletsound = mixer.Sound("bullet.wav")
                    bulletsound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 654:
        playerX = 654
    for i in range(No_of_enemies):
        # GAME OVER
        if enemyY[i] > 380:
            for j in range(No_of_enemies):
                enemyY[i] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 654:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = Collide(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            explosionsound = mixer.Sound("collision.wav")
            explosionsound.play()
            bulletY = 420
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = r.randint(0, 653)
            enemyY[i] = r.randint(20, 90)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 420
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(testX, testY)
    pygame.display.update()
