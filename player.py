from agent import Agent
from pandac.PandaModules import NodePath
from pandac.PandaModules import BitMask32
from direct.task import Task
from tasktimer import taskTimer
from direct.showbase.DirectObject import DirectObject

class Player(Agent, DirectObject):
    def __init__(self, 
                modelStanding, 
                modelAnimationDict, 
                turnRate, 
                speed, 
                agentList,
                name = "",
                massKg = 0.1,
                collisionMask = BitMask32.allOff(),
                scale = 1.0,
                collisionHandler = None,
                collisionTraverser = None):
        Agent.__init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList, massKg, collisionMask, name, collisionHandler, collisionTraverser)
            
    playerKeys = []
    
    def addKey(self, key):
        self.playerKeys.append(key)
    
    def hasKey(self, key):
        return key in self.playerKeys
    
    def removeKey(self, key):
        assert(key in self.playerKeys)
        if key in self.playerKeys:
            self.playerKeys.remove(key)
    
    
    __keyMap = {"left":False,
            "right":False,
            "up":False,
            "down":False,
            "keyTaken":False,
            "gotKey":False,
            "leftRoom":False}
    
    waypointPositions = []
    def setKeymap(self):
        
        wpFile = open("waypoints.txt", "w")
        def dropWp():
            torus = loader.loadModel("models/Torus/Torus")
            torus.reparentTo(render)
            torus.setPos(self.getPos())
            self.waypointPositions.append(torus.getPos())
            wpFile.write(str((int(self.getX()), int(self.getY()))) + "\r\n")
        
        self.accept("space", dropWp)
        
        def setKey(key, value):
            self.__keyMap[key] = value
        
        self.accept("arrow_left",     setKey, ["left", True])
        self.accept("arrow_left-up",  setKey, ["left", False])
        self.accept("arrow_right",    setKey, ["right", True])
        self.accept("arrow_right-up", setKey, ["right", False])
        self.accept("arrow_up",       setKey, ["up", True])
        self.accept("arrow_up-up",    setKey, ["up", False])
        self.accept("arrow_down",     setKey, ["down", True])
        self.accept("arrow_down-up",  setKey, ["down", False])
        self.accept("a",              setKey, ["keyTaken", True])
        self.accept("a-up",           setKey, ["keyTaken", False])
        self.accept("b",              setKey, ["gotKey", True])
        self.accept("b-up",           setKey, ["gotKey", False])
        self.accept("c",              setKey, ["leftRoom", True])
        self.accept("c-up",           setKey, ["leftRoom", False])
    
    def processKey(self, task):
        
        turnAngle = self.turnRate * taskTimer.elapsedTime
        distance = self.speed * taskTimer.elapsedTime
        
        self.previousPosition = self.getPos()
        
        if self.__keyMap["left"]:
            self.turnLeft(turnAngle)
        if self.__keyMap["right"]:
            self.turnRight(turnAngle)
        if self.__keyMap["up"]:
            self.moveForward(distance)
        if self.__keyMap["down"]:
            self.moveBackward(distance)
        if self.__keyMap["keyTaken"]:
            self.handleTransition("keyTaken")
        if self.__keyMap["gotKey"]:
            self.handleTransition("gotKey")
        if self.__keyMap["leftRoom"]:
            self.handleTransition("leftRoom")
        
            
        if self.__keyMap["left"] or \
            self.__keyMap["right"] or \
            self.__keyMap["up"] or \
            self.__keyMap["down"]:
            if not self.isMoving:
                self.loop("run")
                self.isMoving = True
        else:
            self.stop()
            self.pose("walk", frame = 5)
            self.isMoving = False
        
        # Store the previous time and continue
        self.__previousTime = task.time
        return Task.cont
    
if __name__ == "__main__":
    print ("compiled")
    
