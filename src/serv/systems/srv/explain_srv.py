#!/usr/bin/env python3
from explain_processor import ExplainProcessor
from services import ServiceNames, ServicePorts
from gen_srv import start_generic_server

""" The explain service is responsible for generating explanations using explain_processor for inferences made by the vision service. """


    
if __name__ == "__main__":
    # start the server for the explain service
    start_generic_server(
        name=ServiceNames.EXPLAIN,
        port=ServicePorts[ServiceNames.EXPLAIN],
        classtype=ExplainProcessor
    )
    print("Explain Service Up and running")