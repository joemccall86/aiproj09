# from the file character.py, import the class character
#include character.py
from pandac.PandaModules import loadPrcFileData
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from npc import NPC
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
##from neural_network import NeuralNetwork
from waypoint import Waypoint
from pathFinder import PathFinder
import random

class World(DirectObject):                
    def __init__(self):
        DirectObject.__init__(self)
        
        self.__setupEnvironment()
        self.__setupCollisions()
        self.__setupGravity()
        self.__setupWalls()
        self.__setupMainAgent()
        self.__setupOtherAgents()
        self.__setupTargets()
        self.__setupCamera()
        
##        frame = loader.loadModel("models/room1")
##        frame.setScale(10)
##        frame.setTexScale(TextureStage.getDefault(), 10)
##        frame.reparentTo(render)
        # TODO move this into NPC's think function
        self.setWaypoints()
        # make the target seek me
        self.bestPath = PathFinder.AStar(self.__mainTarget, self.__mainAgent, self.waypoints)        
        #self.bestPath = PathFinder.AStar(self.__mainAgent, self.__mainTarget, self.waypoints)
        
        self.__setupTasks()
        
    def __setupCollisions(self):
        self.cTrav = CollisionTraverser("traverser")
        base.cTrav = self.cTrav

    def __setupGravity(self):
        base.particlesEnabled = True
        base.enableParticles()
        
        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-32.18) #gravity acceleration ft/s^2
##        gravityForce.setMassDependent(1)
        gravityFN.addForce(gravityForce)
        
##        base.cTrav.showCollisions(render)

        base.physicsMgr.addLinearForce(gravityForce)

    def __setupEnvironment(self):
        cm = CardMaker("ground")
        size = 1000
        cm.setFrame(-size, size, -size, size)
        environment = render.attachNewNode(cm.generate())
        environment.setPos(0, 0, 0)
        environment.lookAt(0, 0, -1)
        environment.setCollideMask(BitMask32.allOn())
        environment.reparentTo(render)
        
        texture = loader.loadTexture("textures/ground.png")
        
        # This is so the textures can look better from a distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        
        environment.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) 
        environment.setTexScale(TextureStage.getDefault(), 0.02, 0.02)
        environment.setTexture(texture, 1)
        
        base.setBackgroundColor(r=0, g=0, b=.1, a=1)
    
    def __setupWalls(self):
        wall = loader.loadModel("models/box")
##        wall.setScale(5, 5, 5)
##        wall.setPos(-5, -5, 0)
##        wall.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        
        stoneTexture = loader.loadTexture('textures/Stones.jpg')
        stoneTexture.setMinfilter(Texture.FTLinearMipmapLinear)
        wall.setTexture(stoneTexture, 1)
        
        wall.find("/Box").setCollideMask(BitMask32.allOn())

        wall.setTexScale(TextureStage.getDefault(), 40, 1, 1)
        frame = NodePath("frame")
        frameScales =    ((200, 5), (200, 5), (5, 200), (5, 200))
        framePositions = ((0, 0),   (0, 200), (0, 0),   (200, 0))
        for scale, pos in zip(frameScales, framePositions):
            tempWall = frame.attachNewNode("frameWall")
            wall.instanceTo(tempWall)
            tempWall.setScale(scale[0], scale[1], 5)
            tempWall.setPos(pos[0], pos[1], 0)
        frame.setPos(-100, -100, 0)
        frame.reparentTo(render)
        
        wall.setTexScale(TextureStage.getDefault(), 20, 1, 1)
        maze = NodePath("maze")
        mazeScales =    ((100, 5),   (100, 5), (5, 100))
        mazePositions = ((-50, -50), (-50, 0), (50, -50))
        for scale, pos in zip(mazeScales, mazePositions):
            tempWall = maze.attachNewNode("mazeWall")
            wall.instanceTo(tempWall)
            tempWall.setScale(scale[0], scale[1], 5)
            tempWall.setPos(pos[0], pos[1], 0)
        maze.reparentTo(render)
        
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
                            scale = 1.0,
                            massKg = 35.0,
                            collisionTraverser = self.cTrav)                    
        # Make it visible
        self.__mainAgent.reparentTo(render)
        self.__mainAgent.setPos(15, 40, 300)
        
        
        
    __otherRalphsCount = 0
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
                                brain = None,
                                massKg = 35.0,
                                collisionTraverser = self.cTrav)
                                for i in range(self.__otherRalphsCount)]
        for index, ralph in enumerate(self.__otherRalphs):
            ralph.reparentTo(render)
            ralph.setZ(200)
            self.__startingPositions[ralph] = ralph.getPos()
            
    __targetCount = 0
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
        
        # This is for path finding
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__mainTarget = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 25,
                                agentList = self.__globalAgentList,
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 30,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionTraverser = self.cTrav)
        self.__mainTarget.setPos(0, -10, 10)
        self.__mainTarget.reparentTo(render)
        
    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        for index, ralph in enumerate(self.__otherRalphs):

            # uncomment this to make Jim happy
##            taskMgr.add(ralph.sense, "sense" + str(index))
##            taskMgr.add(ralph.think, "think" + str(index))
##            taskMgr.add(ralph.act,   "act"   + str(index))
            taskMgr.add(ralph.wanderTask, "wander" + str(index))
##            taskMgr.add(ralph.seekTask, "seekTask" + str(index), extraArgs = [self.__agentToTargetMap[ralph]], appendTask = True)
            
        taskMgr.add(self.__printPositionAndHeading, "__printPositionAndHeading")
        
