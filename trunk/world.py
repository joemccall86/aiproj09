# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

class World(DirectObject):
        
    # Now to make our first agent
    modelStanding = "models/ralph"
    modelRunning = "models/ralph-run"
    modelWalking = "models/ralph-walk"
    
    globalAgentList = []
    ralph = NPC(modelStanding, 
                {"run":modelRunning, "walk":modelWalking},
                turnRate = 150, 
                speed = 5,
                agentList = globalAgentList,
                collisionMask = BitMask32.bit(0),
                adjacencySensorThreshold = 5,
                radarSlices = 4,
                radarLength = 5)

                
    # Key map dictionary; These represent the keys pressed
    __keyMap = {"left":False, "right":False, "up":False, "down":False}
    
    # Keep track of time at previous frame to keep speed consistant on different platforms.
    __previousTime = 0
    
    def __init__(self):
        groundModel = "models/gridBack"
        
        DirectObject.__init__(self)
        env = loader.loadModel(groundModel)
        
        
        # Make it visible
        env.reparentTo(render)
        
        texture = loader.loadTexture("textures/ground.png")
        
        # This is so the textures can look better from a distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        env.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        env.setTexScale(TextureStage.getDefault(), 0.1, 0.1)
        env.setTexture(texture, 1)
        
        # Make it so that it's big enough to walk on
        env.setPos(0, 0, 0)
        env.setScale(100)
        
        otherRalphsCount = 3
        otherRalphs = [NPC(self.modelStanding, 
                    {"run":self.modelRunning, "walk":self.modelWalking},
                    turnRate = 150, 
                    speed = 5,
                    agentList = self.globalAgentList,
                    collisionMask = BitMask32.bit(i+1))
                    for i in range(otherRalphsCount)]
        
        index = 1
        for ralph in otherRalphs:
            ralph.reparentTo(render)
            ralph.setScale(0.2)
            ralph.setX(5 * index)
            index += 1
            # uncomment this to make Jim happy
##            taskMgr.add(ralph.sense, "sense" + str(index))
                    
        # Make it visible
        self.ralph.reparentTo(render)
        self.ralph.setScale(0.2)
        
        stoneTexture = loader.loadTexture("textures/Stones.jpg")
        stoneTexture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        #Add some wallz
        wallModel = "models/box.egg.pz"
        wall = loader.loadModel(wallModel)
        wall.setPos(0, -10, 0)
        wall.setScale(1, 10, 10)
        wall.setTexture(stoneTexture, 1)
        
        # Add collision stuff to the wall
        tempWallCollideNodePath = wall.find("/Box")
        tempWallCollideNodePath.node().setIntoCollideMask(BitMask32.allOn())
        tempWallCollideNodePath.node().setFromCollideMask(BitMask32.allOn())
        
        # One's not enough, let's make 10!
        # Instance this wall several times
        for i in range(2):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i*10, -10, 0)
            wall.instanceTo(tempWall)
    
##        base.oobeCull()
        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.ralph)
        base.camera.setPos(0, 30, 10)
        base.camera.lookAt(self.ralph)
        base.camera.setP(base.camera.getP() + 15)
        
        self.__setKeymap()
        taskMgr.add(self.__processKey, "processKey")
        
        # now add the sense loop
        taskMgr.add(self.ralph.sense, "sense")
        
        self.isMoving = False
        
        base.setBackgroundColor(r=0, g=0, b=.1, a=1)
        
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

    def __processKey(self, task):
        elapsedTime = task.time - self.__previousTime
        turnAngle = self.ralph.turnRate * elapsedTime
        distance = self.ralph.speed * elapsedTime
        
        if self.__keyMap["left"]:
            self.ralph.turnLeft(turnAngle)
        if self.__keyMap["right"]:
            self.ralph.turnRight(turnAngle)
        if self.__keyMap["up"]:
            self.ralph.moveForward(distance)
        if self.__keyMap["down"]:
            self.ralph.moveBackward(distance)
            
        if self.__keyMap["left"] or \
            self.__keyMap["right"] or \
            self.__keyMap["up"] or \
            self.__keyMap["down"]:
            if not self.isMoving:
                self.ralph.loop("run")
                self.isMoving = True
        else:
            self.ralph.stop()
            self.ralph.pose("walk", frame = 5)
            self.isMoving = False
        
        # Store the previous time and continue
        self.__previousTime = task.time
        return Task.cont
    
    def __setKey(self, key, value):
        self.__keyMap[key] = value
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")