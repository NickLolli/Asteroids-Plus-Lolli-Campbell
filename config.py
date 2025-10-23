import pygame
pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800
# create "scree" that way we can load our images here once
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

TILESIZE = 16
#42 by 42 tile size

#Asteroid Sizes
BIG_ASTEROID_SIZE = TILESIZE * 7
MED_ASTEROID_SIZE = TILESIZE * 5
SM_ASTEROID_SIZE = TILESIZE * 3

#target FPS
FPS = 60

#layers
PLAYER_LAYER = 4
SHIP_LAYER = 3
ASTEROID_LAYER = 3
SHIP_BULLET_LAYER = 2

#Lives
PLAYER_LIVES = 3

# vulnerability time in ms
DAMAGE_LOOP = 0

# speeds (temporary)
PLAYER_SPEED = 3
ASTEROID_SPEED = 1

#colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
CYAN = (0, 200, 200)

# saucer bullets
BULLET_SPEED = 8
BULLET_COLOR = BLACK 
BULLET_SIZE = 5
SPECIAL_BULLET_COLOR = RED
SPECIAL_BULLET_SPEED = 8

# player ship images
SHIP_A = [
    pygame.image.load('Images/ships/ship-a/ship-a1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a-damaged.png').convert_alpha()
]

SHIP_A_BUTTON = [
    pygame.transform.scale(SHIP_A[0], (200,200)),
    pygame.transform.scale(SHIP_A[1], (200,200)),
    pygame.transform.scale(SHIP_A[2], (200,200))
]

SHIP_B = [
    pygame.image.load('Images/ships/ship-b/ship-b1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b-damaged.png').convert_alpha()
]

SHIP_B_BUTTON = [
    pygame.transform.scale(SHIP_B[0], (200,200)),
    pygame.transform.scale(SHIP_B[1], (200,200)),
    pygame.transform.scale(SHIP_B[2], (200,200))
]

SHIP_C = [
    pygame.image.load('Images/ships/ship-c/ship-c1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c-damaged.png').convert_alpha()
]

SHIP_C_BUTTON = [
    pygame.transform.scale(SHIP_C[0], (200,200)),
    pygame.transform.scale(SHIP_C[1], (200,200)),
    pygame.transform.scale(SHIP_C[2], (200,200))
]

SHIP_D = [
    pygame.image.load('Images/ships/ship-d/ship-d1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d-damaged.png').convert_alpha()
]

SHIP_D_BUTTON = [
    pygame.transform.scale(SHIP_D[0], (200,200)),
    pygame.transform.scale(SHIP_D[1], (200,200)),
    pygame.transform.scale(SHIP_D[2], (200,200))
]

SELECTED_SHIP = 0 # default ship-a

# images for explosion animation

EXPLOSION = [
    pygame.image.load('Images/Explosions/explosions-a1.png').convert_alpha(),
    pygame.image.load('Images/Explosions/explosions-a2.png').convert_alpha(),
    pygame.image.load('Images/Explosions/explosions-a3.png').convert_alpha(),
    pygame.image.load('Images/Explosions/explosions-a4.png').convert_alpha(),
    pygame.image.load('Images/Explosions/explosions-a5.png').convert_alpha(),
    pygame.image.load('Images/Explosions/explosions-a6.png').convert_alpha()
]


# player bullet variables
BULLET_SPEED = 4
BULLET_COLOR = WHITE 
BULLET_SIZE = 5
SPECIAL_BULLET_COLOR = RED
SPECIAL_BULLET_SPEED = 4
SPAWN_DELAY_POWERUP = 30

# initialize Pygame mixer
import pygame
pygame.mixer.init()

# imports all the music and sound effects
BACKGROUND_MUSIC = pygame.mixer.Sound('Sounds/Background Music.mp3')
ASTEROID_MUSIC = pygame.mixer.Sound('Sounds/Asteroid Destroyed.mp3')
PLAYER_BULLET_MUSIC = pygame.mixer.Sound('Sounds/Player Bullet.mp3')
SHIP_MUSIC = pygame.mixer.Sound('Sounds/Ship Sounds.mp3')
PLAYER_DESTROYED_MUSIC = pygame.mixer.Sound('Sounds/Player Destroyed.mp3')
POWERUP_MUSIC = pygame.mixer.Sound('Sounds/Obtain Powerup.mp3')
BOMB_MUSIC = pygame.mixer.Sound('Sounds/Explosion.mp3')
        
# play music on separate channels
MUSIC_CHANNEL = pygame.mixer.Channel(0)
ASTEROID_CHANNEL = pygame.mixer.Channel(1)
PLAYER_CHANNEL = pygame.mixer.Channel(2)
PLAYER_DESTROYED_CHANNEL = pygame.mixer.Channel(3)
SHIP_CHANNEL = pygame.mixer.Channel(4)
POWERUP_CHANNEL = pygame.mixer.Channel(5)

# set volume, needs continuous testing
pygame.mixer.Channel(0).set_volume(2)
pygame.mixer.Channel(1).set_volume(10)
pygame.mixer.Channel(2).set_volume(3)
pygame.mixer.Channel(4).set_volume(0.5)
pygame.mixer.Channel(3).set_volume(10)

