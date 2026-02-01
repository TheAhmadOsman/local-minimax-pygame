import pygame
import random
import sys

# ============== CONSTANTS ==============
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

# Colors
BG_COLOR = (173, 216, 230)  # Light blue pastel
GROUND_COLOR_DARK_BROWN = (101, 67, 33)
GROUND_COLOR_YELLOW = (240, 230, 140)

BIRD_DARK_COLORS = [
    (30, 30, 30),      # Near black
    (60, 40, 40),      # Dark reddish
    (40, 50, 40),      # Dark greenish
    (40, 40, 60),      # Dark bluish
    (50, 45, 35),      # Dark brownish
]

PIPE_COLORS = [
    (34, 139, 34),     # Forest green
    (139, 90, 43),     # Light brown
    (80, 80, 80),      # Dark gray
]

# Physics
GRAVITY = 1500
FLAP_STRENGTH = -400
MAX_VELOCITY = 500

# Ground
GROUND_HEIGHT = 80

# Pipes
PIPE_WIDTH = 60
PIPE_SPEED = 250
PIPE_GAP_MIN = 150
PIPE_GAP_MAX = 200
PIPE_SPAWN_MIN = 1.5
PIPE_SPAWN_MAX = 2.5

# Bird
BIRD_SIZE = 30


# ============== HELPER CLASSES ==============

class Bird:
    SHAPES = ['square', 'circle', 'triangle']

    def __init__(self):
        self.shape = random.choice(self.SHAPES)
        self.color = random.choice(BIRD_DARK_COLORS)
        self.rect = pygame.Rect(80, SCREEN_HEIGHT // 2 - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
        self.vel_y = 0
        self.rotation = 0

    def flap(self):
        self.vel_y = FLAP_STRENGTH

    def update(self, dt):
        self.vel_y += GRAVITY * dt
        self.vel_y = max(-MAX_VELOCITY, min(MAX_VELOCITY, self.vel_y))
        self.rect.y += int(self.vel_y * dt)
        self.rotation = max(-30, min(30, int(self.vel_y * 0.05)))

    def draw(self, surface):
        color = self.color
        if self.shape == 'square':
            pygame.draw.rect(surface, color, self.rect)
        elif self.shape == 'circle':
            center = self.rect.center
            pygame.draw.circle(surface, color, center, BIRD_SIZE // 2)
        elif self.shape == 'triangle':
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom),
            ]
            pygame.draw.polygon(surface, color, points)

    def get_hitbox(self):
        if self.shape == 'circle':
            return self.rect.inflate(-10, -10)
        return self.rect


class PipePair:
    def __init__(self, x):
        self.x = x
        self.gap_size = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
        self.gap_y = random.randint(
            GROUND_HEIGHT + 50,
            SCREEN_HEIGHT - GROUND_HEIGHT - 50 - self.gap_size
        )
        self.color = random.choice(PIPE_COLORS)
        self.passed = False

        self.top_rect = pygame.Rect(0, 0, PIPE_WIDTH, self.gap_y)
        self.bottom_rect = pygame.Rect(
            0, self.gap_y + self.gap_size, PIPE_WIDTH,
            SCREEN_HEIGHT - self.gap_y - self.gap_size - GROUND_HEIGHT
        )

    def update(self, dt):
        self.x -= PIPE_SPEED * dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface):
        # Draw top pipe
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        pygame.draw.rect(surface, self.color, top_rect)
        pygame.draw.rect(surface, (min(self.color[0] + 20, 255), min(self.color[1] + 20, 255), min(self.color[2] + 20, 255)),
                         (self.x, self.gap_y - 20, PIPE_WIDTH, 20))  # Cap

        # Draw bottom pipe
        bottom_top = self.gap_y + self.gap_size
        bottom_height = SCREEN_HEIGHT - bottom_top - GROUND_HEIGHT
        bottom_rect = pygame.Rect(self.x, bottom_top, PIPE_WIDTH, bottom_height)
        pygame.draw.rect(surface, self.color, bottom_rect)
        pygame.draw.rect(surface, (min(self.color[0] + 20, 255), min(self.color[1] + 20, 255), min(self.color[2] + 20, 255)),
                         (self.x, bottom_top, PIPE_WIDTH, 20))  # Cap

    def collides_with(self, bird_hitbox):
        return (self.top_rect.colliderect(bird_hitbox) or
                self.bottom_rect.colliderect(bird_hitbox))

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def get_score_x(self):
        return self.x + PIPE_WIDTH // 2


# ============== GAME CLASS ==============

class Game:
    STATE_READY = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)

        self.reset_game()
        self.run()

    def reset_game(self):
        self.state = self.STATE_READY
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.best_score = 0
        self.ground_color = random.choice([GROUND_COLOR_DARK_BROWN, GROUND_COLOR_YELLOW])

        self.pipe_spawn_timer = 0
        self.next_spawn_delay = random.uniform(PIPE_SPAWN_MIN, PIPE_SPAWN_MAX)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    if self.state == self.STATE_READY:
                        self.state = self.STATE_PLAYING
                    elif self.state == self.STATE_PLAYING:
                        self.bird.flap()
                    elif self.state == self.STATE_GAME_OVER:
                        self.reset_game()

    def update(self, dt):
        if self.state == self.STATE_PLAYING:
            self.bird.update(dt)

            # Spawn pipes
            self.pipe_spawn_timer += dt
            if self.pipe_spawn_timer >= self.next_spawn_delay:
                self.pipes.append(PipePair(SCREEN_WIDTH))
                self.pipe_spawn_timer = 0
                self.next_spawn_delay = random.uniform(PIPE_SPAWN_MIN, PIPE_SPAWN_MAX)

            # Update pipes and check collisions
            bird_hitbox = self.bird.get_hitbox()

            for pipe in self.pipes:
                pipe.update(dt)

                if not pipe.passed and pipe.get_score_x() < self.bird.rect.centerx:
                    pipe.passed = True
                    self.score += 1

                if pipe.collides_with(bird_hitbox):
                    self.game_over()

            # Remove off-screen pipes
            self.pipes = [p for p in self.pipes if not p.is_off_screen()]

            # Check ground collision
            if self.bird.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.game_over()

        elif self.state == self.STATE_GAME_OVER:
            pass

    def game_over(self):
        self.state = self.STATE_GAME_OVER
        if self.score > self.best_score:
            self.best_score = self.score

    def draw(self):
        self.screen.fill(BG_COLOR)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, self.ground_color, ground_rect)

        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

        if self.state == self.STATE_READY:
            text = self.big_font.render("Press SPACE to start", True, (0, 0, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)

        elif self.state == self.STATE_GAME_OVER:
            go_text = self.big_font.render("Game Over", True, (0, 0, 0))
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(go_text, go_rect)

            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(score_text, score_rect)

            best_text = self.font.render(f"Best: {self.best_score}", True, (0, 0, 0))
            best_rect = best_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(best_text, best_rect)

            restart_text = self.font.render("Press SPACE to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_input()
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Game()