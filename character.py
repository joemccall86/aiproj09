from direct.actor.Actor import Actor
import direct.directbase.DirectStart
from direct.task import Task

class Character(Actor):
    
    def __init__(self, modelStanding, modelRunning, modelWalking, turnRate, speed):
        Actor.__init__(self, modelStanding, {"run":modelRunning, "walk":modelWalking})
        self.turnRate = turnRate
        self.speed = speed
        
##        self.maxFrames = self.getNumFrames(animName="run")
##        self.currentFrameIndex = 0
##        
##    def step(self, animationName):
##        self.currentFrameIndex += 1
##        if self.currentFrameIndex > self.maxFrames:
##            self.currentFrameIndex = 0
##        self.pose(animationName, self.currentFrameIndex)
    
    def turnLeft(self, angle):
        self.setH(self.getH() + angle)
    
    def turnRight(self, angle):
        self.setH(self.getH() - angle)
    
    def moveForward(self, distance):
        # Gets the net transform from render as a matrix, and get the second
        # row, which represents the transform on the y-axis
        backward = self.getNetTransform().getMat().getRow3(1)
        
        # Normalize the vector
        backward.normalize()
        
        # Now move our character forward
        self.setPos(self.getPos() - backward * distance)
    
    def moveBackward(self, distance):
        backward = self.getNetTransform().getMat().getRow3(1)
        backward.normalize()
        self.setPos(self.getPos() + backward * distance)


if __name__ == "__main__":
    C = Character("models/ralph", "models/ralph-run", turnRate = 300, speed = 5)
    print("character compiled correctly")