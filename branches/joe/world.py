# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
import sys

class World(DirectObject):
    __model = "models/misc/gridBack"
        
    # Now to make our first agent
    __modelStanding = "models/ralph"
    __modelRunning = "models/ralph-run"
    __ralph = NPC(__modelStanding, __modelRunning)
    
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
        self.__ralph.reparentTo(render)
        self.__ralph.setScale(0.2)
        
##        base.oobeCull()
        base.disableMouse()
        base.camera.reparentTo(self.__ralph)
        base.camera.setPos(0, 20, 10)
        base.camera.lookAt(self.__ralph)
        base.camera.setP(base.camera.getP() + 15)
        
        self.__setKeys()
        
    def __setKeys(self):
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.__ralph.turnLeft)
        self.accept("arrow_right", self.__ralph.turnRight)
        self.accept("arrow_up", self.__ralph.moveForward)
        self.accept("arrow_down", self.__ralph.moveBackward)
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")
