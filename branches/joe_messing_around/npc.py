from character import Character

class NPC(Character):

    def __init__(self, modelStanding, modelRunning, modelWalking, turnRate, speed):
        Character.__init__(self, modelStanding, modelRunning, modelWalking, turnRate, speed)
        
    def sense(self):
        self.rangeFinderCount = 5
        self.rangeFinders = []
        for i in range(self.rangeFinderCount):
            self.rangeFinders.append(CollisionRay())
            
        for rangeFinder in self.rangeFinders:
            rangeFinder.setDirection(LVector3f.unitY)
        return
    
    def think(self):
        return
    
    def act(self):
        return

if __name__ == "__main__":
    print("from npc.py: __name__ is " + __name__)