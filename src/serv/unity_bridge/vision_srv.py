#!/usr/bin/env python3

from yolo_clnt import detect
import socket
import struct
import time
import threading

human_detected = False # It's one global, get over it

def detection_thread():
    global human_detected
    while True:
        human_detected = detect()
        time.sleep(.1) # Add a delay to avoid excessive polling

def callback(conn: socket.socket):
    MSG_FORMAT = '?'
    response = human_detected
    raw_data = struct.pack(MSG_FORMAT, response)
    try:
        conn.sendall(raw_data)
    except BrokenPipeError:
        print("Connection closed unexpectedly by the client.")

def print_shutdown():
    SHUTDOWN_MSG = "User wants to shutdown, cleaning up resources"
    print(SHUTDOWN_MSG)

def handle_request(conn, sock):
    try:
        while True:
            data = conn.recv(4)
            if not data:
                break
            callback(conn)
    except KeyboardInterrupt:
        print_shutdown()
        conn.shutdown(socket.SHUT_RDWR)
        sock.shutdown(socket.SHUT_RDWR)
    finally:
        conn.close()
        sock.close()

def setup_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 7002))
    server_socket.listen(1)
    print("Vision service is listening on 0.0.0.0:7002...")
    return server_socket

def connect_sock(server_socket: socket.socket):
    try:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        return conn
    except KeyboardInterrupt:
        print("Closed before connection could be made")
        exit()

def main():
    detection_thread_obj = threading.Thread(target=detection_thread)
    detection_thread_obj.daemon = True
    detection_thread_obj.start()

    server_socket = setup_server()
    conn = connect_sock(server_socket)
    handle_request(conn, server_socket)
    server_socket.close()

if __name__ == "__main__":
    main()