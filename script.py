import pygame
from random import randrange

width, height = 1300, 700 # HINT: width and height must be divisable by snake_size


black = (0, 0, 0)
white = (255, 255, 255)
green = (50,205,50)
red = (255, 0, 0)

snake_size = 25
fps = 5
offset_width = width//snake_size
offset_height = height//snake_size

assert width%snake_size == 0 and height%snake_size == 0, 'width and height should be divisible by snake_size'

win = pygame.display.set_mode((width+offset_width, height+offset_height))
pygame.display.set_caption("Snake AI")

def draw_snake(snake):
    for rect in snake:
        pygame.draw.rect(win, green, rect)  

def draw_border():
    for i in range(width//snake_size+offset_width):
        pygame.draw.line(win, white, (snake_size*i, 0), (snake_size*i, height+offset_height), 1)

    for i in range(height//snake_size+offset_height):
        pygame.draw.line(win, white, (0, snake_size*i), (width+offset_width, snake_size*i), 1)

def move_snake(snake, offset):
    new_snake = []
    for rect in snake:
        new_snake.append(rect.move(offset[0], offset[1]))
    return new_snake


def main():
    snake = [pygame.Rect(width//2, height//2, snake_size, snake_size)]
    offset = (0, -snake_size)
    clock = pygame.time.Clock()
    apple = True

    while True:
        clock.tick_busy_loop(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
     
        if apple:
            x_coord = randrange(0, width, 25)
            y_coord = randrange(0, height, 25)
            apple = False
        
        pygame.draw.circle(win, green, (x_coord + (snake_size//2), y_coord + (snake_size//2)), snake_size//2)
        draw_snake(snake)
        snake = move_snake(snake, offset)
        draw_border()
        pygame.display.update()
        win.fill(black)   

if __name__ == '__main__':
    main()

