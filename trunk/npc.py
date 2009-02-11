from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import Vec3
from pandac.PandaModules import BitMask32
from pandac.PandaModules import LineSegs
from pandac.PandaModules import NodePath
from pandac.PandaModules import TextNode
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import math

class NPC(Agent):
    collisionCount = 0
    
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                agentList, 
                collisionMask=BitMask32.allOff(),
                adjacencySensorThreshold = 0,
                radarSlices = 0,
                radarLength = 0.0):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList)
        self.collisionMask = collisionMask
        self.adjacencySensorThreshold = adjacencySensorThreshold
        self.radarSlices = radarSlices
        self.radarLength = radarLength
        
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
        
        # Set up visualizations for radar
        
        ls = LineSegs()
        ls.setThickness(5.0)
        ls.setColor(0, 0, 1, 1)
        for i in range(radarSlices):
            ls.moveTo(0, 0, 0)
            ls.drawTo(self.radarLength * math.cos(i * 2 * math.pi / radarSlices), 
                      self.radarLength * math.sin(i * 2 * math.pi / radarSlices), 0)
            ls.drawTo(self.radarLength * math.cos((i+1) * 2 * math.pi / radarSlices), 
                      self.radarLength * math.sin((i+1) * 2 * math.pi / radarSlices), 0)
            np = NodePath(ls.create())
            np.reparentTo(self)
            

    def sense(self, task):
        self.rangeFinderSense()
        self.adjacencySense()
        self.radarSense()
        return Task.cont
    
    def think(self):
        return
    
    def act(self):
        return
    
    rangeFinderText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                       pos=(-1.3,0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
    def rangeFinderSense(self):
        self.traverser.traverse(render)
        for rangeFinder in self.rangeFinders:
            self.persistentRangeFinderData[rangeFinder] = 0
        for i in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(i)
            point = entry.getSurfacePoint(self)
            length = point.length()
            self.persistentRangeFinderData[entry.getFrom()] = length

        pd = []
        for i in range(self.rangeFinderCount):
            pd.append(int(self.persistentRangeFinderData[self.rangeFinders[i]]))

        self.rangeFinderText.clearText()
        self.rangeFinderText.setText(str(pd))
        return
    
    adjacencyText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                                 pos=(-1.3,0.90), align=TextNode.ALeft, scale = .05, mayChange = True)
    def adjacencySense(self):
        # loop thru the positionDictionary
        for agent in self.agentList:
            if self != agent:
                transform = self.getPos() - agent.getPos()
                distance = transform.length()
                if distance <= self.adjacencySensorThreshold:
                    if agent not in self.adjacentAgents:
                        self.adjacentAgents.append(agent)
                else:
                    if agent in self.adjacentAgents:
                        self.adjacentAgents.remove(agent)
                        
        self.adjacencyText.clearText()
        self.adjacencyText.setText(str(len(self.adjacentAgents)))
        return
    
    radarText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                             pos=(-1.3,0.85), align=TextNode.ALeft, scale = .05, mayChange = True)
##    angleText = OnscreenText(text="", style=1, fg=(1,1,1,1),
##                             pos=(-1.3,0.80), align=TextNode.ALeft, scale = .05, mayChange = True)
    def radarSense(self):
        self.radarActivationLevels = [0] * self.radarSlices
        angleStep = 360.0 / self.radarSlices
        for agent in self.agentList:
            if self != agent:
                transform = self.getPos() - agent.getPos()
                if transform.length() > self.radarLength:
                    continue
                # Handle the special case
                if transform.getX() == 0:
                    if transform.getY() < 0:
                        transformAngle = 270.0
                    else:
                        transformAngle = 90.0
                else:
                    transformAngle = math.atan(transform.getY()/transform.getX())
                    transformAngle = math.degrees(transformAngle)
                    if transform.getY() < 0 and transform.getX() < 0:
                        transformAngle += 180.0
                    elif transform.getX() < 0:
                        transformAngle = 180.0 - transformAngle
                    elif transform.getY() < 0:
                        transformAngle = 360.0 - transformAngle
            
                transformAngle += self.getH()
                while transformAngle >= 360.0:
                    transformAngle -= 360.0
                while transformAngle < 0.0:
                    transformAngle += 360.0
                
##                self.angleText.clearText()
##                self.angleText.setText(str(transformAngle))
                    
                orthant = int(transformAngle // angleStep) # // means floor
                self.radarActivationLevels[orthant] += 1
            
        self.radarText.clearText()
        self.radarText.setText(str(self.radarActivationLevels))
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100,
            agentList = [])
    print ("compiled good")
    