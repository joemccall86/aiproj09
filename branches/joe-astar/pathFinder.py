from waypoint import Waypoint
from pandac.PandaModules import BitMask32
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import NodePath
from pandac.PandaModules import Point3
from pandac.PandaModules import Vec3

import psyco
psyco.full()

import math
from math import sqrt

# So this is what I'm going to do. Since PathFinder does not need to be a 
# class, I'm going to make it a simple module instead

wallRayNP = NodePath(CollisionNode("wall ray collision node"))
# THIS IS A HACK!!!! We should find out what this can point to.
wallRayNP.node().addSolid(CollisionRay(0,0,0,0,0,1))
#wallRayNP.node().setIntoCollideMask(BitMask32.allOff())
#wallRayNP.node().setFromCollideMask(BitMask32.allOn())
wallRayNP.show()
wallRayDistance = 0

collisionHandler = CollisionHandlerQueue()
collisionTraverser = CollisionTraverser("pathfinder's collisionTraverser")
collisionTraverser.setRespectPrevTransform(True)
collisionTraverser.addCollider(wallRayNP, collisionHandler)

def AStar(source, target, waypoints):
    infinity = 1E400
    
    def waypointIsReachable(source, waypoint):
        """
        Determines whether the waypoint is reachable from NodePath source
        
        Currently this function does not work. Eventually it will cast a collision
        ray to the waypoint, and check for collisions. If collisions happen before
        it reaches the waypoint, then this function will return false. Otherwise it
        will return true.
        
        For now it will always return true because it's not fully implemented yet.
        """
        
        return True
        
        #Calculate direction from source to waypoint
        worldYDirection = waypoint.getY() - source.getY()
        worldXDirection = waypoint.getX() - source.getX()
        directionToTarget = math.degrees(math.atan2(worldYDirection, worldXDirection))
        directionToTarget %= 360
        
        #Calculate distance between waypoint and source.
        distanceToTarget = distance(source, waypoint)
        
        #Calculate distance to wall
        distanceToWall = 1E400 #This represnts infinity... Replace with actual value once calculated.
        
        # We need to keep the ray not reparented to source, because it uses a separate collision traverser.
        wallRayNP.setPos(source, 0, 0, 0)
        wallRayNP.node().modifySolid(0).setOrigin(wallRayNP.getPos(render))
        direction = Vec3(worldXDirection, worldYDirection, 0)
        assert direction != Vec3.zero(), "the direction vector should not be zero"
        wallRayNP.node().modifySolid(0).setDirection(direction)
        
        # TODO uncomment this once Jim is satisfied with AStar
#            collisionTraverser.traverse(wallRayNP)
##        collisionHandler.sortEntries()
        # Now that the collision handler's entries are sorted, the first one should be the collision closest to us
##            if collisionHandler.getNumEntries() <= 0:
##               print("There were no collisions detected! Something went wrong here...")
##            else:
##               print(collisionHandler.getEntry(0))

        
        #Compare "distance to source" to "distance to wall" to decide if there is a wall in the way.
        if(distanceToTarget < distanceToWall):
            return True
        else:
            print("There is a wall in the way of nearest waypoint, ignore it and check next nearest")
            return False
    
    def getClosestWaypointTo(thing):
        #Make sure there is a direct path between thing and the nearestWaypoint.
        possiblyReachableWaypoints = waypoints
        
        if thing in waypoints:
            return thing
        
        #Find closest Waypoint
        shortest = infinity
        closest = None
        for waypoint in possiblyReachableWaypoints:
            dist = distance(thing, waypoint)
            if dist < shortest and \
                    waypointIsReachable(thing, waypoint):
                closest = waypoint
                shortest = dist
        return closest
    
    closestNodeToSource = getClosestWaypointTo(source)
    closestNodeToSource.changeToYellow()
    closestNodeToTarget = getClosestWaypointTo(target)
    closestNodeToTarget.changeToGreen()
    
    #AStar from wiki
    def reconstructPath(cameFrom, currentNode):            
        pathToTarget = cameFrom.has_key(currentNode) and [currentNode] or []
        while cameFrom.has_key(currentNode):
            pathToTarget.append(cameFrom[currentNode])
            currentNode = cameFrom[currentNode]
        pathToTarget.reverse()
        return pathToTarget

    closedSet = set([])
    openSet = set([closestNodeToSource])
    gScore = {closestNodeToSource: 0} # Distance from start along optimal path.
    hScore = {closestNodeToSource: distance(closestNodeToSource, closestNodeToTarget)}
    fScore = {closestNodeToSource: hScore[closestNodeToSource]} #Estimated total distance from start to goal
    
    infinity = 1E400
    cameFrom = {}
    while openSet:
        lowestFScoreFound = infinity 
        nodeWithLowestFScoreFound = None #Node in openset having lowest fScore[] value
        for waypoint in openSet:
            if fScore[waypoint] < lowestFScoreFound:
                lowestFScoreFound = fScore[waypoint]
                nodeWithLowestFScoreFound = waypoint
        #Make sure that something was found
        assert nodeWithLowestFScoreFound, "Something went horribly wrong, no node found with fScore < infinity"
            
        if nodeWithLowestFScoreFound == closestNodeToTarget: #If goal is found
##            assert cameFrom, "cameFrom should be defined before reconstructPath is called"
            returnValue = reconstructPath(cameFrom, closestNodeToTarget) #Be sure to define cameFrom
            return returnValue + [target]
        
        openSet.discard(nodeWithLowestFScoreFound)
        closedSet.add(nodeWithLowestFScoreFound)
        for neighbor in nodeWithLowestFScoreFound.getNeighbors():
            if neighbor in closedSet:
                continue
            neighborGScore = gScore[nodeWithLowestFScoreFound] + distance(nodeWithLowestFScoreFound, neighbor)
            neighborIsBetter = False
            if neighbor not in openSet:
                openSet.add(neighbor)
                hScore[neighbor] = distance(neighbor, closestNodeToTarget)
                neighborIsBetter = True
            elif neighborGScore < gScore[neighbor]:
                neighborIsBetter = True
            if neighborIsBetter:
                cameFrom[neighbor] = nodeWithLowestFScoreFound
                gScore[neighbor] = neighborGScore
                fScore[neighbor] = gScore[neighbor] + hScore[neighbor]
    return None

def distance(source, target):
    return math.hypot(source.getX(render) - target.getX(render), source.getY(render) - target.getY(render))
