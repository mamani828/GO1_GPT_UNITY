#!/usr/bin/env python3
from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
def listen():
    return call_service(port=ServicePorts[ServiceNames.LISTEN],
                        request=GenericRequest(
                            function="listen_for_command",
                            args={}
                        ))

def get_should_speak():
    return call_service(port=ServicePorts[ServiceNames.LISTEN],
                        request=GenericRequest(
                            function="get_should_speak",
                            args={}
                        ))

def set_should_speak(value):
    return call_service(port=ServicePorts[ServiceNames.LISTEN],
                        request=GenericRequest(
                            function="set_should_speak",
                            args={"value": value}
                        ))




if __name__ == "__main__":
    listen()