# from the file character.py, import the class character
#include character.py
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
from tasktimer import taskTimer
import random

class World(DirectObject):     
    def __init__(self):
        DirectObject.__init__(self)
        self.__setupEnvironment()
        self.__setupCollisions()
        self.__setupGravity()
        self.__setupLevel()
        self.__setupMainAgent()
        self.__setupOtherAgents()
        self.__setupTargets()
        self.__setupCamera()
        #Many things within the NPC are dependant on the level it is in.
        # make the target seek me.
        self.bestPath = PathFinder.AStar(self.__room1NPC, self.__mainAgent, self.waypoints)
        if self.bestPath != None:
            ls = LineSegs()
            ls.setThickness(10.0)
            for i in range(len(self.bestPath) - 1):
                ls.setColor(0,0,1,1)
                ls.moveTo(self.bestPath[i].getPos())
                ls.drawTo(self.bestPath[i+1].getPos())
                np = NodePath(ls.create("aoeu"))
                np.reparentTo(render)
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
    
    def __setupLevel(self):
        self.setWaypoints()
        room = loader.loadModel("rooms/room1")
        room.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room.setScale(10)
        room.setTexScale(TextureStage.getDefault(), 10)
        room.reparentTo(render)
        
        room2 = loader.loadModel("rooms/room2")
        room2.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room2.setScale(10)
        room2.setTexScale(TextureStage.getDefault(), 10)
        room2.reparentTo(render)
        room2.setY(-200)
        
        box = loader.loadModel("models/box")
        box.setPos(80, -100, 0)
        box.setScale(10)
        box.reparentTo(render)
        box.hide()
        
        self.box = box
        
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
                            collisionTraverser = self.cTrav,
                            waypoints = self.waypoints)                    
        # Make it visible
        self.__mainAgent.reparentTo(render)
        self.__mainAgent.setPos(31, 35, 50)
        self.box.setCollideMask(~self.__mainAgent.collisionMask)
        
        
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
                                collisionTraverser = self.cTrav,
                                waypoints = self.waypoints)
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
        self.__room1NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 20,
                                agentList = self.__globalAgentList,
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionTraverser = self.cTrav,
                            waypoints = self.waypoints)
        self.__room1NPC.setPos(20, -15, 10)
        self.__room1NPC.setPlayer(self.__mainAgent)
        self.__room1NPC.reparentTo(render)
        
    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        
        taskMgr.add(taskTimer, "taskTimer")
        
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
        taskMgr.add(self.__room1NPC.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
        taskMgr.add(self.__room1NPC.act, "actTask")

        # This is for path finding
        #taskMgr.add(self.__room1NPC.followPath, "followPathTask", extraArgs = [self.bestPath], appendTask = True)

    def __setupCamera(self):
        base.camera.setPos(0,0*-200,400) #This is debug camera position.     
        base.camera.lookAt(0,0*-200,0)    
##        base.oobeCull()
        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.__mainAgent.actor)
        base.camera.setPos(0, 60, 60)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 10)
        
    waypointPositions = []
    __keyMap = {"left":False,
                "right":False,
                "up":False,
                "down":False,
                "keyTaken":False,
                "gotKey":False}
    def __setKeymap(self):
        
        self.accept("escape", sys.exit)
        
        wpFile = open("waypoints.txt", "w")
        def dropWp():
            torus = loader.loadModel("models/Torus/Torus")
            torus.reparentTo(render)
            torus.setPos(self.__mainAgent.getPos())
            self.waypointPositions.append(torus.getPos())
            wpFile.write(str((int(self.__mainAgent.getX()), int(self.__mainAgent.getY()))) + "\r\n")
        
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

    def __proccessKey(self, task):
        turnAngle = self.__mainAgent.turnRate * taskTimer.elapsedTime
        distance = self.__mainAgent.speed * taskTimer.elapsedTime
        
        self.previousPosition = self.__mainAgent.getPos()
        
        if self.__keyMap["left"]:
            self.__mainAgent.turnLeft(turnAngle)
        if self.__keyMap["right"]:
            self.__mainAgent.turnRight(turnAngle)
        if self.__keyMap["up"]:
            self.__mainAgent.moveForward(distance)
        if self.__keyMap["down"]:
            self.__mainAgent.moveBackward(distance)
        if self.__keyMap["keyTaken"]:
            self.__room1NPC.handleTransition("keyTaken")
        if self.__keyMap["gotKey"]:
            self.__room1NPC.handleTransition("gotKey")
        
            
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
        execfile("rooms/room1.py")
        #execfile("rooms/room2.py")
        for w in self.waypoints:
            w.draw()
            
    
if __name__ == "__main__":
    w = World()

    run()
    print("World compiled correctly")
