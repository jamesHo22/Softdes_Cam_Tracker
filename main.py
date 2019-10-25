#MARK: Imports
import pygame
import tracker
from imutils.video import VideoStream
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
    def __init__(self):
        #create view, and controller objects
        self.view = View(640,700)
        self.controller = Controller()

    def runGameLoop(self):
        #create the cursor which will follow the user's hand
        cursor = Goal(self.view)

        #draw the content in the view
        self.view.draw()

        #MARK: Runtime Variables
        mainLoop = True
        FPS = 60

        # Make a tracker object
        newTracker = tracker.newTracker()
        
        
        #MARK: gameLoop
        while mainLoop:
            

            #MARK: event listeners
            for event in pygame.event.get():

                #handle events
                mainLoop = self.controller.handleEvent(event)

            #draw objects
            self.view.draw()

        #quit the program and close the window
        pygame.quit()
#MARK: object classes
class GameObject:

    def __init__(self,view, pos = None,color = (255,255,255), *geometry):
        #if no positional argument was supplied
        if pos == None:
            #set the default position
            pos = [300,300]

        #if no geometry was provided make the default circle
        if not geometry:
            #set the default geometry
            geometry = ('circle',30,0)

        #set up object Variables
        self.view = view
        self.pos = pos
        self.color = color
        self.geometry = geometry

        #creates the surface for the object changing the size based on the geometry provided
        if self.geometry[0] == 'circle':
            self.surface = pygame.Surface((2*self.geometry[1],2*self.geometry[1]))
        elif self.geometry[0] == 'rectangle':
            #creates the surface for the ball
            self.surface = pygame.Surface((self.geometry[1],self.geometry[2]))

        #add the object to the view
        view.addObj(self)

    def draw(self, view):
        """A method which draws the object to the screen."""
        if self.geometry[0] == 'circle':
            #draw the circle on to the surface
            pygame.draw.circle(self.surface,self.color,(self.geometry[1],self.geometry[1]),self.geometry[1],self.geometry[2])

        elif self.geometry[0] == 'rectangle':
            pygame.draw.rect(self.surface,self.color,pygame.Rect(0, 0,self.geometry[1],self.geometry[2]),self.geometry[3])

        #optimize the surface in memory so it is faster to draw
        self.surface = self.surface.convert_alpha()

        #display the circle
        view.window.blit(self.surface,self.pos)


class Ball (GameObject):
    """A class which draws a ball on the screen"""
    def __init__(self,view, pos = [300,300],color = (255,255,255),radius = 30):

        super().__init__(view,pos,color,'circle',radius,0)

class Goal (GameObject):
    """A class which draws a ball on the screen"""
    def __init__(self,view, pos = [300,300],color = (255,255,255),width = 30,height = 30,thickness = 2):

        super().__init__(view,pos,color,'rectangle',width,height,thickness)

def runGame(argv):
    """A function which runs the game when called"""
    model = Model()
    model.runGameLoop()

#if the program is called from the command line
if __name__ == '__main__':
    import sys
    #print("Args are:*",sys.argv)
    #run the program
    runGame(sys.argv)
