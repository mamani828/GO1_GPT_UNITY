#!/usr/bin/env python3

class Logging():
    @staticmethod
    def log_server_active_message(name: str, host: str, port: str):
        print(f"{name} Server is Up and Running on {host}:{port}")

    @staticmethod
    def log_connection_message(addr):
        print(f"Connected by {addr}")
        
    @staticmethod
    def log_data_rcv_message(name):
        print(f"Received Data From {name} Client")