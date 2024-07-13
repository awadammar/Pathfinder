# Pathfinder

## Description
This program finds the shortest path for a point-shaped robot in a 2D space with polygonal obstacles. The robot starts at a specified point and aims to reach a goal point, avoiding obstacles along the way.

## Features
- **Pathfinding**: Uses the A* algorithm to find the shortest path.
- **Obstacle Validation**: Ensures obstacles are valid and do not overlap or exceed bounds.
- **Visualization**: Plots the obstacles, start and goal points, and the computed path.
- **Configuration**: Easily configurable via a YAML file.

## Requirements
- Python 3.12+
- Virtual environment (recommended)

## Installation
1. **Option 1: Invoke the installer bash script**:
    ```bash
    bash install.sh  # On Windows
    # or
    ./install.sh  # On Unix-based systems
    ```

2. **Option 2: Install the pathfinder package directly**:
    ```bash
    pip install -e .
    ```

## Usage
1. **Prepare a configuration file**:
    - Edit your configuration file to set the start and goal points, space size, obstacles, mass, and maximum acceleration.
    - Example configuration:
    
```yaml:tests/config.yaml
x_start: 2
y_start: 2
x_goal: 98
y_goal: 98
x_space_size: 100
y_space_size: 100
list_obstacles: [
[[5,5], [10,5], [8,12]],
[[50,60], [70,40], [80,90], [60,80]],
[[60, 60], [60, 80], [80, 80], [80, 60]]
]
mass: 1.0
max_acceleration: 1.0
```

2. **Run the program**:
    ```bash
    pathfinder config_file.yaml output_file.txt --plot
    ```

3. **Output**:
    - The shortest path will be saved to an output file named as passed in the program arguments or to `solution.txt` if no file name was provided.
    - Plots of the scene and solution will be saved as `scene.png` and `solution.png` respectively, only if  the `--plot` flag is passed.

## Limitations and Assumptions
- **Limitations**:
  - The program assumes that the obstacles are simple polygons and does not handle complex shapes or 3D obstacles.
  - The space is assumed to be a 2D plane with fixed dimensions.
  - The A* algorithm may not be the most efficient for very large spaces or a high number of obstacles.

- **Assumptions**:
  - The start and goal points are within the bounds of the space.
  - The obstacles are defined as lists of points in a counter-clockwise order.
  - The configuration file is correctly formatted as a YAML file.