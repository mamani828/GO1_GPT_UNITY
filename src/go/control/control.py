#!/usr/bin/env python3

from go_clnt import get_info, turn
from imu import get_imu_data
from float import float_equals
from angles import wrap_angle
from math import radians 
import rospy

def print_info(current, desired):
    print(f"current: {current}")           
    print(f"desired: {desired}")

def get_current_angle():
    response = get_info()
    data = get_imu_data(response)
    if data is not None:
        return data.yaw
    return None

def get_desired_angle(current, relative):
    if current is not None:
        desired = wrap_angle(current+relative)
        print_info(current, desired)
        return desired
    return None

def adjust_angle(initial, desired, relative):
    sign = -1 if relative < 0 else 1
    REASONABLE_VELOCITY = .2 * sign
    if initial is None or desired is None: 
        return
    rate = rospy.Rate(15)
    current = initial
    while not float_equals(current, desired):
        current = get_current_angle()
        print_info(current, desired)        
        turn(REASONABLE_VELOCITY)
        rate.sleep()

if __name__ == "__main__":
    rospy.init_node('Were_Team_GO')
    DESIRED_MOVEMENT = 5
    current = get_current_angle()
    desired = get_desired_angle(current, radians(DESIRED_MOVEMENT))
    adjust_angle(current, desired, DESIRED_MOVEMENT)