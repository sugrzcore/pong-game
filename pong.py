import pygame
import sys
import random

# --- INIT ---
pygame.init()

# Window
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Normal AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PLAYER_SPEED = 6
AI_SPEED = 4          # سختی نرمال

# Ball settings
BALL_SIZE = 15
ball_speed_x = 5
ball_speed_y = 5

# Objects
left_paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2,
                          PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 35, HEIGHT//2 - PADDLE_HEIGHT//2,
                           PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

# Score
score_left = 0
score_right = 0
font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()


def reset_ball():
    """Reset ball to center after scoring."""
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x *= -1
    ball_speed_y = random.choice([-5, 5])


# --- GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- PLAYER CONTROL ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PLAYER_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PLAYER_SPEED

    # --- AI CONTROL (NORMAL) ---
    error = random.randint(-30, 30)  # مقداری خطا برای طبیعی بودن
    if right_paddle.centery < ball.centery + error and right_paddle.bottom < HEIGHT:
        right_paddle.y += AI_SPEED
    if right_paddle.centery > ball.centery + error and right_paddle.top > 0:
        right_paddle.y -= AI_SPEED

    # --- BALL MOVEMENT ---
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle collision
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Scoring
    if ball.left < -20:
        score_right += 1
        reset_ball()
    if ball.right > WIDTH + 20:
        score_left += 1
        reset_ball()

    # --- DRAW ---
    win.fill(BLACK)

    pygame.draw.rect(win, WHITE, left_paddle)
    pygame.draw.rect(win, WHITE, right_paddle)
    pygame.draw.ellipse(win, PINK, ball)

    pygame.draw.aaline(win, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score_left}    {score_right}", True, WHITE)
    win.blit(score_text, (WIDTH//2 - 40, 20))

    pygame.display.flip()
    clock.tick(60)

