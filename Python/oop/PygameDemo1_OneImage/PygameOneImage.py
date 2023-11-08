import pygame
from pygame.locals import *
import sys
from pathlib import Path
import random

BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
BALL_WIDTH_HEIGHT = 100
MAX_WIDTH = WINDOW_WIDTH - BALL_WIDTH_HEIGHT
MAX_HEIGHT = WINDOW_HEIGHT - BALL_WIDTH_HEIGHT
TARGET_X = 400
TARGET_Y = 320
TARGET_WIDTH_HEIGHT = 120
N_PIXELS_TO_MOVE = 3

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

ballImage = pygame.image.load('images/ball.png')
targetImage = pygame.image.load('images/target.jpg')

ballX = random.randrange(MAX_WIDTH)
ballY = random.randrange(MAX_HEIGHT)
targetRect = pygame.Rect(TARGET_X, TARGET_Y, TARGET_WIDTH_HEIGHT, TARGET_WIDTH_HEIGHT)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keyPressedTuple = pygame.key.get_pressed()

    if keyPressedTuple[pygame.K_LEFT]:
            ballX = ballX - N_PIXELS_TO_MOVE

    if keyPressedTuple[pygame.K_RIGHT]:
            ballX = ballX + N_PIXELS_TO_MOVE

    if keyPressedTuple[pygame.K_UP]:
            ballY = ballY - N_PIXELS_TO_MOVE

    if keyPressedTuple[pygame.K_DOWN]:
            ballY = ballY + N_PIXELS_TO_MOVE
        # if event.type == pygame.MOUSEBUTTONUP:
        #     mouseX, mouseY = event.pos
        #     if ballRect.collidepoint(event.pos):
        #         ballX = random.randrange(MAX_WIDTH)
        #         ballY = random.randrange(MAX_HEIGHT)
        #         ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)

    ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)

    if ballRect.colliderect(targetRect):
        print('Ball is touching the target')

    window.fill(BLACK)
    window.blit(targetImage, (TARGET_X, TARGET_Y))

    window.blit(ballImage, (ballX, ballY))
    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)