##        listOfTargets = [(target.getX(), target.getY()) for target in self.__targets]
##        agentList = [(ralph.getX(), ralph.getY()) for ralph in self.__otherRalphs]
##        taskMgr.add(self.neatEvaluateTask, "self.neatEvaluateTask", extraArgs = [listOfTargets, self.__otherRalphs], appendTask = True)
        
        self.__setKeymap()
        taskMgr.add(self.__proccessKey, "processKeyTask")
##        taskMgr.add(self.__mainAgent.handleCollisionTask, "handleCollisionTask")
##        taskMgr.add(self.ralph.wanderTask, "wander")
        taskMgr.add(self.__mainTarget.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
        taskMgr.add(self.__mainTarget.act, "actTask")

        # This is for path finding
        taskMgr.add(self.__mainTarget.followPath, "followPathTask", extraArgs = [self.bestPath], appendTask = True)

    def __setupCamera(self):                
##        base.oobeCull()
##        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.__mainAgent.actor)
        base.camera.setPos(0, 60, 60)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 10)
        
    waypointPositions = []
    __keyMap = {"left":False, "right":False, "up":False, "down":False}
    def __setKeymap(self):
        
        self.accept("escape", sys.exit)
            
        def dropWp():
            torus = loader.loadModel("models/Torus/Torus")
            torus.reparentTo(render)
            torus.setPos(self.__mainAgent.getPos())
            self.waypointPositions.append(torus.getPos())
        
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
            str(self.__mainAgent.getX()) + ", " + 
            str(self.__mainAgent.getY()) + ", " +
            str(self.__mainAgent.getZ()) + ") at heading " + 
            str(heading))
        return Task.cont

    # Every generation, throw out the old brains and put in the new ones. At
    # this point we can start all over with new nodes.
    generationCount = 0
    generationLifetimeTicks = 500
    neatEvaluateTaskCallCount = 0
##    neuralNetwork = NeuralNetwork()
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
        
    def setWaypoints(self):
        # TODO FIX THIS!!!!
        col1 = -17*5
        col2 = -12*5
        col3 = -7*5
        col4 = -2*5
        col5 = 3*5
        col6 = 8*5
        col7 = 13*5
        col8 = 18*5
        rowA = 19*5
        rowB = 14*5
            
        
        rowA = 3*5
        rowB = -1*5

        waypointPosition = Vec3(col1,rowA,0)
        self.waypointA1 = Waypoint(waypointPosition, 1)
        waypointPosition = Vec3(col2,rowA,0)
        self.waypointA2 = Waypoint(waypointPosition, 2)
        waypointPosition = Vec3(col3,rowA,0)
        self.waypointA3 = Waypoint(waypointPosition, 3)
        waypointPosition = Vec3(col4,rowA,0)
        self.waypointA4 = Waypoint(waypointPosition, 4)
        waypointPosition = Vec3(col5,rowA,0)
        self.waypointA5 = Waypoint(waypointPosition, 5)
        waypointPosition = Vec3(col6,rowA,0)
        self.waypointA6 = Waypoint(waypointPosition, 6)
        waypointPosition = Vec3(col7,rowA,0)
        self.waypointA7 = Waypoint(waypointPosition, 7)
        waypointPosition = Vec3(col8,rowA,0)
        self.waypointA8 = Waypoint(waypointPosition, 8)
        
        waypointPosition = Vec3(col1,rowB,0)
        self.waypointB1 = Waypoint(waypointPosition, 11)
        waypointPosition = Vec3(col2,rowB,0)
        self.waypointB2 = Waypoint(waypointPosition, 12)
        waypointPosition = Vec3(col3,rowB,0)
        self.waypointB3 = Waypoint(waypointPosition, 13)
        waypointPosition = Vec3(col4,rowB,0)
        self.waypointB4 = Waypoint(waypointPosition, 14)
        waypointPosition = Vec3(col5,rowB,0)
        self.waypointB5 = Waypoint(waypointPosition, 15)
        waypointPosition = Vec3(col6,rowB,0)
        self.waypointB6 = Waypoint(waypointPosition, 16)
        waypointPosition = Vec3(col7,rowB,0)
        self.waypointB7 = Waypoint(waypointPosition, 17)
        waypointPosition = Vec3(col8,rowB,0)
        self.waypointB8 = Waypoint(waypointPosition, 18)
        
        self.waypoints = [self.waypointA1, self.waypointA2, self.waypointA3, self.waypointA4, self.waypointA5, self.waypointA6, self.waypointA7, self.waypointA8]
        self.waypoints.extend([self.waypointB1, self.waypointB2, self.waypointB3, self.waypointB4, self.waypointB5, self.waypointB6, self.waypointB7, self.waypointB8])
        
        #Set paths
        self.waypointA2.setNeighbors([self.waypointA3, self.waypointB2])
        self.waypointA3.setNeighbors([self.waypointA2, self.waypointA4])
        self.waypointA4.setNeighbors([self.waypointA3, self.waypointA5])
        self.waypointA5.setNeighbors([self.waypointA4, self.waypointA6])
        self.waypointA6.setNeighbors([self.waypointA5])
        
        self.waypointB2.setNeighbors([self.waypointB3, self.waypointA2])
        self.waypointB3.setNeighbors([self.waypointB2, self.waypointB4])
        self.waypointB4.setNeighbors([self.waypointB3, self.waypointB5])
        self.waypointB5.setNeighbors([self.waypointB4, self.waypointB6])
        self.waypointB6.setNeighbors([self.waypointB5])
        
        self.waypoints = [self.waypointA2, self.waypointA3, self.waypointA4, self.waypointA5, self.waypointA6]
        self.waypoints.extend([self.waypointB2, self.waypointB3, self.waypointB4, self.waypointB5, self.waypointB6])
        for w in self.waypoints:
            w.draw()
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")
