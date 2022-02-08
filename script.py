import pygame
from random import randrange

width, height = 1300, 700  # width and height must be divisable by snake_size

# RGB values
black = (0, 0, 0)
white = (255, 255, 255)
green = (50, 205, 50)
red = (255, 0, 0)

snake_size = 25
fps = 3

assert width % snake_size == 0 and height % snake_size == 0, 'width and height should be divisible by snake_size'

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake AI")


class Snake():
    def __init__(self, size, color, snake_body) -> None:
        self.size = size
        self.color = color
        self.head = snake_body[0]
        self.body = snake_body
        self.direction = None

    def moveSnake(self, appleX, appleY):
        new_snake = []

        if appleX < self.head.x:  # Left
            self.direction = (-snake_size, 0)
        elif appleX > self.head.x:  # Right
            self.direction = (snake_size, 0)
        elif appleY < self.head.y:  # Up
            self.direction = (0, -snake_size)
        else:  # Down
            self.direction = (0, snake_size)

        previousRect = self.head

        for rect in self.body:
            if rect == self.head:
                new_snake.append(rect.move(
                    self.direction[0], self.direction[1]))
            else:
                new_snake.append(previousRect)
                previousRect = rect

        self.body = new_snake
        self.head = new_snake[0]

    def drawSnake(self):
        # Draws every rect induvidally
        for rect in self.body:
            pygame.draw.rect(win, green, rect)


# Divides the width and height by the snake size and draws lines that many times spaced out by the snake size
def draw_border():
    for i in range(width // snake_size):
        pygame.draw.line(win, white, (snake_size * i, 0),
                         (snake_size * i, height), 1)

    for i in range(height // snake_size):
        pygame.draw.line(win, white, (0, snake_size * i),
                         (width, snake_size * i), 1)


def handle_collision(snake, x_coord, y_coord):
    apple = pygame.Rect(x_coord, y_coord, snake_size, snake_size)
    return apple.colliderect(snake)


def main():
    snake_body = [pygame.Rect(width // 2, height // 2, snake_size, snake_size)]
    snake = Snake(snake_size, green, snake_body)
    clock = pygame.time.Clock()
    apple = True

    while True:
        # Slows down the loop to the fps
        #clock.tick_busy_loop(fps)

        # If the wants to quit then quit and exit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if apple:

            # Spawns the apple in the fixed locations inside the cells
            appleX = randrange(0, width, snake.size)
            appleY = randrange(0, height, snake.size)
            apple = False

            # If its not the first time spawning the apple spawn another infront of the head
            if snake.direction:
                snake_body = snake.body
                snake_body.append(pygame.Rect(
                    snake.head.x + snake.direction[0], snake.head.y + snake.direction[1], snake.size, snake.size))

                snake.body = snake_body
                snake.head = snake_body[0]
                print(snake.body)

        # Draw the apple
        pygame.draw.circle(win, red, (appleX + (snake_size // 2),
                                      appleY + (snake_size // 2)), snake_size // 2)

        snake.moveSnake(appleX, appleY)
        snake.drawSnake()

        apple = handle_collision(snake.head, appleX, appleY)

        draw_border()

        # Display everything that just happened and fill the screen with a color
        pygame.display.update()
        win.fill(black)


if __name__ == '__main__':
    main()
