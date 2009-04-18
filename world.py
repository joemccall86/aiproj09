# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import BitMask32
from pandac.PandaModules import CardMaker
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionPolygon
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import ForceNode
from pandac.PandaModules import LinearVectorForce
from pandac.PandaModules import LineSegs
from pandac.PandaModules import NodePath
from pandac.PandaModules import PhysicsCollisionHandler
from pandac.PandaModules import Point3
from pandac.PandaModules import TexGenAttrib
from pandac.PandaModules import TextNode
from pandac.PandaModules import Texture
from pandac.PandaModules import TextureStage
from pandac.PandaModules import Vec3
from npc import NPC
from player import Player
import sys
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
##from neural_network import NeuralNetwork
from waypoint import Waypoint
from pathFinder import PathFinder
from tasktimer import taskTimer
from direct.gui.DirectEntry import DirectEntry
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
        self.__room1NPC.setKeyAndNestReference(self.keyNest, self.roomKey)
##        # make the target seek me.
##        self.bestPath = PathFinder.AStar(self.__room1NPC, self.__mainAgent, self.waypoints)
##        if self.bestPath != None:
##            ls = LineSegs()
##            ls.setThickness(10.0)
##            for i in range(len(self.bestPath) - 1):
##                ls.setColor(0,0,1,1)
##                ls.moveTo(self.bestPath[i].getPos())
##                ls.drawTo(self.bestPath[i+1].getPos())
##                np = NodePath(ls.create("aoeu"))
##                np.reparentTo(render)
        self.__setupTasks()
        
    def __setupCollisions(self):
        self.cTrav = CollisionTraverser("traverser")
        base.cTrav = self.cTrav
        
        self.physicsCollisionHandler = PhysicsCollisionHandler()
        self.physicsCollisionHandler.setDynamicFrictionCoef(0.5)
        self.physicsCollisionHandler.setStaticFrictionCoef(0.7)

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
        
    def animateItems(self, task):
        self.rotate(self.roomKey)
        return Task.cont
            
    currentAngle = 0
    def rotate(self, someItem):
        if someItem != None:
            self.currentAngle = self.currentAngle + 250 * taskTimer.elapsedTime
            if self.currentAngle >= 360:
                self.currentAngle = self.currentAngle - 360
            someItem.setH(self.currentAngle)
    
    def __setupLevel(self):
        self.setWaypoints()
        
        room = loader.loadModel("rooms/room1")
        room.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room.setScale(10)
        room.setTexScale(TextureStage.getDefault(), 10)
        room.reparentTo(render)
        
        #place keyNest (Like a birds nest, but for keys!)
        self.keyNest = loader.loadModel("models/nest")
        self.keyNest.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.keyNest.setScale(5)
        self.keyNest.setPos(0,0,0.5)
        self.keyNest.reparentTo(render)
        
        self.roomKey = loader.loadModel("models/redKey")
        self.roomKey.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        self.roomKey.setScale(10)
        self.roomKey.setPos(self.keyNest.getX(),self.keyNest.getY(),self.keyNest.getZ())
        self.roomKey.reparentTo(render)
        
        self.chatTextDE = DirectEntry( parent=self.waypoints[0],
                      width=20, numLines=3,
                      frameColor=(0,0,0,0),
                      text_fg=(1,1,1,1), #text_shadow=(0,0,0,1),
                      text_align=TextNode.ACenter,
                      text='SMILEY', # the name
                      text_pos=(0,-1.2),
                      initialText='_____________ press Enter to chat _____________')
        self.chatTextDE.reparentTo(self.waypoints[0])
        #waypointIDText = OnscreenText(text="this is a test", style=1, fg=(1,1,1,1))
        #waypointIDText.setText("This is a test")
        #waypointIDText.reparentTo(self.waypoints[0])
        
        room2 = loader.loadModel("rooms/room2")
        room2.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room2.setScale(10)
        room2.setTexScale(TextureStage.getDefault(), 10)
        room2.reparentTo(render)
        room2.setY(-200)
        
                
        room3 = loader.loadModel("rooms/room3")
        room3.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room3.setScale(10)
        room3.setTexScale(TextureStage.getDefault(), 10)
        room3.reparentTo(render)
        room3.setX(200)
        room3.setH(90)
        room3.setP(180)
        room3.setZ(20)
        
        box = loader.loadModel("models/box")
        box.setPos(80, -100, 0)
        box.setScale(10)
        box.reparentTo(render)
        box.hide()
        
        room1Floor = room.attachNewNode(CollisionNode("room1Floor"))
        room1Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                 Point3(-9,9,0), Point3(-9,-9,0)))
                                                
        room2Floor = room2.attachNewNode(CollisionNode("room2Floor"))
        room2Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                 Point3(-9,9,0), Point3(-9,-9,0)))        

        # TODO: This is a quick hack because we flipped the room 3
        room3Floor = render.attachNewNode(CollisionNode("room3Floor"))
        room3Floor.setPos(room3.getPos())
        room3Floor.setZ(0)
        room3Floor.node().addSolid(CollisionPolygon(Point3(90,-90,0), Point3(90,90,0),
                                                 Point3(-90,90,0), Point3(-90,-90,0)))
        
        self.physicsCollisionHandler.addInPattern("%fn-into-%in")
        self.physicsCollisionHandler.addOutPattern("%fn-out-%in")
        
        def myPrint(a, entry):
            print a
        
        self.accept("ralph collision node-into-room1Floor", myPrint, ["ralph has entered room 1"])
        self.accept("ralph collision node-out-room1Floor", myPrint, ["ralph has left room 1"])
        self.accept("ralph collision node-into-room2Floor", myPrint, ["ralph has entered room 2"])
        self.accept("ralph collision node-out-room2Floor", myPrint, ["ralph has left room 2"])
        self.accept("ralph collision node-into-room3Floor", myPrint, ["ralph has entered room 3"])
        self.accept("ralph collision node-out-room3Floor", myPrint, ["ralph has left room 3"])
        
        self.box = box
        
    __globalAgentList = []
    __mainAgent = None
    def __setupMainAgent(self):
        modelStanding = "models/ralph"
        modelRunning = "models/ralph-run"
        modelWalking = "models/ralph-walk"
        self.__mainAgent = Player(modelStanding, 
                            {"run":modelRunning, "walk":modelWalking},
                            turnRate = 150, 
                            speed = 25,
                            agentList = self.__globalAgentList,
                            collisionMask = BitMask32.bit(1),
                            name="ralph",
                            massKg = 35.0,
                            collisionHandler = self.physicsCollisionHandler,
                            collisionTraverser = self.cTrav)
        # Make it visible
        self.__mainAgent.reparentTo(render)
        self.__mainAgent.setPos(31, 35, 50)
        self.box.find("**/Cube;+h").setCollideMask(~self.__mainAgent.collisionMask)
        
        
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
                                collisionHandler = self.physicsCollisionHandler,
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
        modelStanding = "models/eve"
        modelRunning = "models/eve-run"
        modelWalking = "models/eve-walk"
        self.__room1NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 25,
                                agentList = self.__globalAgentList,
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
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
        
        self.__mainAgent.setKeymap()
        taskMgr.add(self.__mainAgent.processKey, "processKeyTask")
