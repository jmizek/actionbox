# ========================================================
# .--.   ,.  ,--. ----- , ,--.  ;.  ,  ;-.  ,--. . ,  .--.
# ||||  /_\ /      /   / /   ) / \ /  /_ / /   ) }{   ||||
# '--' /  \ \__,  /   /  \__/ /  \/  /__)  \__/ / \   '--'
# ========================================================
# 
# Actionbox - Mario edition
#
# Controls:
# 	Left/right arrow keys = Move AB left and right
#	Up arrow key = Make AB jump when on the ground
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
gravity = 1 #acceleration due to gravity
terminal_velocity = 9 #max downward speed
max_jump = 5

# This class represents the bar at the bottom that the player controls
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
        
        
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # Set speed vector
    x_speed=0
    y_speed=0
    has_jump=True #has_jump is a boolean that lets the player jump iff True
    jumping=False #jumping is a boolean which indicates that a player has just jumped and not peaked or let go of the key
    jump_duration=0 #jump duration is the length of time for which the player has held the jump key, up to a max value


    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(white)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.x_speed+=x
        self.y_speed+=y
    
    # Move player if necessary
    def update(self,walls):
        # Get the old x position, in case we need to go back to it
        old_x=self.rect.left
        new_x=old_x+self.x_speed
        self.rect.left = new_x
        
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            self.rect.left=old_x #Hit a wall. Go back to the old position

        # Check for surface beneath us
        old_y=self.rect.top # Get the old y position, in case we need to go back to it
        new_y=old_y+1 #Gravity factor
        self.rect.top = new_y
        collide = pygame.sprite.spritecollide(self, walls, False) #check for collision
        if collide: #there's something beneath us
            self.has_jump=True #give jumps back -- maybe need to check if jumping?
            self.rect.top=old_y
            if self.y_speed > 0:
                self.y_speed=0
        else: #nothing beneath us, apply gravity
            self.has_jump=False
            if self.y_speed < terminal_velocity: #have we reached terminal velocity?
                self.y_speed+=gravity #no, go faster

        # If jumping, handle that
        if self.jumping:
            if self.jump_duration < max_jump:
                self.jump_duration+=1
                self.y_speed-=(max_jump-self.jump_duration)
            else: #reached max_jump, stop jumping
                self.jumping=False

        if  self.y_speed>0:
            for i in range(0, self.y_speed):
                old_y=self.rect.top # Get the old y position, in case we need to go back to it
                new_y=old_y+1
                self.rect.top = new_y
                # Did this update cause us to hit a wall?
                collide = pygame.sprite.spritecollide(self, walls, False)
                if collide:
                    self.rect.top=old_y # Hit a wall. Go back to the old position
        elif self.y_speed<0:        
            for i in range(self.y_speed, 0):
                old_y=self.rect.top # Get the old y position, in case we need to go back to it
                new_y=old_y-1
                self.rect.top = new_y
                # Did this update cause us to hit a wall?
                collide = pygame.sprite.spritecollide(self, walls, False)
                if collide:
                    self.rect.top=old_y # Hit a wall. Go back to the old position
            
score = 0
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 500])

# Set the title of the window
pygame.display.set_caption('ActionBox - Mario')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

# Create the player paddle object
player = Player( 50,50 )
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
            if event.key == pygame.K_UP and player.has_jump: 
                player.changespeed(0,-3)
                player.has_jump=False
                player.jumping=True
                player.jump_duration=0
                    
            #if event.key == pygame.K_DOWN:
                #player.changespeed(0,3)
                
        if event.type == pygame.KEYUP: #releasing a key
            if event.key == pygame.K_LEFT:
                player.changespeed(3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3,0)
            if event.key == pygame.K_UP and player.jumping:
                player.jumping=False
                
            #if event.key == pygame.K_DOWN:
                #player.changespeed(0,-3)
                
    player.update(wall_list)
    
    screen.fill(black)
    
    movingsprites.draw(screen)
    wall_list.draw(screen)
    pygame.display.flip()

    clock.tick(40)
            
pygame.quit()
