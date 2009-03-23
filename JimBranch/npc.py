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
from math import sqrt
from waypoint import Waypoint


class NPC(Agent):
    collisionCount = 0
    __previousTime = 0
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                agentList,
                agentName, 
                rangeFinderCount = 13,
                collisionMask=BitMask32.allOff(),
                adjacencySensorThreshold = 0,
                radarSlices = 0,
                radarLength = 0.0,
                scale = 1.0):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList, agentName)
        self.collisionMask = collisionMask
        self.adjacencySensorThreshold = adjacencySensorThreshold
        self.radarSlices = radarSlices
        self.radarLength = radarLength
        self.scale = scale
        self.turnRate = turnRate
        self.speed = speed
        self.setScale(self.scale)
        
        self.rangeFinderCount = rangeFinderCount
        self.rangeFinders = [CollisionRay() for i in range(self.rangeFinderCount)]
        self.persistentRangeFinderData = {}
        
        self.currentTarget = NodePath()
        
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
        rangeFinderCollisionNodePath.show()
        
        # Create the CollisionTraverser and the CollisionHandlerQueue
        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        
        self.traverser.addCollider(rangeFinderCollisionNodePath, self.queue)
        # Uncomment the following line to show the collisions
        self.traverser.showCollisions(render)

        self.adjacentAgents = []

        # Set up visualizations for radar
        ls = LineSegs()
        ls.setThickness(5.0)
        relativeRadarLength = float(self.radarLength) / self.scale
        ls.setColor(0, 0, 1, 1)
        for i in range(radarSlices):
            ls.moveTo(0, 0, 0)            
            ls.drawTo(relativeRadarLength * math.cos(float(i) * 2. * math.pi / float(radarSlices)), 
                      relativeRadarLength * math.sin(float(i) * 2. * math.pi / float(radarSlices)), 0)
            np = NodePath(ls.create())
            np.reparentTo(self)
            
        # Draw a circle around NPC
        circleResolution = 100
        for i in range(circleResolution):
            ls.drawTo(relativeRadarLength * math.cos(float(i) * 2. * math.pi / float(circleResolution)), 
                        relativeRadarLength * math.sin(float(i) * 2. * math.pi / float(circleResolution)), 0)
            ls.drawTo(relativeRadarLength * math.cos(float(i+1.) * 2. * math.pi / float(circleResolution)), 
                        relativeRadarLength * math.sin(float(i+1.) * 2. * math.pi / float(circleResolution)), 0)
            np = NodePath(ls.create())
            np.reparentTo(self)
        
        


    def sense(self, task):
        self.rangeFinderSense()
        self.adjacencySense()
        self.radarSense()
        return Task.cont
    
    def think(self):
        someCondition = True
        if someConditon:
            None
        return
    
    def act(self, task):
        #if(self.agentName == "ralph"):
            #This loop will be replaced with whatever 'think' decides should be sought.
        print("currentTarget = " + str(self.currentTarget.getNodeID()))
        elapsedTime = task.time - self.__previousTime
        self.seek(self.currentTarget.getPos(), elapsedTime)
