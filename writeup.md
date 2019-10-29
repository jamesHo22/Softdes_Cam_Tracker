# Camera Basketball
By Timothy Novak and James Ho
## Abstract:
The purpose of this assignment was to create an interactive experience controlled by tracking the movement of an object with a camera. The resuls are a simple basketball game where the user has to try to fling the basketball into a goal. The user controlls the position of the basketball by moving an object in front of the camera.

## Results
upon boot up of the game the user will have the opportunity to select what object they want to use as their controller via the creation of a bounding box in the camera feed. As the user moves the object around in physical space, an orange ball will be moved around on the screen. If the user causes the ball to undergo a high acceleration, the program will throw the ball. When the program throws the ball the user can no longer controll it and the ball is acted upon by gravity. If the user scores a oal feedback will be presented through the command output. **[revise and add screenshot of program]**

*Present what you accomplished. This will be different for each project, but screenshots are likely to be helpful.*

## Implementation

The program is separated into two files, one is `main.py` this handels the execution of the program and the pygame aspects of the program. This imports `tracker.py` as a custom library for handeling OpenCV image and camera processing. `main.py` is archetected in a model view controller pattern. This architecture seperates the various jobs of the program into seperate classes. The controller handels user input and events, such as fetching the positional tracker data from the functions in 'tracer.py' to read the user's input into the program. The view handels displaying all of the game objects to the screen. The model is the principle component of the program as it handels the back end calulations of how to translate inputs from the controller into movements in the view. The models handels calculations such as finding the position of the ball after it has been thrown, or determining if a oal has been scored. A more detailed look in at the classes and programs involved in the 'main.py' program can be seen here

![alt text](/UML.jpg "The UML diagram of main.py") 

One decision illustrated by the UML diagram above is the decision to make the Ball and Goal classes inherit from a shared Game Object class. With the general simplicity of each and the few numbers of them involved it likely would have been suficent to implement each as it's own seperate class. However building a parrent GameObject class allowed us to build a common interface for the view class to interface with these objects. The view treats each as merely a game object as it is able to call each's draw function to display it to the screen and it can get the arguments to inform what to display from the object's geometry property. The view does not have to worry about having to interface with each seperately. Also extracting the shared code allows the ball ang goal classes to focus on the unique functionality of each while relying on the underlying GameObject class to handle displaying them. Finally this decision allows for ease of expandability and ease of addition of new objects. A backboard class could be easily added by instantiating a rectangular Game object which has a function to redirect the ball, however the view class would not have to be changed and could easily accomodate the new object.

**[talk about tracker.py architecture]**

*Describe your implementation at a system architecture level. Include a UML class diagram, and talk about the major components, algorithms, data structures and how they fit together. You should also discuss at least one design decision where you had to choose between multiple alternatives, and explain why you made the choice you did.*

## Reflection

### Overall
The project was effective overall. we each made progress towards our individual learning goals and developed a workable project at the end.We divided the work on the project in accordance with each of our goals (Tim wanted to work on GUI/Grapics and so he took on the pygame side of the project while James wanted to work with camera processing and so he took on the OpenCV side of the project). This worked well as we could each work autonomously but we also got the experience of pair programming during merging and integrating the two code segments together. 

The program allows for a user to controll a program via moving an object in the camera. This could be a helpful technology/input device for people with tremmors or malformed apendages as this allows them to use a 'mouse' without having to use the standard computer input devices. With further development a visual keyboard could be made so the user would not have to use the keyboard of the computer for typing. Although the technology demonstrated here could help with inclusivity of technology, it is not perfect and it is still inaccessable to those with limited hange of motion or those who have difficulty moving their limbs. One possible concern might be that with the use of computer vision, the program may not recognise people of different ethnicities or genders. However the computer vision code tracks any object via changes from one omage to the next, and so it would likely be able to track the face or limbs of a user with a differing background from those of the researchers. 

### Individual: Tim
I felt that his program was useful to exposing me to the tools of openCV and pygame. I feel that I have achieved suficent fmiliarity with these tools as to be able and comfortable with using them in my future projects. I personally would have liked to guild a starting interface for the game, or to have implemented a scoreboard to track the player's score as these would have factored more greatly into my goal of learning how to build GUIs. As it stands I learned about Pygame which is a simple tool I can use for my future projects which can aid me in the creation of GUIs for my python based projects.

### Individual: James
**[write individual reflection here]**
