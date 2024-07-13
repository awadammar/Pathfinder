#!/usr/bin/env python

import argparse
import logging
import os
import sys
from pathfind.obstacle_course import ObstacleCourse
from pathfind.configuration import Configuration

# Configure logging
logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger('main')


def main():
    parser = argparse.ArgumentParser(
        prog='shortestPathFinding', description='Find the Shortest Path that avoids obstacles')
    parser.add_argument(
        'inputyaml', help='Path to the input YAML configuration file')
    parser.add_argument('output', nargs='?', default='solution.txt',
                        help='Path to the output solution file')
    parser.add_argument('--plot', action='store_true',
                        help='Flag to generate plot images')
    args = parser.parse_args()

    # Validate input YAML file
    if not os.path.isfile(args.inputyaml):
        LOGGER.error(f"The input YAML file '{args.inputyaml}' does not exist.")
        sys.exit(1)

    # Load configuration
    try:
        config = Configuration(args.inputyaml)
    except Exception as e:
        LOGGER.error(f"Failed to load configuration from '{
                     args.inputyaml}'. {e}")
        sys.exit(1)

    # Find fastest path
    try:
        obstacle_course = ObstacleCourse(config)
        path = obstacle_course.find_path()
    except Exception as e:
        LOGGER.error(f"{e}")
        sys.exit(1)

    # Save solution to file
    try:
        with open(args.output, 'w') as f:
            f.write(str(path))
    except Exception as e:
        LOGGER.error(f"Failed to write solution to '{args.output}'. {e}")
        sys.exit(1)

    # Plot and save results if needed
    try:
        if args.plot:
            obstacle_course.plot(path)
    except Exception as e:
        LOGGER.error(f"Failed to plot the scene. {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
