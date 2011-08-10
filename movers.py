# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import pygame

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

# This class represents the pits around the edge of the screen
class Pit(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a black pit, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(black)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
        
# This class represents the movers placed by the mover
class Mover(pygame.sprite.Sprite):

    # Set speed vector
    change_x=0
    change_y=0

    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.Surface([32, 32]) #sprite limited in size?
        self.image.fill(blue)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
    
    # Change the speed of the mover
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
        
    # Find a new position for the mover
    def update(self,pits):
        # Get the old position, in case we need to go back to it
        old_x=self.rect.left
        new_x=old_x+self.change_x
        self.rect.left = new_x
        
        # Did this update cause us to hit a pit?
        collide = pygame.sprite.spritecollide(self, pits, False)
        if collide:
            # Whoops, hit a pit. Go back to the old position
            self.rect.left=old_x

        old_y=self.rect.top
        new_y=old_y+self.change_y
        self.rect.top = new_y
        
        # Did this update cause us to hit a pit?
        collide = pygame.sprite.spritecollide(self, pits, False)
        if collide:
            # Whoops, hit a pit. Go back to the old position
            self.rect.top=old_y

            
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 500])

# Set the title of the window
pygame.display.set_caption('Test')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(white)

# Create the mover paddle object
mover = Mover( 50,50 )
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(mover)

# Make the pits. (x_pos, y_pos, width, height)
pit_list=pygame.sprite.RenderPlain()
pit=Pit(0,0,32,500)
pit_list.add(pit)
pit=Pit(10,0,790,32)
pit_list.add(pit)
pit=Pit(10,200,100,32)
pit_list.add(pit)

clock = pygame.time.Clock()

done = False

while done == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mover.changespeed(-3,0)
            if event.key == pygame.K_RIGHT:
                mover.changespeed(3,0)
            if event.key == pygame.K_UP:
                mover.changespeed(0,-3)
            if event.key == pygame.K_DOWN:
                mover.changespeed(0,3)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mover.changespeed(3,0)
            if event.key == pygame.K_RIGHT:
                mover.changespeed(-3,0)
            if event.key == pygame.K_UP:
                mover.changespeed(0,3)
            if event.key == pygame.K_DOWN:
                mover.changespeed(0,-3)
                
    mover.update(pit_list)
    
    screen.fill(white)
    
    movingsprites.draw(screen)
    pit_list.draw(screen)
    pygame.display.flip()

    clock.tick(40)
            
pygame.quit()
