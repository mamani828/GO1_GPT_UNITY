#!/usr/bin/env python3

import speech_recognition as sr
from speak_clnt import speak
import os
import sys
import threading
from go_clnt import dance, stop_dance
import time
from explain_clnt import explain
import os
from pathlib import Path
from vision_config import DirectoryContext
import json
from multiprocessing import Value
# Redirect stderr to /dev/null to suppress ALSA and JACK warnings
FNULL = open(os.devnull, 'w')
os.dup2(FNULL.fileno(), sys.stderr.fileno())
class ListenProcessor():
    def __init__(self):
        self.should_speak = Value('i', 1) 
        self.dir_context = DirectoryContext(base_dir=f"{Path.home()}/RevivingUnitree/src/go/videos")
    def read_variables(self):
        file_path = os.path.join(self.dir_context.inference_data_dir, "inference_variables.json")
        with open(file_path, 'r') as f:
            data = json.load(f)
        video_path = data["good_path"]
        activity = data["clas"]
        probability = data["prob"]
        timestamp = data["timestamp"]
        return video_path, activity, probability, timestamp
    def get_should_speak(self):
        with self.should_speak.get_lock():
            return self.should_speak.value

    def set_should_speak(self, value):
        with self.should_speak.get_lock():
            self.should_speak.value = value


    def listen_for_command(self):
        recognizer = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                print("Listening for 'aztec'...")
                recognizer.adjust_for_ambient_noise(source, duration=0.45)
                try:
                    audio = recognizer.listen(source, timeout=1.25, phrase_time_limit=1.25)
                    print("Audio captured. Attempting to recognize...")
                except sr.WaitTimeoutError:
                    print("No audio detected in the last 0.75 seconds. Continuing to listen...")
                    continue

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {text}")

                if "continue" in text or "resume" in text:
                    with self.should_speak.get_lock():
                        self.should_speak.value= 1
                    speak("sounds good, Resuming speaking activations")
                    print("Resuming speaking activations")
                    continue
                if "dance" in text:
                    speak("I'm going to dance!")
                    dance()
                    speak("I hope you are enjoying my dance!")
                if "stop" in text:
                    stop_dance()
                    speak("I hope you enjoyed my dance!")

                if "aztec" in text or "fantastic" in text or "tech" in text or "as" in text or "attack" in text:
                    print("Wake word detected! Listening for command...")
                    try:
                        speak("Yes?")
                        with self.should_speak.get_lock():
                            self.should_speak.value = 0
                        print("Speaking disabled")
                        print(self.should_speak.value)
                        self.text = text
                    except Exception as e:
                        print(f"Failed to speak: {e}")
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.45)
                        try:
                            audio = recognizer.listen(source, timeout=2.25, phrase_time_limit=2)
                            print("Command audio captured. Attempting to recognize...")
                        except sr.WaitTimeoutError:
                            print("No command detected. Resuming wake word detection.")
                            continue

                    try:
                        
                        command = recognizer.recognize_google(audio).lower()
                        self.text = command
                        if "dance" in command:
                            speak("I'm going to dance!")
                            dance()
                            speak("I hope you are enjoying my dance!")
                        if "stop" in command:
                            stop_dance()
                            speak("I hope you enjoyed my dance!")
                        if "today" in command or "weather" in command:
                            speak("It is a bit hot innit?")
                        print(f"Recognized command: {command}")
                        if any(keyword in command for keyword in ["why", "explain", "what", "how", "think"]) and "weather" not in command:
                            speak_thread = threading.Thread(target=speak, args=("Let me explain!",))
                            explain_thread = threading.Thread(target=explain,
                                                            args=(*self.read_variables(), self.dir_context))
                            # Start both threads
                            speak_thread.start()
                            explain_thread.start()
                            # Wait for both threads to complete
                            speak_thread.join()
                            explain_thread.join()
                        else:
                            speak("I heard you, but I'm not sure what you're asking. Can you rephrase that as a question?")
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand the command audio")
                        speak("Sorry, I couldn't understand the command. Can you try again?")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                        speak("Sorry, I'm having trouble connecting to my speech recognition service. Please try again later.")

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
if __name__ == "__main__":
    processor = ListenProcessor()