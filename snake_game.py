import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif not self.game_over:
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT

    def update(self):
        if self.game_over:
            return

        # Get the current head position
        head_x, head_y = self.snake[0]

        # Update head position based on direction
        if self.direction == Direction.UP:
            head_y -= 1
        elif self.direction == Direction.DOWN:
            head_y += 1
        elif self.direction == Direction.LEFT:
            head_x -= 1
        elif self.direction == Direction.RIGHT:
            head_x += 1

        # Check for collisions with walls
        if head_x < 0 or head_x >= GRID_COUNT or head_y < 0 or head_y >= GRID_COUNT:
            self.game_over = True
            return

        # Check for collisions with self
        new_head = (head_x, head_y)
        if new_head in self.snake[1:]:
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            if len(self.snake) == GRID_COUNT * GRID_COUNT:
                # Snake filled the board; end the game
                self.food = None
                self.game_over = True
                return
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw grid lines
        for i in range(GRID_COUNT):
            pygame.draw.line(self.screen, GRAY, (i * GRID_SIZE, 0), (i * GRID_SIZE, WINDOW_SIZE))
            pygame.draw.line(self.screen, GRAY, (0, i * GRID_SIZE), (WINDOW_SIZE, i * GRID_SIZE))

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN,
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # Draw food if available
        if self.food is not None:
            pygame.draw.rect(
                self.screen,
                RED,
                (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1),
            )

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 