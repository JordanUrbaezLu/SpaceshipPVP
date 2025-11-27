import pygame
import os
import random
import math

pygame.init()
pygame.font.init()
pygame.mixer.init()

KEY_BACKTICK = pygame.key.key_code('`')
KEY_QUOTE = pygame.key.key_code("'")

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE BATTLE 1v1!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_GREY = (50, 50, 50)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

MENU_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
FIREBALL_HIT_SOUND = pygame.mixer.Sound('Assets/ExplosionHit.mp3')
FIREBALL_SHOT_SOUND = pygame.mixer.Sound('Assets/FireShot.mp3')
HEALTH_GRAB_SOUND = pygame.mixer.Sound('Assets/Health.wav')


def load_game_music_tracks():
    tracks = []
    for name in os.listdir('Assets'):
        lower = name.lower()
        if lower.startswith('gamemusic') and lower.endswith('.mp3'):
            tracks.append(pygame.mixer.Sound(os.path.join('Assets', name)))
    if not tracks:
        tracks.append(pygame.mixer.Sound('Assets/GameMusic.mp3'))
    return tracks


GAME_MUSIC_TRACKS = load_game_music_tracks()
LASER_SOUND = pygame.mixer.Sound('Assets/Laser.mp3')
BEAM_HIT_SOUND = pygame.mixer.Sound('Assets/BEAM_HIT.mp3')
MENU_SOUND = pygame.mixer.Sound('Assets/MenuSound.mp3')
START_SOUND = pygame.mixer.Sound('Assets/Start.mp3')
FREEZE_SOUND = pygame.mixer.Sound('Assets/Freeze.mp3')
LIGHTNING_SOUND = pygame.mixer.Sound('Assets/Lightning.mp3')
SHIELD_HIT_SOUND = pygame.mixer.Sound('Assets/Shield.mp3')
FREEZE_SOUND_HALF_MS = max(1, int(FREEZE_SOUND.get_length() * 500))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BASE_BULLET_VEL = 16
BULLET_SPEED_MULTIPLIER = 1.2
BULLET_VEL = int(BASE_BULLET_VEL * BULLET_SPEED_MULTIPLIER)
MAX_BULLETS = 2
BULLET_DAMAGE = 15
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # legacy defaults
SHIP_RENDER_W, SHIP_RENDER_H = 55, 40
SHIP_COLLISION_W, SHIP_COLLISION_H = 55, 50
BULLET_W, BULLET_H = 10, 5
FIREBALL_RENDER_W, FIREBALL_RENDER_H = 100, 80
FIREBALL_HIT_W, FIREBALL_HIT_H = 80, 80
ICE_RENDER_W, ICE_RENDER_H = 100, 100
ICE_HIT_W, ICE_HIT_H = 100, 100
ICE_FREEZE_MS = 900
LIGHTNING_RENDER_W, LIGHTNING_RENDER_H = 100, 100
LIGHTNING_HIT_W, LIGHTNING_HIT_H = 100, 100
HEALTH_RENDER_W, HEALTH_RENDER_H = 40, 40
HEALTH_HIT_W, HEALTH_HIT_H = 40, 40
FLAME_RENDER_W, FLAME_RENDER_H = 180, 180
FLAME_HIT_W, FLAME_HIT_H = 130, 130
SHIELD_RENDER_W, SHIELD_RENDER_H = 90, 90
SHIELD_HIT_W, SHIELD_HIT_H = 90, 90
SHIELD_OVERLAY_W, SHIELD_OVERLAY_H = 80, 80
LASER_RENDER_W, LASER_RENDER_H = 1200, 120
LASER_HIT_W, LASER_HIT_H = 1000, 60
BLACKHOLE_ENABLED = False
BLACKHOLE_RENDER_W, BLACKHOLE_RENDER_H = 140, 140
BLACKHOLE_HIT_W, BLACKHOLE_HIT_H = 100, 100
BLACKHOLE_PULL_BASE = 0.4
BLACKHOLE_PULL_RADIUS = 350
BLACKHOLE_LOCK_RADIUS = 80
BLACKHOLE_LOCK_FORCE = 6
BLACKHOLE_DURATION_TICKS = 200
BLACKHOLE_INTERVAL_MIN = 500
BLACKHOLE_INTERVAL_MAX = 900
SPAWN_RATE_MULTIPLIER = 0.5
LIGHTNING_MULTIPLIER = 1.6
GAME_MUSIC_VOLUME = 0.4
MAX_HEALTH = 500
LASER_DAMAGE = 2
PLAYFIELD_MARGIN = 50
SHOW_HITBOXES = False
HITBOX_COLOR = (255, 0, 255)

PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_FIRE_HIT = pygame.USEREVENT + 2
PLAYER_HEALTH_GRAB = pygame.USEREVENT + 3
PLAYER_FLAME_GRAB = pygame.USEREVENT + 4
LASER_HIT = pygame.USEREVENT + 5
PLAYER_ICE_GRAB = pygame.USEREVENT + 6
PLAYER_LIGHTNING_GRAB = pygame.USEREVENT + 7
PLAYER_SHIELD_GRAB = pygame.USEREVENT + 8

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SHIP_RENDER_W, SHIP_RENDER_H)), 90)

EXTRA_HEALTH_IMAGE = pygame.image.load(os.path.join('Assets', 'Health.png'))
EXTRA_HEALTH = pygame.transform.scale(EXTRA_HEALTH_IMAGE, (HEALTH_RENDER_W, HEALTH_RENDER_H))

FLAME_BEAM_IMAGE = pygame.image.load(os.path.join('Assets', 'FlameBeam.png'))
FLAME_BEAM = pygame.transform.scale(FLAME_BEAM_IMAGE, (FLAME_RENDER_W, FLAME_RENDER_H))
FLAME_BEAM_WIDTH = FLAME_BEAM.get_width()
FLAME_BEAM_HEIGHT = FLAME_BEAM.get_height()

ICE_CUBE_IMAGE = pygame.image.load(os.path.join('Assets', 'IceCube.png'))
ICE_CUBE = pygame.transform.scale(ICE_CUBE_IMAGE, (ICE_RENDER_W, ICE_RENDER_H))

FROZEN_IMAGE = pygame.image.load(os.path.join('Assets', 'Frozen.png'))
FROZEN = pygame.transform.scale(FROZEN_IMAGE, (150, 150))

LASER_BEAM_IMAGE = pygame.image.load(os.path.join('Assets', 'LaserBeam.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SHIP_RENDER_W, SHIP_RENDER_H)), 270)

FIREBALL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'FireBall.png'))
FIREBALL = pygame.transform.scale(
    FIREBALL_IMAGE, (FIREBALL_RENDER_W, FIREBALL_RENDER_H))

LIGHTNING_IMAGE = pygame.image.load(os.path.join('Assets', 'Lightning.png'))
LIGHTNING = pygame.transform.scale(LIGHTNING_IMAGE, (LIGHTNING_RENDER_W, LIGHTNING_RENDER_H))

SHIELD_IMAGE = pygame.image.load(os.path.join('Assets', 'Shield.png'))
SHIELD = pygame.transform.scale(SHIELD_IMAGE, (SHIELD_RENDER_W, SHIELD_RENDER_H))
SHIELD_OVERLAY = pygame.transform.scale(SHIELD_IMAGE, (SHIELD_OVERLAY_W, SHIELD_OVERLAY_H))

if os.path.exists(os.path.join('Assets', 'BlackHole.jpeg')):
    BLACKHOLE_IMAGE = pygame.image.load(os.path.join('Assets', 'BlackHole.jpeg'))
else:
    BLACKHOLE_IMAGE = pygame.image.load(os.path.join('Assets', 'BlackHole.jpg'))
BLACKHOLE_SPRITE = pygame.transform.scale(BLACKHOLE_IMAGE, (BLACKHOLE_RENDER_W, BLACKHOLE_RENDER_H))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'BlackHole.jpg')), (WIDTH, HEIGHT))

