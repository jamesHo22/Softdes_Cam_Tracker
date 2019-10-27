#MARK: Imports
import pygame
import tracker
from imutils.video import VideoStream
#initalize pygame
pygame.init()


#MARK: view
class View:
    """Handle updates to the user display"""

    def __init__(self,screenWidth = 600,screenHeight = 600, backgroundColor = (0,0,0)):
        """Set up the View

        Keyword arguments:
        screenwidth(optional) -- the width of the screen generated in pixels
        screenHeight(optional) -- the height of the screen generated in pixels
        backgroundColor(optional) -- the color in rgb of the background of the screen"""

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
        """a method which adds an object to the lit of objects to draw"""
        self.objects.append(obj)

#MARK: controller
class Controller:

    def __init__(self):
        self.isRunning = True
        self.mousePos = ()

    def handleEvent(self,event):
        """Handle the events from the pygame event colors"""
        #checks for the x in the corner
        if event.type == pygame.QUIT:
            #stop looping
            self.isRunning = False
        #listens for key presses
        elif event.type == pygame.KEYDOWN:

            #excape keypress
            if event.key == pygame.K_ESCAPE:
                #stop looping
                self.isRunning = False
            else:
                self.isRunning = True
        elif event.type == pygame.MOUSEMOTION:
            self.mousePos = event.pos
        else:
            self.isRunning = True

    def getControlInput(self,input,vs,tracker):
        """gets the posion that the controller is at"""
        if input == 'pygame':
            return self.mousePos
        elif input == 'openCV':
            return tracker.getPosition(vs)
            
            
            #get the opencv tracked cords

#MARK: Model
class Model:
    def __init__(self):
        #create view, and controller objects
        self.view = View(640,700)
        self.controller = Controller()

    def runGameLoop(self):
        #create the game objects

        goal = Goal(self.view)
        startButton = Button(self.view)
        startButton.visible = True

        ball = Ball(self.view)
        ball.visible = True

        #draw the content in the view
        self.view.draw()

        #MARK: Runtime Variables
        running = True
        FPS = 60

        # Make a tracker object
        newTracker = tracker.newTracker()
        vs = VideoStream(src=0).start()
        newTracker = tracker.newTracker()
        
        #MARK: gameLoop
        while running:

            #MARK: event listeners
            for event in pygame.event.get():

                #handle events
                self.controller.handleEvent(event)
                running = self.controller.isRunning
            
            
            #update positions
            cntPos = self.controller.getControlInput('openCV',vs,newTracker)
            if cntPos != None:
                ball.pos = cntPos

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
        self.visible = False

        #creates the surface for the object changing the size based on the geometry provided
        if self.geometry[0] == 'circle':
            self.surface = pygame.Surface((2*self.geometry[1],2*self.geometry[1]),pygame.SRCALPHA, 32)
        elif self.geometry[0] == 'rectangle':
            #creates the surface for the ball
            self.surface = pygame.Surface((self.geometry[1],self.geometry[2]),pygame.SRCALPHA, 32)

        #add the object to the view
        view.addObj(self)

    def draw(self, view):
        """A method which draws its parent object to the screen if the object is supposed to be drawn"""
        if self.visible:
            if self.geometry[0] == 'circle':
                #draw the circle on to the surface
                pygame.draw.circle(self.surface,self.color,(self.geometry[1],self.geometry[1]),self.geometry[1],self.geometry[2])

            elif self.geometry[0] == 'rectangle':
                pygame.draw.rect(self.surface,self.color,pygame.Rect(0, 0,self.geometry[1],self.geometry[2]),self.geometry[3])

            #optimize the surface in memory so it is faster to draw
            self.surface = self.surface.convert_alpha()

            #display the circle
            view.window.blit(self.surface,self.pos)
        else:
            return


class Ball (GameObject):
    """A class which draws a ball on the screen"""
    def __init__(self,view, pos = [300,300],color = (255,140,0),radius = 30):

        super().__init__(view,pos,color,'circle',radius,0)

class Goal (GameObject):
    """A class which draws a goal on the screen"""
    def __init__(self,view, pos = [300,300],color = (255,255,255),width = 30,height = 30,thickness = 2):

        super().__init__(view,pos,color,'rectangle',width,height,thickness)

class Button (GameObject):
    """A class which draws a button on the screen"""
    def __init__(self,view, pos = [300,300],color = (255,255,255),width = 90,height = 70,thickness = 0):

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
