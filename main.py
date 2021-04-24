# dataclass likes a named tuple, but it is mutable and has default value
from dataclasses import dataclass
import pygame # all the available pygame modules
from pygame.locals import * # for some helpful constants and functions
import random

# constants
TITLE = "貪吃蛇"
WIDTH = 1200
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)
ICON = "assets/icon.png"
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
BLACK = pygame.Color(0, 0, 0)
K_NONE = -1
SIZE_UNIT = 10

# data class
@dataclass
class Position:
    x: int
    y: int

# global variables
running = True
prev_key = K_RIGHT
speed = 0
arrows = [K_UP, K_DOWN, K_LEFT, K_RIGHT] # key arrows
snake = []
score = 0
bean = Position(
        random.randint(0, WIDTH, SIZE_UNIT),
        random.randint(0, HEIGHT, SIZE_UNIT))
    
direction = {
    K_UP: Position(0, -1*SIZE_UNIT),
    K_DOWN: Position(0, SIZE_UNIT),
    K_LEFT: Position(-1*SIZE_UNIT, 0),
    K_RIGHT: Position(SIZE_UNIT, 0),
}

pygame.init() # Initialize all imported pygame modules
print("init done")

screen = pygame.display.set_mode(size=SCREEN_SIZE) # set screen size
clock = pygame.time.Clock() # an object to help track time

def update_bean():
    global bean
    
    while True:
        x = random.randint(0, WIDTH, SIZE_UNIT)
        y = random.randint(0, HEIGHT, SIZE_UNIT)
        if Position(x, y) not in snake: # do not overlap with snake body
            break
    
    bean = Position(x, y)

def eat_bean(pos):
    if pos.x == bean.x and pos.y == bean.y:
        update_bean()
        return True
    
    return False   

def update_snake(key=-1):
    # not in reverse direction
    if (key == K_DOWN and prev_key != K_UP) or
        (key == K_UP and prev_key != K_DOWN) or
        (key == K_LEFT and prev_key != K_RIGHT) or
        (key == K_RIGHT and prev_key != K_LEFT):
        
        # update next position
        curr_pos = snake[0]
        next_x = snake.x + direction[key].x
        next_y = snake.y + direction[key].y
        next_pos = Position(next_x, next_y)
        snake.insert(0, next_pos)
        
        prev_key = key # update previous pressed key
    else:
        # update next position
        next_x = snake.x + direction[prev_key].x
        next_y = snake.y + direction[prev_key].y
        next_pos = Position(next_x, next_y)
        snake.insert(0, next_pos)
        
    if not eat_bean(next_pos):
        del snake[-1] # remove last snake position

def render():
    screen.fill(WHITE) # set screen with white color
    
    # draw snake
    for pos in snake:
        pygame.draw.rect(screen, BLACK,
                         pygame.Rect(pos.x, pos.y, SIZE_UNIT, SIZE_UNIT))
        
    # draw bean
    pygame(screen, GREEN,
           pygame.Rect(bean.x, bean.y SIZE_UNIT, SIZE_UNIT))

def check_fail():
    if snake[0] in snake[1:]: # snake head overlap with body
        return True

    # collide with wall
    if snake[0].x < 0 or
        snake[0].x > WIDTH or
        snake[0].y < 0 or
        snake[0].y > HEIGHT:
        return True
    
    return False

pygame.image.load(ICON)
pygame.display.set_caption(TITLE) # set screen title
clock.tick(5) # every second at most 5 frames should pass

while running: # game loop
    has_update = False
    
    for e in pygame.event.get(): # get events from the queue
        if e.type == pygame.QUIT: # if close botton is pressed
            running = False
        
        else e.type == pygame.KEYDOWN: # if key is pressed down
            if event.key in arrows and not has_update:
                update_snake(event.key)
                has_update = True
        
        if not has_update:
            update_snake()
    
    if check_fail():
        running = False
    else:
        render()
        
    pygame.display.flip() # update the full display Surface to the screen

pygame.quit() # uninitialize all pygame modules
print("quit done")