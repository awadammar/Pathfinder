import logging
from shapely.validation import explain_validity

LOGGER = logging.getLogger('validation')

def is_point_in_bounds(point, x_space_size, y_space_size):
    """
    Check if a point is within the defined space bounds.

    Parameters:
    - point (tuple): The point to check.
    - x_space_size (int): The width of the space.
    - y_space_size (int): The height of the space.

    Returns:
    - bool: True if the point is within the bounds, False otherwise.
    """
    return 0 <= point[0] <= x_space_size and 0 <= point[1] <= y_space_size

def validate_obstacles(obstacles):
    """
    Validate that all obstacles are valid polygons.

    Parameters:
    - obstacles (list): A list of shapely Polygon objects.

    Raises:
    - ValueError: If any obstacle is not a valid polygon.
    """
    for polygon in obstacles:
        if not polygon.is_valid:
            raise ValueError(f"Invalid obstacle: {explain_validity(polygon)}")


def check_for_overlaps_and_exceeding_bounds(obstacles, x_space_size, y_space_size):
    """
    Check for overlapping obstacles and obstacles exceeding the defined space bounds.

    Parameters:
    - obstacles (list): A list of shapely Polygon objects.
    - x_space_size (int): The width of the space.
    - y_space_size (int): The height of the space.
    """
    for i in range(len(obstacles)):
        for j in range(i + 1, len(obstacles)):
            if obstacles[i].intersects(obstacles[j]):
                LOGGER.warning(
                    f"Obstacle {obstacles[i]} overlaps with {obstacles[j]}.")

        # Check if the obstacle exceeds the bounds
        if not obstacles[i].bounds[0] >= 0 or not obstacles[i].bounds[2] <= x_space_size:
            LOGGER.warning(
                f"Obstacle {obstacles[i]} exceeds horizontal bounds.")
        if not obstacles[i].bounds[1] >= 0 or not obstacles[i].bounds[3] <= y_space_size:
            LOGGER.warning(
                f"Obstacle {obstacles[i]} exceeds vertical bounds.")