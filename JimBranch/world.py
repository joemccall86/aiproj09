# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
from waypoint import Waypoint
from pathFinder import PathFinder
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import math
from math import sqrt
from Queue import Queue
#from heapq import heapq
import heapq


class World(DirectObject):                
    # Key map dictionary; These represent the keys pressed
    __keyMap = {"left":False, "right":False, "up":False, "down":False}
    
    # Keep track of time at previous frame to keep speed consistant on different platforms.
    __previousTime = 0
    
    def __init__(self):
        groundModel = "models/gridBack"
        
        DirectObject.__init__(self)
        env = loader.loadModel(groundModel)
        
        self.globalAgentList = []
        # Now to make our first agent
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.ralph = NPC(modelStanding, 
                    {"run":modelRunning, "walk":modelWalking},
                    turnRate = 150, 
                    speed = 5,
                    agentList = self.globalAgentList,
                    agentName = "ralph",
                    collisionMask = BitMask32.bit(0),
                    adjacencySensorThreshold = 5,
                    radarSlices = 8,
                    radarLength = 6,
                    scale = 0.2)
        
        # Make it visibler
        
        env.reparentTo(render)
        
        texture = loader.loadTexture("textures/snowish.jpg")
        
        # This is so the textures can look better from a distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        env.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        env.setTexScale(TextureStage.getDefault(), 0.1, 0.1)
        env.setTexture(texture, 1)
        
        # Make it so that it's big enough to walk on
        env.setPos(0, 0, 0)
        env.setScale(100)
        
        bunnyStanding = "models/bunny/bunny"
        bunnyRunning = "models/bunny/bunny"
        bunnyWalking = "models/bunny/bunny"
        bunnyCount = 1
        self.bunnies = [NPC(bunnyStanding, 
                    {"run":bunnyRunning, "walk":bunnyWalking},
                    turnRate = 150, 
                    speed = 6,
                    agentList = self.globalAgentList,
                    agentName = "bunny",
                    rangeFinderCount = 4,
                    collisionMask = BitMask32.bit(i+1),
                    scale = 0.2)
                    for i in range(bunnyCount)]
        index = 1 
        for bunny in self.bunnies:
            bunny.reparentTo(render)
            bunny.setX(-5 * index + 11)
            bunny.setY(6)
            index += 1
            taskMgr.add(bunny.sense, "sense" + str(index))
        

            # uncomment this to make Jim happy
            #taskMgr.add(ralph.sense, "sense" + str(index))
                    
        # Make it visible
        self.ralph.reparentTo(render)
        
        #waypointPosition = Vec3(0,5,0)
        #self.someWaypoint = Waypoint(waypointPosition)
        #######################################################
        #######################################################
        self.setWaypoints()
        bestPath = PathFinder.AStar(self.ralph, self.bunnies[0], self.waypoints)
        #######################################################
        #######################################################
        self.draw()
        
        #base.oobeCull()
        base.camera.setPos(0,0,50)
        base.camera.lookAt(0,0,0)
        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.ralph)
        base.camera.setPos(0, 30, 10)
        base.camera.lookAt(self.ralph)
        base.camera.setP(base.camera.getP() + 15)
        
        self.__setKeymap()
        taskMgr.add(self.__processKey, "processKey", extraArgs = [self.bunnies[0]], appendTask = True)
        taskMgr.add(self.ralph.act, "act")
        # now add the sense loop
        #taskMgr.add(self.ralph.sense, "sense")
        taskMgr.add(self.__printPositionAndHeading, "__printPositionAndHeading")
        
        taskMgr.add(self.ralph.followPath, "followPath", extraArgs = [bestPath], appendTask = True)
        
        
        self.isMoving = False
        
        base.setBackgroundColor(r=0, g=0, b=.1, a=1)
        
    def setWaypoints(self):
        col1 = -17
        col2 = -12
        col3 = -7
        col4 = -2
        col5 = 3
        col6 = 8
        col7 = 13
        col8 = 18
        rowA = 19
        rowB = 14
        
        rowA = 3
        rowB = -1

        waypointPosition = Vec3(col1,rowA,0)
        self.waypointA1 = Waypoint(waypointPosition, 1)
        waypointPosition = Vec3(col2,rowA,0)
        self.waypointA2 = Waypoint(waypointPosition, 2)
        waypointPosition = Vec3(col3,rowA,0)
        self.waypointA3 = Waypoint(waypointPosition, 3)
        waypointPosition = Vec3(col4,rowA,0)
        self.waypointA4 = Waypoint(waypointPosition, 4)
        waypointPosition = Vec3(col5,rowA,0)
        self.waypointA5 = Waypoint(waypointPosition, 5)
        waypointPosition = Vec3(col6,rowA,0)
        self.waypointA6 = Waypoint(waypointPosition, 6)
        waypointPosition = Vec3(col7,rowA,0)
        self.waypointA7 = Waypoint(waypointPosition, 7)
        waypointPosition = Vec3(col8,rowA,0)
        self.waypointA8 = Waypoint(waypointPosition, 8)
        
        waypointPosition = Vec3(col1,rowB,0)
        self.waypointB1 = Waypoint(waypointPosition, 11)
        waypointPosition = Vec3(col2,rowB,0)
        self.waypointB2 = Waypoint(waypointPosition, 12)
        waypointPosition = Vec3(col3,rowB,0)
        self.waypointB3 = Waypoint(waypointPosition, 13)
        waypointPosition = Vec3(col4,rowB,0)
        self.waypointB4 = Waypoint(waypointPosition, 14)
        waypointPosition = Vec3(col5,rowB,0)
        self.waypointB5 = Waypoint(waypointPosition, 15)
        waypointPosition = Vec3(col6,rowB,0)
        self.waypointB6 = Waypoint(waypointPosition, 16)
        waypointPosition = Vec3(col7,rowB,0)
        self.waypointB7 = Waypoint(waypointPosition, 17)
        waypointPosition = Vec3(col8,rowB,0)
        self.waypointB8 = Waypoint(waypointPosition, 18)
        
        self.waypoints = [self.waypointA1, self.waypointA2, self.waypointA3, self.waypointA4, self.waypointA5, self.waypointA6, self.waypointA7, self.waypointA8]
        self.waypoints.extend([self.waypointB1, self.waypointB2, self.waypointB3, self.waypointB4, self.waypointB5, self.waypointB6, self.waypointB7, self.waypointB8])
        
        #Set paths
        self.waypointA2.setNeighbors([self.waypointA3, self.waypointB2])
        self.waypointA3.setNeighbors([self.waypointA2, self.waypointA4])
        self.waypointA4.setNeighbors([self.waypointA3, self.waypointA5])
        self.waypointA5.setNeighbors([self.waypointA4, self.waypointA6])
        self.waypointA6.setNeighbors([self.waypointA5])
        
        self.waypointB2.setNeighbors([self.waypointB3, self.waypointA2])
        self.waypointB3.setNeighbors([self.waypointB2, self.waypointB4])
        self.waypointB4.setNeighbors([self.waypointB3, self.waypointB5])
        self.waypointB5.setNeighbors([self.waypointB4, self.waypointB6])
        self.waypointB6.setNeighbors([self.waypointB5])
        
        self.waypoints = [self.waypointA2, self.waypointA3, self.waypointA4, self.waypointA5, self.waypointA6]
        self.waypoints.extend([self.waypointB2, self.waypointB3, self.waypointB4, self.waypointB5, self.waypointB6])

    
    def draw(self):
        self.drawSky()
        self.drawWalls()
        for waypoint in self.waypoints:
            waypoint.draw()
        
    def drawWalls(self):        
        
        stoneTexture = loader.loadTexture("textures/Stones.jpg")
        stoneTexture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        wallModel = "models/box.egg.pz"
        wall = loader.loadModel(wallModel)
        wall.setPos(0, 1, 0)
        wall.setScale(1, 1, 1)
        wall.setTexture(stoneTexture, 1)
        
        # Add collision stuff to the wall
        tempWallCollideNodePath = wall.find("/Box")
        tempWallCollideNodePath.node().setIntoCollideMask(BitMask32.allOn())
        tempWallCollideNodePath.node().setFromCollideMask(BitMask32.allOff())
        
        # Create a box
        for i in range(40):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i*1 - 20, -20, 0)
            wall.instanceTo(tempWall)
        for i in range(40):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i*1 - 20, 20, 0)
            wall.instanceTo(tempWall)
        for i in range(40):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(-20, i*1 - 20, 0)
            wall.instanceTo(tempWall)
        for i in range(41):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(20, i*1 - 20, 0)
            wall.instanceTo(tempWall)
            
        # Create a maze in the box
        for i in range(20):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i - 10, 0, 0)
            wall.instanceTo(tempWall)
        for i in range(20):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(10, i - 10, 0)
            wall.instanceTo(tempWall)
        for i in range(21):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i - 10, 10, 0)
            wall.instanceTo(tempWall)
        return
        
    def drawSky(self):
        
        #Add the sky!
        skyModel = "models/SunnySky/sunny.egg"
        sky = loader.loadModel(skyModel)
        sky.setPos(0,0,0)
        sky.setScale(0.5, 0.5, 0.5)
        #tempSky = render.attachNewNode("sky")
        #tempSky.setPos(i*1 - 20, -20, 0)
        #sky.instanceTo(tempSky)
        sky.reparentTo(render)
    
    def __setKeymap(self):
        self.accept("escape", sys.exit)
        
        self.accept("arrow_left", self.__setKey, ["left", True])
        self.accept("arrow_left-up", self.__setKey, ["left", False])
        self.accept("arrow_right", self.__setKey, ["right", True])
        self.accept("arrow_right-up", self.__setKey, ["right", False])
        self.accept("arrow_up", self.__setKey, ["up", True])
        self.accept("arrow_up-up", self.__setKey, ["up", False])
        self.accept("arrow_down", self.__setKey, ["down", True])
        self.accept("arrow_down-up", self.__setKey, ["down", False])

    def __processKey(self, actor, task):
        elapsedTime = task.time - self.__previousTime
        turnAngle = actor.turnRate * elapsedTime
        distance = actor.speed * elapsedTime
        
        if self.__keyMap["left"]:
            actor.turnLeft(turnAngle)
        if self.__keyMap["right"]:
            actor.turnRight(turnAngle)
        if self.__keyMap["up"]:
            actor.moveForward(distance)
        if self.__keyMap["down"]:
            actor.moveBackward(distance)
            
        if self.__keyMap["left"] or \
            self.__keyMap["right"] or \
            self.__keyMap["up"] or \
            self.__keyMap["down"]:
            if not self.isMoving:
                #actor.loop("run")
                self.isMoving = True
        else:
            actor.stop()
            #actor.pose("walk", frame = 5)
            self.isMoving = False
        
        # Store the previous time and continue
        self.__previousTime = task.time
        return Task.cont
    
    def __setKey(self, key, value):
        self.__keyMap[key] = value
        
    positionHeadingText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                   pos=(-1.3,-0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
                
    def __printPositionAndHeading(self, task):
        heading = self.ralph.getH()
        while heading > 360.0:
            heading -= 360.0
        while heading < 0.0:
            heading += 360.0
            
        self.positionHeadingText.setText("Position: (" + 
            str(self.ralph.getPos().getX()) + ", " + 
            str(self.ralph.getPos().getY()) + ") at heading " + 
            str(heading))
        return Task.cont
    
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")
