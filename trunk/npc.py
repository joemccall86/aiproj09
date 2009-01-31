from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import Vec3
import math

class NPC(Agent):

    def __init__(self, modelStanding, modelRunning, turnRate, speed):
        Agent.__init__(self, modelStanding, modelRunning, turnRate, speed)
        self.rangeFinderCount = 5
        self.rangeFinders = []
        for i in range(self.rangeFinderCount):
            self.rangeFinders.append(CollisionRay())
            
        # Set up the range finders
        deviation = 180 / self.rangeFinderCount
        angle = 0
        for rangeFinder in self.rangeFinders:
            rangeFinder.setOrigin(self.getX(), self.getY(), self.getZ() + 5)
            rangeFinder.setDirection(self.getX() + math.cos(self.getH()+deviation),
                                    self.getY() + math.sin(self.getH()+deviation),
                                    0)
                                    
            rangeFinderCollision = CollisionNode("rangeFinder")
            rangeFinderCollision.addSolid(rangeFinder)
##            rangeFinderColision.setFromCollideMask(BitMask32.bit(0))
##            rangeFinderColision.setIntoCollideMask(BitMask32.allOff())
                                    
##            rangeFinderCollisionNodePointer = self.attachNewNode(rangeFinderCollision) 
##            rangeFinderCollisionNodePointer.show()
            
            angle += deviation
        
        self.rangeFinderCollisions = []
        for i in range(self.rangeFinderCount):
            self.rangeFinderCollisions.append(CollisionNode("rangeFinder" + str(i)))
            self.rangeFinderCollisions[i].addSolid(self.rangeFinders[i])
            
        
        self.rangeFinderCollisionNodePointers = []
        for i in range(self.rangeFinderCount):
            
            pointer = self.attachNewNode(self.rangeFinderCollisions[i])
            self.rangeFinderCollisionNodePointers.append(pointer)
            self.rangeFinderCollisionNodePointers[i].show()
            
        
        
        rangeFinderCollision
    def sense(self):
        return
    
    def think(self):
        return
    
    def act(self):
        return

if __name__ == "__main__":
    N = NPC(modelStanding = "models/ralph",
            modelRunning = "models/ralph-run",
            turnRate = 5,
            speed = 100)
    print ("compiled good")