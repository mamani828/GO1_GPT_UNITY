#!/usr/bin/env python3

from yolo import PeopleDetector
from services import ServiceNames, ServicePorts
from gen_srv import start_generic_server

""" The yolo service server is responsible for detecting people in images. """

if __name__ == "__main__":
    start_generic_server(ServiceNames.YOLO, ServicePorts[ServiceNames.YOLO], PeopleDetector)