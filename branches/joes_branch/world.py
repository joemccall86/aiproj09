# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from neural_network import NeuralNetwork
import random

class World(DirectObject):                

    
    def __init__(self):
        DirectObject.__init__(self)
        
        self.__setupEnvironment()
        self.__setupWalls()
        self.__setupMainAgent()
        self.__setupOtherAgents()
        self.__setupTargets()
        self.__setupTasks()
        self.__setupCamera()

    __envirnoment = None
    def __setupEnvironment(self):
        groundModel = "models/gridBack"
        
        self.__envirnoment = loader.loadModel(groundModel)
        
        # Make it visibler
        
        self.__envirnoment.reparentTo(render)
        
        texture = loader.loadTexture("textures/ground.png")
        
        # This is so the textures can look better from a distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        self.__envirnoment.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        self.__envirnoment.setTexScale(TextureStage.getDefault(), 0.02, 0.02)
        self.__envirnoment.setTexture(texture, 1)
        
        # Make it so that it's big enough to walk on
        self.__envirnoment.setPos(0, 0, 0)
        self.__envirnoment.setScale(500)
        
        base.setBackgroundColor(r=0, g=0, b=.1, a=1)
    
    def __setupWalls(self):
        stoneTexture = loader.loadTexture("textures/Stones.jpg")
        stoneTexture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        #Add some wallz
        wallModel = "models/box.egg.pz"
        wall = loader.loadModel(wallModel)
        wall.setPos(0, -10, 0)
        wall.setScale(10, 100, 100)
        wall.setTexture(stoneTexture, 1)
        
        # Add collision stuff to the wall
        tempWallCollideNodePath = wall.find("/Box")
        # We want everyone to collide with the box
        tempWallCollideNodePath.node().setIntoCollideMask(BitMask32.allOn())
        # But we don't care if the wall collides into anybody
        tempWallCollideNodePath.node().setFromCollideMask(BitMask32.allOff())
        
        tempWall = render.attachNewNode("wall")
        tempWall.setPos(250, 250, 0)
        wall.instanceTo(tempWall)
        
        # One's not enough, let's make 10!
        # Instance thiss wall several times
        numWallsPerSide = 0
        for i in range(numWallsPerSide):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(0, -i*wall.getScale().getY(), 0)
            tempWall.setY(-tempWall.getY())
            wall.instanceTo(tempWall)
        for i in range(numWallsPerSide):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(numWallsPerSide * wall.getScale().getY(), -i*wall.getScale().getY(), 0)
            tempWall.setY(-tempWall.getY())
            wall.instanceTo(tempWall)
        wall2 = loader.loadModel(wallModel)
        wall2.setScale(10, 1, 10)
        wall2.setTexture(stoneTexture, 1)
        for i in range(numWallsPerSide):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(i*wall2.getScale().getX(), 0, 0)
            tempWall.setY(-tempWall.getY())
            wall2.instanceTo(tempWall)
        for i in range(numWallsPerSide):
            tempWall = render.attachNewNode("wall")
            tempWall.setPos(numWallsPerSide * wall2.getScale().getX() - ((1+i)*wall2.getScale().getX()), 
                            -numWallsPerSide * wall2.getScale().getX(), 0)
            tempWall.setY(-tempWall.getY())
            wall2.instanceTo(tempWall)
        return
    
    __globalAgentList = []
    __mainAgent = None
    def __setupMainAgent(self):
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__mainAgent = NPC(modelStanding, 
                            {"run":modelRunning, "walk":modelWalking},
                            turnRate = 150, 
                            speed = 25,
                            agentList = self.__globalAgentList,
                            collisionMask = BitMask32.bit(1),
                            rangeFinderCount = 13,
                            adjacencySensorThreshold = 5,
                            radarSlices = 5,
                            radarLength = 25,
                            scale = 1.0)                    
        # Make it visible
        self.__mainAgent.reparentTo(render)
        
    __otherRalphsCount = 5
    __otherRalphs = []
    __startingPositions = {}
    def __setupOtherAgents(self):
        """
        This function sets up the other agents' position, scale, radars, etc.
        """
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__otherRalphs = [NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 25,
                                agentList = self.__globalAgentList,
                                rangeFinderCount = 13,
                                radarSlices = 5,
                                collisionMask = BitMask32.bit(i+2),
                                scale = 1.0,
                                brain = None)
                                for i in range(self.__otherRalphsCount)]
        for index, ralph in enumerate(self.__otherRalphs):
            ralph.reparentTo(render)
            ralph.setX(random.random() * 500)
            ralph.setY(random.random() * 500)
            self.__startingPositions[ralph] = ralph.getPos()
            
    __targetCount = __otherRalphsCount
    __targets = []
    __agentToTargetMap = {}
    def __setupTargets(self):
        targetCount = self.__otherRalphsCount
        self.__targets = [loader.loadModel("models/bunny") for i in range(self.__targetCount)]
        for target in self.__targets:
            target.setPos(random.randint(1, 500) * 1, random.randint(1, 500) * 1, 0)
            target.reparentTo(render)
        for agent,target in zip(self.__otherRalphs, self.__targets):
            self.__agentToTargetMap[agent] = target
    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        for index, ralph in enumerate(self.__otherRalphs):

            # uncomment this to make Jim happy
