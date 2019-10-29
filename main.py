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
    """Handle updates to the user display"""
    

    def __init__(self,screenWidth = SCREEN_WIDTH, screenHeight = SCREEN_HEIGHT, backgroundColor = (0,0,0)):
        """Set up the View

        Keyword arguments:
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
        """A function which creates a pygame window specified by the properties of the view."""
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
            X, Y = tracker.getPosition(vs)
            return -X*2+SCREEN_WIDTH, Y*3-SCREEN_HEIGHT/2
            #get the opencv tracked cords

#MARK: Model
class Model:
    def __init__(self):
        #create view, and controller objects
        self.view = View(640,700)
        self.controller = Controller()

    def getBallPos(self, currentX, currentY, dt):
        '''
        This function encapsulates the physics of the ball motion.
        (numpy.array) currentX: the current x position of the ball
        (numpy.array) currentY: the current y position of the ball
        (tuple) returns: new x and y
        '''
        # TODO: determine the acceleration of the ball
        # Take the second derivative of both x and y lists
        xVel = np.gradient(currentX, dt)
        yVel = np.gradient(currentY, dt)
        xAcc = np.gradient(xVel, dt)[-1]
        yAcc = np.gradient(yVel, dt)[-1]
        # print(f'x acc: {xAcc}, y acc: {yAcc}')
        # print(xAcc)
        cutoff = 7000
        threshold = 12000
        # print(xAcc)
        if xAcc >= cutoff and xAcc < threshold:
            return xVel[-1], yVel[-1], True
        else:
            return currentX[-1], currentY[-1], False      

    def throwBall(self, xVel, yVel, xInit, yInit, tEnd, goal):
        ACCELERATION = 100
        '''
        This function takes in velocities and computes trajectories that are then displayed to the user
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
        #create the game objects

        goal = Goal(self.view)
        goal.visible = True
        startButton = Button(self.view)
        startButton.visible = False

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

    def __init__(self,view, pos = None,color = (255,255,255), *geometry):
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
        self.mass = 1
        super().__init__(view,pos,color,'circle',radius,0)


class Goal (GameObject):
    """A class which draws a goal on the screen"""
    def __init__(self,view, pos = [700,300],color = (255,255,255),width = 70,height = 30,thickness = 2):

        super().__init__(view,pos,color,'rectangle',width,height,thickness)
    
    def ballInGoal(self, ball):
        """Check if the a ball is in the goal

        (Ball) ball: the ball to check if there is a goal

        Returns:
        (bool):True if there is a ball in the goal and false if there isn`t"""
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
