import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np

FILE_EXTENSION = ".png"
SCENE_FILE_NAME = "scene"
SOLUTION_FILE_NAME = "solution"


class Plotter:
    def plot_scene(path, start, goal, obstacles, x_space_size, y_space_size):
        """
        Plot the scene with the start and goal points, obstacles, and the path.

        Parameters:
        - path (list): The list of points representing the path.
        - start (tuple): The starting point coordinates.
        - goal (tuple): The goal point coordinates.
        - obstacles (list): A list of obstacles, each defined by a list of points.
        - x_space_size (int): The width of the space.
        - y_space_size (int): The height of the space.
        - savePlots (bool): If True, save the plots as images. Default is False.
        """
        fig, ax = plt.subplots()
        for polygon in obstacles:
            patch_polygon = patch.Polygon(
                polygon.exterior.coords[:-1], closed=True, edgecolor='black', facecolor='gray', zorder=2)
            ax.add_patch(patch_polygon)

        ax.scatter(start[0], start[1], color='green', label='Start')
        ax.scatter(goal[0], goal[1], color='blue', label='Goal')
        # Add labels to the start and goal points
        ax.annotate('Start', start, textcoords="offset points",
                    xytext=(0, 10), ha='center')
        ax.annotate('Goal', goal, textcoords="offset points",
                    xytext=(0, 10), ha='center')

        ax.set_xlim([0, x_space_size])
        ax.set_ylim([0, y_space_size])
        plt.title("Shortest Path From Start To Goal")
        plt.savefig(SCENE_FILE_NAME + FILE_EXTENSION)

        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], color='red', linewidth=3)
        plt.savefig(SOLUTION_FILE_NAME + FILE_EXTENSION)
