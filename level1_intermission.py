import pygame
import sys

def level1_intermission(screen):
    #DISPLAY INFORMATION
    font = pygame.font.SysFont("Impact Regular", 72)
    font2 = pygame.font.SysFont("Impact Regular", 36)
    level = font.render("Level 1", True, (255, 255, 255))
    prompt = font2.render("Press ENTER to begin", True, (255, 255, 255))

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
        screen.blit(level,((screen.get_width() - level.get_width())/2, screen.get_height()/2 - level.get_height()))
        screen.blit(prompt,((screen.get_width() - prompt.get_width())/2, screen.get_height()/2))
        pygame.display.flip()
