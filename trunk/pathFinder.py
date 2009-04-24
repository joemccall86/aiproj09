from waypoint import Waypoint
from pandac.PandaModules import Vec3

import math
from math import sqrt

class PathFinder():
    
##    def __init__(self, position, ID = -1):
##        NodePath.__init__(self, "Waypoint")
##        self.position = position
##        self.texture = loader.loadTexture("textures/blue.jpg")
##        self.costToThisNode = 0
##        self.visited = False
##        self.neighbors = []
##        self.ID = ID
##        self.previousWaypoint = None

    @classmethod
    def AStar(self, source, target, waypoints):
##        print "AStar called"
        infinity = 1E400
        
##  def castRayToNextTarget(self):
##        if self.bestPath:
##            if len(self.bestPath) > 1:
##                worldPosition = self.getPos()
##                worldTargetPosition = self.player.getPos()
##                worldHeading = self.getH()
##                worldHeading = worldHeading % 360
##                worldYDirection = worldTargetPosition.getY() - worldPosition.getY()
##                worldXDirection = worldTargetPosition.getX() - worldPosition.getX()
##                worldDirectionToTarget = math.degrees(math.atan2(worldYDirection, worldXDirection))
##                distanceToTarget = math.sqrt(worldYDirection * worldYDirection + worldXDirection * worldXDirection)
##                #print("distanceToTarget = " + str(distanceToTarget))
##                angleToTarget = worldDirectionToTarget - worldHeading + 180
##                angleToTarget = angleToTarget % 360
##                
##                self.targetTrackerCollisionNodePath.lookAt(self.bestPath[1])         
# self.distanceToWall = entry.getSurfacePoint(self).length()
        def waypointIsReachable(thing, waypoint):
            #Calculate distance between waypoint and thing.
##            thingPosition = thing.getPos()
##            waypointPosition = waypoint.getPos()
##            worldYDirection = waypointPosition.getY() - thingPosition.getY()
##            worldXDirection = waypoint.getX() - thingPosition.getX()
##            distanceToTarget = math.sqrt(worldYDirection * worldYDirection + worldXDirection * worldXDirection)
            distanceToTarget = thing.getDistance(waypoint)

            
            #Calculate direction from thing to waypoint
            worldYDirection = waypoint.getY() - thing.getY()
            worldXDirection = waypoint.getX() - thing.getX()
            directionToTarget = math.degrees(math.atan2(worldYDirection, worldXDirection))
            directionToTarget = directionToTarget % 360
            
            #Calculate distance to wall
            distanceToWall = 1E400 #This represnts infinity... Replace with actual value once calculated.
            
            
            #Compare "distance to thing" to "distance to wall" to decide if there is a wall in the way.
            if(distanceToTarget < distanceToWall):
                return True
            else:
                return False
        
        def getClosestNodeTo(thing):
            #Make sure there is a direct path between thing and the nearestWaypoint.
            possiblyReachableWaypoints = waypoints
            
            #Find closest Waypoint
            shortestDistanceFound = infinity
            closestNodeToSource = Waypoint(Vec3(0,0,5))
            closestNodeIndex = 0
            for i in range(len(waypoints)):
                #print("distance = " + str(self.distance(self, self.waypoints[i])))
                if self.distance(thing, possiblyReachableWaypoints[i]) < shortestDistanceFound \
                                            and waypointIsReachable(thing, possiblyReachableWaypoints[i]):
                    closestNodeToSource = possiblyReachableWaypoints[i]
                    shortestDistanceFound = self.distance(thing, possiblyReachableWaypoints[i])
            return closestNodeToSource
        
##        print("Got here")
        closestNodeToSource = getClosestNodeTo(source)
        
##        print("Closest Node = " + str(closestNodeToSource.getNodeID()) + " at pos (" + str(closestNodeToSource.getX()) + ", " + str(closestNodeToSource.getY())) + ")"
        closestNodeToSource.changeToYellow()
        #print("Starting node = " + str(closestNodeToSelf.getNodeID()) + " exected to be B4 which is 14") 
        closestNodeToTarget = getClosestNodeTo(target)
        #print("End node = " + str(closestNodeToTarget.getNodeID()) + "expected to be A6 which is 6")
        closestNodeToTarget.changeToGreen()
        
        
        #AStar from wiki
        def reconstructPath(cameFrom, currentNode):            
            #print("Reconstructing path")
            pathToTarget = [currentNode]
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
        openSet = [closestNodeToSource]
        gScore = {closestNodeToSource: 0} # Distance from start along optimal path.
        hScore = {closestNodeToSource: self.distance(closestNodeToSource, closestNodeToTarget)}
        fScore = {closestNodeToSource: hScore[closestNodeToSource]} #Estimated total distance from start to goal
        
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
##                if returnValue == None:
##                    print("A* returning None")
##                else:
##                    print("A* is NOT returning None")
                return returnValue + [target]
            
            openSet.remove(nodeWithLowestFScoreFound)
            closedSet.append(nodeWithLowestFScoreFound)
            #print("Current node has " + str(len(nodeWithLowestFScoreFound.getNeighbors())) + " neighbors")
            for neighbor in nodeWithLowestFScoreFound.getNeighbors():
                #print("Checking neighbor " + str(neighbor.getNodeID()))
                if neighbor in closedSet:
                    continue
                neighborGScore = gScore[nodeWithLowestFScoreFound] + self.distance(nodeWithLowestFScoreFound, neighbor)
##                print("neighborGScore = " + str(neighborGScore))
                #print("gScore[neighbor] = " + str(gScore[neighbor]))
                #Assume that neighbor is not better than what we have
                neighborIsBetter = False
                if neighbor not in openSet:
                    openSet.append(neighbor)
                    hScore[neighbor] = self.distance(neighbor, closestNodeToTarget)
                    neighborIsBetter = True
                elif neighborGScore < gScore[neighbor]:
                    neighborIsBetter = True
                if neighborIsBetter:
                    cameFrom[neighbor] = nodeWithLowestFScoreFound
                    ##print("cameFrom is type " + str(type(cameFrom)))
                    gScore[neighbor] = neighborGScore
                    fScore[neighbor] = gScore[neighbor] + hScore[neighbor]
##        print("Returning NONE from A*")
        return None
    
    @staticmethod
    def distance(source, target):
        return source.getDistance(target)
