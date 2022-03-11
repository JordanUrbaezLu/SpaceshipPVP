import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE BATTLE 1v1!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

MENU_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
FIREBALL_HIT_SOUND = pygame.mixer.Sound('Assets/ExplosionHit.mp3')
FIREBALL_SHOT_SOUND = pygame.mixer.Sound('Assets/FireShot.mp3')
HEALTH_GRAB_SOUND = pygame.mixer.Sound('Assets/Health.wav')
GAME_MUSIC = pygame.mixer.Sound('Assets/GameMusic.mp3')
LASER_SOUND = pygame.mixer.Sound('Assets/Laser.mp3')
BEAM_HIT_SOUND = pygame.mixer.Sound('Assets/BEAM_HIT.mp3')
MENU_SOUND = pygame.mixer.Sound('Assets/MenuSound.mp3')
START_SOUND = pygame.mixer.Sound('Assets/Start.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 16
MAX_BULLETS = 2
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_FIRE_HIT = pygame.USEREVENT + 3
RED_FIRE_HIT = pygame.USEREVENT + 4
YELLOW_HEALTH_GRABBED = pygame.USEREVENT + 5
RED_HEALTH_GRABBED = pygame.USEREVENT + 6
YELLOW_FLAME_GRABBED = pygame.USEREVENT + 7
RED_FLAME_GRABBED = pygame.USEREVENT + 8
LASER_HIT_YELLOW = pygame.USEREVENT + 9
LASER_HIT_RED = pygame.USEREVENT + 10
YELLOW_ICE_GRAB = pygame.USEREVENT + 11
RED_ICE_GRAB = pygame.USEREVENT + 12

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

EXTRA_HEALTH_IMAGE = pygame.image.load(os.path.join('Assets', 'Health.png'))
EXTRA_HEALTH = pygame.transform.scale(EXTRA_HEALTH_IMAGE, (40, SPACESHIP_HEIGHT))

FLAME_BEAM_IMAGE = pygame.image.load(os.path.join('Assets', 'FlameBeam.png'))
FLAME_BEAM = pygame.transform.scale(FLAME_BEAM_IMAGE, (150, 150))

ICE_CUBE_IMAGE = pygame.image.load(os.path.join('Assets', 'IceCube.png'))
ICE_CUBE = pygame.transform.scale(ICE_CUBE_IMAGE, (150, 150))

FROZEN_IMAGE = pygame.image.load(os.path.join('Assets', 'Frozen.png'))
FROZEN = pygame.transform.scale(FROZEN_IMAGE, (150, 150))

LASER_BEAM_IMAGE = pygame.image.load(os.path.join('Assets', 'LaserBeam.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

FIREBALL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'FireBall.png'))
FIREBALL = pygame.transform.scale(
    FIREBALL_IMAGE, (SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'BlackHole.jpg')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_fire_bullet, yellow_fire_bullet, red_health,
                yellow_health, health, health_spawn, flame, flame_spawn, laser_shooter, ice, ice_spawn):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    if ice_spawn:
        WIN.blit(ICE_CUBE, (ice.x, ice.y))
        ice_collision(ice, red, yellow)

    if health_spawn:
        WIN.blit(EXTRA_HEALTH, (health.x, health.y))
        health_collision(health, red, yellow)

    if flame_spawn:
        WIN.blit(FLAME_BEAM, (375, 175))
        flame_collision(flame, red, yellow)

    if laser_shooter[0] == "R":
        laser_beam = pygame.transform.rotate(pygame.transform.scale(LASER_BEAM_IMAGE, (1000, 80)), 180)
        WIN.blit(laser_beam, (- 1000 + red.x, red.y - 20))

    if laser_shooter[0] == "Y":
        laser_beam = pygame.transform.scale(LASER_BEAM_IMAGE, (1000, 80))
        WIN.blit(laser_beam, (yellow.x + 50, yellow.y - 20))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Yellow Health Bar
    pygame.draw.rect(WIN, GREEN, [10, 10, yellow_health, 20])
    pygame.draw.rect(WIN, RED, [yellow_health + 10, 10, 420 - yellow_health, 20])

    # Red Health Bar
    pygame.draw.rect(WIN, GREEN, [WIDTH - red_health - 10, 10, red_health, 20])
    pygame.draw.rect(WIN, RED, [WIDTH - 430, 10, 420 - red_health, 20])

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_fire_bullet:
        WIN.blit(FIREBALL, (bullet.x - 120, bullet.y - 10))

    for bullet in yellow_fire_bullet:
        WIN.blit(FIREBALL, (bullet.x, bullet.y - 10))

    pygame.display.update()


def redraw_window(red, yellow, red_bullets, yellow_bullets, red_fire_bullet,
                  yellow_fire_bullet, red_health, yellow_health, health,
                  health_spawn, flame, flame_spawn, laser_shooter, ice, ice_spawn):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    if health_spawn:
        WIN.blit(EXTRA_HEALTH, (health.x, health.y))
        health_collision(health, red, yellow)

    if flame_spawn:
        WIN.blit(FLAME_BEAM, (375, 175))
        flame_collision(flame, red, yellow)

    if laser_shooter[0] == "R":
        laser_beam = pygame.transform.rotate(pygame.transform.scale(LASER_BEAM_IMAGE, (1000, 80)), 180)
        WIN.blit(laser_beam, (- 1000 + red.x, red.y - 20))

    if laser_shooter[0] == "Y":
        laser_beam = pygame.transform.scale(LASER_BEAM_IMAGE, (1000, 80))
        WIN.blit(laser_beam, (yellow.x + 50, yellow.y - 20))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Yellow Health Bar
    pygame.draw.rect(WIN, GREEN, [10, 10, yellow_health, 20])
    pygame.draw.rect(WIN, RED, [yellow_health + 10, 10, 420 - yellow_health, 20])

    # Red Health Bar
    pygame.draw.rect(WIN, GREEN, [WIDTH - red_health - 10, 10, red_health, 20])
    pygame.draw.rect(WIN, RED, [WIDTH - 430, 10, 420 - red_health, 20])

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_fire_bullet:
        WIN.blit(FIREBALL, (bullet.x - 120, bullet.y - 10))

    for bullet in yellow_fire_bullet:
        WIN.blit(FIREBALL, (bullet.x, bullet.y - 10))


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_fire_bullet, red_fire_bullet, yellow_bullets, red_bullets, yellow, red, laser_shooter):
    if laser_shooter[0] == "Y":
        if red.colliderect(pygame.Rect(yellow.x, yellow.y + 6, 1000, SPACESHIP_HEIGHT / 3)):
            pygame.event.post(pygame.event.Event(LASER_HIT_RED))

    if laser_shooter[0] == "R":
        if yellow.colliderect(pygame.Rect(-1000, red.y + 6, 2000, SPACESHIP_HEIGHT / 3)):
            pygame.event.post(pygame.event.Event(LASER_HIT_YELLOW))

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in yellow_fire_bullet:
        bullet.x += BULLET_VEL / 2
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_FIRE_HIT))
            yellow_fire_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_fire_bullet.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    for bullet in red_fire_bullet:
        bullet.x -= BULLET_VEL / 2
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_FIRE_HIT))
            red_fire_bullet.remove(bullet)
        elif bullet.x < 0:
            red_fire_bullet.remove(bullet)


