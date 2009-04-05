coords = [ (5,25),
         (-15,45),
         (10,60),
         (25,40),
        
        (40,25),
         (60,5),
         (40,-10),
         (20,5),
        
        (-5,-16),
         (10,-35),
         (-10,-50),
         (-25,-35),
        
        (-40,-15),
         (-60,5),
         (-40,25),
         (-25,5),
        ]
        
self.waypoints = waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.waypoints.append(waypoint)


self.waypoints[0].setNeighbors([waypoints[3], waypoints[1]])
self.waypoints[1].setNeighbors([waypoints[0], waypoints[2]])
self.waypoints[2].setNeighbors([waypoints[1], waypoints[3]])
self.waypoints[3].setNeighbors([waypoints[2], waypoints[0]])

self.waypoints[4].setNeighbors([waypoints[7], waypoints[5]])
self.waypoints[5].setNeighbors([waypoints[4], waypoints[6]])
self.waypoints[6].setNeighbors([waypoints[5], waypoints[7]])
self.waypoints[7].setNeighbors([waypoints[6], waypoints[4]])

self.waypoints[8].setNeighbors([waypoints[11], waypoints[9]])
self.waypoints[9].setNeighbors([waypoints[8], waypoints[10]])
self.waypoints[10].setNeighbors([waypoints[9], waypoints[11]])
self.waypoints[11].setNeighbors([waypoints[10], waypoints[8]])

self.waypoints[12].setNeighbors([waypoints[15], waypoints[13]])
self.waypoints[13].setNeighbors([waypoints[12], waypoints[14]])
self.waypoints[14].setNeighbors([waypoints[13], waypoints[15]])
self.waypoints[15].setNeighbors([waypoints[14], waypoints[12]])
#################################################
self.waypoints[3].addNeighbor(self.waypoints[4])
self.waypoints[4].addNeighbor(self.waypoints[3])

self.waypoints[0].addNeighbor(self.waypoints[7])
self.waypoints[7].addNeighbor(self.waypoints[0])
#################################################
self.waypoints[8].addNeighbor(self.waypoints[7])
self.waypoints[7].addNeighbor(self.waypoints[8])

self.waypoints[6].addNeighbor(self.waypoints[9])
self.waypoints[9].addNeighbor(self.waypoints[6])
#################################################
self.waypoints[15].addNeighbor(self.waypoints[8])
self.waypoints[8].addNeighbor(self.waypoints[15])

self.waypoints[12].addNeighbor(self.waypoints[11])
self.waypoints[11].addNeighbor(self.waypoints[12])
#################################################
self.waypoints[1].addNeighbor(self.waypoints[14])
self.waypoints[14].addNeighbor(self.waypoints[1])

self.waypoints[0].addNeighbor(self.waypoints[15])
self.waypoints[15].addNeighbor(self.waypoints[0])

