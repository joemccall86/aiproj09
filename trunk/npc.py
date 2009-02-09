from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import Vec3
from pandac.PandaModules import BitMask32
from direct.task import Task
import math

class NPC(Agent):
    collisionCount = 0
    
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                positionDictionary, 
                collisionMask=BitMask32.allOff(),
                adjacencySensorThreshold = 0):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, positionDictionary)
        self.collisionMask = collisionMask
        self.adjacencySensorThreshold = adjacencySensorThreshold
        
        self.rangeFinderCount = 13
        self.rangeFinders = [CollisionRay() for i in range(self.rangeFinderCount)]
        self.persistentRangeFinderData = {}
        for rangeFinder in self.rangeFinders:
            self.persistentRangeFinderData[rangeFinder] = 0
            
        
        
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

            # Set the Collision mask
            rangeFinderCollisionNode.setFromCollideMask(self.collisionMask)
            rangeFinderCollisionNode.setIntoCollideMask(self.collisionMask)
            
            angle += deviation
            
        rangeFinderCollisionNodePath = self.attachNewNode(rangeFinderCollisionNode)
        # Uncomment the following line to show the collision rays
##        rangeFinderCollisionNodePath.show()
        
        # Create the CollisionTraverser and the CollisionHandlerQueue
        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        
        self.traverser.addCollider(rangeFinderCollisionNodePath, self.queue)
        # Uncomment the following line to show the collisions
##        self.traverser.showCollisions(render)

        self.adjacentAgents = []

    def sense(self, task):
        self.rangeFinderSense()
        self.adjacencySense()
        return Task.cont
    
    def think(self):
        return
    
    def act(self):
        return
    
    def rangeFinderSense(self):
        self.traverser.traverse(render)
        for rangeFinder in self.rangeFinders:
            self.persistentRangeFinderData[rangeFinder] = 0
        for i in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(i)
            point = entry.getSurfacePoint(self)
            length = point.length()
            self.persistentRangeFinderData[entry.getFrom()] = length
        
##        pd = []
##        for i in range(self.rangeFinderCount):
##            pd.append(self.persistentRangeFinderData[self.rangeFinders[i]])
##        print(pd)
        return
    
    def adjacencySense(self):
        # loop thru the positionDictionary
        for position in self.positionDictionary.items():
            if self != position[0]:
                transform = self.getPos() - position[-1]
                distance = transform.length()
                if distance <= self.adjacencySensorThreshold:
                    if position[0] not in self.adjacentAgents:
                        self.adjacentAgents.append(position[0])
                else:
                    if position[0] in self.adjacentAgents:
                        self.adjacentAgents.remove(position[0])
                        
##        print(len(self.adjacentAgents))
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100)
    print ("compiled good")