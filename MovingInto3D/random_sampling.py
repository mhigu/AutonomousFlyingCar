import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Polygon, Point

"""
In this notebook you'll work with the obstacle's polygon representation itself.

Your tasks will be:

Create polygons.
Sample random 3D points.
Remove points contained by an obstacle polygon.
Recall, a point  (x,y,z)(x,y,z)  collides with a polygon if the  (x,y)(x,y)  coordinates are 
contained by the polygon and the  zz  coordinate (height) is less than the height of the polygon.
"""


def extract_polygons(data):
    polygons = []
    for i in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[i, :]

        # TODO: Extract the 4 corners of the obstacle
        #
        # NOTE: The order of the points matters since
        # `shapely` draws the sequentially from point to point.
        #
        # If the area of the polygon is 0 you've likely got a weird
        # order.
        corners = [(north - d_north, east - d_east),
                   (north - d_north, east + d_east),
                   (north + d_north, east + d_east),
                   (north + d_north, east - d_east)]

        # TODO: Compute the height of the polygon
        height = alt + d_alt

        # TODO: Once you've defined corners, define polygons
        p = Polygon(corners)
        polygons.append((p, height))

    return polygons


def collides(polygons, point):
    # TODO: Determine whether the point collides
    # with any obstacles.
    # return False
    for polygon in polygons:
        if polygon[1] > point[2] and polygon[0].contains(Point(*point[:2])):
                return True
    return False


if __name__ == "__main__":
    # This is the same obstacle data from the previous lesson.
    filename = 'data/colliders.csv'
    data = np.loadtxt(filename, delimiter=',', dtype='Float64', skiprows=2)
    print(data)

    polygons = extract_polygons(data)

    xmin = np.min(data[:, 0] - data[:, 3])
    xmax = np.max(data[:, 0] + data[:, 3])

    ymin = np.min(data[:, 1] - data[:, 4])
    ymax = np.max(data[:, 1] + data[:, 4])

    zmin = 0
    # Limit the z axis for the visualization
    zmax = 10

    print("X")
    print("min = {0}, max = {1}\n".format(xmin, xmax))

    print("Y")
    print("min = {0}, max = {1}\n".format(ymin, ymax))

    print("Z")
    print("min = {0}, max = {1}".format(zmin, zmax))

    num_samples = 100

    xvals = np.random.uniform(xmin, xmax, num_samples)
    yvals = np.random.uniform(ymin, ymax, num_samples)
    zvals = np.random.uniform(zmin, zmax, num_samples)

    samples = list(zip(xvals, yvals, zvals))

    print(samples[:10])

    t0 = time.time()
    to_keep = []
    for point in samples:
        if not collides(polygons, point):
            to_keep.append(point)
    time_taken = time.time() - t0
    print("Time taken {0} seconds ...", time_taken)
    print(len(to_keep))
