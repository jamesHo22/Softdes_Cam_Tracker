#MARK: Imports
import pygame
import tracker
from imutils.video import VideoStream
import numpy as np
import time
#initalize pygame
pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

#MARK: view
class View:
    """Handle updates to the user display

    Properties:
    (int) width: the width of the pygame screen
    (int) height: the height of the pygame screen
    (tuple) backgroundColor: the color of the background of the screen in rgb
    ([GameObject]) objects: a list of objects in the scene
    (pygame.display) window: the pygame Window
    (pygame.surface) background: the background of the Window
    """


    def __init__(self,screenWidth = SCREEN_WIDTH, screenHeight = SCREEN_HEIGHT, backgroundColor = (0,0,0)):
        """Set up the View

        screenwidth(optional) -- the width of the screen generated in pixels
        screenHeight(optional) -- the height of the screen generated in pixels
        backgroundColor(optional) -- the color in rgb of the background of the screen"""

        #initalize the view variables
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.backgroundColor = backgroundColor
        self.objects = []
        #sets up the pygame display window
        self.initWindow()

    def initWindow (self):
        """Creates a pygame window specified by the properties of the view."""
        #MARK: Window setup
        #create the pygame window of the designated size
        print(self.width)
        self.window = pygame.display.set_mode((self.width, self.height))
        #create a surface (layer) the same size as the window to draw the background on
        self.background = pygame.Surface(self.window.get_size())
        #paint the background black
        self.background.fill(self.backgroundColor)
        #optimize the surface in memory so it is faster to draw
        #use convert_alpha() if the surface has transparency
        self.background = self.background.convert()

    def draw(self):
        """Draws all of the pygame surfaces"""
        self.window.blit(self.background, (0,0))

        for obj in self.objects:
            obj.draw(self)

        #update the display
        pygame.display.flip()

    def addObj(self, obj):
        """Adds an object to the list of objects to draw

        (GameObject) obj: the object to add"""
        self.objects.append(obj)

#MARK: controller
class Controller:
    """Handle user inputs

    Properties:
    (bool) isRunning: stores whether or not the main game loop is running
    (tuple) mousePos: stores the position of the mouse in the pygame window"""

    def __init__(self):
        self.isRunning = True
        self.mousePos = ()

    def handleEvent(self,event):
        """Handle the pygame events from the controller

        (pygame.event) event: the event to process"""
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
        """get the position that the controller is at

        (string) input: the input source to get data from
        (videoStream) vs: the videop stream from the camera
        (tracker) tracker: the oject tracker which identifies the location of an
         object in the stream

         (tuple) returns: the x and y positions of the controller input"""

        #check inputs
        if input == 'pygame':
            return self.mousePos
        elif input == 'openCV':
            X, Y = tracker.getPosition(vs)
            return -X*2+SCREEN_WIDTH, Y*3-SCREEN_HEIGHT/2
            #get the opencv tracked cords

#MARK: Model
class Model:
    """Handle back end calculations

    Properties:
    (view) view: the view object for the program
    (Controller) controller: the controller object for the program"""

    def __init__(self):
        #create view, and controller objects
        self.view = View(640,700)
        self.controller = Controller()

    def getBallPos(self, currentX, currentY, dt):
        '''Encapsulates the physics of the ball motion.

        (numpy.array) currentX: the current x position of the ball
        (numpy.array) currentY: the current y position of the ball
        (numpy.array) dt: the array of time steps for each position of the ball

        (tuple) returns: new x and y
        '''
        # TODO: determine the acceleration of the ball
        # Take the second derivative of both x and y lists
        xVel = np.gradient(currentX, dt)
        yVel = np.gradient(currentY, dt)
        xAcc = np.gradient(xVel, dt)[-1]
        yAcc = np.gradient(yVel, dt)[-1]
        # print(f'x acc: {xAcc}, y acc: {yAcc}')
        print(xAcc)
        cutoff = 8000
        threshold = 12000
        # print(xAcc)
        if xAcc >= cutoff and xAcc < threshold:
            return xVel[-1], yVel[-1], True
        else:
            return currentX[-1], currentY[-1], False

    def throwBall(self, xVel, yVel, xInit, yInit, tEnd, goal):
        ACCELERATION = 100
        '''Computes trajectories which are displayed to the user

        (numpy.array) xVel: an array of the x axis velocities in time
        (numpy.array) yVel: an array of the y axis velocities in time
        (int) xInit: the inital x posiion of the ball on throw
        (int) yInit: the inital y posiion of the ball on throw
        (float) tEnd:the ending time of the movement
        (Goal) goal: the game object describing the basket ball hoop
        '''
        times = np.linspace(0, tEnd, 20*tEnd)
        xPos = np.ones(len(times)+1)
        xPos[0] = xInit
        yPos = np.ones(len(times)+1)
        yPos[0] = yInit
        for i in range(len(times)):
            xPos[i+1] = xPos[i] + (xVel/40)*times[i]
            yPos[i+1] = yPos[i] + (yVel/40)*times[i] + 0.5*ACCELERATION*times[i]**2

        ball = Ball(self.view)
        ball.visible = True

        for i in range(len(xPos)):
            ball.pos = xPos[i], yPos[i]
            goal.ballInGoal(ball)
            self.view.draw()

    def runGameLoop(self):
        """Sets up and executes the main game loop
        """

        #create the game objects

        goal = Goal(self.view)
        goal.visible = True

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
        currentX = []
        currentY = []
        timesteps = []
        N = 10

        while running:
            startTime = time.time()
            #MARK: event listeners
            for event in pygame.event.get():

                #handle events
                self.controller.handleEvent(event)
                running = self.controller.isRunning


            #update positions
            cntPos = self.controller.getControlInput('openCV',vs,newTracker)
            endTime = time.time()
            dt = endTime-startTime
            # TODO: check length of the currentX array
            # If the length is longer than some number, compute the gradient then delete the last item and add new x to front
            # Else, append to the array
            if len(currentX) >= N:
                timesteps = timesteps[1:]
                timesteps.append(dt)

                currentX = currentX[1:]
                currentX.append(cntPos[0])

                currentY = currentY[1:]
                currentY.append(cntPos[1])
                ballState = self.getBallPos(currentX, currentY, dt)
                thrown = ballState[2]
                if thrown:
                    print('ball thrown')
                    ball.visible = False
                    xVel, yVel = ballState[0], ballState[1]
                    self.throwBall(xVel, yVel, currentX[-1], currentY[-1], 3, goal)

                else:
                    ball.visible = True
                    cntPos = ballState[0], ballState[1]
            else:
                currentX.append(cntPos[0])
                currentY.append(cntPos[1])
                timesteps.append(dt)

            if cntPos != None:
                ball.pos = cntPos

            #draw objects
            self.view.draw()

        #quit the program and close the window
        pygame.quit()


