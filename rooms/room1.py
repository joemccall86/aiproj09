coords = [ (0,0),
         (0,10),
         (10,10),
         (10,0) ]
        
self.waypoints = waypoints = []
for i in range(len(coords)):
    coord = coords[i]
    waypoint = Waypoint(Vec3(coord[0], coord[1], 0), i)
    self.waypoints.append(waypoint)


self.waypoints[0].setNeighbors([waypoints[-1], waypoints[1]])
self.waypoints[1].setNeighbors([waypoints[0], waypoints[2]])
self.waypoints[2].setNeighbors([waypoints[1], waypoints[3]])
self.waypoints[3].setNeighbors([waypoints[2], waypoints[0]])
