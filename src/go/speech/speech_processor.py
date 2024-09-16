#!/usr/bin/env python3
import os
import time
import pygame
import subprocess
import requests
############################################################
"""
    String Literals For Bash Handling
"""
BASH_INTERPRETER    = 'bash'
BASH_SUCCESS        = "Bash script executed successfully"
BASH_ERROR          = "Error running Bash script:"
############################################################

############################################################
""" 
    - Trigger:  Bash Script to send signal to dog to play certain file already on dog (fast)
    - Send:     Bash Script to send custom wav file to dog to speak (slow)
"""

#TODO fix imports for more modularity
TRIGGER_WAV_SCRIPT = "/home/WorkingPC/WorkingDir/src/go/speech/dog_trigger_speech.sh"
SEND_WAV_SCRIPT = "/home/WorkingPC/WorkingDir/src/go/speech/dog_send_speech.sh"
############################################################

def send_signal_to_dog(filename: str):
    """ 
        Filename is a file already on the dog that you would like to trigger it to play
    """
    try:
        subprocess.run([BASH_INTERPRETER, TRIGGER_WAV_SCRIPT, filename], check=True)
        print(BASH_SUCCESS)
    except subprocess.CalledProcessError as e:
        print(BASH_ERROR, e)

def send_temp_wav_file_to_dog():
    try:
        subprocess.run([BASH_INTERPRETER, SEND_WAV_SCRIPT], check=True)
        print(BASH_SUCCESS)
    except subprocess.CalledProcessError as e:
        print(BASH_ERROR, e)

############################################################
"""     
    This file is used to store a custom message, after language processing creates the wav file it saves it here,
    Then to send to the dog this file is referenced in the bash script to scp over to the dog's computer 
"""
#TODO fix imports for more modularity
TEMPORARY_WAV_FILE = '/home/WorkingPC/WorkingDir/src/go/speech/waves/temp.wav'
############################################################

class SpeechProcessor:
    def __init__(self):
        self.api_key = "INSERT API KEY" # Hardcoded API key
        self.voice_id = "NFG5qt843uXKj4pFvR7C" # Specify the correct voice ID
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech/"
        #TODO fix imports for more modularity
        self.output_dir = "/home/WorkingPC/WorkingDir/src/go/speech/waves"
    def speak(self, phrase: str, file: str = "activity.wav"):
        url = self.base_url + self.voice_id
        file_path = os.path.join(self.output_dir, file) 
        print(file_path)
        headers = {
            "Accept": "audio/wav",  # Changed to request WAV format
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": phrase,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.9,
                "similarity_boost": 0.7
            },
            "output_format": "wav"  # Assuming the API supports this parameter to specify format
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
                f.flush()
                os.fsync(f.fileno())
            print("Speech generated and saved to", file_path)
            time.sleep(1)  # Wait a second before playing the file
            self.play_audio(file_path)
        else:
            print("Failed to generate speech:", response.text)
    def play_audio(self, file_path):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2)  # Initialize mixer with common settings
        print("Initializing playback...")
        try:
            my_sound = pygame.mixer.Sound(file_path)
            my_sound.set_volume(1.0)  # Set volume to 100%
            print("Playing sound...")
            my_sound.play()
            # Wait for the sound to finish playing
            while pygame.mixer.get_busy():
                pygame.time.wait(10)  
        except Exception as e:
            print(f"Failed to play sound: {e}")


if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.speak()
