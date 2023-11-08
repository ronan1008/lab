import pygame
from pygame.locals import *

class SimpleButton():
    STATE_IDLE = 'idle'
    STATE_ARMED = 'armed'
    STATE_DISARMED = 'disarmed'

    def __init__(self, window, loc, up, down, callBack=None):
        self.window = window
        self.loc = loc
        self.surfaceUP = pygame.image.load(up)
        self.surfaceDown = pygame.image.load(down)
        self.callBack = callBack
        self.rect = self.surfaceUP.get_rect()
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]

        self.state = SimpleButton.STATE_IDLE

    def handleEvent(self, eventObj):
        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return False

        eventPointButtonRect = self.rect.collidepoint(eventObj.pos)

        if self.state == SimpleButton.STATE_IDLE:
            if ( eventObj.type == MOUSEBUTTONDOWN ) and eventPointButtonRect:
                self.state = SimpleButton.STATE_ARMED
        elif self.state == SimpleButton.STATE_ARMED:
            if ( eventObj.type == MOUSEBUTTONUP ) and eventPointButtonRect:
                self.state = SimpleButton.STATE_IDLE
                if self.callBack != None:
                    self.callBack()
                return True
            if ( eventObj.type == MOUSEMOTION ) and (not eventPointButtonRect) :
                self.state = SimpleButton.STATE_DISARMED
        elif self.state == SimpleButton.STATE_DISARMED:
            if eventPointButtonRect:
                self.state = SimpleButton.STATE_ARMED
            elif eventObj.type == MOUSEBUTTONUP:
                self.state = SimpleButton.STATE_IDLE
        return False

    def draw(self):
        if self.state == SimpleButton.STATE_ARMED:
            self.window.blit(self.surfaceDown, self.loc)
        else:
            self.window.blit(self.surfaceUP, self.loc)