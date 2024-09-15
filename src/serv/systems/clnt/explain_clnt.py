#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

""" Explain service client responsible for calling explain_srv to generate explanations for inferences made by the vision service. """
def explain(video_path: str, activity: str, probability: float, timestamp: str, dir_context):
    # call explain_srv using the generic call_service to get inference explanation
    response = call_service(port=ServicePorts[ServiceNames.EXPLAIN], 
                # create a request to trigger the EXPLAIN service
                request=GenericRequest(
                    function="explain", # this is the function called by the server
                    args={
                        "video_path": video_path,
                        "activity": activity,
                        "probability": probability,
                        "timestamp": timestamp,
                        "dir_context": dir_context
                        }
    ))

    if not response:
        print("Failed to generate explanation.")



if __name__ == "__main__":
    # example usage: explain(<path to video file>, <detected activity>, <inference probability>)
    explain("path/to/video.mp4", "human is hammering", 0.85)
    