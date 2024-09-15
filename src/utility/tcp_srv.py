#!/usr/bin/env python3

import socket

class TCPServer:
    def __init__(self, name='default', host='0.0.0.0', port=6000, callback=(), payload_size=4):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback
        self.payload_size = payload_size
        self.name = name

    def bind(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self):
        self.server_socket.listen(1)
        print(f"{self.name} Service listening on {self.host}:{self.port}")

    def accept_connections(self):
        try:
            connection, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.handle_connection(connection)
        except Exception as e:
            print(f"Error accepting connections: {e}")
        finally:
            self.close()

    def handle_connection(self, connection):
        try:
            while True:
                data = connection.recv(self.payload_size)
                if not data:
                    raise Exception("No data received, closing connection.")
                self.callback(data)
        except Exception as e:
            print(f"Connection handling error: {e}")
            self.server_socket.shutdown(socket.SHUT_RDWR)
        finally:
            connection.close()

    def run(self):
        try:
            self.bind()
            self.listen()
            self.accept_connections()
        except KeyboardInterrupt:
            print(f"Server shutdown by user, freeing port {self.port}")
            self.close()

    def close(self):
        self.server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    server = TCPServer()
    server.run()
