# 1 - Import packages
import pygame
from pygame.locals import *
from SimpleButton import *
import sys

# Define constants
GRAY = (200, 200, 200)
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 100
FRAMES_PER_SECOND = 30

# 2 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

oButtonA = SimpleButton(window, (25, 30), 'images/buttonAUp.png', 'images/buttonADown.png')
oButtonB = SimpleButton(window, (150, 30), 'images/buttonBUp.png', 'images/buttonBDown.png')
oButtonC = SimpleButton(window, (275, 30), 'images/buttonCUp.png', 'images/buttonCDown.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if oButtonA.handleEvent(event):
            print('User has clicked the button A')
        if oButtonB.handleEvent(event):
            print('User has clicked the button B')
        if oButtonC.handleEvent(event):
            print('User has clicked the button C')
    window.fill(GRAY)
    oButtonA.draw()
    oButtonB.draw()
    oButtonC.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)