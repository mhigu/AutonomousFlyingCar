import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString
from queue import PriorityQueue

"""
In this notebook you'll expand on previous random sampling exercises by creating a graph from the points and running A*.

Load the obstacle map data
Sample nodes (use KDTrees here)
Connect nodes (use KDTrees here)
Visualize graph
Define heuristic
Define search method
Execute and visualize
We'll load the data for you and provide a template for visualization.
"""


def extract_polygons(data):
    polygons = []
    for i in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[i, :]

        # Extract the 4 corners of the obstacle
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

        # Compute the height of the polygon
        height = alt + d_alt

        # Once you've defined corners, define polygons
        p = Polygon(corners)
        polygons.append((p, height))

    return polygons


def collides(polygons, point):
    # Determine whether the point collides
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

    # TODO: sample points randomly
    # then use KDTree to find nearest neighbor polygon
    # and test for collision
    sample_row_indices = np.random.choice(range(len(data)), size=3, replace=False)
    sample_rows = data[sample_row_indices, :]

    # print(len(polygons))
    polygons = extract_polygons(data)

    from sklearn.neighbors import KDTree
    # tree = KDTree(samples[:, :3])
    # indices = tree.query([samples[0][:3]], k=3, return_distance=False)
    # print(indices)