# dataclass likes a named tuple, but it is mutable and has default value
from dataclasses import dataclass
import pygame # all the available pygame modules
from pygame.locals import * # for some helpful constants and functions
import random

# constants
TITLE = "貪吃蛇"
WIDTH = 800
HEIGHT = 600
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
speed = 5
arrows = [K_UP, K_DOWN, K_LEFT, K_RIGHT] # key arrows
score = 0
bean = Position(
        random.randrange(0, WIDTH - SIZE_UNIT, SIZE_UNIT),
        random.randrange(0, HEIGHT - SIZE_UNIT, SIZE_UNIT))
snake = []
    
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
        x = random.randrange(0, WIDTH - SIZE_UNIT, SIZE_UNIT)
        y = random.randrange(0, HEIGHT - SIZE_UNIT, SIZE_UNIT)
        if Position(x, y) not in snake: # do not overlap with snake body
            break
    
    bean = Position(x, y)

def eat_bean(pos):
    if pos.x == bean.x and pos.y == bean.y:
        update_bean()
        return True
    
    return False   

def update_snake(key=-1):
    global prev_key
    
    curr_pos = snake[0]

    # not in reverse direction
    if (key == K_DOWN and prev_key != K_UP) or \
        (key == K_UP and prev_key != K_DOWN) or \
        (key == K_LEFT and prev_key != K_RIGHT) or \
        (key == K_RIGHT and prev_key != K_LEFT):
        
        # update next position
        next_x = curr_pos.x + direction[key].x
        next_y = curr_pos.y + direction[key].y
        next_pos = Position(next_x, next_y)
        snake.insert(0, next_pos)
        
        prev_key = key # update previous pressed key
    else:
        # update next position
        next_x = curr_pos.x + direction[prev_key].x
        next_y = curr_pos.y + direction[prev_key].y
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
    pygame.draw.rect(screen, GREEN,
                     pygame.Rect(bean.x, bean.y, SIZE_UNIT, SIZE_UNIT))

def check_fail():
    if snake[0] in snake[1:]: # snake head overlap with body
        return True

    # collide with wall
    if snake[0].x < 0 or \
        snake[0].x > WIDTH or \
        snake[0].y < 0 or \
        snake[0].y > HEIGHT:
        return True
    
    return False

pygame.image.load(ICON)
pygame.display.set_caption(TITLE) # set screen title
# snake first position
snake.insert(0, Position(
                random.randrange((WIDTH // 4), (WIDTH // 4)*3, SIZE_UNIT),
                random.randrange((HEIGHT // 4), (HEIGHT // 4)*3, SIZE_UNIT)))

while running: # game loop
    has_update = False
    clock.tick(speed) # every second at most q frames should pass
    
    for e in pygame.event.get(): # get events from the queue
        if e.type == pygame.QUIT: # if close botton is pressed
            running = False
        
        elif e.type == pygame.KEYDOWN: # if key is pressed down
            if e.key in arrows and not has_update:
                update_snake(e.key)
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