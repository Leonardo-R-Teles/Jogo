import pygame

# inicia o Pygame
pygame.init()

# janela inicial
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD Movimento")

# configuração do personagem
player_size = 50
player_color = "blue"
player_x = 100
player_y = 400
player_speed = 200
transition_cooldown = 0.0  # segundos para evitar transições seguidas

clock = pygame.time.Clock()

running = True
dt = 0  # delta time para normalizar a fisica do jogo independente do FPS

# fases
tile_size = 50

level_1 = [
    "................................................................................................",
    "................................................................................................",
    "................................................................................................",
    "................................................................................................",
    ".............................................................................................XXX",
    "............................................................................................XXXX",
    "...........................................................................................XXXXX",
    "................................................................................XXXXXXXXXXXXXXXX",
    "...........................T..................................................XXXXXXXXXXXXXXXXXX",
    "....................XXXXXXXXXXXXXXX.........................................XXXXXXXXXXXXXXXXXXXX",
    "XXX............XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX....................XXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

dungeon_1 = [
    "XXXXXXX..XXXXXXX",
    "X..............X",
    "X..............X",
    "X..............X",
    "X..............X",
    "................",
    "................",
    "X..............X",
    "X..............X",
    "X..............X",
    "X..............X",
    "XXXXXXX..XXXXXXX",
]

platforms: list[pygame.Rect] = []
transition_zones: list[pygame.Rect] = []
for i, row in enumerate(level_1):
    for j, tile in enumerate(row):
        if tile == "X":
            platforms.append(
                pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            )
        elif tile == "T":
            transition_zones.append(
                pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            )

rooms: list[pygame.Rect] = []
for i, row in enumerate(dungeon_1):
    for j, tile in enumerate(row):
        if tile == "X":
            rooms.append(
                pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            )

# Zona de saída do dungeon: entrada inferior (fileira 11, colunas 7-8)
dungeon_exit_zone: pygame.Rect = pygame.Rect(
    7 * tile_size, 11 * tile_size, 2 * tile_size, 1 * tile_size
)

look = "side-scroller"

# camera
camera_x = 0
scroll_margin = 250
level_width = 0

if look == "top-down":
    level_width = len(dungeon_1[0]) * tile_size
else:
    level_width = len(level_1[0]) * tile_size


# loop principal do jogo
while running:
    # eventos pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # entrada do teclado
    keys = pygame.key.get_pressed()  # pega as teclas pressionadas

    # Reduz o cooldown de transição
    transition_cooldown = max(0, transition_cooldown - dt)

    if look == "side-scroller":
        # --- Movimento ---
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= player_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += player_speed * dt
        player_x += dx

        # adicionar pulo e gravidade

        # adicionar colisão, com exceção da zona de transição

        # --- Transição para dungeon ---
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for zone in transition_zones:
            if (
                transition_cooldown <= 0
                and player_rect.colliderect(zone)
                and (keys[pygame.K_s] or keys[pygame.K_DOWN])
            ):
                look = "top-down"
                player_x = 375
                player_y = 480
                transition_cooldown = 1
                camera_x = 0
                level_width = len(dungeon_1[0]) * tile_size
                break

    else:  # top-down
        # --- Transição de volta para side-scroller ---
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if (
            transition_cooldown <= 0
            and player_rect.colliderect(dungeon_exit_zone)
            and (keys[pygame.K_s] or keys[pygame.K_DOWN])
        ):
            look = "side-scroller"
            player_x = 1375  # mesma coluna do tile T
            player_y = 400  # acima do tile T para cair com gravidade
            transition_cooldown = 0.5
            camera_x = max(0, 1350 - screen_width // 2)
            level_width = len(level_1[0]) * tile_size
            continue

        # --- Movimento ---
        dx = 0
        dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= player_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += player_speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= player_speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += player_speed * dt

        player_x += dx
        player_y += dy

    # define posição do personagem
    player = pygame.Rect((player_x, player_y, player_size, player_size))

    # define posição da câmera
    if player.x - camera_x > screen_width - scroll_margin:
        camera_x = player.x - (screen_width - scroll_margin)
    elif player.x - camera_x < scroll_margin:
        camera_x = player.x - scroll_margin

    camera_x = max(0, min(camera_x, level_width - screen_width))

    # limpa a tela
    screen.fill("black")

    # desenha a fase
    if look == "top-down":
        for room in rooms:
            pygame.draw.rect(
                screen,
                "gray",
                (
                    room.x - camera_x,
                    room.y,
                    room.width,
                    room.height,
                ),
            )
        # Desenha zona de saída (roxa, igual ao tile T do side-scroller)
        pygame.draw.rect(
            screen,
            "purple",
            (
                dungeon_exit_zone.x - camera_x,
                dungeon_exit_zone.y,
                dungeon_exit_zone.width,
                dungeon_exit_zone.height,
            ),
        )
    else:
        # Desenha tiles de transição (fundo roxo, sem colisão)
        for zone in transition_zones:
            pygame.draw.rect(
                screen,
                "purple",
                (
                    zone.x - camera_x,
                    zone.y,
                    zone.width,
                    zone.height,
                ),
            )
        # Desenha plataformas sólidas
        for platform in platforms:
            pygame.draw.rect(
                screen,
                "green",
                (
                    platform.x - camera_x,
                    platform.y,
                    platform.width,
                    platform.height,
                ),
            )

    # desenha o personagem
    pygame.draw.rect(
        screen,
        player_color,
        (player.x - camera_x, player.y, player.width, player.height),
    )

    # atualiza a tela
    pygame.display.flip()

    # fps = 60
    dt = clock.tick(60) / 1000

# quando o loop principal termina, finaliza o Pygame
pygame.quit()
