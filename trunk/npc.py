from agent import Agent
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import Vec3

class NPC(Agent):

    def __init__(self, modelStanding, modelRunning, turnRate, speed):
        Agent.__init__(self, modelStanding, modelRunning, turnRate, speed)
        self.rangeFinderCount = 5
        self.rangeFinders = []
        for i in range(self.rangeFinderCount):
            self.rangeFinders.append(CollisionRay())
            
        index = 0
##        for rangeFinder in self.rangeFinders:
##            angle = 180 / self.rangeFinderCount
##            index += 1
##            angle *= index
##            rangeFinder.setDirection(Vec3.unitY*angle)
        
    def sense(self):
        return
    
    def think(self):
        return
    
    def act(self):
        return

if __name__ == "__main__":
    N = NPC(modelStanding = "models/ralph",
            modelRunning = "models/ralph-run",
            turnRate = 5,
            speed = 100)
    print ("compiled good")