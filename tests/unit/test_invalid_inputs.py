import sys
import unittest
import subprocess
import os


class TestInvalidInputs(unittest.TestCase):

    def run_program(self, args):
        result = subprocess.run(
            [sys.executable, './src/pathfind/main.py'] + args,
            capture_output=True,
            text=True
        )

        return result

    def test_missing_input_file(self):
        result = self.run_program(['nonexistent.yaml'])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "The input YAML file 'nonexistent.yaml' does not exist.", result.stderr)

    def test_invalid_yaml_format(self):
        with open('tests/invalid.yaml', 'w') as f:
            f.write("invalid: [unclosed list")
        result = self.run_program(['tests/invalid.yaml'])
        self.assertNotEqual(result.returncode, 0)
        os.remove('tests/invalid.yaml')
        self.assertIn(
            "Failed to load configuration from 'tests/invalid.yaml'.", result.stderr)

    def test_start_point_out_of_bounds(self):
        with open('tests/out_of_bounds.yaml', 'w') as f:
            f.write("""
x_start: 200
y_start: 200
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: []
""")
        result = self.run_program(['tests/out_of_bounds.yaml'])
        self.assertNotEqual(result.returncode, 0)
        os.remove('tests/out_of_bounds.yaml')
        self.assertIn("Start point is out of bounds.", result.stderr)

    def test_goal_point_out_of_bounds(self):
        with open('tests/out_of_bounds.yaml', 'w') as f:
            f.write("""
x_start: 2
y_start: 2
x_goal: 200
y_goal: 200
x_space_size: 100
y_space_size: 100
list_obstacles: []
""")
        result = self.run_program(['tests/out_of_bounds.yaml'])
        self.assertNotEqual(result.returncode, 0)
        os.remove('tests/out_of_bounds.yaml')
        self.assertIn("Goal point is out of bounds.", result.stderr)

    def test_invalid_obstacle(self):
        with open('tests/invalid_obstacle.yaml', 'w') as f:
            f.write("""
x_start: 2
y_start: 2
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: [
[[0, 0], [1, 1], [1, 0], [0, 1]]  # Self-intersecting polygon
]
""")
        result = self.run_program(['tests/invalid_obstacle.yaml'])
        self.assertNotEqual(result.returncode, 0)
        os.remove('tests/invalid_obstacle.yaml')
        self.assertIn("Invalid obstacle:", result.stderr)

    def test_no_valid_path(self):
        with open('tests/no_valid_path.yaml', 'w') as f:
            f.write("""
x_start: 2
y_start: 2
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: [
[[0, 0], [100, 0], [100, 100], [0, 100]]  # Enclosing the entire space
]
""")
        result = self.run_program(['tests/no_valid_path.yaml'])
        self.assertNotEqual(result.returncode, 0)
        os.remove('tests/no_valid_path.yaml')
        self.assertIn("No valid path found", result.stderr)


if __name__ == '__main__':
    unittest.main()
