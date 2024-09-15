#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from control import get_current_angle, get_desired_angle, adjust_angle
from math import radians

class TestRobotMovement(unittest.TestCase):
    def setUp(self):
        self.initial_yaw = radians(45)  

    @patch('control.get_info')
    @patch('control.get_imu_data')
    def test_get_current_angle(self, mock_get_imu_data, mock_get_info):        
        mock_get_imu_data.return_value.yaw = self.initial_yaw
        mock_get_info.return_value = MagicMock()
        
        yaw = get_current_angle()
        
        self.assertEqual(yaw, self.initial_yaw)

    @patch('control.wrap_angle')
    @patch('control.print_info')
    def test_get_desired_angle(self, mock_print_info, mock_wrap_angle):        
        mock_wrap_angle.return_value = radians(135)
        current_yaw = radians(45)
        relative_yaw = radians(90)
        
        desired_yaw = get_desired_angle(current_yaw, relative_yaw)
        
        mock_print_info.assert_called_with(current_yaw, radians(135))
        self.assertEqual(desired_yaw, radians(135))

    @patch('control.get_current_angle')
    @patch('control.print_info')
    @patch('control.turn')
    @patch('control.rospy.Rate')
    def test_adjust_angle(self, mock_rate, mock_turn, mock_print_info, mock_get_current_angle):        
        mock_rate.return_value.sleep = MagicMock()
        mock_get_current_angle.side_effect = [radians(45), radians(90)]  
        
        adjust_angle(radians(45), radians(90))
        
        mock_turn.assert_called_with(0.2)        
        self.assertTrue(mock_print_info.call_count >= 1)

if __name__ == '__main__':
    unittest.main()
