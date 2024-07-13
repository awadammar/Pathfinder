import os
import unittest
from pathfind.configuration import Configuration

from pathfind.obstacle_course import ObstacleCourse


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
            ObstacleCourse(config)
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
        [[0,0], [100,0], [100,100], [0, 100]]
]""")

        config = Configuration('tests/config.yaml')

        obstacle_course = ObstacleCourse(config)
        with self.assertRaises(Exception):
            obstacle_course.find_path()


if __name__ == '__main__':
    unittest.main()
