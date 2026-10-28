import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry Dash Ripoff")

screen_width = 800
screen_height = 600

WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)

floor_y = 500

player_x = 375
player_y = 500
speed = 1.5
player_size = 50

velocity_y = 0
is_jumping = False
gravity = 0.09
jump_force =-7

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x = player_x - speed

    if keys[pygame.K_RIGHT]:
        player_x = player_x + speed

    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = jump_force
        is_jumping = True

    if is_jumping:
        velocity_y += gravity
        player_y += velocity_y

    if player_x < 0:
        player_x = 0

    if player_x > screen_width - player_size:
        player_x = screen_width - player_size

    if player_y >= floor_y:
        player_y = floor_y
        velocity_y = 0
        is_jumping = False
    
    screen.fill(SKY_BLUE)

    pygame.draw.line(screen, WHITE, (0, floor_y + player_size), (screen_width, floor_y + player_size), 2)

    player = pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))

    pygame.display.flip()

pygame.quit()