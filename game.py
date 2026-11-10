import pygame
import os
import random

pygame.init()

# set the directory for the image
os.chdir(os.path.dirname(os.path.abspath(__file__)))


clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry Dash Ripoff") #Title for the game

screen_width = 800
screen_height = 600

# IMAGE LOADING AND STATS
bg_image = pygame.image.load("images.png").convert() #load the image
bg_image = pygame.transform.scale(bg_image, (screen_width, 550)) #set the image to be the same resolution as the screen
bg_x = 0
scroll_speed = 2

score = 0
font = pygame.font.Font(None, 36)

#COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pow_x = random.randint(200, 500) 
pow_y = random.randint(450, 500)

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
jump_force =-13

#POWER UP STATS AND LIST
power_ups = []
power_up_timer = 0
power_active = True
effect_end_time = 0

#BULLET STATS AND LIST
bullets = []
bullet_speed = 8
bullet_spawn_timer = 0

level = 1
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

    keys = pygame.key.get_pressed()

    bg_x = background(bg_x, scroll_speed, screen_width)

    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + screen_width, 0))

    player_x, player_y, velocity_y, is_jumping = player_movement(player_x, player_y, velocity_y, is_jumping, speed, jump_force, gravity, screen_width, player_size, floor_y)

    # Spawn bullets
    bullet_spawn_timer += 1
    if bullet_spawn_timer > random.randint(60, 120):  
        bullet_y = random.randint(445, 520)          
        bullets.append(pygame.Rect(screen_width, bullet_y, 25, 12)) # adds bullets to a list
        bullet_spawn_timer = 0

    
    for bullet in bullets[:]:
        bullet.x -= bullet_speed  # Move bullet to the left
        
        if bullet.x < -30:
            # Remove bullet if it goes off-screen
            bullets.remove(bullet)
        elif player_rect.colliderect(bullet):
            # Reset player position on hit and remove bullet
            player_x = 100
            player_y = floor_y
            bullets.remove(bullet)
            score = 0
            level = 1
        else:
            # Only draw the bullet if it wasn't removed
            pygame.draw.rect(screen, RED, bullet)

    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    player = pygame.draw.rect(screen, GREEN, (player_x, player_y, 50, 50))

    Time_slow = pygame.Rect(pow_x, pow_y, 20, 20)
    pygame.draw.line(screen, BLACK, (0, floor_y + player_size), (screen_width, floor_y + player_size), 2)

    power_up_timer += 0.2

    if power_up_timer >= random.randint(120, 240):
        pow_y = random.randint(445, 525)
        power_ups.append(pygame.Rect(screen_width, pow_y, 20, 20))
        power_up_timer = 0

    for time_slow in power_ups[:]:
        time_slow.x -= 2

        pygame.draw.rect(screen, SKY_BLUE, time_slow)

        if player_rect.colliderect(time_slow):
            bullet_speed = 6
            power_active = True
            effect_end_time = pygame.time.get_ticks() + 5000
            power_ups.remove(time_slow)
        
        if power_active and pygame.time.get_ticks() >= effect_end_time:
            bullet_speed = 15
            power_active = False
             
        elif time_slow.x < -20:
            power_ups.remove(time_slow)

    if level == 1 and score < 1000:
        scroll_speed = 2
        bullet_speed = 8

    if score >= 1000 and level == 1:
        level = 2
        scroll_speed = 4
        bullet_speed = 12
        bullet_spawn_timer += 10
        bullets.clear()
        power_active = False

    if score >= 2000 and level == 2:
        level = 3
        scroll_speed = 8
        bullet_speed = 20
        bullet_spawn_timer += 30
        bullets.clear()
        power_active = False

    score_text = font.render(f"Score: {score}   |   level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    score += 1

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
