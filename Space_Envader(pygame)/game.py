import pygame, random, math
from pygame import mixer

# initialization
pygame.init()

# FONT
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Background Sound
# mixer.music.load('filename')
# mixer.music.play(-1)------> -1 means loop

# Screen Creation
screen = pygame.display.set_mode((600, 700))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Background
Background = pygame.image.load("bg.png")

# Player
PlayerImg = pygame.image.load("ship.png")
PlayerX = 280
PlayerY = 500

# Bullet
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 500
Bullet_change_x = 0
Bullet_change_y = 3
Bullet_state = "ready"

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []

Enemy_change_x = []
Enemy_change_y = []
No_of_enemies = 6

# Game Over Text
over = pygame.font.Font("freesansbold.ttf", 64)

for i in range(No_of_enemies):
    EnemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(0, (600 - 64)))
    EnemyY.append(random.randint(50, 150))

    Enemy_change_x.append(0.4)
    Enemy_change_y.append(40)

    Player_change_x = 0

score = 0


def game_over_text(x=120, y=290):
    FONT = over.render("GAME OVER!!", True, (255, 255, 255))
    screen.blit(FONT, (x, y))

def Player(x, y):
    # Blit Just Means Draw in Brief
    screen.blit(PlayerImg, (x, y))


def Enemy(x, y, i):
    # Blit Just Means Draw in Brief
    screen.blit(EnemyImg[i], (x, y))


def Bullet_fire(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def IsCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

while running:

    # RGB Color -------> 0,0,0 = black

    screen.fill((0, 0, 0))

    # Image BG
    # screen.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            # print("Left Pressed")
            Player_change_x = -0.3

        if event.key == pygame.K_RIGHT:
            # print("Right Pressed")
            Player_change_x = +0.3

        if event.key == pygame.K_SPACE:
            if Bullet_state == "ready":
                BulletX = int(PlayerX)
                # Bullet_sound = mixer.Sound("FileName")
                # Bullet_sound.play()----Sound for Only Once and music for Continous Sound
                Bullet_fire(BulletX, BulletY)

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            Player_change_x = 0

    PlayerX += Player_change_x

    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= (600 - 64):
        PlayerX = (600 - 64)

    for i in range(No_of_enemies):

        # Game Over
        if EnemyY[i] > 455:
            for j in range(No_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += Enemy_change_x[i]

        if EnemyX[i] <= 0:
            Enemy_change_x[i] = 0.4
            # Enemy_change_y = 40
            EnemyY[i] += Enemy_change_y[i]
        elif EnemyX[i] >= (600 - 64):
            Enemy_change_x[i] = -0.4
            # Enemy_change_y = 40
            EnemyY[i] += Enemy_change_y[i]
        # collision
        collision = IsCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)

        if collision:
            BulletY = 500
            Bullet_state = "ready"
            score += 1
            EnemyX[i] = random.randint(0, 500)
            EnemyY[i] = random.randint(50, 150)
        Enemy(EnemyX[i], EnemyY[i], i)

    # Enemy_change_y = random.randint(0, 5)
    # EnemyY += Enemy_change_y

    # Bullet Moment
    if BulletY <= 0:
        BulletY = 500
        Bullet_state = "ready"

    if Bullet_state is "fire":
        BulletY -= Bullet_change_y
        Bullet_fire(BulletX, BulletY)

    text = STAT_FONT.render("Score: " + str(score), 1, (0, 255, 255))
    screen.blit(text, (600 - 10 - text.get_width(), 10))

    Player(PlayerX, PlayerY)

    # Always Write To keep updating screen
    pygame.display.update()