def draw_winner(text, red, yellow):
    if text[0] == "R":
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
        # draw_text = WINNER_FONT.render(text, True, RED)
        # WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
        # 2, HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    if text[0] == "Y":
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        # draw_text = WINNER_FONT.render(text, True, YELLOW)
        # WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
        # 2, HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)


def health_collision(health, red, yellow):
    if yellow.colliderect(health):
        pygame.event.post(pygame.event.Event(YELLOW_HEALTH_GRABBED))

    if red.colliderect(health):
        pygame.event.post(pygame.event.Event(RED_HEALTH_GRABBED))


def flame_collision(flame, red, yellow):
    if yellow.colliderect(flame):
        pygame.event.post(pygame.event.Event(YELLOW_FLAME_GRABBED))

    if red.colliderect(flame):
        pygame.event.post(pygame.event.Event(RED_FLAME_GRABBED))


def ice_collision(ice, red, yellow):
    if yellow.colliderect(ice):
        pygame.event.post(pygame.event.Event(YELLOW_ICE_GRAB))

    if red.colliderect(ice):
        pygame.event.post(pygame.event.Event(RED_ICE_GRAB))


def fade(width, height, red, yellow, red_bullets, yellow_bullets, red_fire_bullet,
         yellow_fire_bullet, red_health, yellow_health, health, health_spawn,
         flame, flame_spawn, laser_shooter, ice, ice_spawn):
    fader = pygame.Surface((width, height))
    fader.fill((0, 0, 0))
    for alpha in range(0, 300):
        fader.set_alpha(alpha)
        redraw_window(red, yellow, red_bullets, yellow_bullets, red_fire_bullet,
                      yellow_fire_bullet, red_health, yellow_health, health,
                      health_spawn, flame, flame_spawn, laser_shooter, ice, ice_spawn)
        WIN.blit(fader, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def game_loop():
    red = pygame.Rect(800, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    health = pygame.Rect(1, 1, 1, 1)
    flame = pygame.Rect(1, 1, 1, 1)
    ice = pygame.Rect(1, 1, 1, 1)

    red_bullets = []
    yellow_bullets = []
    red_fire_bullet = []
    yellow_fire_bullet = []
    i = 0
    x = 0
    y = 0
    z = 0
    health_spawn = False
    flame_spawn = False
    ice_spawn = False
    red_health = 420
    yellow_health = 420
    laser_shooter = "N"

    clock = pygame.time.Clock()
    random_tick = 0
    flame_tick = 0
    ice_tick = 0
    run = True
    while run:
        clock.tick(FPS)

        if laser_shooter[0] != "N":
            z += 1
            if z == 318:
                laser_shooter = "N"
                z = 0

        if i == 0:
            ice_tick = random.randint(300, 600)
        i += 1
        if i == ice_tick:
            ice = pygame.Rect(random.randint(50, 800), random.randint(50, 451), 100, 100)
            WIN.blit(ICE_CUBE, (ice.x, ice.y))
            ice_spawn = True

        if x == 0:
            random_tick = random.randint(200, 400)
        x += 1
        if x == random_tick:
            health = pygame.Rect(random.randint(50, 800), random.randint(50, 451), 40, 40)
            WIN.blit(EXTRA_HEALTH, (health.x, health.y))
            health_spawn = True

        if y == 0:
            flame_tick = random.randint(500, 1000)
        y += 1
        if y == flame_tick:
            flame = pygame.Rect(430, 200, 60, 90)
            WIN.blit(FLAME_BEAM, (375, 175))
            flame_spawn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_fire_bullet) < 1:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 40, 80, 80)
                    red_fire_bullet.append(bullet)
                    FIREBALL_SHOT_SOUND.play()

                if event.key == pygame.K_1 and len(yellow_fire_bullet) < 1:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height // 2 - 40, 80, 80)
                    yellow_fire_bullet.append(bullet)
                    FIREBALL_SHOT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 10
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 10
                BULLET_HIT_SOUND.play()

            if event.type == RED_FIRE_HIT:
                red_health -= 50
                FIREBALL_HIT_SOUND.play()

            if event.type == YELLOW_FIRE_HIT:
                yellow_health -= 50
                FIREBALL_HIT_SOUND.play()

            if event.type == YELLOW_HEALTH_GRABBED:
                if yellow_health >= 345:
                    yellow_health = 420
                else:
                    yellow_health += 75
                health_spawn = False
                x = 0
                HEALTH_GRAB_SOUND.play()

            if event.type == RED_HEALTH_GRABBED:
                if red_health >= 345:
                    red_health = 420
                else:
                    red_health += 75
                health_spawn = False
                x = 0
                HEALTH_GRAB_SOUND.play()

            if event.type == YELLOW_FLAME_GRABBED:
                laser_shooter = "Y"
                flame_spawn = False
                y = 0
                LASER_SOUND.play()

            if event.type == RED_FLAME_GRABBED:
                laser_shooter = "R"
                flame_spawn = False
                y = 0
                LASER_SOUND.play()

            if event.type == LASER_HIT_YELLOW:
                yellow_health -= 5
                yellow_health -= 5
                BEAM_HIT_SOUND.play()

            if event.type == LASER_HIT_RED:
                red_health -= 5
                BEAM_HIT_SOUND.play()

            if event.type == YELLOW_ICE_GRAB:
                i = 0
                ice_spawn = False
            if event.type == RED_ICE_GRAB:
                i = 0
                ice_spawn = False

        winner_text = ""
        if red_health <= 0:
            fade(900, 500, red, yellow, red_bullets, yellow_bullets, red_fire_bullet,
                 yellow_fire_bullet, red_health, yellow_health, health, health_spawn,
                 flame, flame_spawn, laser_shooter, ice, ice_spawn)
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            fade(900, 500, red, yellow, red_bullets, yellow_bullets, red_fire_bullet,
                 yellow_fire_bullet, red_health, yellow_health, health, health_spawn,
                 flame, flame_spawn, laser_shooter, ice, ice_spawn)
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text, red, yellow)
            break

        draw_window(red, yellow, red_bullets, yellow_bullets, red_fire_bullet, yellow_fire_bullet,
                    red_health, yellow_health, health, health_spawn, flame, flame_spawn, laser_shooter, ice, ice_spawn)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_fire_bullet, red_fire_bullet, yellow_bullets, red_bullets, yellow, red, laser_shooter)

    game_loop()


