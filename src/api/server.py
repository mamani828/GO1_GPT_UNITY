#!/usr/bin/env python3

import socket
from server_log import Logging
from defaults import Defaults
import pickle

def loop(name, sock, callback):
    conn, addr = sock.accept()
    with conn:
        Logging.log_connection_message(addr)
        data = conn.recv(Defaults.BUFFER_SIZE)
        if data:
            Logging.log_data_rcv_message(name)
            request = pickle.loads(data)
            response = callback(request)
            conn.sendall(pickle.dumps(response))

"""
    Generic Server API to Spawn Server Process
"""
def start_server(name=Defaults.DEFAULT_NAME, 
                host=Defaults.LOCALHOST, port=Defaults.PORT, 
                callback=Defaults.default_callback):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        Logging.log_server_active_message(name, host, port)
        try:
            while True:
                loop(name, sock, callback)
        except KeyboardInterrupt:
            print(f"\nServer shut down by user - freeing port {port}")
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

if __name__ == "__main__":
    start_server()