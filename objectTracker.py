#MARK: Imports
import pygame
#initalize pygame
pygame.init()


#MARK: view
class View:
    """A class that handels updates to the user side display."""

    def __init__(self,screenWidth = 600,screenHeight = 600, backgroundColor = (0,0,0)):
        """sets up the view for the program"""

        #initalize the view variables
        self.width = screenWidth
        self.height = screenHeight
        self.backgroundColor = backgroundColor
        self.objects = []
        #sets up the pygame display window
        self.initWindow()

    def initWindow (self):
        """A function which creates a pygame window specified by the properties of the view."""
        #MARK: Window setup
        #create the pygame window of the designated size
        self.window = pygame.display.set_mode((self.width,self.height))
        #create a surface (layer) the same size as the window to draw the background on
        self.background = pygame.Surface(self.window.get_size())
        #paint the background black
        self.background.fill(self.backgroundColor)
        #optimize the surface in memory so it is faster to draw
        #use convert_alpha() if the surface has transparency
        self.background = self.background.convert()

    def draw(self):
        """a method which draws all of the pygame surfaces"""
        self.window.blit(self.background, (0,0))

        for obj in self.objects:
            obj.draw(self)

        #update the display
        pygame.display.flip()

    def addObj(self, obj):


        self.objects.append(obj)

#MARK: controller
class Controller:
    def handleEvent(self,event):
        #checks for the x in the corner
        if event.type == pygame.QUIT:
            #stop looping
            return False
        #listens for key presses
        elif event.type == pygame.KEYDOWN:

            #excape keypress
            if event.key == pygame.K_ESCAPE:
                #stop looping
                return False
            else:
                return True
        else:
            return True

#MARK: Model
class Model:
    pass

class ball:
    """A class which draws a circle on the screen at a given set of cordinates"""
    def __init__(self,view, pos = [300,300],color = (255,0,255),radius = 30):

        #sets personal variables
        self.pos = pos
        self.color = color
        self.radius = radius
        #creates the surface for the ball
        self.surface = pygame.Surface((2*self.radius,2*self.radius))

        #add itself to the view
        view.addObj(self)

    def draw (self,view):
        """This is a method which will display the object to the screen"""

        #draw the circle on to the surface
        pygame.draw.circle(self.surface,self.color,(self.radius,self.radius),self.radius)
        #optimize the surface in memory so it is faster to draw
        self.surface = self.surface.convert_alpha()

        #display the circle
        view.window.blit(self.surface,self.pos)




#create model, view, and controller objects
view = View(640,700)
controller = Controller()
model = Model()

#create the cursor which will follow the user's hand
cursor = ball(view)

#draw the content in the view
view.draw()

#MARK: Runtime Variables
mainLoop = True
FPS = 60

#MARK: gameLoop
while mainLoop:

    #MARK: event listeners
    for event in pygame.event.get():

        #handle events
        mainLoop = controller.handleEvent(event)

    #draw objects
    view.draw()

#quit the program and close the window
pygame.quit()

"""if __name__ == '__main__':
    import sys
     print("Args are:*",sys.argv)"""
