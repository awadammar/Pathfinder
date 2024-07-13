import os
import unittest
from src.pathfinder.configuration import Configuration

from src.pathfinder.obstacle_course import ObstacleCourse
from src.pathfinder.path_strategy import ShortestPathStrategy


class TestRegression(unittest.TestCase):

    def test_self_intersecting_polygon(self):
        with open('tests/config.yaml', 'w') as f:
            f.write("""
        x_start: 2
        y_start: 2
        x_goal: 98
        y_goal: 98
        x_space_size: 100
        y_space_size: 100
        list_obstacles: [
        [[0,0], [1,1], [1,0], [0, 1]],
        ]
        """)

        config = Configuration('tests/config.yaml')
        with self.assertRaises(ValueError):
            ObstacleCourse(config, ShortestPathStrategy)
        os.remove('tests/config.yaml')

    def test_no_valid_path(self):
        # Enclosing the entire space
        with open('tests/config.yaml', 'w') as f:
            f.write("""
        x_start: 2
        y_start: 2
        x_goal: 98
        y_goal: 98
        x_space_size: 100
        y_space_size: 100
        list_obstacles: [
        [[0,0], [100,0], [100,100], [0, 100]],
        ]
        """)

        config = Configuration('tests/config.yaml')

        obstacle_course = ObstacleCourse(
            config, ShortestPathStrategy)
        with self.assertRaises(Exception):
            obstacle_course.find_path()


if __name__ == '__main__':
    unittest.main()
