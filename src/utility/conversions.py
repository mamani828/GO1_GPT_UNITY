#!/usr/bin/env python3

import math

def quaternion_to_euler(w, x, y, z):
    """
    Convert a quaternion into Euler angles (roll, pitch, yaw).
    This function converts a quaternion (w, x, y, z) into Euler angles,
    assuming the standard convention of rotations in the order of roll (X-axis),
    pitch (Y-axis), and yaw (Z-axis).
    """
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x**2 + y**2)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp) 
    else:
        pitch = math.asin(sinp)
    
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y**2 + z**2)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


def euler_to_quaternion(yaw, pitch, roll):
    """
    Convert Euler angles (roll, pitch, yaw) to a quaternion.
    Angles must be in radians.
    """
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return w, x, y, z

def degrees_to_radians(yaw, pitch, roll):
    """
    Convert yaw, pitch, and roll angles from degrees to radians.
    This function converts angles given in degrees to radians,
    useful for transforming Euler angles to a format suitable
    for mathematical computations and functions that require radians.
    """
    return math.radians(yaw), math.radians(pitch), math.radians(roll)

def radians_to_degrees(yaw, pitch, roll):
    """
    Convert yaw, pitch, and roll angles from degrees to radians.
    This function converts angles given in degrees to radians,
    useful for transforming Euler angles to a format suitable
    for mathematical computations and functions that require radians.
    """
    return math.degrees(yaw), math.degrees(pitch), math.degrees(roll)

if __name__ == "__main__":
    yaw, pitch, roll = quaternion_to_euler(x=-0.028026025935007363,y=-0.7639695300163926,z=-0.6437651947236414,w=0.03363737711615717)
    yaw, pitch, roll = radians_to_degrees(yaw,pitch,roll)
    print (yaw, pitch, roll)

    yaw, pitch, roll = quaternion_to_euler(x=0.7686640998401458,y=0.019500606118823264,z=-0.008383110028113847,w=0.6393003608979063)
    yaw, pitch, roll = radians_to_degrees(yaw,pitch,roll)
    print (yaw, pitch, roll)