# Camera Basketball

By Timothy Novak and James Ho

## Abstract:

The purpose of this assignment was to create an interactive experience controlled by tracking the movement of an object with a camera. The results are a simple basketball game where the user has to try to fling the basketball into a goal. The user controls the position of the basketball by moving an object in front of the camera.

  

## Results

upon boot up of the game the user will have the opportunity to select what object they want to use as their controller via the creation of a bounding box in the camera feed. As the user moves the object around in physical space, an orange ball will be moved around on the screen. If the user causes the ball to undergo a high acceleration, the program will throw the ball. When the program throws the ball the user can no longer controll it and the ball is acted upon by gravity. If the user scores a oal feedback will be presented through the command output.

## Implementation

The program is separated into two files, one is `main.py` this handles the execution of the program and the pygame aspects of the program. This imports `tracker.py` as a custom library for handling OpenCV image and camera processing. `main.py` is architected in a model view controller pattern. This architecture separates the various jobs of the program into separate classes. The controller handles user input and events, such as fetching the positional tracker data from the functions in `tracker.py` to read the user's input into the program. The view handles displaying all of the game objects to the screen. The model is the principle component of the program as it handles the back end calculations of how to translate inputs from the controller into movements in the view.

The two interesting parts of the model we'd like to point out are the ball throwing detection and the trajectory simulation.

When thinking about how to implement the throw detection, we decided to look at the acceleration of the tracked object to determine the thrown state of the ball. If the acceleration exceeded a certain threshold, we would take the final x and y velocities and generate a trajectory the ball would follow. This is implemented in `main.py` in the `getBallPos()` function. This function uses numpy's `gradient()` function to calculate the first and second time derivative of the position of the ball given a numpy array. These values are used to detect a throw and determine the final x and y velocities after the ball is thrown.

Once the ball is thrown, the final x and y velocities are passed to `throwBall()` where the trajectory is calculated. This is done simply using forward euler's method and 2D kinematic equations of motion. A new ball set to follow this trajectory and the old ball is set to be invisible.

In summary, the model handles calculations such as finding the position of the ball after it has been thrown, or determining if a goal has been scored. A more detailed look in at the classes and programs involved in the 'main.py' program can be seen here.

![alt text](/MP4-ulm.jpg "The UML diagram of main.py") 

One decision illustrated by the UML diagram above is the decision to make the Ball and Goal classes inherit from a shared Game Object class. With the general simplicity of each and the few numbers of them involved it likely would have been suficent to implement each as it's own seperate class. However building a parrent GameObject class allowed us to build a common interface for the view class to interface with these objects. The view treats each as merely a game object as it is able to call each's draw function to display it to the screen and it can get the arguments to inform what to display from the object's geometry property. The view does not have to worry about having to interface with each seperately. Also extracting the shared code allows the ball ang goal classes to focus on the unique functionality of each while relying on the underlying GameObject class to handle displaying them. Finally this decision allows for ease of expandability and ease of addition of new objects. A backboard class could be easily added by instantiating a rectangular Game object which has a function to redirect the ball, however the view class would not have to be changed and could easily accomodate the new object.

`tracker.py` is a module that contains all the openCV functionality. Most of the code was from https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/. I packaged everything into a class, which made working with openCV very easy. The tracker object only has one function that returns the x,y coordinates of the tracked object. This position is easily passed to the controller in `main.py`.

## Reflection

What went well: The project was well scoped and we both enjoyed the product we were building. James got to play with OpenCV and Tim got to learn how to use pygame, which satisfied both our learning goals.

What didn't go well: During the end of the project, we started to push bigger changes without checking whether or not we always had a working version of the codebase. In the end, this led to reverting back to a old commit, forcing it to become the new head of the master branch, and resolving confusing merge errors. While this process took longer than expected, we learned how to debug efficiently by following errors back to their source
What to improve: We overlooked the importance of unit tests for this project. This would have helped during the refactoring processes of some functions, as we would instantly know if a function broke. This is something we would like to include in our final projects.

From an accessibility standpoint, our game requires the user to be able to move any part of their body with control and speed. The ability to track almost any moving object makes the game accessible to people who lack fine motor skills. 

The work was split up pretty evenly. We both agreed at the start the amount of time we wanted to spend on it and we pretty much succeeded in matching our predetermined commitment level. James worked on the physics simulation and openCV while Tim worked on architecture and user interaction. Next time, we would both focus on making sure there is always a working version of the code and unit testing. James would like to learn how to architecture the codebase (working with classes and defining methods).
