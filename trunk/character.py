from direct.actor.Actor import Actor
import direct.directbase.DirectStart

class Character(Actor):
    
    def __init__(self, modelStanding, modelRunning):
        Actor.__init__(self, modelStanding, {"run":modelRunning})
    
    def turnLeft(self, task, prevTime):
        elapsed = task.time - prevTime
        
        self.setH(self.getH() + (elapsed*300))
        return
    
    def turnRight(self, task, prevTime):
        elapsed = task.time - prevTime
        
        self.setH(self.getH() - (elapsed*300))
        return
    
    def moveForward(self):
        elapsed = task.time - prevTime
        
        # Gets the net transform from render as a matrix, and get the second
        # row, which represents the transform on the y-axis
        backward = self.getNetTransform().getMat().getRow3(1)
        
        # Normalize the vector
        backward.normalize()
        
        # Now move our character forward
        self.setPos(self.getPos() - backward*(elapsed*5))
        return
    
    def moveBackward(self):
        elapsed = task.time - prevTime
        backward = self.getNetTransform().getMat().getRow3(1)
        backward.normalize()
        self.setPos(self.getPos() + backward*(elapsed*5))
        return


if __name__ == "__main__":
    C = Character("models/ralph", "models/ralph-run")
    print("character compiled correctly")