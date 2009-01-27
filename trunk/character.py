from direct.actor.Actor import Actor
import direct.directbase.DirectStart

class Character(Actor):
    
    def __init__(self, modelStanding, modelRunning, turnRate, speed):
        Actor.__init__(self, modelStanding, {"run":modelRunning})
        self.turnRate = turnRate
        self.speed = speed
    
    def turnLeft(self, angle):
        self.setH(self.getH() + angle)
        return
    
    def turnRight(self, angle):
        self.setH(self.getH() - angle)
        return
    
    def moveForward(self, distance):
        # Gets the net transform from render as a matrix, and get the second
        # row, which represents the transform on the y-axis
        backward = self.getNetTransform().getMat().getRow3(1)
        
        # Normalize the vector
        backward.normalize()
        
        # Now move our character forward
        self.setPos(self.getPos() - backward * distance)
        return
    
    def moveBackward(self, distance):
        backward = self.getNetTransform().getMat().getRow3(1)
        backward.normalize()
        self.setPos(self.getPos() + backward * distance)
        return


if __name__ == "__main__":
    C = Character("models/ralph", "models/ralph-run", turnRate = 300, speed = 5)
    print("character compiled correctly")