import pygame
import sys

def gameover(screen):
    #DISPLAY OPTIONS
    font = pygame.font.SysFont("Impact Regular", 72)
    cont_prompt = font.render("Continue? Y/N", True, (255, 255, 255))

    #GET USER INPUT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                return False

        #DRAW TO SCREEN
        screen.fill((0, 0, 0))
        screen.blit(cont_prompt,((screen.get_width() - cont_prompt.get_width())/2, (screen.get_height() - cont_prompt.get_height())/2))
        pygame.display.flip()
        
