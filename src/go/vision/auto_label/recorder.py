#!/usr/bin/env python3

import cv2
import os
from datetime import datetime
import shutil
from vision_config import DirectoryContext
from is_recording import is_recording

class VideoRecorder:
    def __init__(self, dir_context: DirectoryContext):
        self.dir_context = dir_context

    def record_video_segment(self, local_server_ip, video_filename='output', is_full_video=False, is_train=False, label=None):
        filename = self.construct_filename(video_filename, is_full_video, is_train, label)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(filename, fourcc, 60.0, (640, 480))
        cap = cv2.VideoCapture(local_server_ip)
        if not cap.isOpened():
            print("Error: Could not open video stream from local server")
            return None
        try:
            return self.capture_frames(cap, out_video, filename)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cap.release()
            out_video.release()

    def construct_filename(self, video_filename, is_full_video, is_train, label):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if is_full_video:
            return os.path.join(self.dir_context.full_vids_dir, f"{video_filename}_{timestamp}.mp4")
        elif is_train:
            return os.path.join(self.dir_context.full_vids_dir, f"{video_filename}_{timestamp}_{label}.mp4")
        else:
            return os.path.join(self.dir_context.outputs_dir, f"{video_filename}.mp4")

    def capture_frames(self, cap: cv2.VideoCapture, out_video: cv2.VideoWriter, filename, max_frames=16):
        global is_recording
        counter = 0
        while is_recording[0]:
            ret, frame = cap.read()
            if not ret or counter >= max_frames:
                break
            out_video.write(frame)
            counter += 1
        return filename

    def archive_video_segment(self, video_file_path, timestamp):
        archive_path = os.path.join(self.dir_context.full_vids_dir, f"{timestamp}.mp4")
        shutil.copy(video_file_path, archive_path)