#MARK: object classes
class GameObject:
    """Base functionality for displayed objects

    Properties:
    (view) view: the view that this belongs to
    (tuple) pos: the x and y cordinates of the top left corner of the object
    (tuple) color: the set of rgb which define the object's coloer
    (tuple) geometry: the extra arguments which define the geometry of the shape
    these are in the order of (string) name which identifies the type of geometry
    then any suplemental arguments which are necessary for drawing that shape
    (bool) visible: this discribes whether or not the object should be drawn"""

    def __init__(self,view, pos = None,color = (255,255,255), *geometry):
        """creates a game object

        (view) view: the view that this belongs to
        (tuple) pos: the x and y cordinates of the top left corner of the object
        (tuple) color: the set of rgb which define the object's coloer
        (tuple) geometry: the extra arguments which define the geometry of the shape
        these are in the order of (string) name which identifies the type of geometry
        then any suplemental arguments which are necessary for drawing that shape"""

        #if no positional argument was supplied
        if pos == None:
            #set the default position
            pos = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]

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
        self.view.addObj(self)

    def draw(self):
        """Draws its parent object to the screen if the object is supposed to be drawn"""

        if self.visible:
            if self.geometry[0] == 'circle':
                #draw the circle on to the surface
                pygame.draw.circle(self.surface,self.color,(self.geometry[1],self.geometry[1]),self.geometry[1],self.geometry[2])

            elif self.geometry[0] == 'rectangle':
                pygame.draw.rect(self.surface,self.color,pygame.Rect(0, 0,self.geometry[1],self.geometry[2]),self.geometry[3])

            #optimize the surface in memory so it is faster to draw
            self.surface = self.surface.convert_alpha()

            #display the circle
            self.view.window.blit(self.surface,self.pos)
        else:
            return


class Ball (GameObject):
    """Draws a ball on the screen"""

    def __init__(self,view, pos = [300,300],color = (255,140,0),radius = 30):
        super().__init__(view,pos,color,'circle',radius,0)


class Goal (GameObject):
    """Draws a goal on the screen"""

    def __init__(self,view, pos = [700,300],color = (255,255,255),width = 70,height = 30,thickness = 2):

        super().__init__(view,pos,color,'rectangle',width,height,thickness)

    def ballInGoal(self, ball):
        """Check if the a ball is in the goal

        (Ball) ball: the ball to check if there is a goal

        (bool) returns: True if there is a ball in the goal and false if there isn`t"""
        goalState = False
        #if the ball is horrizontally in the hoop
        if ball.pos[0] >= self.pos[0] and ball.pos[0]+ball.surface.get_width() <= self.pos[0]+self.surface.get_width() and ball.visible:

                #if the top of the ball is below the top surface and above the bottom surface of the goal
            if ball.pos[1] >= self .pos[0] and ball.pos[1] <= self.surface.get_height()+self.pos[1]:
                ballState = True
                print("goal")
            #if the top of the ball is above the top surface and the bottom surface of the ball is below the bottom surface of the goal
            elif ball.pos[1] <= self .pos[0] and ball.pos[1]+ball.surface.get_height() >= self.surface.get_height()+self.pos[1]:
                ballState = True
                print("goal")
            #if the bottom of the ball is below the top surface and above the bottom surface of the goal
            elif ball.pos[1]+ball.surface.get_height() >= self .pos[0] and ball.pos[1]+ball.surface.get_height() <= self.surface.get_height()+self.pos[1]:
                ballState = True
                print("goal")
            else:
                ballState = False
        else:
            ballState = False

def runGame(argv):
    """Runs the game when called

    (tuple) argv: any command line arguments which were passed to the program"""
    model = Model()
    model.runGameLoop()

#if the program is called from the command line
if __name__ == '__main__':
    import sys
    #print("Args are:*",sys.argv)
    #run the program
    runGame(sys.argv)
