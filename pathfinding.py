
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class plane:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plane = [[0 for _ in range(30)] for _ in range(30)]

    def addStartPosition(self, position):
        self.startPosition = position

    def addEndPosition(self, position):
        self.endPosition = position

    def Astar_search(self):

        # Create start and end node
        start_node = Node(None, self.startPosition)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.endPosition)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            neighbors = self.getNeighbors(current_node)

            # Loop through children
            for neighbor in neighbors:

                # Child is on the closed list
                for closed_node in closed_list:
                    if neighbor == closed_node:
                        continue

                # Create the f, g, and h values
                neighbor.g = current_node.g + 1
                neighbor.h = ((neighbor.position[0] - end_node.position[0]) **
                              2) + ((neighbor.position[1] - end_node.position[1]) ** 2)
                neighbor.f = neighbor.g + neighbor.h

                # Child is already in the open list
                for open_node in open_list:
                    if neighbor == open_node and neighbor.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(neighbor)

    def getNeighbors(self, current_node):
        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(self.plane) - 1) or node_position[0] < 0 or node_position[1] > (len(self.plane[len(self.plane)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if self.plane[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
        return children

    def printPlane(self):
        path = self.Astar_search()
        for i, row in enumerate(self.plane):
            for j, column in enumerate(row):

                if (i, j) == self.startPosition:
                    print('\033[32m' + str(column) + '\033[0m' + ' ', end='')
                elif (i, j) == self.endPosition:
                    print('\033[91m' + str(column) + '\033[0m' + ' ', end='')
                elif (i, j) in path:
                    print('\033[35m' + str(column) + '\033[0m' + ' ', end='')
                else:
                    print(f'{column} ', end='')
            print()


grid = plane(30, 30)
grid.addStartPosition((4, 15))
grid.addEndPosition((29, 4))
grid.printPlane()
