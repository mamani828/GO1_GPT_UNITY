#!/usr/bin/env python3

from req_resp import GenericRequest
from server import start_server

# Pass in any custom class type for object
def generic_callback(request: GenericRequest, object): 
    function_call = getattr(object, request.function)
    return function_call(**request.args)

def start_generic_server(name, port, classtype):
    object = classtype()
    try:
        start_server(name=name, port=port, callback=lambda request: generic_callback(request, object))
    except Exception as e:
        print(e)