PLAYER_CONFIGS = [
    {
        "id": "P1",
        "name": "Player 1",
        "color": YELLOW,
        "image": YELLOW_SPACESHIP,
        "start_pos": (120, HEIGHT // 3 - 60),
        "direction": "right",
        "team": "A",
        "keys": {
            "up": pygame.K_2,
            "left": pygame.K_q,
            "down": pygame.K_w,
            "right": pygame.K_e,
            "shoot": pygame.K_1,
            "fireball": KEY_BACKTICK
        }
    },
    {
        "id": "P2",
        "name": "Player 2",
        "color": RED,
        "image": RED_SPACESHIP,
        "start_pos": (WIDTH - 180, HEIGHT // 3 - 60),
        "direction": "left",
        "team": "B",
        "keys": {
            "up": pygame.K_0,
            "left": pygame.K_i,
            "down": pygame.K_o,
            "right": pygame.K_p,
            "shoot": pygame.K_MINUS,
            "fireball": pygame.K_EQUALS
        }
    },
    {
        "id": "P3",
        "name": "Player 3",
        "color": RED,
        "image": RED_SPACESHIP,
        "start_pos": (120, 2 * HEIGHT // 3 - 60),
        "direction": "right",
        "team": "A",
        "keys": {
            "up": pygame.K_d,
            "left": pygame.K_z,
            "down": pygame.K_x,
            "right": pygame.K_c,
            "shoot": pygame.K_s,
            "fireball": pygame.K_a
        }
    },
    {
        "id": "P4",
        "name": "Player 4",
        "color": RED,
        "image": RED_SPACESHIP,
        "start_pos": (WIDTH - 180, 2 * HEIGHT // 3 - 60),
        "direction": "left",
        "team": "B",
        "keys": {
            "up": pygame.K_l,
            "left": pygame.K_COMMA,
            "down": pygame.K_PERIOD,
            "right": pygame.K_SLASH,
            "shoot": pygame.K_SEMICOLON,
            "fireball": KEY_QUOTE
        }
    }
]

current_game_music = None


def scaled_spawn(min_val, max_val, multiplier=None):
    """Scale spawn intervals by the global multiplier (lower multiplier = slower spawns)."""
    mult = SPAWN_RATE_MULTIPLIER if multiplier is None else multiplier
    low = max(1, int(min_val / mult))
    high = max(1, int(max_val / mult))
    return random.randint(low, high)


def start_game_music(force_new=False):
    """Pick a random background track and start looping it."""
    global current_game_music
    if force_new and current_game_music is not None:
        current_game_music.stop()
        current_game_music = None
    if current_game_music is not None:
        return
    current_game_music = random.choice(GAME_MUSIC_TRACKS)
    current_game_music.set_volume(GAME_MUSIC_VOLUME)
    current_game_music.play(-1)


def create_players(mode):
    if mode == "1v1":
        selected_configs = [cfg.copy() for cfg in PLAYER_CONFIGS if cfg["id"] in ("P1", "P2")]
        # Override controls for 1v1: P1 uses WASD + 1/2, P2 uses arrows + -/=
        for cfg in selected_configs:
            if cfg["id"] == "P1":
                cfg["keys"] = {
                    "up": pygame.K_w,
                    "left": pygame.K_a,
                    "down": pygame.K_s,
                    "right": pygame.K_d,
                    "shoot": pygame.K_1,
                    "fireball": pygame.K_2
                }
            if cfg["id"] == "P2":
                cfg["keys"] = {
                    "up": pygame.K_UP,
                    "left": pygame.K_LEFT,
                    "down": pygame.K_DOWN,
                    "right": pygame.K_RIGHT,
                    "shoot": pygame.K_MINUS,
                    "fireball": pygame.K_EQUALS
                }
    else:
        selected_configs = PLAYER_CONFIGS
    players = []
    for cfg in selected_configs:
        rect = pygame.Rect(cfg["start_pos"][0], cfg["start_pos"][1], SHIP_COLLISION_W, SHIP_COLLISION_H)
        players.append({
            "id": cfg["id"],
            "name": cfg["name"],
            "color": cfg["color"],
            "image": cfg["image"],
            "rect": rect,
            "direction": cfg["direction"],
            "team": cfg["team"],
            "keys": cfg["keys"],
            "health": MAX_HEALTH,
            "bullets": [],
            "fireballs": [],
            "freeze_until": 0,
            "vel": VEL,
            "dead": False,
            "shield_hp": 0
        })
    return players


def draw_health_bars(players):
    bar_width = 240
    bar_height = 15
    spacing = 8
    positions = [
        (10, 10),
        (WIDTH - bar_width - 10, 10),
        (10, 10 + bar_height + spacing),
        (WIDTH - bar_width - 10, 10 + bar_height + spacing)
    ]
    for idx, player in enumerate(players):
        if player["health"] <= 0:
            continue
        x, y = positions[idx % len(positions)]
        current = max(0, player["health"])
        pygame.draw.rect(WIN, DARK_GREY, (x, y, bar_width, bar_height))
        fill_width = int(bar_width * (current / MAX_HEALTH))
        pygame.draw.rect(WIN, GREEN, (x, y, fill_width, bar_height))


def draw_window(players, health, health_spawn, flame, flame_spawn, laser_info, ice, ice_spawn,
                lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map):
    WIN.blit(SPACE, (0, 0))

    if ice_spawn:
        ice_offset_x = (ice.width - ICE_RENDER_W) // 2
        ice_offset_y = (ice.height - ICE_RENDER_H) // 2
        WIN.blit(ICE_CUBE, (ice.x + ice_offset_x, ice.y + ice_offset_y))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, ice, 2)

    if lightning_spawn:
        lightning_offset_x = (lightning.width - LIGHTNING_RENDER_W) // 2
        lightning_offset_y = (lightning.height - LIGHTNING_RENDER_H) // 2
        WIN.blit(LIGHTNING, (lightning.x + lightning_offset_x, lightning.y + lightning_offset_y))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, lightning, 2)

    if health_spawn:
        health_offset_x = (health.width - HEALTH_RENDER_W) // 2
        health_offset_y = (health.height - HEALTH_RENDER_H) // 2
        WIN.blit(EXTRA_HEALTH, (health.x + health_offset_x, health.y + health_offset_y))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, health, 2)

    if flame_spawn:
        flame_offset_x = (flame.width - FLAME_RENDER_W) // 2
        flame_offset_y = (flame.height - FLAME_RENDER_H) // 2
        WIN.blit(FLAME_BEAM, (flame.x + flame_offset_x, flame.y + flame_offset_y))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, flame, 2)

    if shield_spawn:
        shield_offset_x = (shield.width - SHIELD_RENDER_W) // 2
        shield_offset_y = (shield.height - SHIELD_RENDER_H) // 2
        WIN.blit(SHIELD, (shield.x + shield_offset_x, shield.y + shield_offset_y))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, shield, 2)

    if blackhole_spawn and SHOW_HITBOXES:
        pygame.draw.rect(WIN, HITBOX_COLOR, blackhole, 2)

    beam_rect = None
    if laser_info["player_id"] is not None:
        shooter = next((p for p in players if p["id"] == laser_info["player_id"] and p["health"] > 0), None)
        if shooter:
            beam_y = shooter["rect"].y + shooter["rect"].height // 2 - LASER_RENDER_H // 2
            if shooter["direction"] == "right":
                laser_beam = pygame.transform.scale(LASER_BEAM_IMAGE, (LASER_RENDER_W, LASER_RENDER_H))
                WIN.blit(laser_beam, (shooter["rect"].x + 50, beam_y))
            else:
                laser_beam = pygame.transform.rotate(
                    pygame.transform.scale(LASER_BEAM_IMAGE, (LASER_RENDER_W, LASER_RENDER_H)), 180)
                WIN.blit(laser_beam, (shooter["rect"].x - LASER_RENDER_W, beam_y))
            beam_y_hit = shooter["rect"].y + shooter["rect"].height // 2 - LASER_HIT_H // 2
            beam_rect = pygame.Rect(
                shooter["rect"].x if shooter["direction"] == "right" else shooter["rect"].x - LASER_HIT_W,
                beam_y_hit,
                LASER_HIT_W,
                LASER_HIT_H
            )

    for player in players:
        if player["health"] <= 0 or player.get("dead"):
            continue
        WIN.blit(player["image"], (player["rect"].x, player["rect"].y))
        if player.get("shield_hp", 0) > 0:
            overlay_x = player["rect"].x + player["rect"].width // 2 - SHIELD_OVERLAY_W // 2
            overlay_y = player["rect"].y + player["rect"].height // 2 - SHIELD_OVERLAY_H // 2
            WIN.blit(SHIELD_OVERLAY, (overlay_x, overlay_y))
        if frozen_map.get(player["id"], False):
            WIN.blit(FROZEN, (player["rect"].x - 50, player["rect"].y - 55))
        if SHOW_HITBOXES:
            pygame.draw.rect(WIN, HITBOX_COLOR, player["rect"], 2)

    for player in players:
        if player["health"] <= 0 or player.get("dead"):
            continue
        for bullet in player["bullets"]:
            pygame.draw.rect(WIN, player["color"], bullet)
            if SHOW_HITBOXES:
                pygame.draw.rect(WIN, HITBOX_COLOR, bullet, 1)
        for bullet in player["fireballs"]:
            offset_x = (bullet.width - FIREBALL_RENDER_W) // 2
            offset_y = (bullet.height - FIREBALL_RENDER_H) // 2
            WIN.blit(FIREBALL, (bullet.x + offset_x, bullet.y + offset_y))
            if SHOW_HITBOXES:
                pygame.draw.rect(WIN, HITBOX_COLOR, bullet, 2)

    if SHOW_HITBOXES and beam_rect:
        pygame.draw.rect(WIN, HITBOX_COLOR, beam_rect, 2)

    draw_health_bars(players)
    pygame.display.update()


