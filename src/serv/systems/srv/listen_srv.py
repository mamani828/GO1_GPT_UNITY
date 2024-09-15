#!/usr/bin/env python3

from multiprocessing import Process
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from server import start_server
from multiprocessing import Process, Value
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from server import start_server
from listen import ListenProcessor

def start_listen_process(should_speak):
    listener = ListenProcessor()
    listener.should_speak = should_speak
    listener.listen_for_command()

def generic_callback(request: GenericRequest, listener: ListenProcessor):
    function_call = getattr(listener, request.function)
    return function_call(**request.args)

def start_listen_server(name, port, should_speak):
    listener = ListenProcessor()
    listener.should_speak = should_speak
    try:
        start_server(name=name, port=port, callback=lambda request: generic_callback(request, listener))
    except Exception as e:
        print(e)

def start_listen(service_name, service_port):
    should_speak = Value('i', 1)
    server_process = Process(target=start_listen_server, args=(service_name, service_port, should_speak))
    listen_process = Process(target=start_listen_process, args=(should_speak,))
    
    server_process.start()
    listen_process.start()

    try:
        server_process.join()
        listen_process.join()
    except KeyboardInterrupt:
        server_process.terminate()
        listen_process.terminate()
        server_process.join()
        listen_process.join()

if __name__ == "__main__":
    try:
        start_listen(ServiceNames.LISTEN, ServicePorts[ServiceNames.LISTEN])
    except Exception as e:
        print(e)