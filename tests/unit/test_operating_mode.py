import sys
import unittest
import subprocess
import os

from pathfind.configuration import Configuration
from pathfind.obstacle_course import ObstacleCourse
from pathfind.path_strategy import FastestPathStrategy, ShortestPathStrategy


class TestOperatingMode(unittest.TestCase):

    def test_operating_with_shortest_path_mode(self):
        with open('tests/config.yaml', 'w') as f:
            f.write("""
x_start: 2
y_start: 2
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: [
    [[5,5], [10,5], [8,12]],
    [[50,60], [70,40], [80,90], [60,80]]
]
        """)
        config = Configuration('tests/config.yaml')
        obstacle_course = ObstacleCourse(config)
        self.assertIsInstance(
            obstacle_course.strategy, ShortestPathStrategy)
        os.remove('tests/config.yaml')

    def test_operating_with_fastest_path_mode(self):
        with open('tests/config.yaml', 'w') as f:
            f.write("""
x_start: 2
y_start: 2
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: [
    [[5,5], [10,5], [8,12]],
    [[50,60], [70,40], [80,90], [60,80]]
]
mass: 1.0
max_acceleration: 12.0
        """)
        config = Configuration('tests/config.yaml')
        obstacle_course = ObstacleCourse(config)
        self.assertIsInstance(
            obstacle_course.strategy, FastestPathStrategy)
        os.remove('tests/config.yaml')


if __name__ == '__main__':
    unittest.main()
