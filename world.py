# from the file character.py, import the class character
#include character.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import BitMask32
from pandac.PandaModules import CardMaker
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionPolygon
from pandac.PandaModules import CollisionSphere
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

        self.accept("escape", sys.exit)
        
        self.__setupEnvironment()
        self.__setupCollisions()
        self.__setupGravity()
        self.__setupLevel()
        self.__setupMainAgent()
#        self.__setupOtherAgents()
        self.__setupNPCs()
        self.__setupCamera()
        #Many things within the NPC are dependant on the level it is in.
        self.__room1NPC.setKeyAndNestReference(self.keyNest, self.roomKey)
        self.__room2NPC.setKeyAndNestReference(self.keyNest, self.roomKey)
        self.__room3NPC.setKeyAndNestReference(self.keyNest, self.roomKey)
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
        
        #Jim's favorite line to uncoment!
        #base.cTrav.showCollisions(render)

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
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    def __setupLevel(self):
        
        #place keyNest (Like a birds nest, but for keys!)
        keyNest = loader.loadModel("models/nest")
        keyNest.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        keyNest.setScale(0.5)
        keyNest.setTexScale(TextureStage.getDefault(), 0.1)
                
        level1 = render.attachNewNode("level 1 node path")
        

        execfile("rooms/room1.py")
        for w in self.room1waypoints:
            w.draw()
        room1 = loader.loadModel("rooms/room1")
        room1.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room1.setScale(10)
        room1.setTexScale(TextureStage.getDefault(), 10)
        room1.reparentTo(level1)

        keyNest1 = room1.attachNewNode("key nest 1")
        keyNest.instanceTo(keyNest1)
        keyNest1.setPos(0, 0, 0.05)
        self.keyNest = keyNest1
        
        room1Key = loader.loadModel("models/redKey")
        room1Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room1Key.setPos(keyNest1.getPos())
        room1Key.setTexScale(TextureStage.getDefault(), 0.1)
        room1Key.reparentTo(room1)
        self.roomKey = room1Key
        
        #self.setWaypoints("room2")
        self.room2waypoints = None
        execfile("rooms/room2.py")
#        print(len(self.room2waypoints))
        for w in self.room2waypoints:
            w.draw()
            print(w.getPos())
        room2 = loader.loadModel("rooms/room2")
        room2.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room2.setScale(10)
        room2.setTexScale(TextureStage.getDefault(), 10)
        room2.reparentTo(level1)
        room2.setY(room1, -20)
        
        keyNest2 = room2.attachNewNode("key nest 2")
        keyNest.instanceTo(keyNest2)
        keyNest2.setPos(-2.5,-2.5,0.05)
        
        room2Key = loader.loadModel("models/blueKey")
        room2Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room2Key.setTexScale(TextureStage.getDefault(), 0.1)
        room2Key.setPos(keyNest2.getPos())
        room2Key.reparentTo(room2)
        
        # Jim thinks there should be a comment here
        # he also thinks that the above comment is very useful
        # TODO: fix this hack by re-creating room3 in blender
        
        #self.setWaypoints("room3")
        
        execfile("rooms/room3.py")
        for w in self.room3waypoints:
            w.draw()
        room3Model = loader.loadModel("rooms/room3")
        room3Model.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room3Model.setH(90)
        room3Model.setP(180)
        room3Model.setZ(2)
        room3 = level1.attachNewNode("room 3")
        room3Model.reparentTo(room3)
        room3.setScale(10)
        room3.setTexScale(TextureStage.getDefault(), 10)
        room3.reparentTo(level1)
        room3.setX(room1, 20)
        
        keyNest3 = room3.attachNewNode("key nest 3")
        keyNest.instanceTo(keyNest3)
        keyNest3.setPos(0,0,0.05)
        
        room3Key = loader.loadModel("models/greenKey")
        room3Key.findTexture("*").setMinfilter(Texture.FTLinearMipmapLinear)
        room3Key.setTexScale(TextureStage.getDefault(), 0.1)
        room3Key.setPos(keyNest3.getPos())
        room3Key.reparentTo(room3)
        
        
        room3SphereOfDoom = room3.attachNewNode(CollisionNode("Jim's Hair"))
        room3SphereOfDoom.node().addSolid(CollisionSphere(3, -9, 0.5, .5))
        
        room1Floor = room1.attachNewNode(CollisionNode("room1Floor"))
        room1Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                 Point3(-9,9,0), Point3(-9,-9,0)))
                                                
        room2Floor = room2.attachNewNode(CollisionNode("room2Floor"))
        room2Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                 Point3(-9,9,0), Point3(-9,-9,0)))

        room3Floor = room3.attachNewNode(CollisionNode("room3Floor"))
        room3Floor.node().addSolid(CollisionPolygon(Point3(9,-9,0), Point3(9,9,0),
                                                 Point3(-9,9,0), Point3(-9,-9,0)))
        
        gate = loader.loadModel("models/box")
        
        gateTo2 = room1.attachNewNode("gateTo2")
        gate.instanceTo(gateTo2)
        gateTo2.setPos(8, -10, 0)
        gateTo2.hide()
        
        gateTo3 = room1.attachNewNode("gateTo3")
        gate.instanceTo(gateTo3)
        gateTo3.setPos(10, 8, 0)
        gateTo3.hide()
        
        self.physicsCollisionHandler.addInPattern("%fn-into-%in")
        self.physicsCollisionHandler.addOutPattern("%fn-out-%in")
        
        def orderNPC(parameters, entry):
            if(parameters == "ralph has entered room 1"):
                self.__room1NPC.handleTransition("playerEnteredRoom")
            elif(parameters == "ralph has left room 1"):
                self.__room1NPC.handleTransition("playerLeftRoom")
            elif(parameters == "ralph has entered room 2"):
                self.__room2NPC.handleTransition("playerEnteredRoom")
            elif(parameters == "ralph has left room 2"):
                self.__room2NPC.handleTransition("playerLeftRoom")
            elif(parameters == "ralph has entered room 3"):
                self.__room3NPC.handleTransition("playerEnteredRoom")
            elif(parameters == "ralph has left room 3"):
                self.__room3NPC.handleTransition("playerLeftRoom")
                

        self.accept("ralph collision node-into-room1Floor", orderNPC, ["ralph has entered room 1"])
        self.accept("ralph collision node-out-room1Floor", orderNPC, ["ralph has left room 1"])
        self.accept("ralph collision node-into-room2Floor", orderNPC, ["ralph has entered room 2"])
        self.accept("ralph collision node-out-room2Floor", orderNPC, ["ralph has left room 2"])
        self.accept("ralph collision node-into-room3Floor", orderNPC, ["ralph has entered room 3"])
        self.accept("ralph collision node-out-room3Floor", orderNPC, ["ralph has left room 3"])
        
        
        self.gate = gate
        
    
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
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
        self.gate.find("**/Cube;+h").setCollideMask(~self.__mainAgent.collisionMask)
        
    __targetCount = 0
    __targets = []
    __agentToTargetMap = {}
    def __setupNPCs(self):
        modelStanding = "models/eve"
        modelRunning = "models/eve-run"
        modelWalking = "models/eve-walk"
        self.__room1NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 26,
                                agentList = self.__globalAgentList,
                                name = "Eve",
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room1waypoints)
        self.__room1NPC.setPos(20, -15, 10)
        self.__room1NPC.setPlayer(self.__mainAgent)
        self.__room1NPC.reparentTo(render)
        
        
