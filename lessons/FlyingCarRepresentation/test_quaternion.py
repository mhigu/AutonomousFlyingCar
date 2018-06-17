from unittest import TestCase

import numpy as np
from lessons.FlyingCarRepresentation.quaternions import euler_to_quaternion, quaternion_to_euler


class TestQuaternion(TestCase):
    def test_euler_to_quaternion(self):
        euler = np.array([np.deg2rad(90), np.deg2rad(30), np.deg2rad(0)])
        q = euler_to_quaternion(euler)  # should be [ 0.683  0.683  0.183 -0.183]
        self.assertTrue(
            (np.around(q, decimals=3) == np.array([0.683, 0.683, 0.183, -0.183])).all()
        )

    def test_quaternion_to_euler(self):
        e = quaternion_to_euler(np.array([0.683, 0.683, 0.183, -0.183]))
        expect = np.around(np.array([np.deg2rad(90), np.deg2rad(30), np.deg2rad(0)]), decimals=3)
        print(e)
        self.assertTrue(
            (expect == np.around(e, decimals=3)).all()
        )
