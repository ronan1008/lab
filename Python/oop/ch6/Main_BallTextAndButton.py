import pygame
from pygame.locals import *
import sys
import random
from Ball import *
from SimpleText import *
from SimpleButton import *

# BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

def myCallBackFunction():
    print('User pressed Button B, called myCallBackFunction')

class CallBackTest():
    def __init__(self):
        pass
    def myMethod(self):
        print('User pressed Button C, called myMethod of the CallBackTest object')

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

oCallBackTest = CallBackTest()

oButtonA = SimpleButton(window, (25, 30), 'images/buttonAUp.png', 'images/buttonADown.png')
oButtonB = SimpleButton(window, (150, 30), 'images/buttonBUp.png', 'images/buttonBDown.png',callBack = myCallBackFunction)
oButtonC = SimpleButton(window, (275, 30), 'images/buttonCUp.png', 'images/buttonCDown.png',callBack = oCallBackTest.myMethod)


# oBall = Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT)
# oFrameCountLabel = SimpleText(window, (60, 20), 'Program has run through this many loops: ', WHITE)
# oFrameCountDisplay = SimpleText(window, (500, 20), '', WHITE)
# oRestartButton = SimpleButton(window, (280, 60), 'images/restartup.png', 'images/restartDown.png')


# frameCounter = 0
counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if oButtonA.handleEvent(event):
            print('User pressed button A, handled in the main loop')

        oButtonB.handleEvent(event)
        oButtonC.handleEvent(event)

    counter = counter + 1
    window.fill(GRAY)

    oButtonA.draw()
    oButtonB.draw()
    oButtonC.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if oRestartButton.handleEvent(event):
#             frameCounter = 0

#     oBall.update()
#     frameCounter = frameCounter + 1
#     oFrameCountDisplay.setValue(str(frameCounter))
#     window.fill(BLACK)
#     oBall.draw()
#     oFrameCountLabel.draw()
#     oFrameCountDisplay.draw()
#     oRestartButton.draw()

#     pygame.display.update()
#     clock.tick(FRAMES_PER_SECOND)