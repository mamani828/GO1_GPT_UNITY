#!/usr/bin/env python3

import threading
from datetime import datetime
from inference import Inferencer
from recorder import VideoRecorder
from vision_config import DirectoryContext, LabelingContext
from is_recording import is_recording
from pathlib import Path

class AutoLabeler:
    def __init__(self, local_server_ip):
        self.local_server_ip = local_server_ip
        #TODO fix imports for more modularity
        self.dir_context = DirectoryContext(base_dir=f"{Path.home()}/WorkingDir/src/go/videos")
        self.recorder = VideoRecorder(self.dir_context)
        self.label_context = LabelingContext()
        self.inferencer = Inferencer(self.label_context, self.dir_context)

    def monitor_video_stream(self):
        input_thread = threading.Thread(target=self.input_handler)
        input_thread.start()
        while is_recording:
            self.process_video_segment()
        
    def process_video_segment(self):
        #TODO Fix video_file_path var naming to reflect that var is a video
        video_file_path = self.recorder.record_video_segment(self.local_server_ip)
        if not video_file_path:
            print("Error recording video segment, trying again...")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.recorder.archive_video_segment(video_file_path, timestamp)
        self.inferencer.evaluate_and_save(video_file_path, timestamp)

    def input_handler(self):
        global is_recording
        STOP_RECORD_MSG = "Press Enter to stop recording...\n"
        input(STOP_RECORD_MSG)
        is_recording[0] = False

if __name__ == "__main__":
    labeler = AutoLabeler("http://146.244.98.34:5000/video_feed")
    labeler.monitor_video_stream()
