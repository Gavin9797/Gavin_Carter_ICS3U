import pygame
import os

pygame.init()

# set the directory for the image
os.chdir(os.path.dirname(os.path.abspath(__file__)))

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry Dash Ripoff")

screen_width = 800
screen_height = 600

bg_image = pygame.image.load("images.png").convert() #load the image
bg_image = pygame.transform.scale(bg_image, (screen_width, 550)) #set the image to be the same resolution as the screen

bg_x = 0
scroll_speed = 2

#COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)

rect_x = 400
rect_y = 500

#PLAYER STATS AND FLOOR POSITION
floor_y = 500
player_x = 100
player_y = 500
speed = 5
player_size = 50

#JUMP PHYSICS STATS
velocity_y = 0
is_jumping = False
gravity = 0.8
jump_force =-16

running = True

#MOVEMENT FUNCION
def player_movement(player_x, player_y, velocity_y, is_jumping, speed, jump_force, gravity, screen_width, player_size, floor_y,):

    keys = pygame.key.get_pressed()

    #MOVEMENT KEYS
    if keys[pygame.K_LEFT]:
        player_x = player_x - speed
    if keys[pygame.K_RIGHT]:
        player_x = player_x + speed
    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = jump_force
        is_jumping = True

    #JUMP PHYSICS
    if is_jumping:
        velocity_y += gravity
        player_y += velocity_y

    #SCREEN
    if player_x < 0:
        player_x = 0
    if player_x > screen_width - player_size:
        player_x = screen_width - player_size

    #FLOOR COLLISION
    if player_y >= floor_y:
        player_y = floor_y
        velocity_y = 0
        is_jumping = False

    return player_x, player_y, velocity_y, is_jumping

def background(bg_x, scroll_speed, screen_width,):

    bg_x -= scroll_speed

    if bg_x <= -screen_width:
        bg_x = 0

    return bg_x


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bg_x = background(bg_x, scroll_speed, screen_width)

    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + screen_width, 0))

    player_x, player_y, velocity_y, is_jumping = player_movement(player_x, player_y, velocity_y, is_jumping, speed, jump_force, gravity, screen_width, player_size, floor_y)

    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    enemy_rect = pygame.Rect(rect_x, rect_y, 10, 50)

    if player_rect.colliderect(enemy_rect):
        running = False
    
    pygame.draw.line(screen, BLACK, (0, floor_y + player_size), (screen_width, floor_y + player_size), 2)
    pygame.draw.rect(screen, RED, (rect_x, rect_y, 10, 50))

    player = pygame.draw.rect(screen, GREEN, (player_x, player_y, 50, 50))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
