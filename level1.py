import pygame
import sys
import math
from GameObject import *

def level1(window, score, lives, dead):
    pygame.mixer.music.load( "Resources/Sound/bgm01.wav" )
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    boundary = window.get_rect()
    font = pygame.font.Font("Resources/Fonts/HIGHSPEED.TTF", 72)
    font2 = pygame.font.Font("Resources/Fonts/HIGHSPEED.TTF", 36)
    start_time = pygame.time.get_ticks()
    ################## INITIALIZE OBJECTS ##################
    #For temoporary invincibility when player respawns after death
    invincibility_start = 0
    tmp_invincible = False
    #Messages
    message = GameObject("Resources/Images/message-enemies_cleared.png", boundary.width/2 - 500/2, boundary.height/2 - 250/2)
    message2 = GameObject("Resources/Images/gameover.png", boundary.width/2 - 500/2, boundary.height/2 - 250/2)
    #BACKGROUNDS
    backgrounds = []
    backgrounds.append(GameObject("Resources/Images/bg03.jpg", -(1920/2+320), -(1080/2+200)))
    backgrounds.append(GameObject("Resources/Images/bg01.png", -(1920/2+320), -(1080/2+200)))
    backgrounds.append(GameObject("Resources/Images/bg02.png", -(1920/2+320), -(1080/2+200)))


    #PLAYERS
    #A function is needed in order to add a non-reference object to the players list
    def spawn_player():
        tmp = GameObject("Resources/Images/ship04-animated.png", boundary.width/2 -100, boundary.bottom -100)
        tmp.has_animation(2, 2, 50)
        tmp.setBeam("Resources/Images/beam01-small.png", "Resources/Sound/beam01.wav", 1)
        tmp.setExplosion("Resources/Images/explosion01.png",  "Resources/Sound/explosion01.wav")
        tmp.fireRate = 0
        tmp.reloadRate = 0
        tmp.ammo = 1
        tmp.ammoClipSize = 1
        return tmp

    players = []
    for x in range(0, 1):
        players.append(spawn_player())


    #ENEMIES
    def enemy_type1(x, y):
        tmp = GameObject("Resources/Images/ship02.png", x, y)
        tmp.SPEED = 0.2
        tmp.setBeam("Resources/Images/beam01-small-purple.png", "Resources/Sound/beam01.wav", 0.3)
        tmp.setExplosion("Resources/Images/explosion01.png",  "Resources/Sound/explosion01.wav")
        tmp.random = random.randrange(10, 350) # I'm using this for circular movement range
        tmp.fireRate = 75
        tmp.reloadRate = 2000
        tmp.ammoClipSize = 2
        for x in range(0, 2):
            tmp.waypoints.append( vector2(100,100) )
            tmp.waypoints.append( vector2(100,200) )
            tmp.waypoints.append( vector2(800,200) )
            tmp.waypoints.append( vector2(800,100) )
        tmp.waypoints.append( vector2(1000,1000) )
        #tmp.SPEED = 0.001
        
        tmp.pos.y -= 720
        return tmp
        
    enemies = []
    tmpPos = 120
    for x in range(0, 12):
        enemies.append(enemy_type1(500, -100 - (tmpPos*x)))

    #Lists of BEAMS and EXPLOSIONS
    beams = []
    enemy_beams = []
    explosions = []
        
    ############################## MAIN LOOP ####################################
    while True:
        ############### CONTROLS ################
        pygame.event.pump()
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                #If player is invincible, they cannot shoot (Remove "and tmp_invincible == False" if we want to allow shooting)
                if len(players) > 0 and tmp_invincible == False:
                    for player in players:
                        player.player_shoot(beams)
                        #print player.ammo
        
        ################## UPDATE ##################
        delta = pygame.time.get_ticks() - start_time
        start_time = pygame.time.get_ticks()
        invincibility_delta = start_time - invincibility_start

        # Once 3 seconds have passed, invinciblity runs out and we go back to the original animation
        if tmp_invincible == True:
            if invincibility_delta > 3000:
                tmp_invincible = False
                players[0].ANIMATION = 0
            
        # Enemy Fire (under-construction)
        for enemy in enemies:
            for player in players:
                enemy.target = player.pos
                enemy.shoot(enemy_beams)

        window.fill( (0,0,0) )
        # BACKGROUNDS
        rot_speed = 0.002
        for i in range(0, len(backgrounds)):
            if i != 0:
                backgrounds[i].moveCircular(100, 100, rot_speed)
                rot_speed *= -1
            backgrounds[i].blit()

        # PLAYER BEAMS: Move, blit, and check boundaries
        for beam in beams:
            beam.move_to()
            beam.blit()
            if beam.outsideBoundary(boundary):
                beams.remove(beam)

                
        # If an enemy collides with a player beam, remove the beam and enemy, and update the score
        for enemy in enemies:
            for beam in beams:
                if enemy.collide(beam) == 1:
                    beams.remove(beam)
                    enemies.remove(enemy)
                    explosions.append(enemy.explode())
                    score.append(score[0] + 100)
                    score.pop(0)
                    break
                    
    ############################

        
        # PLAYERS
        for player in players:
            player.move(delta)
            player.checkBounds(boundary)
            player.blit()

        # ENEMIES
        for enemy in enemies:
            #enemy.pos.y += 1
            enemy.paths()
            enemy.move_to()
            #enemy.move_to(enemy.pos.sub((vector2(0, -1))))
            enemy.checkBounds2(boundary) # returns enemies to top of screen
            """ Instead of returning enemies back to the top of the screen, maybe remove them from the list
                since the player missed their chance to destroy them and get points.
                The way it is now, once the enemies get to the bottom of screen, they all get in a
                column and it is impossible to destroy them"""
            for player in players:
                enemy.face_target(player.pos)
                if tmp_invincible == False:
                    if enemy.collide(player) == 1:
                        explosions.append(enemy.explode())
                        explosions.append(player.explode())
                        enemies.remove(enemy)
                        players.remove(player)
                        lives.append(lives[0] - 1)
                        lives.pop(0)
                    
            enemy.blit()
            
        # ENEMY BEAMS
        for beam in enemy_beams:
            beam.face_target()
            beam.move_to()
            if beam.outsideBoundary(boundary) == True:
                enemy_beams.remove(beam)
            else:
                for player in players:
                    if tmp_invincible == False:
                        if beam.collide(player) == 1:
                            explosions.append(player.explode())
                            enemy_beams.remove(beam)
                            players.remove(player)
                            lives.append(lives[0] - 1)
                            lives.pop(0)
                        
            beam.blit()
    
        # OTHER
        for explosion in explosions:
            explosion.move_to()
            explosion.blit()
            if explosion.FRAME == 15:
                explosions.remove(explosion)
                #Once explosion ends, if player is dead, they respawn with temporary invincibility and a different animation
                if len(players) < 1 and lives[0] != 0:
                    players.append(spawn_player())
                    invincibility_start = pygame.time.get_ticks()
                    players[0].ANIMATION = 1
                    tmp_invincible = True
        #window.blit( img, loc.xy(), area=clip )
            
        #Player wins
        if len(enemies) == 0:
            message.blit()
            #level = 2

        #Player loses
        if lives[0] == 0:
            message2.blit()
            dead.append(True)
            dead.pop(0)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    pygame.mixer.music.stop()
                    return

        #Display how much invincibility time is left
        if tmp_invincible == True: 
            if invincibility_delta < 1000:
                invince_time_left = font.render("3", True, (255, 200, 0))
                window.blit(invince_time_left,(window.get_width()/2 - invince_time_left.get_width(),window.get_height()/2 - invince_time_left.get_height()))
            elif invincibility_delta < 2000:
                invince_time_left = font.render("2", True, (255, 200, 0))
                window.blit(invince_time_left,(window.get_width()/2 - invince_time_left.get_width(),window.get_height()/2 - invince_time_left.get_height()))
            elif invincibility_delta < 3000:
                invince_time_left = font.render("1", True, (255, 200, 0))
                window.blit(invince_time_left,(window.get_width()/2 - invince_time_left.get_width(),window.get_height()/2 - invince_time_left.get_height()))

        #Display the score and the amount of lives left        
        scoretext = font2.render("Score: " + str(score[0]), True, (255, 200, 0))
        livestext = font2.render("Lives: " + str(lives[0]), True, (255, 200, 0))
        window.blit(scoretext,(window.get_width() - scoretext.get_width(),0))
        window.blit(livestext,(0,0))
        """#TEXT TEST
        text = enemies[1].delta
        font = pygame.font.Font("Resources/Fonts/HIGHSPEED.TTF", 60)
        text = str(text)
        RGB = (253, 200, 0)
        textobj = font.render(text, 1, RGB)
        textpos = textobj.get_rect()
        textpos.centerx = window.get_rect().centerx
        window.blit(textobj, textpos)
        """
        pygame.display.flip()