##        for i in self.agentList:
##            if(i.agentName == "bunny"):
##                elapsedTime = task.time - self.__previousTime
##                self.seek(i.getPos(), elapsedTime)
        self.__previousTime = task.time
        return Task.cont
    
    rangeFinderText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                       pos=(-1.3,0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
    
    #@classmethod
    def AStar(self, target, waypoints):
        infinity = 1E400
        def getClosestNodeTo(thing):
            #Find closest Waypoint
            shortestDistanceFound = infinity
            closestNodeToSelf = Waypoint(Vec3(0,0,5))
            closestNodeIndex = 0
            for i in range(8):
                #print("distance = " + str(self.distance(self, self.waypoints[i])))
                if self.distance(thing, waypoints[i]) < shortestDistanceFound:
                    closestNodeToSelf = waypoints[i]
                    shortestDistanceFound = self.distance(thing, waypoints[i])
            return closestNodeToSelf
                    
        closestNodeToSelf = getClosestNodeTo(self)
        closestNodeToSelf.changeToYellow()
        #print("Starting node = " + str(closestNodeToSelf.getNodeID()) + " exected to be B4 which is 14") 
        closestNodeToTarget = getClosestNodeTo(target)
        #print("End node = " + str(closestNodeToTarget.getNodeID()) + "expected to be A6 which is 6")
        closestNodeToTarget.changeToGreen()
        
        
        #AStar from wiki
        def reconstructPath(cameFrom, currentNode):            
            #print("Reconstructing path")
            pathToTarget = []
            while cameFrom.has_key(currentNode):
##                print("ID of currentNode = " + str(currentNode.getNodeID()))
                pathToTarget.append(cameFrom[currentNode])
                currentNode = cameFrom[currentNode]
            pathToTarget.reverse()
            return pathToTarget
            
##            print("Reconstructing path")
##            pathToTarget = []
##            if cameFrom.has_key(currentNode):
##                print("Current Node ID = " + str(currentNode.getNodeID()))
##                returnValue = reconstructPath(cameFrom,cameFrom[currentNode])
##                if returnValue != None:
##                    pathToTarget = returnValue
##                    print("Returning something != None")
##                return pathToTarget.append(currentNode)
##            else:
##                ##print("reconstuct path returning none")
##                return None

        closedSet = []
        openSet = [closestNodeToSelf]
        gScore = {closestNodeToSelf: 0} # Distance from start along optimal path.
        hScore = {closestNodeToSelf: self.distance(closestNodeToSelf, closestNodeToTarget)}
        fScore = {closestNodeToSelf: hScore[closestNodeToSelf]} #Estimated total distance from start to goal
        
        infinity = 1E400
        cameFrom = {}
        while len(openSet) > 0:
            #print("size of openSet = " + str(len(openSet)))
            lowestFScoreFound = infinity 
            nodeWithLowestFScoreFound = None #Node in openset having lowest fScore[] value
            for waypoint in openSet:
                if fScore[waypoint] < lowestFScoreFound:
                    lowestFScoreFound = fScore[waypoint]
                    nodeWithLowestFScoreFound = waypoint
            #Make sure that something was found
            if(nodeWithLowestFScoreFound == None):
                print("Something went horribly wrong, no node found with fScore < infinity")
                
            if nodeWithLowestFScoreFound == closestNodeToTarget: #If goal is found
                returnValue = reconstructPath(cameFrom, closestNodeToTarget) #Be sure to define cameFrom
                if returnValue == None:
                    print("A* returning None")
                else:
                    print("A* is NOT returning None")
                return returnValue
            
            openSet.remove(nodeWithLowestFScoreFound)
            closedSet.append(nodeWithLowestFScoreFound)
            #print("Current node has " + str(len(nodeWithLowestFScoreFound.getNeighbors())) + " neighbors")
            for neighbor in nodeWithLowestFScoreFound.getNeighbors():
                #print("Checking neighbor " + str(neighbor.getNodeID()))
                if neighbor in closedSet:
                    continue
                neighborGScore = gScore[nodeWithLowestFScoreFound] + self.distance(nodeWithLowestFScoreFound, neighbor)
                #Assume that neighbor is not better than what we have
                neighborIsBetter = False
                if neighbor not in openSet:
                    openSet.append(neighbor)
                    hScore[neighbor] = self.distance(neighbor, closestNodeToTarget)
                    neighborIsBetter = True
                elif neigborGScore < gScore[neighbor]:
                    neighborIsBetter = True
                if neighborIsBetter:
                    cameFrom[neighbor] = nodeWithLowestFScoreFound
                    ##print("cameFrom is type " + str(type(cameFrom)))
                    gScore[neighbor] = neighborGScore
                    fScore[neighbor] = gScore[neighbor] + hScore[neighbor]
        print("Returning NONE from A*")
        return None

    #@staticmethod
    def distance(self, source, target):
        xComponent = source.getX() - target.getX()
        yComponent = source.getY() - target.getY()
        return math.hypot(xComponent, yComponent)

#########################################
##########################################
########################################
#######################################
##########################################
    def followPath(self, path, target, task):
        if len(path) > 0:
            nextWaypoint = path[0]
            #print("followPath() distance = " + str(self.distance(self, nextWaypoint)))
            if self.distance(self, nextWaypoint) < 1:
                #print("WAYPOINT FOUND, UPDATING CURRENT TARGET")
                path.pop(0)
                if len(path) > 0:
                    nextWaypoint = path[0]
                #print("Telling Ralph to seek waypoint:" + str(nextWaypoint.getNodeID()))
                self.currentTarget = nextWaypoint
                #print("Set self.currentTarget to node " + str(self.currentTarget.getNodeID()) + " at position " + str(self.currentTarget.getX()) + ", " + str(self.currentTarget.getY()))
                #self.setCurrentTarget(path.pop(0))
        else:
            #print("Telling Ralph to seek final Target")
            self.setCurrentTarget(target)
        return Task.cont
        
        
        
    def getCurrentTarget(self):
        return self.currentTarget
    
    def setCurrentTarget(self, target):
        self.currentTarget = target
        
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

        self.rangeFinderText.setText("Range Data (feelers): " + str(pd))
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
                    self.adjacencyTexts[agent].setText("Agent " + str(index) + ": (" + 
                            str(agent.getPos().getX()) + ", " +
                            str(agent.getPos().getY()) + ") at heading " + 
                            str(agent.getH()))
                else:   
                    if agent in self.adjacentAgents:
                        self.adjacentAgents.remove(agent)
            index += 1
        
        self.adjacencyText.setText("Adjacent Agents: " + str(len(self.adjacentAgents)))
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
            if self != agent and self.getPos() != agent.getPos():        

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
            
        self.radarText.setText("Radar (Pie Slice): " + str(self.radarActivationLevels))
        return
    
    def seek(self, position, elapsedTime):
        #print("Seeking position " + str(position.getX()) + ", " + str(position.getY()))
        #print("Current position " + str(self.getX())     + ", " + str(position.getY()))
        worldPosition = self.getPos()
        worldTargetPosition = position
        worldHeading = self.getH()
        worldHeading = worldHeading % 360
        worldYDirection = worldTargetPosition.getY() - worldPosition.getY()
        worldXDirection = worldTargetPosition.getX() - worldPosition.getX()
        worldDirectionToTarget = math.degrees(math.atan2(worldYDirection, worldXDirection))
        distanceToTarget = math.sqrt(worldYDirection * worldYDirection + worldXDirection * worldXDirection)
        #print("distanceToTarget = " + str(distanceToTarget))
        angleToTarget = worldDirectionToTarget - worldHeading + 180
        angleToTarget = angleToTarget % 360
        turnAngle = self.turnRate * elapsedTime
        distance = self.speed * elapsedTime

        if(distanceToTarget < self.radarLength):
            #print("Target is in range")
            if(distanceToTarget < 1):
                self.moveForward(0)#do nothing
            elif(80 <= angleToTarget and angleToTarget <= 100):
                self.moveForward(distance)
            elif(0 <= angleToTarget and angleToTarget < 90):
                #self.moveForward(0)#do nothing
                #self.moveForward(distance)
                #self.turnLeft(turnAngle)
                self.turnRight(turnAngle)
            elif(90 <= angleToTarget and angleToTarget < 180):
                #self.moveForward(0)#do nothing
                #self.moveForward(distance)
                self.turnLeft(turnAngle)
                #self.turnRight(turnAngle)
            elif(180 <= angleToTarget and angleToTarget < 270):
                self.moveForward(0)#do nothing
                #self.moveForward(distance)
                self.turnLeft(turnAngle)
                #self.turnRight(turnAngle)
            elif(270 <= angleToTarget and angleToTarget < 360):
                self.moveForward(0)#do nothing
                #self.moveForward(distance)
                #self.turnLeft(turnAngle)
                self.turnRight(turnAngle)
            else:
                print("You can start crying now.")
        else:
            print("Target is out of range")
        return

if __name__ == "__main__":
    N = NPC("models/ralph",
            {"run":"models/ralph-run"},
            turnRate = 5,
            speed = 100,
            agentList = [],
            agentName = "")
    print ("compiled good")
    