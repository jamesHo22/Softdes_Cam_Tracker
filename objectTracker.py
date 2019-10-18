#MARK: Imports
import pygame
#initalize pygame
pygame.init()


#MARK: Window setup
#create the pygame window of the designated size
window = pygame.display.set_mode((640,480))
#create a surface (layer) the same size as the window to draw the background on
background = pygame.Surface(window.get_size())
#paint the background black
background.fill((0,0,0))
#optimize the surface in memory so it is faster to draw
#use convert_alpha() if the surface has transparency
background = background.convert()
#blit (draw) the background surface to the window so that the upper left corner
#is at screen coord (0,0)
window.blit(background, (0,0))

#MARK: Runtime Variables
mainLoop = True
FPS = 60

#MARK: gameLoop
while mainLoop:

    #MARK: event listeners
    for event in pygame.event.get():

        #checks for the x in the corner
        if event.type == pygame.QUIT:
            #stop looping
            mainLoop = False

        #listens for key presses
        elif event.type == pygame.KEYDOWN:

            #excape keypress
            if event.key == pygame.K_ESCAPE:
                #stop looping
                mainLoop = False

    #update the display
    pygame.display.flip()

#quit the program and close the window
pygame.quit()