##        taskMgr.add(self.__mainAgent.handleCollisionTask, "handleCollisionTask")
##        taskMgr.add(self.ralph.wanderTask, "wander")
        taskMgr.add(self.__room1NPC.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
        taskMgr.add(self.__room1NPC.act, "actTask")
        taskMgr.add(self.animateItems, "animateItemsTask")

        # This is for path finding
        #taskMgr.add(self.__room1NPC.followPath, "followPathTask", extraArgs = [self.bestPath], appendTask = True)

    def __setupCamera(self):
        base.camera.setPos(0,0*-200,400) #This is debug camera position.     
        base.camera.lookAt(0,0*-200,0)    
##        base.oobeCull()
##        base.oobe()
        base.disableMouse()
        base.camera.reparentTo(self.__mainAgent.actor)
        base.camera.setPos(0, 60, 60)
        base.camera.lookAt(self.__mainAgent)
        base.camera.setP(base.camera.getP() + 10)
        
    waypointPositions = []
    positionHeadingText = OnscreenText(text="", style=1, fg=(1,1,1,1),
                   pos=(-1.3,-0.95), align=TextNode.ALeft, scale = .05, mayChange = True)
    
                

    def __printPositionAndHeading(self, task):
        heading = self.__mainAgent.getH()
        heading %= 360.0
            
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
##        execfile("rooms/room2.py")
        #for w in self.waypoints:
        #    w.draw()
            
    
if __name__ == "__main__":
    w = World()
    
    run()
    print("World compiled correctly")
