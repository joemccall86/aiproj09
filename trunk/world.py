# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
import sys
from direct.task import Task

class World(DirectObject):
    __model = "models/misc/gridBack"
        
    # Now to make our first agent
    modelStanding = "models/ralph"
    modelRunning = "models/ralph-run"
    ralph = NPC(modelStanding, modelRunning)
    
    
    # Key map dictionary; These represent the keys pressed
    __keyMap = {"left":False, "right":False, "up":False, "down":False}
    
    # Keep track of time at previous frame to keep speed consistant on different platforms.
    __previousTime = 0
    
    def __init__(self):
        DirectObject.__init__(self)
        env = loader.loadModel(self.__model)
        
        
        # Make it visible
        env.reparentTo(render)
        
        texture = loader.loadTexture("textures/ground.png")
        
        # This is so the textures can look better from a distance
##        texture.setMinfilter(Texture.FTLinearMipmapNearest)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        env.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        env.setTexture(texture, 1)
        
        # Make it so that it's big enough to walk on
        env.setPos(0, 0, 0)
        env.setScale(100)
        
        # Make it visible
        self.ralph.reparentTo(render)
        self.ralph.setScale(0.2)
        
##        base.oobeCull()
        base.disableMouse()
        base.camera.reparentTo(self.ralph)
        base.camera.setPos(0, 20, 10)
        base.camera.lookAt(self.ralph)
        base.camera.setP(base.camera.getP() + 15)
        
        self.__setKeymap()
        taskMgr.add(self.__processKey, "processKey")
        
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
        if self.__keyMap["left"]:
            self.ralph.turnLeft()
        if self.__keyMap["right"]:
            self.ralph.turnRight()
        if self.__keyMap["up"]:
            self.ralph.moveForward()
        if self.__keyMap["down"]:
            self.ralph.moveBackward()
        return Task.cont
    
    def __setKey(self, key, value):
        self.__keyMap[key] = value
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")