##            taskMgr.add(ralph.sense, "sense" + str(index))
##            taskMgr.add(ralph.think, "think" + str(index))
##            taskMgr.add(ralph.act,   "act"   + str(index))
            taskMgr.add(ralph.handleCollisionTask, "handleCollisions" + str(index))
##            taskMgr.add(ralph.wanderTask, "wander" + str(index))
            taskMgr.add(ralph.seekTask, "seekTask" + str(index), extraArgs = [self.__agentToTargetMap[ralph]], appendTask = True)
            
        taskMgr.add(self.__printPositionAndHeading, "__printPositionAndHeading")
        
##        listOfTargets = [(target.getX(), target.getY()) for target in self.__targets]
##        agentList = [(ralph.getX(), ralph.getY()) for ralph in self.__otherRalphs]
##        taskMgr.add(self.neatEvaluateTask, "self.neatEvaluateTask", extraArgs = [listOfTargets, self.__otherRalphs], appendTask = True)
        
        self.__setKeymap()
        taskMgr.add(self.__proccessKey, "processKeyTask")
        taskMgr.add(self.__mainAgent.handleCollisionTask, "handleCollisionTask")
##        taskMgr.add(self.ralph.wanderTask, "wander")
##        taskMgr.add(self.ralph.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
##        taskMgr.add(self.ralph.act, "actTask")

    def __setupCamera(self):                
##        base.oobeCull()
##        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.__mainAgent)
        base.camera.setPos(0, 30, 10)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 15)
        
    __keyMap = {"left":False, "right":False, "up":False, "down":False}
    def __setKeymap(self):
        
        self.accept("escape", sys.exit)
        
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

    
    # Keep track of time at previous frame to keep speed consistant on different platforms.
    __previousTime = 0
    def __proccessKey(self, task):
        elapsedTime = task.time - self.__previousTime
        turnAngle = self.__mainAgent.turnRate * elapsedTime
        distance = self.__mainAgent.speed * elapsedTime
        
        self.previousPosition = self.__mainAgent.getPos()
        
        if self.__keyMap["left"]:
            self.__mainAgent.turnLeft(turnAngle)
        if self.__keyMap["right"]:
            self.__mainAgent.turnRight(turnAngle)
        if self.__keyMap["up"]:
            self.__mainAgent.moveForward(distance)
        if self.__keyMap["down"]:
            self.__mainAgent.moveBackward(distance)
            
        if self.__keyMap["left"] or \
            self.__keyMap["right"] or \
            self.__keyMap["up"] or \
            self.__keyMap["down"]:
            if not self.__mainAgent.isMoving:
                self.__mainAgent.loop("run")
                self.__mainAgent.isMoving = True
        else:
            self.__mainAgent.stop()
            self.__mainAgent.pose("walk", frame = 5)
            self.__mainAgent.isMoving = False
        
        # Store the previous time and continue
        self.__previousTime = task.time
        return Task.cont
        
    positionHeadingText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                   pos=(-1.3,-0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
    def __printPositionAndHeading(self, task):
        heading = self.__mainAgent.getH()
        while heading > 360.0:
            heading -= 360.0
        while heading < 0.0:
            heading += 360.0
            
        self.positionHeadingText.setText("Position: (" + 
            str(self.__mainAgent.getPos().getX()) + ", " + 
            str(self.__mainAgent.getPos().getY()) + ") at heading " + 
            str(heading))
        return Task.cont

    # Every generation, throw out the old brains and put in the new ones. At
    # this point we can start all over with new nodes.
    generationCount = 0
    generationLifetimeTicks = 500
    neatEvaluateTaskCallCount = 0
    neuralNetwork = NeuralNetwork()
    def neatEvaluateTask(self, listOfTargets, agentList, task):
        self.neatEvaluateTaskCallCount += 1
        if self.generationLifetimeTicks == self.neatEvaluateTaskCallCount:
            self.neatEvaluateTaskCallCount = 0
            oldBrains = [agent.brain for agent in agentList]
            self.generationCount += 1
            listOfPositions = [(agent.getX(), agent.getY()) for agent in agentList]
            newBrains = self.neuralNetwork.nextGeneration(oldBrains, listOfTargets, listOfPositions)
            
            for agent, brain in zip(agentList, newBrains):
                agent.brain = brain
                agent.setPos(self.startingPositions[agent])
                
        return Task.cont
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")
