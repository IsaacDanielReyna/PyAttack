import pygame
import sys
from GameObject import *
from Controls import *
from level1_intermission import *
from level3 import *
from gameover import *

#INITIALIZE PYGAME AND DECLARE VARIABLES
pygame.init()
pygame.mixer.pre_init( 44100, -16, 2 )
#screen = pygame.display.set_mode((1366,768), pygame.FULLSCREEN | pygame.HWSURFACE)
screen = pygame.display.set_mode((1280,720))
score = None
lives = None
cont_level = None
dead = None

while True:
    #DISPALY THE CONTROLS
    controls(screen)

    #INITIALIZE VARIABLES TO ALLOW GAMEPLAY
    cont_level = True
    dead = [False]
    
    #LEVEL 1
    while cont_level == True:
        #INITIALIZE SCORE AND LIVES AND PROCEED TO LEVEL 1
        score = [0]
        lives = [3]
        level1(screen, score, lives, dead)

        #PLAYER DIED; ASK IF THEY WANT TO CONTINUE AND SAVE THEIR ANSWER
        #IF THEY WANT TO CONTINUE, GO BACK TO THE BEGINNING OF THE LEVEL
        if dead[0] == True:
        #    cont_level = gameover(screen)
        #    dead[0] = False
            break
            #cont_level = gameover(screen)
            #dead[0] = False
            break
        #IF THEY DO NOT WANT TO CONTINUE, GO BACK TO THE TITLE SCREEN

        #if cont_level == False:   
        #   break
        #if cont_level == False:   
           # break
        
