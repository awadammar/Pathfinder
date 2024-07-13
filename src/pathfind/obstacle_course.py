from shapely.geometry import Polygon

from pathfind.pathfinder import Pathfinder
from utils.graph_factory import create_graph
from utils.plotter import Plotter
from utils.validation import check_for_overlaps_and_exceeding_bounds, is_point_in_bounds, validate_obstacles


class ObstacleCourse:
    def __init__(self, config, path_finding_strategy):
        """
        Initialize the obstacle course with start and goal points, space size, and obstacles.

        Parameters:
        - config (Configuration): The configuration object.
        - path_finding_strategy (PathStrategy): The pathfinding strategy to use.
        """
        self.start = config.start
        self.goal = config.goal
        self.x_space_size = config.x_space_size
        self.y_space_size = config.y_space_size
        self.mass = config.mass
        self.max_acceleration = config.max_acceleration
        self.obstacles = [Polygon(obstacle) for obstacle in config.obstacles]
        self.validate_course()
        self.pathfinder = Pathfinder(path_finding_strategy)

    def validate_course(self):
        """
        Validate the obstacle course by checking start and goal points, obstacles, and bounds.
        """
        if not is_point_in_bounds(self.start, self.x_space_size, self.y_space_size):
            raise ValueError("Start point is out of bounds.")
        if not is_point_in_bounds(self.goal, self.x_space_size, self.y_space_size):
            raise ValueError("Goal point is out of bounds.")

        validate_obstacles(self.obstacles)
        check_for_overlaps_and_exceeding_bounds(
            self.obstacles, self.x_space_size, self.y_space_size)

    def find_path(self):
        """
        Find the shortest path from start to goal using the A* algorithm.

        Returns:
        - list: The shortest path as a list of points.

        Raises:
        - Exception: If no valid path is found.
        """
        graph = create_graph(self.start, self.goal, self.obstacles)
        return self.pathfinder.find_path(graph, tuple(self.start), tuple(self.goal), self.mass, self.max_acceleration)

    def plot(self, path):
        """
        Plot the scene with obstacles, start, goal, and the computed path.

        Parameters:
        - path (list): The computed path as a list of points.
        """
        Plotter.plot_scene(path, self.start, self.goal,
                           self.obstacles, self.x_space_size, self.y_space_size)
