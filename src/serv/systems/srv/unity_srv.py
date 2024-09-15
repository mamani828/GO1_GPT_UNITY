#!/usr/bin/env python3

from forker import Forker

""" Starts all the services that interact with the Unity GameEngine. """

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "angular_srv.py",
            "linear_srv.py",
            "vision_srv.py",
            "speech_srv.py",
            "dance_srv.py",
            "stop_dance_srv.py"
            
        ]
    )
