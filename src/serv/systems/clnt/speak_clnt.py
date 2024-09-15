#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

def speak(phrase: str):
    call_service(port=ServicePorts[ServiceNames.SPEAK], 
                request=GenericRequest(
                    function="speak", 
                    args={"phrase": phrase}
    ))

if __name__ == "__main__":
    speak("Starting Activity Recognition")