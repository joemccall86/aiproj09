


coords = [ (0,0),
         (0,1),
         (0,2),
         (4,2) ]
        


for i in range(len(coords)):
    coord = coords[i]
    waypoint = Waypoint(Vec3(coord[0], coord[1], 0), i)
    waypoints.append(waypoint)


waypoints[0].setNeighbors,([waypoints[-1], waypoints[1]])
waypoints[1].setNeighbors,([waypoints[0], waypoints[2]])
waypoints[2].setNeighbors,([waypoints[1], waypoints[3]])
waypoints[3].setNeighbors,([waypoints[2], waypoints[0]])

