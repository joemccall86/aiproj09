The intent of this project was to demonstrate basic AI concepts in a real time game.

Here are a few skills that were practiced during development
Planning and development of the project
  * Using A`*` path finding to guide NPC to player
  * Using a state machine to ensure that NPC behaved properly
  * Used Object oriented style and used inheritance extensively
  * Coded in Python
  * Used Subversion(SVN) to coordinate efforts between developers
  * Used toggle-able graphical debugging
  * Meeting strict deadlines
  * Presenting project to a customer. (The instructor and the class)
  * Mapped keyboard buttons to wii-mote using GlovePIE
  * Created our own level using Blender

Object of the game
---

The object to the game is to collect a key from each room without allowing any of the NPC's to catch you.

Rules NPC's are bound to
---

  * NPC's will seek you if you are near them (They will not find their way around a wall.)
  * NPC's will find you wherever you are in the room if you have the key
  * If an NPC catches you with a key, they take it back to it's original position
  * If an NPC catches you without a key, you lose
  * NPC's are bound to their room, they are not allowed to chase you into a neighboring room.
  * NPC's cannot see you when you are in another room

Controls:
---

  * Up Arrow    - Walk forward
  * Down Arrow  - Walk backward
  * Left Arrow  - Turn Left
  * Right Arrow - Turn Right
  * C           - Show/Hide collisions graphically
  * P           - Enable/Disable path smoothing
  * W           - Show/Hide way points for path finding
  * (Mappings for wii-mote are not included, you will have to download GlovePIE and map them yourself.)

Running the game:
---

Download and install the Panda3D library
  http://www.panda3d.org/download.php
  
Download and install Python version 2.5
  http://www.python.org/download/
  
In the directory where source has been downloaded type:

  {{{python world.py}}}

Known bug:
---

  The NPC's will sometimes fall through the floor causing the program to crash, after searching through the physics code for the game engine and speaking with the developers, it was found to be a problem in the physics engine. As a workaround, we have added logic in our code to force the height value of characters to never drop below ground level.

Here's some theoretical fake box-art:


http://mcc4ll.us/front_cover.png
http://mcc4ll.us/back_cover.png

We're in the process of uploading a second video. There's not much we can show in 30 seconds. Here's some of the features you can see in the video:

  * Multiple agents
  * Wander task (more advanced random movement)
  * Custom maps built with blender
  * Built-in physics engine handling gravity, collision handling

Some of the features not highlighted:

  * Evolving Artificial Neural Network using a modified version of pyNEAT
  * A`*` path finding algorithm
  * Seek task


Here's a short video of our game in the state it was when we turned it in for a grade. (Also its current state.)

http://www.youtube.com/watch?v=C1p3C8w7Pc0

For historical purposes, check out the first video!
----

http://www.youtube.com/watch?v=frUA_Ncay9c

`*` The reference to NPC throughout this text refers to what is commonly known as a Non-Player Character, or computer character. That is, any entity in the game that interacts with the user and is controlled by the computer.
