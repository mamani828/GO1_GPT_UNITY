#!/usr/bin/env python3
from req_resp import Object

class Defaults():
    LOCALHOST = '0.0.0.0'
    PORT = 6002
    DEFAULT_NAME = "Generic"
    BUFFER_SIZE = 1024

    @staticmethod
    def default_callback(request: Object):
        return request.x + request.y + request.z

    Trigger = 0
    request = Object(1,2,3)