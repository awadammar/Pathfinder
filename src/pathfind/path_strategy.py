import math
from abc import ABC, abstractmethod


class PathStrategy(ABC):
    def euclidean_distance(self, start_node, end_node):
        """
        Calculate the Euclidean distance between two points.

        Parameters:
        - start_node (tuple): The starting point coordinates.
        - end_node (tuple): The ending point coordinates.

        Returns:
        - float: The Euclidean distance between the points.
        """
        return math.sqrt((start_node[0] - end_node[0])**2 + (start_node[1] - end_node[1])**2)
    
    @abstractmethod
    def calculate_travel_cost(self, start, goal, mass, max_acceleration):
        pass


class FastestPathStrategy(PathStrategy):
    def calculate_travel_cost(self, start_node, end_node, mass, a_max):
        """
        Calculate the travel time between two points considering the robot's mass and maximum acceleration.

        Parameters:
        - start_node (tuple): The starting point.
        - end_node (tuple): The ending point.
        - mass (float): The mass of the robot.
        - a_max (float): The maximum acceleration of the robot.

        Returns:
        - float: The travel time between the points.
        """
        distance = self.euclidean_distance(start_node, end_node)

        if distance == 0:
            return 0

        # Time to accelerate to maximum velocity
        t_acc = math.sqrt(2 * distance / a_max) / 2
        d_acc = 0.5 * a_max * t_acc**2

        # Time to decelerate to zero velocity
        t_dec = t_acc
        d_dec = d_acc

        # If the total distance is less than twice the acceleration distance
        if d_acc + d_dec >= distance:
            t_acc = math.sqrt(distance / a_max)
            t_dec = t_acc
            t_const = 0
        else:
            t_const = (distance - (d_acc + d_dec)) / (a_max * t_acc)

        return t_acc + t_const + t_dec


class ShortestPathStrategy(PathStrategy):
    def calculate_travel_cost(self, start, goal, mass=1, max_acceleration=1):
        """
        Calculate the travel cost between two points using the Euclidean distance.

        Parameters:
        - start (tuple): The starting point coordinates.
        - goal (tuple): The goal point coordinates.
        - mass (float, optional): The mass of the robot. Defaults to 1.
        - max_acceleration (float, optional): The maximum acceleration of the robot. Defaults to 1.

        Returns:
        - float: The Euclidean distance between the points.
        """
        return self.euclidean_distance(start, goal)