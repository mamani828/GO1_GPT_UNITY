#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from snap import Snapper
#TODO fix imports for more modularity
""" # /home/WorkingPC/WorkingDir/src/go/videos/person.jpeg """

def detect():
    snapper = Snapper()
    snapper.get_frame()
    #TODO fix imports for more modularity
    return call_service(port=ServicePorts[ServiceNames.YOLO], 
                request=GenericRequest(
                    function="detect", 
                    args={"filepath": "/home/WorkingPC/WorkingDir/src/go/vision/snapper/current_frame.jpg"}
    ))

if __name__ == "__main__":
    print(detect())
