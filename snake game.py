import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.handle_keys()
        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        screen.fill(BLACK)