##        modelStanding = "models/bunny/bunny"
##        modelRunning = "models/bunny/bunny"
##        modelWalking = "models/bunny/bunny"
        self.__room2NPC = NPC(modelStanding,
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 25,
                                agentList = self.__globalAgentList,
                                name = "das Osterhase",
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room2waypoints)
        self.__room2NPC.setPos(-20, -210, 10)
        self.__room2NPC.setPlayer(self.__mainAgent)
        self.__room2NPC.reparentTo(render)

        self.__room3NPC = NPC(modelStanding, 
                                {"run":modelRunning, "walk":modelWalking},
                                turnRate = 150, 
                                speed = 25,
                                agentList = self.__globalAgentList,
                                name = "der Hoppelhaschen",
                                collisionMask = BitMask32.bit(3),
                                rangeFinderCount = 13,
                                adjacencySensorThreshold = 5,
                                radarSlices = 5,
                                radarLength = 40,
                                scale = 1.0,
                                massKg = 35.0,
                                collisionHandler = self.physicsCollisionHandler,
                                collisionTraverser = self.cTrav,
                                waypoints = self.room2waypoints)#TODO: Change this to room 3 once created!!!
        self.__room3NPC.setPos(210, 0, 10)
        self.__room3NPC.setPlayer(self.__mainAgent)
        self.__room3NPC.reparentTo(render)
    
    def __setupTasks(self):
        """
        This function sets up all the tasks used in the world
        """
        taskMgr.add(taskTimer, "taskTimer")
        
        #for index, ralph in enumerate(self.__otherRalphs):

            # uncomment this to make Jim happy
##            taskMgr.add(ralph.sense, "sense" + str(index))
##            taskMgr.add(ralph.think, "think" + str(index))
##            taskMgr.add(ralph.act,   "act"   + str(index))
            #taskMgr.add(ralph.wanderTask, "wander" + str(index))
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
        taskMgr.add(self.__room2NPC.sense, "senseTask")
        taskMgr.add(self.__room3NPC.sense, "senseTask")
##        taskMgr.add(self.ralph.think, "thinkTask")
        taskMgr.add(self.__room1NPC.act, "actTask")
        taskMgr.add(self.__room2NPC.act, "actTask")
        taskMgr.add(self.__room3NPC.act, "actTask")
        taskMgr.add(self.animateItems, "animateItemsTask")

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
        
##    def setWaypoints(self, file):
##        execfile("rooms/room1.py")
##        execfile("rooms/room2.py")
##        #for w in self.waypoints:
##        #    w.draw()
            
    
if __name__ == "__main__":
    w = World()
    
    run()
    print("World compiled correctly")
