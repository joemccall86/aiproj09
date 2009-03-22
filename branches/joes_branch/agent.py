from direct.actor.Actor import Actor
from pandac.PandaModules import NodePath
from pandac.PandaModules import ActorNode
from pandac.PandaModules import PandaNode
from direct.task import Task
import direct.directbase.DirectStart

def instanceCount():
    ic = 0
    while True:
        ic += 1
        yield ic

class Agent(NodePath):
    """
    The Agent class takes care of the Actor component (game) and the ActorNode
    component (physics) inside an agent. You can call this as you would any
    NodePath.
    """
    def __init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList, massKg):
        NodePath.__init__(self, "agent node " + str(instanceCount()))
        
        self.actor = Actor()
        self.actor.loadModel(modelStanding)
        self.actor.loadAnims(modelAnimationDict)
    
        self.loop = self.actor.loop
        self.stop = self.actor.stop
        self.pose = self.actor.pose
        
        self.turnRate = turnRate
        self.speed = speed
        self.agentList = agentList
        
        if self.actor not in agentList:
            self.agentList.append(self.actor)
                    
        actorNode = ActorNode(str(self.actor) + " physics")
        actorNodePath = self.attachNewNode(actorNode)
        base.physicsMgr.attachPhysicalNode(actorNode)
        self.actor.reparentTo(actorNodePath)
        
        actorNode.getPhysicsObject().setMass(massKg)
    
    def turnLeft(self, angle):
        self.setH(self.getH() + angle)
        return
    
    def turnRight(self, angle):
        self.setH(self.getH() - angle)
        return
    
    previousPosition = None
    def moveForward(self, distance):
        self.previousPosition = self.getPos()
        # Gets the net transform from render as a matrix, and get the second
        # row, which represents the transform on the y-axis (in front of us)
        backward = self.getNetTransform().getMat().getRow3(1)
        
        # Normalize the vector
        backward.normalize()
        
        # Now move our  forward
        self.setPos(self.getPos() - backward * distance)
        return
    
    def moveBackward(self, distance):
        self.previousPosition = self.getPos()
        backward = self.getNetTransform().getMat().getRow3(1)
        backward.normalize()
        self.setPos(self.getPos() + backward * distance)
        return


if __name__ == "__main__":
    A = Agent("models/ralph", {"run":"models/ralph-run"}, turnRate = 300, speed = 5, agentList=[])
    print(" compiled correctly")