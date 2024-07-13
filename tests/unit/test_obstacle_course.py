import os
import unittest

from shapely.geometry import Polygon
from pathfind.configuration import Configuration

from pathfind.obstacle_course import ObstacleCourse
from pathfind.path_strategy import ShortestPathStrategy
from utils.graph_factory import create_graph, is_line_crossing_obstacles
from utils.validation import check_for_overlaps_and_exceeding_bounds, validate_obstacles


class TestObstacleCourse(unittest.TestCase):

    def setUp(self):
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

        self.config = Configuration('tests/config.yaml')
        self.obstacle_course = ObstacleCourse(
            self.config, ShortestPathStrategy)

    def test_validate_obstacles(self):
        # Test valid obstacles
        valid_obstacles = [Polygon(obstacle)
                           for obstacle in self.config.obstacles]
        try:
            validate_obstacles(valid_obstacles)
        except ValueError:
            self.fail("validate_obstacles() raised ValueError unexpectedly!")

        # Test invalid obstacle
        # Self-intersecting polygon
        invalid_obstacles = [Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])]
        with self.assertRaises(ValueError):
            validate_obstacles(invalid_obstacles)

    def test_check_for_overlaps_and_exceeding_bounds(self):
        # Test no overlaps and within bounds
        obstacles = [
            [(5, 5), (10, 5), (8, 12)],
            [(50, 60), (70, 40), (80, 90), (60, 80)]
        ]
        valid_obstacles = [Polygon(obstacle) for obstacle in obstacles]
        check_for_overlaps_and_exceeding_bounds(
            valid_obstacles, self.config.x_space_size, self.config.y_space_size)

        # Test overlaps and within bounds
        obstacles.append([(60, 60), (60, 80), (80, 80), (80, 60)])
        valid_obstacles = [Polygon(obstacle) for obstacle in obstacles]
        with self.assertLogs(level='WARNING'):
            check_for_overlaps_and_exceeding_bounds(
                valid_obstacles, self.config.x_space_size, self.config.y_space_size)

    def test_check_for_exceeding_bounds(self):
        # Test exceeding bounds
        exceeding_obstacles = [
            Polygon([(-2, 20), (5, 10), (20, 10)])]
        with self.assertLogs(level='WARNING'):
            check_for_overlaps_and_exceeding_bounds(
                exceeding_obstacles, self.config.x_space_size, self.config.y_space_size)

    def test_create_graph(self):
        graph = create_graph(self.config.start, self.config.goal, [
                             Polygon(obstacle) for obstacle in self.config.obstacles])
        self.assertIn(tuple(self.config.start), graph.nodes)
        self.assertIn(tuple(self.config.goal), graph.nodes)

    def find_optimal_path(self):
        path = self.obstacle_course.find_path()
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], self.config.start)
        self.assertEqual(path[-1], self.config.goal)

    def test_is_line_crossing_obstacles(self):
        obstacles = [
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(7, 7), (9, 7), (9, 9), (7, 9)])
        ]

        # Line that crosses the first obstacle
        line_crossing = [(2, 2), (4, 6)]
        self.assertTrue(is_line_crossing_obstacles(line_crossing, obstacles))

        # Line that does not cross any obstacle
        line_not_crossing = [(5, 5), (6, 6)]
        self.assertFalse(is_line_crossing_obstacles(
            line_not_crossing, obstacles))

        # Line that touches the edge of the first obstacle
        line_touching_edge = [(3, 2), (3, 6)]
        self.assertFalse(is_line_crossing_obstacles(
            line_touching_edge, obstacles))

        # Line that is completely inside the first obstacle
        line_inside_obstacle = [(1, 1), (2, 2)]
        self.assertTrue(is_line_crossing_obstacles(
            line_inside_obstacle, obstacles))

    def tearDown(self):
        # Clean up inupt file
        os.remove('tests/config.yaml')

if __name__ == '__main__':
    unittest.main()
