import numpy as np
from enum import Enum

np.set_printoptions(precision=3, suppress=True)


class Rotation(Enum):
    ROLL = 0
    PITCH = 1
    YAW = 2  


class EulerRotation:
    
    def __init__(self, rotations):
        """
        `rotations` is a list of 2-element tuples where the
        first element is the rotation kind and the second element
        is angle in degrees.
        
        Ex:
        
            [(Rotation.ROLL, 45), (Rotation.YAW, 32), (Rotation.PITCH, 55)]
            
        """
        self._rotations = rotations
        self._rotation_map = {Rotation.ROLL: self.roll, Rotation.PITCH: self.pitch, Rotation.YAW: self.yaw}

    def roll(self, phi):
        """Returns a rotation matrix along the roll axis"""
        rx = np.array([
            [1, 0, 0], 
            [0, np.cos(phi), -np.sin(phi)],
            [0, np.sin(phi), np.cos(phi)]
            ])
        return rx
    
    def pitch(self, theta):
        """Returns the rotation matrix along the pitch axis"""
        ry = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
            ])
        return ry

    def yaw(self, psi):
        """Returns the rotation matrix along the yaw axis"""
        rz = np.array([
            [np.cos(psi), -np.sin(psi), 0],
            [np.sin(psi), np.cos(psi), 0],
            [0, 0, 1]
        ])
        return rz

    def rotate(self):
        """Applies the rotations in sequential order"""
        t = np.eye(3)
        for rotation in self._rotations:
            dimension = rotation[0]
            value = np.deg2rad(rotation[1])
            f = self._rotation_map[dimension]
            t = np.dot(f(value), t)
        return t
