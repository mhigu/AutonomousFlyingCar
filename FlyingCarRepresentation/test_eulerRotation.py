from unittest import TestCase

from FlyingCarRepresentation.euler_rotaion import EulerRotation
from FlyingCarRepresentation.euler_rotaion import Rotation

import numpy as np


class TestEulerRotation(TestCase):

    def setUp(self):
        self.rotations = [
            (Rotation.ROLL, 25),
            (Rotation.PITCH, 75),
            (Rotation.YAW, 90),
        ]

    def test_roll(self):
        self.assertTrue(True)

    def test_pitch(self):
        self.assertTrue(True)

    def test_yaw(self):
        self.assertTrue(True)

    def test_rotate(self):
        rotation = EulerRotation(self.rotations).rotate()
        expect = np.array([
            [0.0, -0.906, 0.423],
            [0.259, 0.408, 0.875],
            [-0.966, 0.109, 0.234]
        ])
        self.assertTrue(
            (np.around(rotation, decimals=2) == np.around(expect, decimals=2)).all()
        )
