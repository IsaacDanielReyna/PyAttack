import pygame
import math
import random

class vector2:
    def __init__( self, x=0, y=0 ):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def xy( self ):
        return (self.x,self.y)

    def add( self, v2 ):
        result = vector2()
        result.x = self.x + v2.x
        result.y = self.y + v2.y
        return result

    def sub( self, v2 ):
        result = vector2()
        result.x = self.x - v2.x
        result.y = self.y - v2.y
        return result

    def scale( self, s ):
        result = vector2()
        result.x = self.x * s
        result.y = self.y * s
        return result

    def mag( self ):
        return math.sqrt( self.x * self.x + self.y * self.y )
   
    def normalized( self ):
        result = vector2()
        m = self.mag()
        if m == 0:
            return vector2( 0, 0 )
        result.x = self.x / m
        result.y = self.y / m
        return result
        
class GameObject:
    # Constructor: If values are not passed, the following values are assigned.
    def __init__( self, image=None, x=None, y=None,  ):

        # If Object's position isn't passed, then it's position will be random.
        if x == None:
            self.x = random.randrange(0, pygame.display.get_surface().get_width() )
        else:
            self.x=x
            
        if y == None:
            self.y = random.randrange(0, pygame.display.get_surface().get_height() )
        else:
            self.y=y
        
        # If the Image is not found or not passed, then set image_not_found.png
        try:
            self.image = pygame.image.load( image ).convert_alpha()
        except Exception:
            self.image = pygame.image.load( "Resources/Images/image_not_found.png" ).convert_alpha()

        #RICs
        self.pos = vector2(self.x, self.y)
        #self.center = self.image_center
        
        self.vel = vector2(0, 0)
        self.SPEED = 0.4
        self.delta = 0
        # For local storage?
        self.random = 0
        self.angle = 0
        self.circularSpeed = 0

        
        # IMAGE MANIPULATION
        self.graphic = self.image
        self.rot_rect = self.graphic.get_rect()
        self.rotated = False
                
        # ANIMATION
        self.animated = False
        self.frame_timer = 0  # init time?
        self.FPS = 1000
        self.ANIMATIONS = 1
        self.ANIMATION = 0
        self.FRAMES = 1
        self.FRAME = 0
        self.start_time = pygame.time.get_ticks()
        self.img_top = 0
        self.clip = None

        # GET IMAGE DIMENSIONS
        size = self.image.get_rect().size
        self.image_width = size[0]
        self.image_height = size[1]
        self.image_center = (self.image_width/2 +self.x, self.image_height/2 + self.y)

        self.width = self.image_width
        self.height = self.image_height
        self.center = (self.width/2, self.height/2)

        # SHOOTING
        self.target = vector2(0,0)
        self.beamImage = None
        self.fireTimer = 0
        self.ammoClipSize = 0
        self.ammo = 0
        self.fireRate = 1000
        self.reloadRate = 1000
        self.safetyDelay = 1000
        self.safety = True

        # PATHS
        self.waypoints = []
        self.wpindex = 0

    def setBeam(self, image_path, sound_path, speed=0.5):
        self.sound = pygame.mixer.Sound( sound_path )
        self.sound.set_volume(0.6)
        self.beamImage =  image_path
        self.beamSpeed = speed
    
    def setExplosion(self, image_path, sound_path):
        self.explosion = pygame.mixer.Sound( sound_path )
        self.sound.set_volume(1.0)
        self.explosionImage = image_path
        
    def explode(self):
        self.explosion.play()
        tmp = GameObject(self.explosionImage, self.pos.x, self.pos.y)
        tmp.has_animation(1, 16, 75)
        tmp.target = self.target
        tmp.SPEED = 0.1
        return tmp
    

    
    # IF TRUE, OBJECT WILL ANIMATE WHILE DURING BLIT
    def has_animation(self, animations, frames, fps, isAnimated=True):
        self.ANIMATIONS = animations
        self.FRAMES = frames
        self.FPS = fps
        self.animated = isAnimated
        self.width = self.image_width/self.FRAMES
        self.height = self.image_height/self.ANIMATIONS

    def updateDelta(self):
        self.delta = pygame.time.get_ticks() - self.start_time
        self.start_time = pygame.time.get_ticks()

        
    # Each column is a frame from one animation. Each row is an animation made up of frames.
    def frame(self):
        if self.FRAME != -1:
            if self.frame_timer > self.FPS:
                self.frame_timer -= self.FPS
                self.FRAME = (self.FRAME + 1) % self.FRAMES
            self.frame_timer += self.delta
        self.clip = pygame.Rect( self.width*self.FRAME, self.height*self.ANIMATION, self.width, self.height )
        return self.clip

    # Enemy fires
    def shoot(self, b):
        self.fireTimer += self.delta
        if self.fireTimer > self.safetyDelay:
            #self.fireTimer -= self.safetyDelay
            
            if self.ammo > 0:
                if self.fireTimer > self.fireRate:
                    self.fireTimer -= self.fireRate
                    self.sound.play()
                    tmp = GameObject(self.beamImage, 10, 10)
                    tmp.has_animation(1, 3, 50)
                    tmp.pos.x = self.pos.x + self.width/4
                    tmp.pos.y = self.pos.y + self.height/2 + 20
                    tmp.target = self.target
                    tmp.SPEED = self.beamSpeed
                    b.append(tmp)
                    self.ammo -= 1
            else:
                if self.fireTimer > self.reloadRate:
                    self.fireTimer -= self.reloadRate
                    self.ammo = self.ammoClipSize

    # Player Fires            
    def player_shoot(self,b):
        self.sound.play()
        tmp = GameObject(self.beamImage, 0, 0)
        tmp.has_animation(1, 3, 50)
        tmp.pos.x = self.pos.x + self.width/2 - 25
        tmp.pos.y = self.pos.y
        tmp.target = vector2(tmp.pos.x , 0 - tmp.height)
        tmp.SPEED = self.beamSpeed
        b.append(tmp)
        
    def blit(self):
        self.updateDelta()
        s = pygame.display.get_surface()
        if self.rotated == True:
            s.blit(self.graphic, (self.pos.x, self.pos.y))
        else:
            s.blit(self.graphic, (self.pos.x, self.pos.y), self.frame())

    def move(self, delta):
        self.target = vector2(self.pos.x + self.width/2, 0)
        self.updateVel(delta)
        self.pos = self.pos.add( self.vel.scale( delta ) )
        
    def move_to(self):
        displacement = self.target.sub(self.pos)
        direction = displacement.normalized()
        velocity = direction.scale(self.SPEED)
        step = velocity.scale(self.delta)
        
        # prevent overshooting (causes jitter back and forth)
        if step.mag() > displacement.mag():
            #self.pos = self.target
            #self.target = None
            self.wpindex +=1
        else:
            # otherwise update position by adding step
            #self.pos = self.pos.add(step)
            pass
            
        self.pos = self.pos.add(step)
        self.target = self.target.add(step)


    def paths(self):
        if len(self.waypoints) == self.wpindex:
            self.wpindex = 0
        self.target = self.waypoints[self.wpindex]
        """
        if reached_waypoint
            index+=1
            if len(waypoints) == index
                index = 0
        """
        pass

    def update(self):
        #self.move_to()
        #self.shoot()
        #self.blit()
        #self.blit()
        pass
        
    #face target
    def face_target(self, target=None):
        if target == None:
            target = self.target
            self.rotated = True
            dx = target.x - self.pos.x
            dy = target.y - self.pos.y
            rads = math.atan2(-dy,dx)
            rads %=2*math.pi
            angle = math.degrees(rads)
            tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            tmp.blit(self.image, (0, 0), self.frame() )
            orig_rect = tmp.get_rect()
            rot_image = pygame.transform.rotate(tmp, angle-90)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            self.graphic = rot_image
    


    def chase_target(self, target, delta):
        displacement = target.sub(self.pos)
        direction = displacement.normalized()
        velocity = direction.scale(self.SPEED)
        step = velocity.scale(delta)
        if step.mag() > displacement.mag():
            self.pos = target
        else:
            self.pos = self.pos.add(step)

    def setTarget(self, target):
        self.target = target
    


    def getRect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        
    def collide(self, target):
        if self.getRect().colliderect(target.getRect()) == 1:
            tmp1 = pygame.Surface( (self.width,self.height), pygame.SRCALPHA )
            tmp1.blit( self.image, (0,0), self.clip )
            
            tmp2 = pygame.Surface( (target.width,target.height), pygame.SRCALPHA )
            tmp2.blit( target.image, (0,0), target.clip )
            
            m1 = pygame.mask.from_surface( tmp1 )
            m2 = pygame.mask.from_surface( tmp2 )

            if m1.overlap( m2, (int(target.pos.x-self.pos.x), int(target.pos.y-self.pos.y) )) is not None:
                return 1
        
    def updateVel(self, delta):
        x_input = 0
        y_input = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_input -= 1.25
        if keys[pygame.K_RIGHT]:
            x_input += 1.25
        if keys[pygame.K_UP]:
            y_input -= 1.25
        if keys[pygame.K_DOWN]:
            y_input += 1.25
        
        # X-INPUT
        if x_input != 0:
            self.vel.x = x_input * self.SPEED
        elif self.vel.x > 0:
            self.vel.x = self.vel.x - 0.05 * delta
            if self.vel.x < 0:
                self.vel.x = 0
        elif self.vel.x < 0:
            self.vel.x = self.vel.x + 0.05 * delta
            if self.vel.x > 0:
                self.vel.x = 0

        # Y-INPUT
        if y_input != 0:
            self.vel.y = y_input * self.SPEED
        elif self.vel.y > 0:
            self.vel.y = self.vel.y - 0.06 * delta
            if self.vel.y < 0:
                self.vel.y = 0
        elif self.vel.y < 0:
            self.vel.y = self.vel.y + 0.06 * delta
            if self.vel.y > 0:
                self.vel.y = 0

    def checkBounds(self, boundary):
        if self.pos.y < boundary.top:
            self.pos.y = 0
            self.vel.y = 0
        elif self.pos.y > boundary.bottom - self.height:
            self.pos.y = boundary.bottom - self.height
            self.vel.y = 0
        if self.pos.x < boundary.left:
            self.pos.x = boundary.left
            self.vel.x = 0
        elif self.pos.x > boundary.right - self.width:
            self.pos.x = boundary.right - self.width
            self.vel.x = 0  

    def checkBounds2(self, boundary):
        if self.pos.y > boundary.bottom + self.height:
            self.pos.y = boundary.top - self.height
            self.wpindex = 0

    def outsideBoundary(self, boundary):
        if (self.pos.y < boundary.top - self.height
        or self.pos.y > boundary.bottom
        or self.pos.x < boundary.left - self.width
        or self.pos.x > boundary.right):
            return True
        else:
            return False


        
    def moveCircular(self, horizontally=0, vertically=0, t=0.01):
        self.pos.x = (int) (self.image_center[0] - horizontally * math.sin(self.circularSpeed) )
        self.pos.y = (int) (self.image_center[1] + vertically * math.cos(self.circularSpeed) )
        self.circularSpeed += t

    def moveCircular2(self, horizontally=0, vertically=0, t=0.01):
        self.pos.x = (int) (127 - horizontally * math.sin(self.circularSpeed) )
        self.pos.y = (int) (0 + vertically * math.cos(self.circularSpeed) )
        self.circularSpeed += t
        
