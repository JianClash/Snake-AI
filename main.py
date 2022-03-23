import pygame
from A_Star import A_star, Node
from random import randrange

snake_size = 20
rows = 30
columns = 30
width = rows * snake_size
height = columns * snake_size

# colors reperesented as RGB values
black = (0, 0, 0)
white = (255, 255, 255)
green = (50, 205, 50)
red = (255, 0, 0)
cyan = (0, 255, 255)

spawnCoords = [pygame.Rect(0, 0, snake_size, snake_size)]
fps = 30

# Initalizing the screen
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

    def move(self, path):
        new_snake = []
        x = path[-1].j * snake_size
        y = path[-1].i * snake_size

    

        for rect in self.body:
            if rect is self.head:
                new_snake.append(pygame.Rect(x,y, snake_size, snake_size))
            else:
                new_snake.append(self.previousRect)
            self.previousRect = rect

        self.body = new_snake
        self.head = new_snake[0]
        self.direction = True


    def draw(self):
        # Loops through every part of the snake and draws them induvidally
        for rect in self.body:
            pygame.draw.rect(win, green, rect)


class Apple:
    def spawn(self, snake_size, snake):
        unavailableSpotsX = []
        unavailableSpotsY = []
        self.x, self.y = None, None
        for rect in snake.body:
            unavailableSpotsX.append(rect.x)
            unavailableSpotsY.append(rect.y)
        # Spawns the apple in the fixed locations inside the cells
        while self.x not in unavailableSpotsX and self.y not in unavailableSpotsY:
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

def getGrid(snake):
    # making a 2d array
    grid = []
    for i in range(columns):
        grid.append([])
        for j in range(rows):
            grid[i].append([])

    num = 0
    for i in range(columns):
        for j in range(rows):
            grid[i][j] = Node(i, j)
            grid[i][j].isSnake(snake)
            if grid[i][j].wall == True: 
                num += 1

    for i in range(columns):
        for j in range(rows):
            grid[i][j].addNeighbours(grid, rows, columns)

    return grid

def draw_path(path):
    for i in path:
        if i.previous != None:
            startX = (i.j*snake_size) + (snake_size//2)
            startY = (i.i*snake_size) + (snake_size//2)
            endX = (i.previous.j*snake_size) + (snake_size//2)
            endY = (i.previous.i*snake_size) + (snake_size//2)

            pygame.draw.line(win, cyan, (startX, startY), (endX, endY), 3)

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
            apple.spawn(snake.size, snake)
            appleSpawned = True

            # If its not the first time spawning the apple add a tail
            if snake.direction:
                snake.body = snake.body + [snake.previousRect]
                snake.head = snake.body[0]


            grid = getGrid(snake)
            start = grid[snake.head.y // snake.size][snake.head.x // snake.size]
            end = grid[apple.y // snake.size][apple.x // snake.size]
            path = A_star(start, end)

        apple.draw(snake.size)

        snake.draw()
        snake.move(path)

        appleSpawned = not handle_collision(snake.head, apple.x, apple.y)

        draw_border()
        draw_path(path)

        # Display everything that just happened and after that fill the screen with a color to be drawn on again
        pygame.display.update()
        win.fill(black)

        if len(snake.body) == rows * columns:
            print('win', len(snake.body))
            break

        path.pop(-1)

if __name__ == '__main__':
    main()