def redraw_window(players, health, health_spawn, flame, flame_spawn, laser_info, ice, ice_spawn,
                  lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map):
    draw_window(players, health, health_spawn, flame, flame_spawn, laser_info, ice, ice_spawn,
                lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)


def handle_player_movement(keys_pressed, player, vel):
    rect = player["rect"]
    keys = player["keys"]
    if keys_pressed[keys["left"]] and rect.x - vel > 0:
        rect.x -= vel
    if keys_pressed[keys["right"]] and rect.x + vel + rect.width < WIDTH:
        rect.x += vel
    if keys_pressed[keys["up"]] and rect.y - vel > 0:
        rect.y -= vel
    if keys_pressed[keys["down"]] and rect.y + vel + rect.height < HEIGHT:
        rect.y += vel


def handle_projectiles(players, laser_info):
    half_bullet_speed = max(1, int(BULLET_VEL / 2))

    def is_enemy(a, b):
        return a.get("team") != b.get("team")

    def mark_dead(p):
        p["health"] = 0
        p["dead"] = True
        p["bullets"].clear()
        p["fireballs"].clear()
        p["freeze_until"] = 0
        p["shield_hp"] = 0

    def apply_damage(target, amount):
        shield_before = target.get("shield_hp", 0)
        if target["shield_hp"] > 0:
            absorbed = min(target["shield_hp"], amount)
            target["shield_hp"] -= absorbed
            amount -= absorbed
            if absorbed > 0:
                SHIELD_HIT_SOUND.play()
        if amount > 0:
            target["health"] = max(0, target["health"] - amount)
            if target["health"] <= 0 and not target.get("dead"):
                mark_dead(target)

    # Bullets and fireballs
    for shooter in players:
        if shooter["health"] <= 0:
            shooter["bullets"].clear()
            shooter["fireballs"].clear()
            continue
        direction = shooter["direction"]
        bullet_delta = BULLET_VEL if direction == "right" else -BULLET_VEL
        fire_delta = half_bullet_speed if direction == "right" else -half_bullet_speed

        for bullet in shooter["bullets"][:]:
            bullet.x += bullet_delta
            if bullet.x < -20 or bullet.x > WIDTH + 20:
                shooter["bullets"].remove(bullet)
                continue
            hit = False
            for target in players:
                if target is shooter or target["health"] <= 0 or not is_enemy(shooter, target):
                    continue
                if target["rect"].colliderect(bullet):
                    apply_damage(target, BULLET_DAMAGE)
                    BULLET_HIT_SOUND.play()
                    hit = True
                    break
            if hit:
                shooter["bullets"].remove(bullet)

        for bullet in shooter["fireballs"][:]:
            bullet.x += fire_delta
            if bullet.x < -100 or bullet.x > WIDTH + 100:
                shooter["fireballs"].remove(bullet)
                continue
            hit = False
            for target in players:
                if target is shooter or target["health"] <= 0 or not is_enemy(shooter, target):
                    continue
                if target["rect"].colliderect(bullet):
                    apply_damage(target, 50)
                    FIREBALL_HIT_SOUND.play()
                    hit = True
                    break
            if hit:
                shooter["fireballs"].remove(bullet)

    # Laser damage
    if laser_info["player_id"] is not None:
        shooter = next((p for p in players if p["id"] == laser_info["player_id"] and p["health"] > 0), None)
        if shooter:
            beam_y_hit = shooter["rect"].y + shooter["rect"].height // 2 - LASER_HIT_H // 2
            if shooter["direction"] == "right":
                beam_rect = pygame.Rect(shooter["rect"].x, beam_y_hit, LASER_HIT_W, LASER_HIT_H)
            else:
                beam_rect = pygame.Rect(shooter["rect"].x - LASER_HIT_W, beam_y_hit, LASER_HIT_W, LASER_HIT_H)
            for target in players:
                if target is shooter or target["health"] <= 0 or not is_enemy(shooter, target):
                    continue
                if target["rect"].colliderect(beam_rect):
                    apply_damage(target, LASER_DAMAGE)
                    BEAM_HIT_SOUND.play()


