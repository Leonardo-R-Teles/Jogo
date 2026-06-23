import pygame

# Game setup
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Player setup
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill("black")

    # Draw logic

    # Floor
    pygame.draw.rect(screen, "green", (0, 550, 800, 50))  # 1
    pygame.draw.rect(screen, "green", (0, 500, 200, 50))  # 2
    pygame.draw.rect(screen, "green", (750, 500, 100, 50))  # 2
    pygame.draw.rect(screen, "green", (0, 500, 100, 50))  # 3
    pygame.draw.rect(screen, "green", (0, 450, 100, 50))  # 3

    # Player
    pygame.draw.rect(screen, "blue", (player_pos.x, player_pos.y, 50, 50))

    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos.x += 300 * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_pos.y += 300 * dt

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()
