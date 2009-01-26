from direct.actor.Actor import Actor
import direct.directbase.DirectStart

class Character(Actor):
    
    __turnRate = 1
    
    def __init__(self, modelStanding, modelRunning):
        Actor.__init__(self, modelStanding, {"run":modelRunning})
    
    def turnLeft(self):
        self.setH(self.getH() + self.__turnRate)
        return
    
    def turnRight(self):
        self.setH(self.getH() - self.__turnRate)
        return
    
    def moveForward(self):
        # Gets the net transform from render as a matrix, and get the second
        # row, which represents the transform on the y-axis
        backward = self.getNetTransform().getMat().getRow3(1)
        
        # Normalize the vector
        backward.normalize()
        
        # Now move our character forward
        self.setPos(self.getPos() - backward)
        return
    
    def moveBackward(self):
        backward = self.getNetTransform().getMat().getRow3(1)
        backward.normalize()
        self.setPos(self.getPos() + backward)
        return


if __name__ == "__main__":
    C = Character("models/ralph", "models/ralph-run")
    print("character compiled correctly")