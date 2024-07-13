import unittest
import subprocess
import os
import sys
import yaml


class TestEndToEnd(unittest.TestCase):

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
        [[5,5], [10,5], [8,12]],
        [[50,60], [70,40], [80,90], [60,80]]
        ]
        """)

        # Load the configuration file
        with open('tests/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.output_file = 'tests/solution.txt'
        self.plot_flag = '--plot'

    def test_end_to_end(self):
        # Print Python executable and environment variables
        print(f"Python executable: {sys.executable}")
        print(f"Environment variables: {os.environ}")

        # Run the main program with the configuration file
        result = subprocess.run(
            [sys.executable, './src/pathfinder/main.py', 'tests/config.yaml',
                self.output_file, self.plot_flag],
            capture_output=True,
            text=True
        )

        # Check if the program ran successfully
        self.assertEqual(result.returncode, 0,
                         msg=f"Program failed with error: {result.stderr}")

        # Check if the output file is created
        self.assertTrue(os.path.exists(self.output_file),
                        "Output file was not created.")

        # Load the output file and check its contents
        with open(self.output_file, 'r') as file:
            output_data = file.read()
            self.assertTrue(output_data.startswith(
                '[['), "Output file does not contain a valid list of lists.")

        # Check if the plot files are created
        self.assertTrue(os.path.exists('solution.png'),
                        "Solution plot file was not created.")
        self.assertTrue(os.path.exists('scene.png'),
                        "Scene plot file was not created.")

    def tearDown(self):
        # Clean up inupt file
        os.remove('tests/config.yaml')
        # Clean up the output files
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists('solution.png'):
            os.remove('solution.png')
        if os.path.exists('scene.png'):
            os.remove('scene.png')


if __name__ == '__main__':
    unittest.main()
