coords = [ (-75,-135),
         (-55,-135),
         (-5,-145),
         (45,-145),
         (45,-165),
         (55,-135),
         (75,-135),
         (75,-275),
         (55,-275),
         (5,-265),
         (-15,-265),
         (-75,-200),
        ]
        
self.room3waypoints = room3waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    room2waypoint = Waypoint(Vec3(coord[0], coord[1], 10.5), i)
    self.room3waypoints.append(waypoint)


self.room3waypoints[0].setNeighbors([room3waypoints[11], room3waypoints[1]])
self.room3waypoints[1].setNeighbors([room3waypoints[0], room3waypoints[2]])
self.room3waypoints[2].setNeighbors([room3waypoints[1], room3waypoints[3]])
self.room3waypoints[3].setNeighbors([room3waypoints[2], room3waypoints[4], room3waypoints[5]])
self.room3waypoints[4].setNeighbors([room3waypoints[3], room3waypoints[5]])
self.room3waypoints[5].setNeighbors([room3waypoints[3], room3waypoints[4], room3waypoints[6]])
self.room3waypoints[6].setNeighbors([room3waypoints[5], room3waypoints[7]])
self.room3waypoints[7].setNeighbors([room3waypoints[6], room3waypoints[8]])
self.room3waypoints[8].setNeighbors([room3waypoints[7], room3waypoints[9]])
self.room3waypoints[9].setNeighbors([room3waypoints[8], room3waypoints[10]])
self.room3waypoints[10].setNeighbors([room3waypoints[9], room3waypoints[11]])
self.room3waypoints[11].setNeighbors([room3waypoints[10], room3waypoints[0]])