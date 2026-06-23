import pygame

# inicia o Pygame
pygame.init()

# janela inicial
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD Movimento")

# configuração personagem
player_size = 50
player_color = (255, 0, 0)  # vermelho
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 5        # velocidade do personagem

clock = pygame.time.Clock()

# mantem o jogo rodando enquanto running = true
running = True
dt = 0

# Player setup
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # evento de apertar "X" da janela, muda o running pra false e fecha o jogo
            running = False

    keys = pygame.key.get_pressed()  # pega as teclas pressionadas
    if keys[pygame.K_w] or keys[pygame.K_UP]:  # move para cima
        player_y -= player_speed * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # move para baixo
        player_y += player_speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # move para a esquerda
        player_x -= player_speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # move para a direita
        player_x += player_speed * dt

    # limita o movimento do personagem dentro da tela
    player_x = max(0, min(player_x, screen_width - player_size))
    player_y = max(0, min(player_y, screen_height - player_size))

    # tela preta
    screen.fill((0, 0, 0))

    # desenha o personagem
    pygame.draw.rect(screen, player_color, (player_x,
                     player_y, player_size, player_size))

    # atualiza a tela
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # tempo em segundos desde o último frame

# quando o loop principal termina, finaliza o Pygame
pygame.quit()

# chão
pygame.draw.rect(screen, "green", (0, 550, 800, 50))  # 1
pygame.draw.rect(screen, "green", (0, 500, 200, 50))  # 2
pygame.draw.rect(screen, "green", (750, 500, 100, 50))  # 2
pygame.draw.rect(screen, "green", (0, 500, 100, 50))  # 3
pygame.draw.rect(screen, "green", (0, 450, 100, 50))  # 3
