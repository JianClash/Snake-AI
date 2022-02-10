from distutils.spawn import spawn
import pygame
from random import randrange

width, height = 1300, 700  # width and height must be divisable by snake_size

# colors reperesented as RGB values
black = (0, 0, 0)
white = (255, 255, 255)
green = (50, 205, 50)
red = (255, 0, 0)

snake_size = 25
spawnCoords = [pygame.Rect(width // 2, height // 2, snake_size, snake_size)]
fps = 10

assert width % snake_size == 0 and height % snake_size == 0, 'width and height should be divisible by snake_size'

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake AI")


class Snake:
    def __init__(self, size, color, snake_body) -> None:
        self.size = size
        self.color = color
        self.head = snake_body[0]
        self.body = snake_body
        self.direction = None
        self.previousRect = self.head

    def move(self, appleX, appleY):
        new_snake = []

        # Checks the x and y coordinates of the apple and compares them to the snakes
        # and determines the direction it is going to move next
        if appleX < self.head.x:  # Left
            self.direction = (-snake_size, 0)
        elif appleX > self.head.x:  # Right
            self.direction = (snake_size, 0)
        elif appleY < self.head.y:  # Up
            self.direction = (0, -snake_size)
        else:  # Down
            self.direction = (0, snake_size)

        # Loops through every snake part and move the head in the direction
        # The other parts follow the rect infront of it
        for rect in self.body:
            if rect == self.head:
                new_snake.append(rect.move(
                    self.direction[0], self.direction[1]))
            else:
                new_snake.append(self.previousRect)

            self.previousRect = rect

        self.body = new_snake
        self.head = new_snake[0]

    def draw(self):
        # Loops through every part of the snake and draws them induvidally
        for rect in self.body:
            pygame.draw.rect(win, green, rect)


class Apple:
    def spawn(self, snake_size):
        # Spawns the apple in the fixed locations inside the cells
        self.x = randrange(0, width, snake_size)
        self.y = randrange(0, height, snake_size)

    def draw(self, snake_size):
        # Draws the apple
        pygame.draw.circle(win, red, (self.x + (snake_size // 2),
                                      self.y + (snake_size // 2)), snake_size // 2)


def draw_border():
    # Divides the width and height by the snake size and draws lines that many times
    # Theres a difference of snake_size between each line
    for i in range(width // snake_size):
        pygame.draw.line(win, white, (snake_size * i, 0),
                         (snake_size * i, height), 1)

    for i in range(height // snake_size):
        pygame.draw.line(win, white, (0, snake_size * i),
                         (width, snake_size * i), 1)


def handle_collision(snake, x_coord, y_coord):
    # Detects if the snake colided with the apple
    apple = pygame.Rect(x_coord, y_coord, snake_size, snake_size)
    return apple.colliderect(snake)


def main():
    snake = Snake(snake_size, green, spawnCoords)
    apple = Apple()
    clock = pygame.time.Clock()
    appleSpawned = False

    while True:
        # Slows down the loop to the fps
        clock.tick_busy_loop(fps)

        # If the wants to quit then quit and exit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if not appleSpawned:
            apple.spawn(snake.size)
            appleSpawned = True

            # If its not the first time spawning the apple spawn another rect in the back
            if snake.direction:
                snake.body = snake.body + [snake.previousRect]
                snake.head = snake.body[0]

        apple.draw(snake.size)

        snake.draw()
        snake.move(apple.x, apple.y)

        appleSpawned = not handle_collision(snake.head, apple.x, apple.y)

        draw_border()

        # Display everything that just happened and fill the screen with a color
        pygame.display.update()
        win.fill(black)


if __name__ == '__main__':
    main()
