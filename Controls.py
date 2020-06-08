import pygame
import sys
from GameObject import *

def controls(screen):
    #BACKGROUNDS
    backgrounds = []
    backgrounds.append(GameObject("Resources/Images/bg03.png", 0, 0))
    backgrounds.append(GameObject("Resources/Images/bg02.png", -(1920/2+320), -(1080/2+200)))
    backgrounds.append(GameObject("Resources/Images/bg01-edited.png", -(1920/2+320), -(1080/2+200)))


    #CONTROLS DISPLAY
    """
    control_bg = pygame.image.load("Resources/Images/control_bg.png").convert_alpha()
    font = pygame.font.SysFont("Impact Regular", 72)
    font2 = pygame.font.SysFont("Impact Regular", 36)
    title = font.render("Tomai Fighter", True, (255, 255, 255))
    control1 = font2.render("W - Move Up", True, (255, 255, 255))
    control2 = font2.render("S - Move Down", True, (255, 255, 255))
    control3 = font2.render("A - Move Left", True, (255, 255, 255))
    control4 = font2.render("D - Move Right", True, (255, 255, 255))
    control5 = font2.render("Space - Shoot Laser", True, (255, 255, 255)) 
    control6 = font2.render("Press ENTER to begin", True, (255, 255, 255))
    control7 = font2.render("Press ESC at any point to close the game", True, (255, 255,255))
    """

    background = pygame.image.load("Resources/Images/TitleControls2.png").convert_alpha()

    #GET USER INPUT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                return

        
        #DRAW TO SCREEN
        screen.fill((0, 0, 0))
        rot_speed = 0.002
        for i in range(0, len(backgrounds)):
            if i != 0:
                backgrounds[i].moveCircular(100, 100, rot_speed)
                rot_speed *= -1
            backgrounds[i].blit()
        """
        screen.blit(control_bg, ((screen.get_width() - control_bg.get_width())/2,(screen.get_height() - control_bg.get_height())/2))
        screen.blit(title,((screen.get_width() - title.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 5))
        screen.blit(control1, ((screen.get_width() - control1.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 105))
        screen.blit(control2, ((screen.get_width() - control2.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 155))
        screen.blit(control3, ((screen.get_width() - control3.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 205))
        screen.blit(control4, ((screen.get_width() - control4.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 255))
        screen.blit(control5, ((screen.get_width() - control5.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 305))
        screen.blit(control6, ((screen.get_width() - control6.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 405))
        screen.blit(control7, ((screen.get_width() - control7.get_width())/2, (screen.get_height() - control_bg.get_height())/2 + 455))
        """
        screen.blit(background,((screen.get_width() - background.get_width())/2,(screen.get_height() - background.get_height())/2))
        pygame.display.flip()

