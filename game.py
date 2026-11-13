import pygame
import os
import random

pygame.init()
pygame.mixer.init()

# set the directory for the image and music
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#MUSIC SET UP
pygame.mixer_music.load("stereo-madness.mp3")
pygame.mixer_music.play(loops=-1)
pygame.mixer_music.set_volume(10)

#SETS UP SCREEN
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
title_font = pygame.font.Font(None, 64)

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
bullet_speed_base = 8
level = 1
running = True



#MOVEMENT FUNCION
def player_movement(player_x, player_y, velocity_y, is_jumping, speed, jump_force, gravity, screen_width, player_size, floor_y,):

    keys = pygame.key.get_pressed()

    #MOVEMENT KEYS
    if keys[pygame.K_a]:
        player_x = player_x - speed
    if keys[pygame.K_d]:
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

#BACKGROUND SCROLL
def background(bg_x, scroll_speed, screen_width,):

    bg_x -= scroll_speed

    if bg_x <= -screen_width:
        bg_x = 0

    return bg_x

#RESET FUNCTION
def reset_game():
    global player_x, player_y, velocity_y, is_jumping, score, level, bullets, power_ups, scroll_speed, bullet_speed, power_active
    player_x = 100
    player_y = floor_y
    velocity_y = 0
    is_jumping = False
    score = 0
    level = 1
    bullets.clear()
    power_ups.clear()
    scroll_speed = 2
    bullet_speed = 8
    power_active = False

game_state = "MENU"

reset_game()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_state = "PLAYING"
        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                game_state = "PLAYING"

    keys = pygame.key.get_pressed()

    bg_x = background(bg_x, scroll_speed, screen_width)   # Calls the function for a scrolling background

    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + screen_width, 0))


    if game_state == "MENU":
        # Draw Menu Screen
        title_text = title_font.render("Geometry Dash Ripoff", True, WHITE)
        start_text = font.render("Press SPACE to Start", True, YELLOW)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 300))

    elif game_state == "PLAYING":
        player_x, player_y, velocity_y, is_jumping = player_movement(player_x, player_y, velocity_y, is_jumping, speed, jump_force, gravity, screen_width, player_size, floor_y)
        # Calls the movement function

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
                game_state = "GAME_OVER"
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
        pygame.draw.line(screen, BLACK, (0, floor_y + player_size), (screen_width, floor_y + player_size), 2)   # Sets up the floor

        power_up_timer += 0.2

        if score >= 1000 and level == 2:
            if power_up_timer >= random.randint(120, 240):
                pow_y = random.randint(445, 525)
                power_ups.append(pygame.Rect(screen_width, pow_y, 20, 20))  # Adds a power up to the list
                power_up_timer = 0

            for time_slow in power_ups[:]:
                time_slow.x -= 2

                pygame.draw.rect(screen, SKY_BLUE, time_slow)

                if player_rect.colliderect(time_slow):
                    bullet_speed = 5. # Slows the bullet to make it like a time slow
                    power_active = True
                    effect_end_time = pygame.time.get_ticks() + 5000. # makes the power up last only 5 seconds
                    power_ups.remove(time_slow)
                
                if power_active and pygame.time.get_ticks() >= effect_end_time: # Sets the game back to normal when the power up ends
                    bullet_speed = bullet_speed_base
                    power_active = False
                    
                elif time_slow.x < -20:   # Remove the power up if you miss it
                    power_ups.remove(time_slow)

            if power_active:
                current_time = pygame.time.get_ticks()
                time_left = max(0, (effect_end_time - current_time) / 1000.0)

                # Show countdown down to 1 decimal place
                timer_text = font.render(f"Power-up: {time_left:.1f}s", True, SKY_BLUE)
                screen.blit(timer_text, (10, 50))

        if level == 1 and score < 1000: # Sets everything back to normal when you die
            scroll_speed = 2
            bullet_speed = 8

        if score >= 1000 and level == 1:  # Increases the difficulty when you get to 1000 score
            level = 2
            scroll_speed = 4
            bullet_speed = 12
            bullet_spawn_timer += 10
            bullets.clear()    # Clears the bullets to give you a moment before the difficulty changes
            power_active = False

        if score >= 2000 and level == 2:  # Final level of difficulty at 2000 score
            level = 3
            scroll_speed = 8
            bullet_speed = 20
            bullet_spawn_timer += 30
            bullets.clear()
            power_active = False

        score_text = font.render(f"Score: {score}   |   level: {level}", True, (255, 255, 255)) #Get a message at the top for your current score and level
        screen.blit(score_text, (10, 10))
        score += 1

    elif game_state == "GAME_OVER":    # When you die This will put a game over screen
        over_text = title_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press SPACE to Play Again", True, WHITE)
        screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, 200))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 300))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
