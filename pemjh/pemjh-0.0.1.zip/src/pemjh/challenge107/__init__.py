""" Challenge107 """
from __future__ import with_statement
from os.path import abspath, dirname


def skimNetwork(grid):
    # Choose row A as the first working row
    connectedRows = [0]
    availableConnections = sorted([(l, 0, i) for i, l in enumerate(grid[0])
                                   if l > 0])
    connections = list()

    # While there are available connections
    while len(availableConnections) > 0:
        # Get shortest available connection
        shortest = availableConnections[0]

        # Add as a connected row
        connectedRows.append(shortest[2])

        # Add the connection
        connections.append(shortest)

        # Remove any from availableConnections that go to a destination
        availableConnections = [link for link in availableConnections
                                if link[2] not in connectedRows]

        # Add the target row to the available connections
        availableConnections.extend([(l, shortest[2], i)
                                     for i, l in enumerate(grid[shortest[2]])
                                     if (l > 0) and not (i in connectedRows)])

        availableConnections.sort()

    # Create the new grid
    newGrid = [[0] * len(grid) for _ in grid]
    for connection in connections:
        newGrid[connection[1]][connection[2]] = connection[0]
        newGrid[connection[2]][connection[1]] = connection[0]
    return newGrid


def scoreGrid(grid):
    total = 0
    offset = 1
    # Loop through rows
    for r in grid[:-1]:
        for v in r[offset:]:
            total += v
        offset += 1

    return total


def challenge107():
    """ challenge107 """
    grid = list()
    # Read in grid
    with open("%s/network.txt" % dirname(abspath(__file__))) as f:
        for line in f:
            # Read into grid
            grid.append([int(link) if link != "-" else
                         0 for link in line.strip().split(",")])

    # Score the grid in its current state
    originalScore = scoreGrid(grid)

    # Shorten the grid to only essentials
    newGrid = skimNetwork(grid)

    # Score the new grid
    newScore = scoreGrid(newGrid)

    # Return original - new
    return originalScore - newScore
