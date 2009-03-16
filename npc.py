from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import Vec3, Vec2
from pandac.PandaModules import BitMask32
from pandac.PandaModules import LineSegs
from pandac.PandaModules import NodePath
from pandac.PandaModules import TextNode
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import random
import math
        
def RandGenerator():
    while True:
        random.seed()
        yield random.uniform(-1000, 1000)
        
RG = RandGenerator()
        
class NPC(Agent):
    collisionCount = 0
    
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                agentList, 
                rangeFinderCount = 13,
                collisionMask=BitMask32.allOff(),
                adjacencySensorThreshold = 0,
                radarSlices = 0,
                radarLength = 0.0,
                scale = 1.0):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList)
        self.collisionMask = collisionMask
        self.adjacencySensorThreshold = adjacencySensorThreshold
        self.radarSlices = radarSlices
        self.radarLength = radarLength
        self.scale = scale
        
        self.setScale(self.scale)
        
        self.rangeFinderCount = rangeFinderCount
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
        relativeRadarLength = float(self.radarLength) / self.scale
        ls.setColor(0, 0, 1, 1)
##        for i in range(radarSlices):
##            ls.moveTo(0, 0, 0)            
##            ls.drawTo(relativeRadarLength * math.cos(float(i) * 2. * math.pi / float(radarSlices)), 
##                      relativeRadarLength * math.sin(float(i) * 2. * math.pi / float(radarSlices)), 0)
##            np = NodePath(ls.create())
##            np.reparentTo(self)
##            
##        # Draw a circle around NPC
##        circleResolution = 100
##        for i in range(circleResolution):
##            ls.drawTo(relativeRadarLength * math.cos(float(i) * 2. * math.pi / float(circleResolution)), 
##                        relativeRadarLength * math.sin(float(i) * 2. * math.pi / float(circleResolution)), 0)
##            ls.drawTo(relativeRadarLength * math.cos(float(i+1.) * 2. * math.pi / float(circleResolution)), 
##                        relativeRadarLength * math.sin(float(i+1.) * 2. * math.pi / float(circleResolution)), 0)
##            np = NodePath(ls.create())
##            np.reparentTo(self)        


    def sense(self, task):
        self.rangeFinderSense()
        self.adjacencySense()
        self.radarSense()
        return Task.cont
    
    def think(self, task):
        self.ANNThink()
        return Task.cont
    
    isMoving = False
    def act(self, task):
        # Based on the neural node outputs, run forward and turn however we need to.
        try:
            if not self.timers.has_key(self.act):
                self.timers[self.act] = 0.0
        except AttributeError:
            self.timers = {}
            self.timers[self.act] = 0.0
            
        elapsedTime = task.time - self.timers[self.act]
        distance = self.speed * elapsedTime
        
        self.moveForward(distance)
        
        if not self.isMoving:
            self.isMoving = True
            self.loop("run")
        
        self.timers[self.act] = task.time
        return Task.cont
    
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

##        self.rangeFinderText.setText("Range Data (feelers): " + str(pd))
        return
    
    adjacencyText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                                 pos=(-1.3,0.90), align=TextNode.ALeft, scale = .05, mayChange = True)

    adjacencyTexts = {}
    def adjacencySense(self):
        # loop thru the positionDictionary
        index = 0
        for agent in self.agentList:
            if not self.adjacencyTexts.has_key(agent):
                self.adjacencyTexts[agent] = OnscreenText(text="", style=1, fg=(1,1,1,1),
                        pos=(-1.3,-0.85 + (index*0.05)), align=TextNode.ALeft, scale = .05, mayChange = True)
                index += 1
        index = 0
        for agent in self.agentList:
            if self != agent:
                transform = self.getPos() - agent.getPos()
                distance = transform.length()
                self.adjacencyTexts[agent].clearText()
                if distance <= self.adjacencySensorThreshold:
                    if agent not in self.adjacentAgents:
                        self.adjacentAgents.append(agent)
##                    self.adjacencyTexts[agent].setText("Agent " + str(index) + ": (" + 
##                            str(agent.getPos().getX()) + ", " +
##                            str(agent.getPos().getY()) + ") at heading " + 
##                            str(agent.getH()))
                else:   
                    if agent in self.adjacentAgents:
                        self.adjacentAgents.remove(agent)
            index += 1
        
##        self.adjacencyText.setText("Adjacent Agents: " + str(len(self.adjacentAgents)))
        return
    
    radarText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                             pos=(-1.3,0.85), align=TextNode.ALeft, scale = .05, mayChange = True)
##    angleText = OnscreenText(text="", style=1, fg=(1,1,1,1),
##                             pos=(-1.3,0.80), align=TextNode.ALeft, scale = .05, mayChange = True)
##    transformAngleText = OnscreenText(text="", style=1, fg=(1,1,1,1),
##                             pos=(-1.3,0.75), align=TextNode.ALeft, scale = .05, mayChange = True)
##    getHText = OnscreenText(text="", style=1, fg=(1,1,1,1),
##                             pos=(-1.3,0.70), align=TextNode.ALeft, scale = .05, mayChange = True)
    def radarSense(self):
        self.radarActivationLevels = [0] * self.radarSlices
        for agent in self.agentList:
            if self != agent:        

                transform = agent.getPos() - self.getPos()
                if transform.length() > self.radarLength:
                    continue
                # Handle the special case
                if transform.getX() == 0:
                    if transform.getY() < 0:
                        transformAngle = 3. * math.pi / 2
                    else:
                        transformAngle = math.pi / 2
                else:
                    transformAngle = math.atan2(transform.getY(), transform.getX())
                        
