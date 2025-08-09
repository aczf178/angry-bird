# Import necessary libraries
import pygame
import sys
import random
from classes import Player, Button

# Initialize Pygame
pygame.init()

# Set up screen dimensions and colors
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")

# Load bird and background images
player_image = pygame.image.load("images/player.png",)
player_image = pygame.transform.scale(player_image, (150, 150))
enemy_image = pygame.image.load("images/enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (150, 150))
background_image = pygame.image.load("images/background.png")
# Scale the background image to fit the screen dimensions
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game set up
# Create the player bird
player = Player(100, SCREEN_HEIGHT // 2, player_image)

# Create enemy birds
enemies = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    enemy = Player(x, y, enemy_image)
    enemies.add(enemy)

# Calculate button positions and initialise score
button_margin = 10
button_top = button_margin
button_left = button_margin
button_spacing = 5

# Initialise player's score
score = 0

# Calculate position for displaying the score
score_position = (800, 80)\

# Create quit and refresh buttons
quit_button_image = pygame.image.load(
    "images/quit_button.png")
quit_button_image = pygame.transform.scale(quit_button_image, (100, 100))
refresh_button_image = pygame.image.load(
    "images/reset_button.png")
refresh_button_image = pygame.transform.scale(refresh_button_image, (100, 100))

quit_button = Button(button_left, button_top, quit_button_image, "quit")
refresh_button = Button(button_left + quit_button_image.get_width() +
                        button_spacing, button_top, 
                        refresh_button_image, "refresh")

# Initialize game loop and state
clock = pygame.time.Clock()
try_again_counter = 0
max_try_again = 3
level_cleared = False
game_over = False

# Enter the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle button clicks and player interactions
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the Quit button was clicked
            if quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

            # Check if the Refresh button was clicked
            elif refresh_button.rect.collidepoint(event.pos):
                # Reset player bird's position and velocity
                player.rect.center = (100, SCREEN_HEIGHT // 2)
                player.velocity = [0, 0]

                # Reset enemy birds and their positions
                enemies.empty()
                for _ in range(5):
                    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    enemy = Player(x, y, enemy_image)
                    enemies.add(enemy)

                # Reset game state
                level_cleared = False
                game_over = False
                try_again_counter = 0
                score = 0

            # Check if the player bird was clicked
            elif player.rect.collidepoint(event.pos):
                player.start_drag()

        elif event.type == pygame.MOUSEBUTTONUP:
            if player.dragging:
                player.end_drag()

                # Increment try_again_counter if no hits occurred
                if not hits:
                    try_again_counter += 1
            else:
                break
       
    # Update enemy bird positions and handle collisions
    hits = pygame.sprite.spritecollide(player, enemies, True)

    if hits:
        for hit_enemy in hits:
            score += hit_enemy.hit_enemy()

    # Reset enemy bird positions
    for enemy in enemies:
        if enemy.rect.right < 0:
            enemy.rect.left = SCREEN_WIDTH
            enemy.rect.top = random.randint(50, SCREEN_HEIGHT - 50)

    # Reset player bird's position if it goes off-screen
    if player.rect.left > SCREEN_WIDTH or player.rect.right < 0 or \
            player.rect.top > SCREEN_HEIGHT or player.rect.bottom < 0:
        player.rect.center = (100, SCREEN_HEIGHT // 2)
        player.velocity = [0, 0]     

    # Clear the screen and draw the background
    screen.blit(background_image, (0, 0))

    # Draw player bird and enemy birds
    player.update()
    screen.blit(player.image, player.rect)

    # Update and draw enemy birds
    enemies.update()
    enemies.draw(screen)

    # Display font
    font = pygame.font.Font(None, 50)

    # Score font
    score_font = pygame.font.Font(None, 36)

    # Draw player's score and buttons
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, score_position)

    screen.blit(quit_button.image, quit_button.rect)
    screen.blit(refresh_button.image, refresh_button.rect)

    # Display "Level Cleared" message if score is 500
    if score >= 500 and not level_cleared:
        level_cleared_text = font.render("LEVEL CLEARED", True, (0, 0, 0))
        text_rect = level_cleared_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(level_cleared_text, text_rect)
        level_cleared = True

    # Display "Game Over" message if score is 0 after three hits
    if score == 0 and try_again_counter >= max_try_again and not game_over:
        game_over_text = font.render("GAME OVER", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        game_over = True

    # Update the display and control the frame rate
    pygame.display.flip()
    clock.tick(60)

pygame.quit()