from direct.fsm import FSM

class npcFSM(FSM.FSM):
    def __init__(self):
        FSM.FSM.__init__(self, "npcFSM")
        self.defaultTransitions = {
            'wander' : [ 'retriveKey', 'seek' ],
            'retriveKey' : [ 'wander', 'returnKey' ],
            'seek' : [ 'wander' ],
            'returnKey' : [ 'wander' ]
            }

##    def wander(self, npc)
##        npc.


    def enterRetriveKey(self, player, npc, pathfinder, waypoints):
        #makeSureAStarIsCalled()
        pass
        
    def exitRetriveKey(self):
        pass
        
    nextState = {
        ('wander', 'keyTaken') : 'retriveKey',
        ('wander', 'withinRange') : 'seek',
        ('retrieveKey', 'leftRoom') : 'wander',
        ('retrieveKey', 'gotKey') : 'returnKey',
        ('seek', 'outOfRange') : 'wander',
        ('seek', 'leftRoom') : 'wander',
        ('returnKey', 'keyReturned') : 'wander',
        }

    def defaultFilter(self, request, args):
        key = (self.state, request)
        return self.nextState.get(key)
    
    
if __name__ == "__main__":
    myfsm = npcFSM()
    print("compiled")

