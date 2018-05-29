import numpy as np


def euler_to_quaternion(angles):
    roll = angles[0]
    pitch = angles[1]
    yaw = angles[2]

    sp = np.sin(pitch / 2.0)
    cp = np.cos(pitch / 2.0)
    sr = np.sin(roll / 2.0)
    cr = np.cos(roll / 2.0)
    sy = np.sin(yaw / 2.0)
    cy = np.cos(yaw / 2.0)

    # array_list = np.

    a = cr * cp * cy + sr * sp * sy
    b = sr * cp * cy - cr * sp * sy
    c = cr * sp * cy + sr * cp * sy
    d = cr * cp * sy - sr * sp * cy
    return [a, b, c, d]


def quaternion_to_euler(quaternion):
    a = quaternion[0]
    b = quaternion[1]
    c = quaternion[2]
    d = quaternion[3]

    roll = np.arctan2(2.0 * (a * b + c * d), 1.0 - 2.0 * (b ** 2 + c ** 2))
    pitch = np.arcsin(2.0 * (a * c - d * b))
    yaw = np.arctan2(2.0 * (a * d + b * c), 1.0 - 2.0 * (c ** 2 + d ** 2))

    return [roll, pitch, yaw]
