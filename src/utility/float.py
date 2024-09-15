#!/usr/bin/env python3

def float_equals(a, b, tolerance=0.01):
    """
    Compare two floating-point numbers to see if they are equivalent within a specified tolerance.
    
    Parameters:
        a (float): The first number to compare.
        b (float): The second number to compare.
        tolerance (float): The margin of error within which the two numbers are considered equivalent.

    Returns:
        bool: True if the numbers are equivalent within the specified tolerance, False otherwise.
    """
    return abs(a - b) <= tolerance