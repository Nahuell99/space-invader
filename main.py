import pygame
import random
import math

# inicializa pygame
pygame.init()

# Crea la ventana
displayX = 800
displayY = 600

screen = pygame.display.set_mode((displayX, displayY))

# Fondo
fondo = pygame.image.load('fondo.png')

# Titulo eh icono de la ventana
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('juegos.png')
pygame.display.set_icon(icon)

# personaje cargado a variable
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_speed = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# enemigo cargado a variable
enemyImg = []
enemyX = []
enemyY = []
enemyX_speed = []
enemyY_speed = []
num_enemy = 6

for i in range(num_enemy):
    enemyImg.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_speed.append(0.3)
    enemyY_speed.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# vacuna cargado a variable
vacunaImg = pygame.image.load('vacuna.png')
vacunaX = 0
vacunaY = 480
vacunaY_speed = 0.5
vacuna_state = "ready"


#Puntuacion

score_value = 0
font = pygame.font.Font('APOLLO.otf', 32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global vacuna_state
    #cambia el estado de la vacuna a 'fire'
    vacuna_state = "fire"
    screen.blit(vacunaImg, (x + 16, y + 10))

#COLICIONES
def isCollision(enemyX,enemyY,vacunaX,vacunaY):
    distance = math.sqrt( (math.pow(enemyX - vacunaX,2)) + (math.pow(enemyY - vacunaY,2)) )
    if distance < 27:
        return True
    else:
        return False


# Loop Game
running = True
while running:
    #Fondo negro (definido por RGB)
    screen.fill((0, 0, 0))
    screen.blit(fondo, (0, 0))

    #Loop para poder cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Movimiento de la nave. Toma el evento PRECIONAR tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_speed = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_speed = 0.2
            if event.key == pygame.K_SPACE: #DETECTA ESPACIO Y DISPARA
                #comprueba si la vacuna ya esta en pantalla
                if vacuna_state is "ready":
                    #toma la posicion 'X' del player para iniciar el disparo de la vacuna
                    vacunaX = playerX
                    fire_bullet(vacunaX, vacunaY)
        #Toma el evento DEJAR DE PRECIONAR una tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                playerX_speed = 0.0


    #Comrpueba choque contra borde, player
    playerX += playerX_speed
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    # Comrpueba choque contra borde, enemigos
    for i in range(num_enemy):
        enemyX[i] += enemyX_speed[i]
        if enemyX[i] <= 0:
            enemyX_speed[i] = 0.3
            enemyY[i] += 7
        elif enemyX[i] >= 736:
            enemyX_speed[i] = -0.3
            enemyY[i] += 7

        # COLICIONES
        collision = isCollision(enemyX[i], enemyY[i], vacunaX, vacunaY)
        if collision:
            vacunaY = 480
            vacuna_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Vacuna movimiento
    if vacunaY <= 0 :
        vacunaY = 480
        vacuna_state = "ready"

    if vacuna_state is "fire":
        fire_bullet(vacunaX,vacunaY)
        vacunaY -= vacunaY_speed



    player(playerX, playerY)
    show_score(textX,textY)


    pygame.display.update()