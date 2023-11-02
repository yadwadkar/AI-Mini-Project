import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BALL_SPEED = 1
PADDLE_SPEED = 3
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
WINNING_SCORE = 100 
GAME_DURATION = 120000  

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize game variables
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))  # Start ball in a random direction
ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))  # Start ball in a random direction

left_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2

left_score = 0
right_score = 0

# AI opponent variables
ai_paddle_speed = 5  # Adjust the AI paddle speed as needed

# Start time for the game timer
start_time = pygame.time.get_ticks()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        right_paddle_y += PADDLE_SPEED

    # AI opponent logic (left paddle)
    ai_center = left_paddle_y + PADDLE_HEIGHT / 2
    if ball_y > ai_center:
        left_paddle_y += ai_paddle_speed
    elif ball_y < ai_center:
        left_paddle_y -= ai_paddle_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collision with paddles
    if (
        ball_x <= PADDLE_WIDTH
        and left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT
    ) or (
        ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE
        and right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT
    ):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:
        right_score += 1
        if right_score >= WINNING_SCORE:
            print("Player on the right wins!")
            pygame.quit()
            sys.exit()
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))  # Random direction
        ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))  # Random direction
    elif ball_x > WIDTH:
        left_score += 1
        if left_score >= WINNING_SCORE:
            print("AI Opponent wins!")
            pygame.quit()
            sys.exit()
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))  # Random direction
        ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))  # Random direction

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, RED, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(
        screen, GREEN, (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    )
    pygame.draw.ellipse(screen, YELLOW, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw the timer and score
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, GAME_DURATION - elapsed_time) // 1000  # Convert to seconds
    WHITE = (255, 255, 255)  # Define the color here
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {remaining_time} seconds", True, WHITE)
    screen.blit(timer_text, (20, 20))

    score_text = font.render(f"Left: {left_score} | Right: {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 200, 20))

    # Update the display
    pygame.display.flip()

    # Check for game timeout
    if elapsed_time >= GAME_DURATION:
        print("Game Over - Time's up!")
        pygame.quit()
        sys.exit()