def draw_winner(text):
    WIN.blit(SPACE, (0, 0))
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def fade(width, height, players, health, health_spawn, flame, flame_spawn,
         laser_info, ice, ice_spawn, lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map):
    fader = pygame.Surface((width, height))
    fader.fill((0, 0, 0))
    for alpha in range(0, 300):
        fader.set_alpha(alpha)
        redraw_window(players, health, health_spawn, flame, flame_spawn, laser_info, ice, ice_spawn,
                      lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)
        WIN.blit(fader, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def game_loop(mode):
    start_game_music(force_new=True)
    players = create_players(mode)
    health = pygame.Rect(1, 1, 1, 1)
    flame = pygame.Rect(1, 1, 1, 1)
    ice = pygame.Rect(1, 1, 1, 1)
    lightning = pygame.Rect(1, 1, 1, 1)
    shield = pygame.Rect(1, 1, 1, 1)
    blackhole = pygame.Rect(1, 1, 1, 1)

    i = 0
    x = 0
    y = 0
    z = 0
    l = 0
    s = 0
    bh = 0
    health_spawn = False
    flame_spawn = False
    ice_spawn = False
    lightning_spawn = False
    shield_spawn = False
    blackhole_spawn = False
    laser_info = {"player_id": None, "timer": 0}

    clock = pygame.time.Clock()
    random_tick = 0
    flame_tick = 0
    ice_tick = 0
    lightning_tick = 0
    shield_tick = 0
    blackhole_tick = 0
    blackhole_timer = 0
    run = True
    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        frozen_map = {p["id"]: current_time < p["freeze_until"] for p in players}

        if laser_info["player_id"] is not None:
            z += 1
            if z == 160:
                laser_info = {"player_id": None, "timer": 0}
                z = 0

        if i == 0:
            ice_tick = scaled_spawn(300, 600)
        i += 1
        if i == ice_tick:
            ice = pygame.Rect(random.randint(PLAYFIELD_MARGIN, WIDTH - ICE_HIT_W - PLAYFIELD_MARGIN),
                              random.randint(PLAYFIELD_MARGIN, HEIGHT - ICE_HIT_H - PLAYFIELD_MARGIN),
                              ICE_HIT_W, ICE_HIT_H)
            ice_spawn = True

        if l == 0:
            lightning_tick = scaled_spawn(400, 800)
        l += 1
        if l == lightning_tick:
            lightning = pygame.Rect(random.randint(PLAYFIELD_MARGIN, WIDTH - LIGHTNING_HIT_W - PLAYFIELD_MARGIN),
                                    random.randint(PLAYFIELD_MARGIN, HEIGHT - LIGHTNING_HIT_H - PLAYFIELD_MARGIN),
                                    LIGHTNING_HIT_W, LIGHTNING_HIT_H)
            lightning_spawn = True

        if BLACKHOLE_ENABLED:
            if bh == 0:
                blackhole_tick = scaled_spawn(BLACKHOLE_INTERVAL_MIN, BLACKHOLE_INTERVAL_MAX, multiplier=2.0)
            bh += 1
            if bh == blackhole_tick:
                blackhole = pygame.Rect(random.randint(PLAYFIELD_MARGIN, WIDTH - BLACKHOLE_HIT_W - PLAYFIELD_MARGIN),
                                        random.randint(PLAYFIELD_MARGIN, HEIGHT - BLACKHOLE_HIT_H - PLAYFIELD_MARGIN),
                                        BLACKHOLE_HIT_W, BLACKHOLE_HIT_H)
                blackhole_spawn = True
                blackhole_timer = 0

        if s == 0:
            shield_tick = scaled_spawn(600, 1000)
        s += 1
        if s == shield_tick:
            shield = pygame.Rect(random.randint(PLAYFIELD_MARGIN, WIDTH - SHIELD_HIT_W - PLAYFIELD_MARGIN),
                                 random.randint(PLAYFIELD_MARGIN, HEIGHT - SHIELD_HIT_H - PLAYFIELD_MARGIN),
                                 SHIELD_HIT_W, SHIELD_HIT_H)
            shield_spawn = True

        if x == 0:
            random_tick = scaled_spawn(200, 400)
        x += 1
        if x == random_tick:
            health = pygame.Rect(random.randint(PLAYFIELD_MARGIN, WIDTH - HEALTH_HIT_W - PLAYFIELD_MARGIN),
                                 random.randint(PLAYFIELD_MARGIN, HEIGHT - HEALTH_HIT_H - PLAYFIELD_MARGIN),
                                 HEALTH_HIT_W, HEALTH_HIT_H)
            health_spawn = True

        if y == 0:
            flame_tick = scaled_spawn(500, 1000)
        y += 1
        if y == flame_tick:
            flame = pygame.Rect(WIDTH // 2 - FLAME_HIT_W // 2, HEIGHT // 2 - FLAME_HIT_H // 2,
                                FLAME_HIT_W, FLAME_HIT_H)
            flame_spawn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                for player in players:
                    if player["health"] <= 0 or frozen_map[player["id"]]:
                        continue
                    keys = player["keys"]
                    if event.key == keys["shoot"] and len(player["bullets"]) < MAX_BULLETS:
                        if player["direction"] == "right":
                            bullet = pygame.Rect(
                                player["rect"].x + player["rect"].width,
                                player["rect"].y + player["rect"].height // 2 - BULLET_H // 2,
                                BULLET_W, BULLET_H)
                        else:
                            bullet = pygame.Rect(
                                player["rect"].x - BULLET_W,
                                player["rect"].y + player["rect"].height // 2 - BULLET_H // 2,
                                BULLET_W, BULLET_H)
                        player["bullets"].append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == keys["fireball"] and len(player["fireballs"]) < 1:
                        if player["direction"] == "right":
                            bullet = pygame.Rect(
                                player["rect"].x + player["rect"].width,
                                player["rect"].y + player["rect"].height // 2 - FIREBALL_HIT_H // 2,
                                FIREBALL_HIT_W, FIREBALL_HIT_H)
                        else:
                            bullet = pygame.Rect(
                                player["rect"].x - FIREBALL_HIT_W,
                                player["rect"].y + player["rect"].height // 2 - FIREBALL_HIT_H // 2,
                                FIREBALL_HIT_W, FIREBALL_HIT_H)
                        player["fireballs"].append(bullet)
                        FIREBALL_SHOT_SOUND.play()

        # Power-up collisions
        if health_spawn:
            for player in players:
                if player["health"] <= 0:
                    continue
                if player["rect"].colliderect(health):
                    player["health"] = min(MAX_HEALTH, player["health"] + 75)
                    health_spawn = False
                    x = 0
                    HEALTH_GRAB_SOUND.play()
                    break

        if flame_spawn:
            for player in players:
                if player["health"] <= 0:
                    continue
                if player["rect"].colliderect(flame):
                    laser_info = {"player_id": player["id"], "timer": 0}
                    z = 0
                    flame_spawn = False
                    y = 0
                    LASER_SOUND.play()
                    break

        if ice_spawn:
            for player in players:
                if player["health"] <= 0:
                    continue
                if player["rect"].colliderect(ice):
                    ice_spawn = False
                    i = 0
                    FREEZE_SOUND.play(maxtime=FREEZE_SOUND_HALF_MS)
                    for target in players:
                        if target["id"] != player["id"] and target["team"] != player["team"]:
                            target["freeze_until"] = current_time + ICE_FREEZE_MS
                    break

        if lightning_spawn:
            for player in players:
                if player["health"] <= 0:
                    continue
                if player["rect"].colliderect(lightning):
                    lightning_spawn = False
                    l = 0
                    player["vel"] = max(VEL, math.ceil(VEL * LIGHTNING_MULTIPLIER))
                    LIGHTNING_SOUND.play()
                    break

        if shield_spawn:
            for player in players:
                if player["health"] <= 0:
                    continue
                if player["rect"].colliderect(shield):
                    shield_spawn = False
                    s = 0
                    player["shield_hp"] = 100
                    break

        if BLACKHOLE_ENABLED and blackhole_spawn:
            blackhole_timer += 1
            if blackhole_timer >= BLACKHOLE_DURATION_TICKS:
                blackhole_spawn = False
                bh = 0

        frozen_map = {p["id"]: current_time < p["freeze_until"] for p in players}

        winner_text = ""
        alive_players = [p for p in players if p["health"] > 0 and not p.get("dead")]
        if mode == "1v1":
            if len(alive_players) == 1:
                frozen_map = {p["id"]: current_time < p["freeze_until"] for p in players}
                fade(WIDTH, HEIGHT, players, health, health_spawn, flame, flame_spawn, laser_info,
                     ice, ice_spawn, lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)
                winner_text = f"{alive_players[0]['name']} wins!"
            elif len(alive_players) == 0:
                fade(WIDTH, HEIGHT, players, health, health_spawn, flame, flame_spawn, laser_info,
                     ice, ice_spawn, lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)
                winner_text = "Draw!"
        else:
            team_counts = {"A": 0, "B": 0}
            for p in alive_players:
                if p["team"] in team_counts:
                    team_counts[p["team"]] += 1
            if team_counts["A"] == 0 and team_counts["B"] == 0:
                winning_team = None
                winner_text = "Draw!"
            elif team_counts["A"] == 0 and team_counts["B"] > 0:
                winning_team = "B"
            elif team_counts["B"] == 0 and team_counts["A"] > 0:
                winning_team = "A"
            else:
                winning_team = None

            if winning_team:
                frozen_map = {p["id"]: current_time < p["freeze_until"] for p in players}
                fade(WIDTH, HEIGHT, players, health, health_spawn, flame, flame_spawn, laser_info,
                     ice, ice_spawn, lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)
                winner_text = f"Team {winning_team} wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        draw_window(players, health, health_spawn, flame, flame_spawn, laser_info, ice, ice_spawn,
                    lightning, lightning_spawn, shield, shield_spawn, blackhole, blackhole_spawn, frozen_map)

        keys_pressed = pygame.key.get_pressed()
        for player in players:
            if player["health"] <= 0 or frozen_map[player["id"]]:
                continue
            handle_player_movement(keys_pressed, player, player["vel"])

        # Blackhole pull
        if BLACKHOLE_ENABLED and blackhole_spawn:
            bh_center = (blackhole.x + blackhole.width / 2, blackhole.y + blackhole.height / 2)
            for player in players:
                if player["health"] <= 0 or player.get("dead"):
                    continue
                px = player["rect"].x + player["rect"].width / 2
                py = player["rect"].y + player["rect"].height / 2
                dx = bh_center[0] - px
                dy = bh_center[1] - py
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                if dist <= BLACKHOLE_PULL_RADIUS:
                    if dist <= BLACKHOLE_LOCK_RADIUS:
                        force = BLACKHOLE_LOCK_FORCE
                    else:
                        force = BLACKHOLE_PULL_BASE * (BLACKHOLE_PULL_RADIUS / dist)
                        force = min(force, BLACKHOLE_LOCK_FORCE)
                    pull_x = (dx / dist) * force
                    pull_y = (dy / dist) * force
                    step_x = int(round(pull_x))
                    step_y = int(round(pull_y))
                    if step_x == 0 and abs(dx) > 1:
                        step_x = 1 if dx > 0 else -1
                    if step_y == 0 and abs(dy) > 1:
                        step_y = 1 if dy > 0 else -1
                    player["rect"].x = max(0, min(WIDTH - player["rect"].width, player["rect"].x + step_x))
                    player["rect"].y = max(0, min(HEIGHT - player["rect"].height, player["rect"].y + step_y))

        handle_projectiles(players, laser_info)

    return


def main_menu():
    menu = True
    options = ["1v1", "2v2", "EXIT"]
    selected = 0
    start_game_music()
    menu_ship_yellow = pygame.transform.rotate(
        pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 90)
    menu_ship_red = pygame.transform.rotate(
        pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), 270)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    MENU_SOUND.play()
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    MENU_SOUND.play()
                if event.key == pygame.K_RETURN:
                    choice = options[selected]
                    if choice == "EXIT":
                        pygame.quit()
                        return None
                    START_SOUND.play()
                    return choice

        WIN.blit(SPACE, (0, 0))
        for idx, option in enumerate(options):
            is_selected = idx == selected
            color = WHITE if is_selected else (120, 120, 120)
            text = MENU_FONT.render(option, True, color)
            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = 120 + idx * 160
            WIN.blit(text, (text_x, text_y))
            if is_selected:
                # show ships only next to the selected option
                WIN.blit(menu_ship_yellow, (text_x - 200, text_y - 30))
                WIN.blit(menu_ship_red, (text_x + text.get_width() + 80, text_y - 30))
        pygame.display.update()


def main():
    while True:
        mode = main_menu()
        if mode is None:
            break
        game_loop(mode)


if __name__ == "__main__":
    main()