##                ls = LineSegs()
##                ls.setThickness(5.0)
##                ls.moveTo(self.getPos())
##                ls.drawTo(transform.length() * math.cos(transformAngle) / self.scale, transform.length() * math.sin(transformAngle) / self.scale, 0)
##                np = NodePath(ls.create("arst"))
##                np.reparentTo(render)
            
##                self.transformAngleText.setText("transformAngle = " + str(math.degrees(transformAngle)))
##                self.getHText.setText("self.getH() = " + str(self.getH()))
                
                transformAngle -= math.radians(self.getH())
                while transformAngle >= 2. * math.pi:
                    transformAngle -= (2. * math.pi)
                while transformAngle < 0.0:
                    transformAngle += (2. * math.pi)
                
##                self.angleText.clearText()
##                self.angleText.setText(str(math.degrees(transformAngle)))
                    
                orthant = int(self.radarSlices * transformAngle / (2. * math.pi))
                orthant = self.radarSlices - orthant - 1
                    
                self.radarActivationLevels[orthant] += 1
            
##        self.radarText.setText("Radar (Pie Slice): " + str(self.radarActivationLevels))
        return

    @classmethod
    def RandomClamped(self):
        r = float(RG.next())
        r /= 1000
        return r
            
    wanderTarget = Vec2(0.0, 0.0)
    previousTime = 0.0
    callCount = 0
    def wanderTask(self, task):
        self.callCount += 1
        wanderCircleRadius = 2.5
        if self.callCount == 5:
            jitter = 50.
            self.wanderTarget += Vec2(
                self.RandomClamped() * jitter, 
                self.RandomClamped() * jitter)
            self.wanderTarget.normalize()
            self.wanderTarget *= wanderCircleRadius
            self.callCount = 0
        
        # Now move the circle in front of us
        # First grab the absolute coordinates. We want to move it 'up' wanderDistance
        wanderDistance = 5.0
        theta = math.atan2(self.wanderTarget.getY(),self.wanderTarget.getX())
        relativeX = (wanderCircleRadius * math.cos(theta))
        relativeY = (wanderCircleRadius * math.sin(theta)) - wanderDistance
        targetLocal = Vec2(relativeX, relativeY)
        
##        # For the hell of it, let's draw the circle
##        if not self.isMoving:
##            circleLineSegs = LineSegs()
##            circleLineSegs.setColor(0, 0, 1)
##            circleLineSegs.moveTo(wanderCircleRadius/self.scale, -wanderDistance/self.scale, 0)
##            circleResolution = 20
##            for i in range(1.0+circleResolution):
##                if 0 == i: continue
##                theta = i*2.0*math.pi/circleResolution
##                R = wanderCircleRadius / self.scale
##                xcoord = R * math.cos(theta)
##                ycoord = R * math.sin(theta)
##                # Move it ahead of us
##                ycoord -= wanderDistance / self.scale
##                circleLineSegs.drawTo(xcoord, ycoord, 0)
##            NodePath(circleLineSegs.create()).reparentTo(self)
##            
##            # Now plot the point on the circle
##            self.pointLineSegs = LineSegs()
##            self.pointLineSegs.setColor(1, 0, 0)
##            self.pointLineSegs.moveTo(0,0,0)
##            
##            self.pointNodePath = None
##            
##        if self.pointNodePath != None:
##            self.pointNodePath.removeNode()
##            self.pointNodePath = None
##        
##        self.pointLineSegs.moveTo(0,0,0)
##        self.pointLineSegs.drawTo(targetLocal.getX()/self.scale, 
##            targetLocal.getY()/self.scale, 0)
##        self.pointNodePath = NodePath(self.pointLineSegs.create())
##        self.pointNodePath.reparentTo(self)
            
            
        # Leave a trail
##        ls = LineSegs()
##        ls.setThickness(2.0)
##        ls.setColor(0, 0, 1)
##        ls.moveTo(self.getPos())
##        NodePath(ls.create()).reparentTo(render)
        
        elapsedTime = task.time - self.previousTime
        distance = self.speed * elapsedTime
        turnAngle = self.turnRate * elapsedTime
        
        # Now we have a relative target. We should go there.
        heading = math.atan2(targetLocal.getY(), targetLocal.getX())
        degreesHeading = math.degrees(heading)
        if -90.0 < degreesHeading and degreesHeading <= 0.0:
            self.turnLeft(turnAngle)
        else:
            self.turnRight(turnAngle)
        
        self.moveForward(distance)
        
        # He's always going to be moving, so let's make him loop the animation.
        if not self.isMoving:
            self.loop("run")
            self.isMoving = True
        
        self.previousTime = task.time
        return Task.cont
    
    #  So we need to define a lifetime for a generation and run it. 
    #  Inputs: Radar Activation Levels
    #  Outputs: Turn Left n degrees, Turn Right n degrees
    
    lifetimeTicks = 500
    ANNThinkCallCount = 0
    tickCount = 0
    def ANNThink(self):
        """ 
        This method is called by the think task to implement an ANN using
        neat-python. Its inputs are the radar activation levels and its
        outputs are movement requests. 
        """
        self.ANNThinkCallCount += 1
        if self.ANNThinkCallCount == self.lifetimeTicks:
            self.tickCount += 1
            self.ANNThinkCallCount = 0
            # Start over
            self.setPos(0,0,0)
            
        
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100,
            agentList = [])
    print ("compiled good")
    
