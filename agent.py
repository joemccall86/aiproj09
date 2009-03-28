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

class Agent(NodePath):
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
        NodePath.__init__(self, ActorNode("actor node"))
        
        self.actor = Actor()
        self.actor.loadModel(modelStanding)
        self.actor.loadAnims(modelAnimationDict)
    
        self.loop = self.actor.loop
        self.stop = self.actor.stop
        self.pose = self.actor.pose
        
        self.turnRate = turnRate
        self.speed = speed
        self.agentList = agentList
        self.massKg = massKg
        self.collisionMask = collisionMask
        
        if self.actor not in agentList:
            self.agentList.append(self.actor)    
            
        self.actor.reparentTo(self)
        
        self.__setupCollisionHandling(collisionTraverser)

    
    def turnLeft(self, angle):
        self.setH(self.getH() + angle)
    
    def turnRight(self, angle):
        self.setH(self.getH() - angle)
    
    def moveForward(self, distance):
        self.setFluidY(self, -distance)
    
    def moveBackward(self, distance):
        self.setFluidY(self, distance)
    
    def __setupCollisionHandling(self, collisionTraverser):
        if not collisionTraverser.getRespectPrevTransform():
            collisionTraverser.setRespectPrevTransform(True)
            
        self.actor.setCollideMask(BitMask32.allOff())
            
        self.node().getPhysicsObject().setMass(self.massKg) 
        base.physicsMgr.attachPhysicalNode(self.node())
        fromObject = self.attachNewNode(CollisionNode("agentCollisionNode"))
        fromObject.node().addSolid(CollisionSphere(0, 0, 2.5, 2.5))
        fromObject.node().setFromCollideMask(self.collisionMask)
        fromObject.node().setIntoCollideMask(BitMask32.allOff())
        fromObject.show()
        
        pusher = PhysicsCollisionHandler()
        pusher.setDynamicFrictionCoef(0.5)
        pusher.setStaticFrictionCoef(0.7)
        pusher.addCollider(fromObject, self)
        collisionTraverser.addCollider(fromObject, pusher)


if __name__ == "__main__":
    A = Agent("models/ralph", {"run":"models/ralph-run"}, turnRate = 300, speed = 5, agentList=[], massKg = 0.1, collisionMask = BitMask32.allOff())
    print(" compiled correctly")