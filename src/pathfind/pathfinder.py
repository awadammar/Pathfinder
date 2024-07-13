from pathfind.path_strategy import PathStrategy
from heapq import heappush, heappop

class Pathfinder:
    def __init__(self, pathStrategy: PathStrategy):
        """
        Initialize the Pathfinder with a specific path strategy.

        Parameters:
        - pathStrategy (PathStrategy): The strategy for calculating the path.
        """
        self.pathStrategy = pathStrategy

    def find_path(self, graph, start, goal, mass, max_acceleration):
        """
        Find the fastest path from start to goal considering the robot's mass and maximum acceleration.

        Parameters:
        - graph (nx.Graph): The graph with nodes and edges.
        - start (tuple): The starting point coordinates.
        - goal (tuple): The goal point coordinates.
        - mass (float): The mass of the robot.
        - max_acceleration (float): The maximum acceleration of the robot.

        Returns:
        - list: The fastest path as a list of points.

        Raises:
        - Exception: If no valid path is found.
        """
        pq = []
        costs = dict()
        came_from = dict()

        costs[start] = 0
        heappush(pq, (0, start))

        while pq:
            current_cost, current_node = heappop(pq)

            if current_node == goal:
                return self.reconstruct_path(start, current_node, came_from)

            for neighbor in graph.neighbors(current_node):
                travel_cost = self.pathStrategy.calculate_travel_cost(
                    current_node, neighbor, mass, max_acceleration)
                estimated_cost = current_cost + travel_cost
                if neighbor not in costs or estimated_cost < costs[neighbor]:
                    came_from[neighbor] = current_node
                    costs[neighbor] = estimated_cost
                    heappush(pq, (estimated_cost, neighbor))

        raise Exception("No valid path found")

    def reconstruct_path(self, start, node, parents):
        """
        Reconstruct the path from start to node using the parent nodes.

        Parameters:
        - start (tuple): The starting point coordinates.
        - node (tuple): The ending point coordinates.
        - parents (dict): A dictionary of node-parent relationships.

        Returns:
        - list: The reconstructed path as a list of points.
        """
        path = []
        while node in parents:
            path.append(list(map(float, node)))
            node = parents[node]
        path.append(list(map(float, start)))
        return path[::-1]