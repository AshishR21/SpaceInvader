import pygame
import random
import math

# Initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((512, 512))

# Title and Icon
pygame.display.set_caption("Space Invader")
# icon = pygame.image.load('./Img/spaceship.png')
# pygame.display.set_icon(icon)
# background = pygame.image.load("./Img/universe.png")

game_state = 'PLAY'

# Player Init
playerImg = pygame.image.load('./Img/spaceship.png')
playerX = 250
playerY = 480
# Player movement
playerX_change = 0
playerY_change = 0

# Enemy Init
No_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(No_of_enemies):
    enemyImg.append(pygame.image.load('./Img/ufo.png'))
    enemyX.append(random.randint(0, 480))
    enemyY.append(random.randint(0, 10))
    enemyX_change.append(0.1 * random.randint(2, 6))
    enemyY_change.append(0.1 * random.randint(1, 2))

# Bullet Init
bulletImg = pygame.image.load('./Img/bullet.png')
bulletX = 0
bulletY = 0
# Enemy movement
bulletX_change = 0
bulletY_change = 0.6
bullet_State = 'READY'

# Score
score = 0
font = pygame.font.SysFont('Calibre', 30)
scoreX = 5
scoreY = 5


def show_score(x, y):
    msg = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(msg, (x, y))


def game_over():
    over_font = pygame.font.SysFont('Calibre', 60)
    over_msg = over_font.render("GAME OVER!", True, (255, 255, 255))
    global game_state
    game_state = 'OVER'
    screen.blit(over_msg, (240, 240))


def draw_player(x, y):
    screen.blit(playerImg, (x, y))


def draw_enemy(x, y, ixy):
    screen.blit(enemyImg[ixy], (x, y))


def draw_bullet(x, y):
    global bullet_State
    screen.blit(bulletImg, (x + 4, y - 20))
    bullet_State = 'FIRE'


def is_collision(eX, eY, bX, bY):
    d = math.sqrt(math.pow((eX - bX), 2) + math.pow((eY - bY), 2))
    if d < 32:
        return True


# Game Loop
running = True
while running:
    # Events
    for event in pygame.event.get():
        # Exit event
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, change player coordinate.
        if event.type == pygame.KEYDOWN:
            # Left Movement
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            # Right Movement
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            # Up Movement
            if event.key == pygame.K_UP:
                playerY_change = -1
            # Down Movement
            if event.key == pygame.K_DOWN:
                playerY_change = 1

            # Bullet Fire
            if event.key == pygame.K_SPACE and bullet_State == 'READY':
                bulletX = playerX
                bulletY = playerY
                draw_bullet(bulletX, bulletY)

        # Stop movement once released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    if game_state == 'PLAY':
        # Background color of screen
        screen.fill((255, 200, 150))
        # screen.blit(background, (0, 0))

        # Updated Position
        playerX += playerX_change
        playerY += playerY_change

        # Limits Movement
        if playerX <= 0:
            playerX = 0
        elif playerX >= 480:
            playerX = 480

        if playerY <= 300:
            playerY = 300
        elif playerY >= 480:
            playerY = 480

        # Enemy Movement
        for i in range(No_of_enemies):
            # Game over
            if is_collision(playerX, playerY, enemyX[i], enemyY[i]):
                for j in range(No_of_enemies):
                    enemyX[j] = 600
                    enemyY[j] = 600
                score = 0
                game_over()
                break

            if enemyX[i] <= 0 or enemyX[i] >= 480:
                enemyX_change[i] = -1 * enemyX_change[i]

            enemyX[i] = enemyX[i] + enemyX_change[i]
            enemyY[i] = enemyY[i] + enemyY_change[i]

            # collision
            if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = playerY
                bulletX = playerX
                enemyX[i] = random.randint(0, 480)
                enemyY[i] = random.randint(0, 10)
                bullet_State = 'READY'
                score += 1

            # Add Enemy
            draw_enemy(enemyX[i], enemyY[i], i)

        # Bullet State
        if bulletY <= 0:
            bulletY = playerY
            bulletX = playerX
            bullet_State = 'READY'

        if bullet_State == 'FIRE':
            bulletY -= bulletY_change
            draw_bullet(bulletX, bulletY)

        # Add Player
        draw_player(playerX, playerY)

        # Add Score
        show_score(scoreX, scoreY)

    # Update screen with every action
    pygame.display.update()
