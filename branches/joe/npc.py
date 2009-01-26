from character import Character

class NPC(Character):

    def __init__(self, modelStanding, modelRunning):
        Character.__init__(self, modelStanding, {"run":modelRunning})

if __name__ == "__main__":
    print("from npc.py: __name__ is " + __name__)