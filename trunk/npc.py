from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import Vec3
import math

class NPC(Agent):

    def __init__(self, modelStanding, modelAnimationDict, turnRate, speed):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed)
        self.rangeFinderCount = 30
        self.rangeFinders = []
        for i in range(self.rangeFinderCount):
            self.rangeFinders.append(CollisionRay())
            
        # Set up the range finders
                                    
        rangeFinderCollisionNode = CollisionNode("rangeFinders")
        deviation = 180 / (self.rangeFinderCount-1)
        angle = 0
        for rangeFinder in self.rangeFinders:
            rangeFinder.setOrigin(self.getX(), self.getY(), self.getZ() + 3.5)
            
            rangeFinder.setDirection(math.cos(math.radians(angle)),
                                    -math.sin(math.radians(angle)),
                                    0)
            
            rangeFinderCollisionNode.addSolid(rangeFinder)
            angle += deviation
            
        rangeFinderCollisionNodePath = self.attachNewNode(rangeFinderCollisionNode)
        rangeFinderCollisionNodePath.show()
        
    def sense(self):
        return
    
    def think(self):
        return
    
    def act(self):
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"}, \
            turnRate = 5,
            speed = 100)
    print ("compiled good")