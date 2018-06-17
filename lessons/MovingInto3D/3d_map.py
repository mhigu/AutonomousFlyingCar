import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# plt.rcParams['figure.figsize'] = 16, 16


"""
While representing the configuration space in 3 dimensions isn't 
entirely practical it's fun (and useful) to visualize things in 3D.

In this exercise you'll finish the implementation of create_grid such that
a 3D grid is returned where cells containing a voxel are set to True. We'll then plot the result!
"""


def create_voxmap(data, voxel_size=5):
    """
    Returns a grid representation of a 3D configuration space
    based on given obstacle data.

    The `voxel_size` argument sets the resolution of the voxel map.
    """

    # minimum and maximum north coordinates
    north_min = np.floor(np.amin(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.amax(data[:, 0] + data[:, 3]))

    # minimum and maximum east coordinates
    east_min = np.floor(np.amin(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.amax(data[:, 1] + data[:, 4]))

    alt_max = np.ceil(np.amax(data[:, 2] + data[:, 5]))

    # given the minimum and maximum coordinates we can
    # calculate the size of the grid.
    north_size = int(np.ceil((north_max - north_min))) // voxel_size
    east_size = int(np.ceil((east_max - east_min))) // voxel_size
    alt_size = int(alt_max) // voxel_size

    voxmap = np.zeros((north_size, east_size, alt_size), dtype=np.bool)

    for i in range(data.shape[0]):
        # continue
        # TODO: fill in the voxels that are part of an obstacle with `True`
        #
        # i.e. grid[0:5, 20:26, 2:7] = True
        north_start = int(np.median(np.array([0, int((data[i][0] - data[i][3]) - north_min)//voxel_size, north_size])))
        north_end = int(np.median(np.array([0, int((data[i][0] + data[i][3]) - north_min)//voxel_size, north_size])))
        east_start = int(np.median(np.array([0, int((data[i][1] - data[i][4]) - east_min)//voxel_size, east_size])))
        east_end = int(np.median(np.array([0, int((data[i][1] + data[i][4]) - east_min)//voxel_size, east_size])))
        alt_end = int(np.median(np.array([0, int(data[i][2] + data[i][5])//voxel_size, alt_size])))

        voxmap[north_start:north_end, east_start:east_end, 0:alt_end] = True

    return voxmap


if __name__ == "__main__":
    # This is the same obstacle data from the previous lesson.
    filename = 'data/colliders.csv'
    data = np.loadtxt(filename, delimiter=',', dtype='Float64', skiprows=2)
    print(data)
    voxmap = create_voxmap(data, 10)
    print(voxmap.shape)

    # visualize 3d map
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(voxmap, edgecolor='k')
    ax.set_xlim(voxmap.shape[0], 0)
    ax.set_ylim(0, voxmap.shape[1])
    # add 100 to the height so the buildings aren't so tall
    ax.set_zlim(0, voxmap.shape[2] + 70)

    plt.xlabel('North')
    plt.ylabel('East')

    plt.show()
