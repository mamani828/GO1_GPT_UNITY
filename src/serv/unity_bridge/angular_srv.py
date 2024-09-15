#!/usr/bin/env python3

from tcp_srv import TCPServer
from struct import unpack, calcsize
from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

DATA_REPRESENTATION = '1f' # Two Floats
PACKET_SIZE = calcsize(DATA_REPRESENTATION)
DOG_IP = '192.168.12.1'

def callback(data):
    x = unpack(DATA_REPRESENTATION, data)
    ang_vel = 1.545*x[0]
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], request=GenericRequest(function="turn", args={"vel": ang_vel}))

if __name__ == "__main__":
    tcp_server = TCPServer(port=7001, name='Angular Velocity', callback=lambda data: callback(data), payload_size=PACKET_SIZE)
    tcp_server.run()
