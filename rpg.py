# ========================================================
# .--.   ,.  ,--. ----- , ,--.  ;.  ,  ;-.  ,--. . ,  .--.
# ||||  /_| /      /   / /   ) / \ /  /_ / /   ) }{   ||||
# '--' /  | \__,  /   /  \__/ /  \/  /__)  \__/ / \   '--'
# ========================================================
# 
# Actionbox - RPG edition
#
# Controls:
# 	Left/right/up/down arrow keys = Move AB
#	??? key = Make AB talk
#
#

## Original code:
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
## Modifications by jmizek

import pygame

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

# This class represents an area that the player cannot pass over
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(blue)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This class the player's sprite, Actionbox
class Player(pygame.sprite.Sprite):

    # Set speed vector
    x_speed=0
    y_speed=0
    x_left=False
    y_down=True

    # Constructor function
    def __init__(self,x,y,filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(white) 

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.x_speed+=x
        self.y_speed+=y

    # Change the player's sprite to match the direction of movement
    def change_sprite(self):
        if abs(self.x_speed)>abs(self.y_speed):
            if self.x_speed<0:
                self.image = pygame.image.load("arrow_l.png").convert()
            elif self.x_speed>0:
                self.image = pygame.image.load("arrow_r.png").convert()
        elif abs(self.x_speed)<abs(self.y_speed):
            if self.y_speed<0:
                self.image = pygame.image.load("arrow_u.png").convert()
            elif self.y_speed>0:
                self.image = pygame.image.load("arrow_d.png").convert()
            
        
    # Move player if necessary
    def update(self,walls):
        if self.x_speed>0: # Are we moving right?
            for i in range(0, self.x_speed): # evaluate potential collision one pixel at a time
                self.rect.left+=1
                if pygame.sprite.spritecollide(self, walls, False): # Did this update cause us to hit a wall?
                    self.rect.left-=1 # Hit a wall. Go back to the old position
        elif self.x_speed<0: # Are we moving left?
            for i in range(self.x_speed, 0): # evaluate potential collision one pixel at a time
                self.rect.left-=1
                if pygame.sprite.spritecollide(self, walls, False): # Did this update cause us to hit a wall?
                    self.rect.left+=1 # Hit a wall. Go back to the old position
                    
        if self.y_speed>0: # Are we moving down?
            for i in range(0, self.y_speed): # evaluate potential collision one pixel at a time
                self.rect.top+=1
                if pygame.sprite.spritecollide(self, walls, False): # Did this update cause us to hit a wall?
                    self.rect.top-=1 # Hit a wall. Go back to the old position
        elif self.y_speed<0: # Are we moving up?
            for i in range(self.y_speed, 0): # evaluate potential collision one pixel at a time
                self.rect.top-=1
                if pygame.sprite.spritecollide(self, walls, False): # Did this update cause us to hit a wall?
                    self.rect.top+=1 # Hit a wall. Go back to the old position

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 500])

# Set the title of the window
pygame.display.set_caption('ActionBox - RPG')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

# Create the player sprite
player = Player( 50,50,"arrow_d.png")
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(player)

# Make the walls. (x_pos, y_pos, width, height)
wall_list=pygame.sprite.RenderPlain()
wall=Wall(0,0,10,500)
wall_list.add(wall)
wall=Wall(10,0,790,10)
wall_list.add(wall)
wall=Wall(10,180,100,10)
wall_list.add(wall)
wall=Wall(10,490,790,10)
wall_list.add(wall)
wall=Wall(790,10,10,490)
wall_list.add(wall)

clock = pygame.time.Clock()

done = False

while done == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.KEYDOWN: #pressing a key
            if event.key == pygame.K_LEFT:
                player.changespeed(-3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(3,0)
            if event.key == pygame.K_UP: 
                player.changespeed(0,-3)
            if event.key == pygame.K_DOWN: 
                player.changespeed(0,3)
                
        if event.type == pygame.KEYUP: #releasing a key
            if event.key == pygame.K_LEFT:
                player.changespeed(3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3,0)
            if event.key == pygame.K_UP: 
                player.changespeed(0,3)
            if event.key == pygame.K_DOWN: 
                player.changespeed(0,-3)
                
    player.update(wall_list)

    player.change_sprite()
    
    screen.fill(black)
    
    movingsprites.draw(screen)
    wall_list.draw(screen)
    pygame.display.flip()

    clock.tick(40)
            
pygame.quit()
