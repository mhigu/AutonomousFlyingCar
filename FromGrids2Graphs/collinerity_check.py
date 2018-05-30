import numpy as np


def collinearity_float(p1, p2, p3, epsilon=1e-2):
    mat = np.vstack((
        np.array([p1[0], p1[1], 1.]),
        np.array([p2[0], p2[1], 1.]),
        np.array([p3[0], p3[1], 1.]),
    ))
    det = np.linalg.det(mat)
    collinear = det < epsilon

    return collinear


def collinearity_int(p1, p2, p3):
    det = p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
    collinear = det == 0

    return collinear


if __name__ == "__main__":
    import time

    p1 = np.array([1, 2])
    p2 = np.array([2, 3])
    p3 = np.array([3, 4])

    t1 = time.time()
    collinear_3d = collinearity_float(p1, p2, p3)
    t_3D = time.time() - t1

    t1 = time.time()
    collinear_2d = collinearity_int(p1, p2, p3)
    t_2D = time.time() - t1
    print(t_3D / t_2D)
