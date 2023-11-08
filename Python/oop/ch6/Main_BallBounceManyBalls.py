import pygame
from pygame.locals import *
import sys
import random
from Ball import *

BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
N_BALLS = 3

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

ballList = []

for oBall in range(0, N_BALLS):
    oBall = Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT)
    ballList.append(oBall)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for oBall in ballList:
        oBall.update()

    window.fill(BLACK)
    for oBall in ballList:
        oBall.draw()
    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)