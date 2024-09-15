#!/usr/bin/env python3

from tcp_srv import TCPServer
from speak_clnt import speak

ENCODING_FORMAT ="utf-8"

def callback(data: bytes):
    speak(data.decode(ENCODING_FORMAT))

if __name__ == "__main__":
    tcp_server = TCPServer(port=7003, name='Speech Processing', callback=lambda data: callback(data), payload_size=1024)
    tcp_server.run()
