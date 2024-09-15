#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

""" The go service client is responsible for calling go_srv to control the robot's movement. """

DOG_IP = '192.168.12.1'

def stop():
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="stop", 
                    args={}
    ))

def turn(vel):
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="turn", 
                    args={"vel":vel}
    ))

def walk(vel):
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="walk", 
                    args={"vel":vel}
    ))

def side(vel):
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="side", 
                    args={"vel":vel}
    ))

def euler(roll, pitch, yaw):
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="euler", 
                    args={"roll": roll,
                          "pitch": pitch,
                          "yaw": yaw}
    ))
def dance():
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="dance", 
                    args={}
    ))
def stop_dance():
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO],
                 request=GenericRequest(function="stop_dance", args={}))

def get_info():
    response = call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], 
                request=GenericRequest(
                    function="get_info", 
                    args={}
    ))
    return response

if __name__ == "__main__":
    print(get_info())
    side(.2)