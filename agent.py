from direct.actor.Actor import Actor
from direct.task import Task
import direct.directbase.DirectStart

class Agent(Actor):
    
    def __init__(self, modelStanding, modelAnimationDict, turnRate, speed, agentList):
        Actor.__init__(self, modelStanding, modelAnimationDict)
        self.turnRate = turnRate
        self.speed = speed
        self.agentList = agentList
        
        if self not in agentList:
            self.agentList.append(self)
    
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
    A = Agent("models/ralph", {"run":"models/ralph-run"}, turnRate = 300, speed = 5)
    print(" compiled correctly")