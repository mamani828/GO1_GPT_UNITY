# #!/usr/bin/env python3

# import subprocess
# import signal
# import os

# def fork_processes(scripts):
#         processes = []
#         for script in scripts:
#             process = subprocess.Popen(script)
#             processes.append(process)
#         return processes

# def terminate_processes(processes):
#     for process in processes:
#         if process.poll() is None:  
#             process.kill()  
#     print("All child processes terminated.")

# class Forker():
#     @staticmethod
#     def run_scripts(scripts):
#         formatted_scripts = []
#         for script in scripts:
#             formatted_script = []
#             formatted_script.append(script)
#             formatted_scripts.append(formatted_script)
#         processes = fork_processes(formatted_scripts)

#         def signal_handler(signum, frame):
#             print("Received signal to terminate. Cleaning up...")
#             terminate_processes(processes)
#             os._exit(0)  

#         signal.signal(signal.SIGINT, signal_handler)

#         for process in processes:
#             process.wait()

# if __name__ == "__main__":
#     Forker.run_scripts(
#         [
#             "unity_srv.py",
#             "speak_srv.py",
#             "ar_srv.py"
#         ]
#     )

""" ORIGINAL forker.py FILE ABOVE -- TESTING EXPLAIN FEATURE BELOW """

#!/usr/bin/env python3

import subprocess
import signal
import os

def fork_processes(scripts):
        processes = []
        for script in scripts:
            process = subprocess.Popen(script)
            processes.append(process)
        return processes

def terminate_processes(processes):
    for process in processes:
        if process.poll() is None:  
            process.kill()  
    print("All child processes terminated.")

class Forker():
    @staticmethod
    def run_scripts(scripts):
        formatted_scripts = []
        for script in scripts:
            formatted_script = []
            formatted_script.append(script)
            formatted_scripts.append(formatted_script)
        processes = fork_processes(formatted_scripts)

        def signal_handler(signum, frame):
            print("Received signal to terminate. Cleaning up...")
            terminate_processes(processes)
            os._exit(0)  

        signal.signal(signal.SIGINT, signal_handler)

        for process in processes:
            process.wait()

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "unity_srv.py",
            "speak_srv.py",
            "ar_srv.py",
            
            # for EXPLAIN service
            "explain_srv.py"
        ]
    )