def main_menu():
    menu, start = True, True
    if GAME_MUSIC.get_volume() == 1.0:
        GAME_MUSIC.set_volume(0.4)
        GAME_MUSIC.play(-1)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not start:
                    start = True
                    MENU_SOUND.play()
                if event.key == pygame.K_DOWN and start:
                    start = False
                    MENU_SOUND.play()
                if event.key == pygame.K_RETURN and not start:
                    pygame.quit()
                if event.key == pygame.K_RETURN and start:
                    START_SOUND.play()
                    return
        if start:
            start_text = MENU_FONT.render(
                "START", True, WHITE)
            exit_text = MENU_FONT.render(
                "EXIT", True, BLACK)
            WIN.blit(SPACE, (0, 0))
            WIN.blit(start_text, (340, 60))
            WIN.blit(exit_text, (365, 375))
            temp_yellow = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (
                SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 90)
            temp_red = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (
                SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 270)
            WIN.blit(temp_yellow, (100, 10))
            WIN.blit(temp_red, (700, 10))
            pygame.display.update()

        if not start:
            start_text = MENU_FONT.render(
                "START", True, BLACK)
            exit_text = MENU_FONT.render(
                "EXIT", True, WHITE)
            WIN.blit(SPACE, (0, 0))
            WIN.blit(start_text, (340, 60))
            WIN.blit(exit_text, (365, 375))
            temp_yellow = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (
                SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 90)
            temp_red = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (
                SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 270)
            WIN.blit(temp_yellow, (100, 325))
            WIN.blit(temp_red, (700, 325))
            pygame.display.update()


def main():
    main_menu()
    game_loop()


if __name__ == "__main__":
    main()
