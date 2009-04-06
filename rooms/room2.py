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
        
self.waypoints = waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    waypoint = Waypoint(Vec3(coord[0], coord[1], 0.5), i)
    self.waypoints.append(waypoint)


self.waypoints[0].setNeighbors([waypoints[11], waypoints[1]])
self.waypoints[1].setNeighbors([waypoints[0], waypoints[2]])
self.waypoints[2].setNeighbors([waypoints[1], waypoints[3]])
self.waypoints[3].setNeighbors([waypoints[2], waypoints[4], waypoints[5]])
self.waypoints[4].setNeighbors([waypoints[3], waypoints[5]])
self.waypoints[5].setNeighbors([waypoints[3], waypoints[4], waypoints[6]])
self.waypoints[6].setNeighbors([waypoints[5], waypoints[7]])
self.waypoints[7].setNeighbors([waypoints[6], waypoints[8]])
self.waypoints[8].setNeighbors([waypoints[7], waypoints[9]])
self.waypoints[9].setNeighbors([waypoints[8], waypoints[10]])
self.waypoints[10].setNeighbors([waypoints[9], waypoints[11]])
self.waypoints[11].setNeighbors([waypoints[10], waypoints[0]])

