from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import Vec3
from direct.task import Task
import math

class NPC(Agent):

    def __init__(self, modelStanding, modelAnimationDict, turnRate, speed):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed)
        
        self.rangeFinderCount = 13
        self.rangeFinders = [CollisionRay() for i in range(self.rangeFinderCount)]
        
        # Set up the range finders                            
        rangeFinderCollisionNode = CollisionNode("rangeFinders")
        deviation = 180 / (self.rangeFinderCount-1)
        angle = 0
        for rangeFinder in self.rangeFinders:
            rangeFinder.setOrigin(self.getX(), self.getY(), self.getZ() + 3.5)
            
            rangeFinder.setDirection(math.cos(math.radians(angle)),
                                    -math.sin(math.radians(angle)),
                                    0)
            
            # This is purely to make them visible
            rangeFinderCollisionNode.addSolid(rangeFinder)
            angle += deviation
            
        rangeFinderCollisionNodePath = self.attachNewNode(rangeFinderCollisionNode)
        rangeFinderCollisionNodePath.show()
        
        # Now set up the persistent data
        self.persistentRangeFinderData = [0] * self.rangeFinderCount
        
        # Create the CollisionTraverser and the CollisionHandlerQueue
        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

    def sense(self, task):
##        index = 0
##        for rangeFinder in self.rangeFinders:
##            # since rangeFinder is relative to our agent, we don't need to subtract the origins
##            transform = rangeFinder.getCollisionOrigin()
##            self.persistentRangeFinderData[index] = transform.length()
##            index += 1
        # Try to create a collision handler queue, and parse through it.
        for i in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(i)
            print(entry)
        return Task.cont
    
    def think(self):
        return
    
    def act(self):
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100)
    print ("compiled good")