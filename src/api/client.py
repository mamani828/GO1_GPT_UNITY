#!/usr/bin/env python3

import socket
from defaults import Defaults
import pickle

def call_service(host=Defaults.LOCALHOST, port=Defaults.PORT, request=Defaults.request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        raw_request = pickle.dumps(request)
        s.sendall(raw_request)
        raw_response = s.recv(Defaults.BUFFER_SIZE)
        if raw_response:
            response = pickle.loads(raw_response)
            return response
        return None # Optional would be much preferred in a typed language, make sure to Null check

if __name__ == "__main__":
    call_service()