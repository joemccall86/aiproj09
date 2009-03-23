from pandac.PandaModules import NodePath
from pandac.PandaModules import Texture


class Waypoint(NodePath):
    
    def __init__(self, position, ID = -1):
        NodePath.__init__(self, "Waypoint")
        self.position = position
        self.texture = loader.loadTexture("textures/blue.jpg")
        self.costToThisNode = 0
        self.visited = False
        self.neighbors = []
        self.ID = ID
        self.previousWaypoint = None

    def getNodeID(self):
        return self.ID
    
    def setPreviousWaypoint(self, previousWaypoint):
        self.previousWaypoint = previousWaypoint

    def getPreviousWaypoint(self):
        return self.previousWaypoint
    
    def visit(self):
        self.visited = True

    def wasVisited(self):
        return self.visited
        
    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        
    def getNeighbors(self):
        return self.neighbors
    
    def setCostToNode(self, cost):
        self.costToThisNode = cost
        
    def getCostToNode(self):
        return self.costToThisNode
    
    def getPos(self):
        return self.position
    
    def getX(self):
        return self.position.getX()
    
    def getY(self):
        return self.position.getY()
    
    def changeToGreen(self):
        self.texture = loader.loadTexture("textures/green.jpg")
        
    def changeToYellow(self):
        self.texture = loader.loadTexture("textures/yellow.jpg")
        
    def changeToBlue(self):
        self.texture = loader.loadTexture("textures/blue.jpg")
        
    def draw(self):        
        torusModel = "models/Torus/Torus.egg"
        torus = loader.loadModel(torusModel)
        torus.setPos(self.position)
        torus.setScale(0.5, 0.5, 0.5)
        torus.setTexture(self.texture, 1)
        torus.reparentTo(render)