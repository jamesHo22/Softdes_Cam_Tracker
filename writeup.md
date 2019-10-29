#Camera Basketball
By Timothy Novak and James Ho
##Abstract:
The purpose of this assignment was to create an interactive experience controlled by tracking the movement of an object with a camera. The resuls are a simple basketball game where the user has to try to fling the basketball into a goal. The user controlls the position of the basketball by moving an object in front of the camera.

##Results
upon boot up of the game the user will have the opportunity to select what object they want to use as their controller via the creation of a bounding box in the camera feed. As the user moves the object around in physical space, an orange ball will be moved around on the screen. If the user causes the ball to undergo a high acceleration, the program will throw the ball. When the program throws the ball the user can no longer controll it and the ball is acted upon by gravity. If the user scores a oal feedback will be presented through the command output.

*Present what you accomplished. This will be different for each project, but screenshots are likely to be helpful.*

##Implementation

The program is separated into two files, one is `main.py` this handels the execution of the program and the pygame aspects of the program. This imports `tracker.py` as a custom library for handeling OpenCV image and camera processing. `main.py` is archetected in a model view controller pattern. This architecture seperates the various jobs of the program into seperate classes. The controller handels user input and events, such as fetching the positional tracker data from the functions in 'tracer.py' to read the user's input into the program. The view handels displaying all of the game objects to the screen. The model is the principle component of the program as it handels the back end calulations of how to translate inputs from the controller into movements in the view. The models handels calculations such as finding the position of the ball after it has been thrown, or determining if a oal has been scored. A more detailed look in at the classes and programs involved in the 'main.py' program can be seen here **[insert UML image here]** 

**[talk about tracker.py architecture]**

*Describe your implementation at a system architecture level. Include a UML class diagram, and talk about the major components, algorithms, data structures and how they fit together. You should also discuss at least one design decision where you had to choose between multiple alternatives, and explain why you made the choice you did.*

##Reflection


