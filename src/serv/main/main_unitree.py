#!/usr/bin/env python3

from forker import Forker

""" Main script to run all services. Uses Forker utility to fork individual processes for each service. """

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "unity_srv.py",
            "speak_srv.py",
            "ar_srv.py",
            "explain_srv.py"
        ]
    )