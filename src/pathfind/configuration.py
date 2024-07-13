import yaml

class Configuration:
    def __init__(self, config_path):
        """
        Initialize the Configuration object and load the configuration from the given path.

        Parameters:
        - config_path (str): The path to the configuration YAML file.
        """
        self.load(config_path)

    def load(self, config_path):
        """
        Load the configuration from a YAML file.

        Parameters:
        - config_path (str): The path to the configuration YAML file.

        Sets the following attributes:
        - x_start (int): The x-coordinate of the start point.
        - y_start (int): The y-coordinate of the start point.
        - x_goal (int): The x-coordinate of the goal point.
        - y_goal (int): The y-coordinate of the goal point.
        - x_space_size (int): The width of the space.
        - y_space_size (int): The height of the space.
        - obstacles (list): A list of obstacles, each defined by a list of points.
        - mass (float): The mass of the robot.
        - max_acceleration (float): The maximum acceleration of the robot.
        """
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.start = [config['x_start'], config['y_start']]
        self.goal = [config['x_goal'], config['y_goal']]
        self.x_space_size = config['x_space_size']
        self.y_space_size = config['y_space_size']
        self.obstacles = config['list_obstacles']
        # Default mass to 1.0 if not specified
        self.mass = config.get('mass')
        # Default max acceleration to 1.0 if not specified
        self.max_acceleration = config.get(
            'max_acceleration')
