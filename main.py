import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
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

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
