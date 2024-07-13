import numpy as np
import networkx as nx
from shapely.geometry import LineString, Point


def create_graph(start, goal, obstacles):
    """
    Create a graph where nodes are points and edges are valid paths between points.

    Parameters:
    - start (tuple): The starting point coordinates.
    - goal (tuple): The goal point coordinates.
    - obstacles (list): A list of shapely Polygon objects.

    Returns:
    - nx.Graph: The created graph with nodes and edges.
    """
    G = nx.Graph()
    G.add_node(tuple(start))
    G.add_node(tuple(goal))

    nodes = [start, goal]
    for polygon in obstacles:
        nodes.extend(polygon.exterior.coords[:-1])

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            if not is_line_crossing_obstacles([node1, node2], obstacles):
                distance = np.linalg.norm(np.array(node1) - np.array(node2))
                G.add_edge(tuple(node1), tuple(node2), weight=distance)

    return G


def is_line_crossing_obstacles(line, obstacles):
    """
    Check if a given line crosses any obstacle.

    Parameters:
    - line (list): A list of two points defining the line.
    - obstacles (list): A list of shapely Polygon objects.

    Returns:
    - bool: True if the line crosses any obstacle, False otherwise.
    """
    line_geom = LineString(line)
    for polygon in obstacles:
        # Check if both points in the same polygon -> polygon.covers(line_geom)
        if polygon.covers(line_geom) or line_geom.crosses(polygon):
            return True
    return False
