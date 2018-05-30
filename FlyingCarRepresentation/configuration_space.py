import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [12, 12]

filename = './data/colliders.csv'
# Read in the data skipping the first two lines.
data = np.loadtxt(filename, delimiter=',', dtype='Float64', skiprows=2)
print(data)

# Static drone altitude (metres)
drone_altitude = 5

# Minimum distance required to stay away from an obstacle (metres)
safe_distance = 3


def create_grid(data, drone_altitude, safety_distance):
    """
    Returns a grid representation of a 2D configuration space
    based on given obstacle data, drone altitude and safety distance
    arguments.
    """

    # minimum and maximum north coordinates
    north_min = np.floor(np.amin(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.amax(data[:, 0] + data[:, 3]))

    # minimum and maximum east coordinates
    east_min = np.floor(np.amin(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.amax(data[:, 1] + data[:, 4]))

    # given the minimum and maximum coordinates we can
    # calculate the size of the grid.
    north_size = int(np.ceil(north_max - north_min))
    east_size = int(np.ceil(east_max - east_min))
    # Initialize an empty grid
    grid = np.zeros((north_size, east_size))
    # Center offset for grid
    north_min_center = np.min(data[:, 0])
    east_min_center = np.min(data[:, 1])
    # Populate the grid with obstacles
    for i in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[i, :]

        # Determine which cells contain obstacles
        # and set them to 1.
        #
        # Example:
        #
        #    grid[north_coordinate, east_coordinate] = 1
        if alt + d_alt + safety_distance > drone_altitude:
            north_center_index = north - north_min_center
            east_center_index = east - east_min_center

            north_from = int(np.clip(north_center_index - d_north, 0, north_size - 1))
            north_to = int(np.clip(north_center_index + d_north, 0, north_size - 1))
            east_from = int(np.clip(east_center_index - d_east, 0, east_size - 1))
            east_to = int(np.clip(east_center_index + d_east, 0, east_size - 1))

            grid[north_from:north_to, east_from:east_to] = 1

    return grid


if __name__ == "__main__":
    grid = create_grid(data, drone_altitude, safe_distance)
    plt.imshow(grid, origin='lower')

    plt.xlabel('EAST')
    plt.ylabel('NORTH')
    plt.show()