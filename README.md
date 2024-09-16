# GO1_GPT_UNITY
This codebase is a configuration of scripts to enable the control, edge sensor communication and BIM integration. The high-level architecture follows a communication between Unity Game Engine which handles navigation and robot control through BIM, a Python backend that handles the inner communications between APIs and processes, and the Go1 API for robotic control. 

The backbone of the communications between processes is done through a generic client-server architecture. This modular setup gives us the opportunity to be able to add custom scripts to the system on seperate processes. Having seperate processes prevents a single process from getting overloaded and slowed down. We use the Python forker to start these processes on launch. 

The current code/example is made to work with an edge camera for activity recognition and autonomius data labeling. OpenAI ChatGPT API, ElevenLabs API for text-to-speech, and a microphone with the Google TTS for speech to text.


To start the code, SSH into the unitree.

Run Python3 go_srv.py

In a seperate terminal run:
 
python3 yolo_internal_srv.py

Either add the listen_srv.py to the forker or run the internal server in a seperate terminal (for logging purposes to not overcrowd one terminal)

python3 listen_internal_srv.py

and then run the main file:

python3 main_unitree.py