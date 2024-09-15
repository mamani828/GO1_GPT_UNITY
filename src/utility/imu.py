#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class IMUData:
    roll: float
    pitch: float
    yaw: float
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float

def get_imu_data(response):
    if response is not None:
        euler, accel, gyro = response
        roll, pitch, yaw = euler
        ax, ay, az = accel
        gx, gy, gz = gyro
        return IMUData(roll, pitch, yaw, ax, ay, az, gx, gy, gz)
    return None
