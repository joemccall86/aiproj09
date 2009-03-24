from direct.actor.Actor import Actor
from pandac.PandaModules import NodePath
from pandac.PandaModules import ActorNode
from pandac.PandaModules import PandaNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerPusher
from pandac.PandaModules import PhysicsCollisionHandler
from pandac.PandaModules import CollisionHandlerFloor
from pandac.PandaModules import BitMask32
from pandac.PandaModules import ForceNode, LinearVectorForce
from direct.task import Task
from direct.showbase import DirectObject
import direct.directbase.DirectStart

class Agent(NodePath, DirectObject.DirectObject):
    """
    The Agent class takes care of the Actor component (game) and the ActorNode
    component (physics) inside an agent. You can call this as you would any
    NodePath.
    """
    def __init__(self, 
                    modelStanding, 
                    modelAnimationDict, 
                    turnRate, 
                    speed, 
                    agentList, 
                    massKg, 
                    collisionMask, 
                    collisionTraverser = None):
        NodePath.__init__(self, "agent node")
        
        self.actor = Actor()
        self.actor.loadModel(modelStanding)
        self.actor.loadAnims(modelAnimationDict)
    
        self.loop = self.actor.loop
        self.stop = self.actor.stop
        self.pose = self.actor.pose
        
        self.turnRate = turnRate
        self.speed = speed
        self.agentList = agentList
        self.collisionMask = collisionMask
        
        if self.actor not in agentList:
            self.agentList.append(self.actor)
                    
        actorNode = ActorNode(str(self.actor) + " physics")
        actorNodePath = self.attachNewNode(actorNode)
        base.physicsMgr.attachPhysicalNode(actorNode)
        self.actor.reparentTo(actorNodePath)
        
        actorNode.getPhysicsObject().setMass(massKg)
        
        self.__setupCollisionHandling(collisionTraverser, actorNodePath)

    
    def turnLeft(self, angle):
        self.setH(self.getH() + angle)
        return
    
    def turnRight(self, angle):
        self.setH(self.getH() - angle)
        return
    
    previousPosition = None
    def moveForward(self, distance):
        self.setFluidY(self, -distance)
    
    def moveBackward(self, distance):
        self.setFluidY(self, distance)
    
    def __setupCollisionHandling(self, collisionTraverser, actorNodePath):
        if not collisionTraverser.getRespectPrevTransform():
            collisionTraverser.setRespectPrevTransform(True)
        
        fromObject = self.attachNewNode(CollisionNode('ralphSphere'))
        collisionSphere = CollisionSphere(0, 0, 2.5, 2.6)
        fromObject.node().addSolid(collisionSphere)
        fromObject.node().setFromCollideMask(self.collisionMask)
        fromObject.node().setIntoCollideMask(BitMask32.allOff())
        
        pusher = CollisionHandlerPusher()
        pusher.addCollider(fromObject, self)
        collisionTraverser.addCollider(fromObject, pusher)
        
        collisionRay = CollisionRay()
        collisionRay.setOrigin(0,0,10)
        collisionRay.setDirection(0, 0, -1)
        collisionNode = CollisionNode("agentRay")
        collisionNode.addSolid(collisionRay)
        collisionNode.setFromCollideMask(self.collisionMask)
        collisionNode.setIntoCollideMask(BitMask32.allOff())
        collisionNodePath = self.actor.attachNewNode(collisionNode)
##        collisionNodePath.show()
        
        base.floor.addCollider(collisionNodePath, self)
        collisionTraverser.addCollider(collisionNodePath, base.floor)
        


if __name__ == "__main__":
    A = Agent("models/ralph", {"run":"models/ralph-run"}, turnRate = 300, speed = 5, agentList=[], massKg = 0.1, collisionMask = BitMask32.allOff())
    print(" compiled correctly")