import pygame
from random import randrange

width, height = 1300, 700 # HINT: width and height must be divisable by snake_size


black = (0, 0, 0)
white = (255, 255, 255)
green = (50,205,50)
red = (255, 0, 0)

snake_size = 25
fps = 5 

assert width%snake_size == 0 and height%snake_size == 0, 'width and height should be divisible by snake_size'

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake AI")

def draw_snake(snake):
    for rect in snake:
        pygame.draw.rect(win, green, rect)  

def draw_border():
    for i in range(width//snake_size):
        pygame.draw.line(win, white, (snake_size*i, 0), (snake_size*i, height), 1)

    for i in range(height//snake_size):
        pygame.draw.line(win, white, (0, snake_size*i), (width, snake_size*i), 1)

def move_snake(snake, x_coord, y_coord):
    new_snake = []

    if x_coord < snake[0].x:
        coords = (-snake_size, 0)
    elif x_coord > snake[0].x:
        coords = (snake_size, 0)
    elif y_coord < snake[0].y:
        coords = (0, -snake_size)
    else:
        coords = (0, snake_size)

    latest_movment = snake[0]

    for block in snake:
        if block == snake[0]:
            new_snake.append(block.move(coords[0], coords[1]))
        else:
            new_snake.append(latest_movment)
            latest_movment = block

    return new_snake, coords
    
def handle_collision(snake, x_coord, y_coord):
    apple = pygame.Rect(x_coord, y_coord, snake_size, snake_size)
    for block in snake:
        if apple.colliderect(block):
            return True
    return False

def main():
    snake = []
    clock = pygame.time.Clock()
    apple = True
    coords = None

    while True:
        #clock.tick_busy_loop(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
     
        if apple:
            x_coord = randrange(0, width, snake_size)
            y_coord = randrange(0, height, snake_size)
            apple = False
            if not coords:
                snake.append(pygame.Rect(width//2, height//2, snake_size, snake_size))
            else:
                snake.append(pygame.Rect(snake[0].x+coords[0], snake[0].y+coords[1], snake_size, snake_size))

        pygame.draw.circle(win, green, (x_coord + (snake_size//2), y_coord + (snake_size//2)), snake_size//2)
        snake, coords = move_snake(snake, x_coord, y_coord)
        apple = handle_collision(snake, x_coord, y_coord)
        draw_snake(snake)
        draw_border()
        pygame.display.update()
        win.fill(black)   
        print(len(snake))

if __name__ == '__main__':
    main()

