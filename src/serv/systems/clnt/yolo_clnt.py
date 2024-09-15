#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from snap import Snapper

""" # /home/dicelabs/RevivingUnitree/src/go/videos/person.jpeg """

def detect():
    snapper = Snapper()
    snapper.get_frame()
    return call_service(port=ServicePorts[ServiceNames.YOLO], 
                request=GenericRequest(
                    function="detect", 
                    args={"filepath": "/home/dicelabs/RevivingUnitree/src/go/vision/snapper/current_frame.jpg"}
    ))

if __name__ == "__main__":
    print(detect())
