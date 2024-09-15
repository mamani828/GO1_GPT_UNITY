#!/usr/bin/env python3
import torch
import numpy as np
import os
from decord import VideoReader
import shutil
from speak_clnt import speak


from explain_clnt import explain

import json
from listen_clnt import get_should_speak
""" The Inferencer class is responsible for inferring human activities in a video using the vision service. """
class Inferencer:
    def __init__(self, label_context, dir_context):
        self.label_context = label_context
        self.dir_context = dir_context
        #Inference classes, change as seen fit
        self.classes = [
            'human is hammering',
            'human is measuring with a measure tape',
            'human is stacking boxes',
            'human is clipping',
            'human is cutting',
            'human is drilling',
            'human is screwdriving',
            'an empty room',
            'human is doing an unsure activity'
        ]
    def infer_activity(self, video_path, start_time=0, stop_time=4):
        """ Infers the human activity in a video segment. """
        try:
            
            inputs = self.analyze_video(video_path, start_time, stop_time)
            probs = self.predict_activity_probabilities(inputs)
            activity, prob = self.determine_activity(probs)
        except:
            print("Skipping inferral after user quit")
            exit()
        if activity == "an empty room" or activity == "human is doing an unsure activity":
            print("None of the assigned activities is detected.")
        else:
            print(f"Detected activity: {activity}")
            should_speak = get_should_speak()
            print(f"Should speak: {should_speak}")
            if prob > 0.7:
                if should_speak == 1:
                    speak(activity)
        return activity, prob

    def predict_activity_probabilities(self, inputs):
        with torch.no_grad():
            outputs = self.label_context.model(**inputs)
        probs = outputs.logits_per_video.softmax(dim=1)
        return probs

    def determine_activity(self, probs):
        prob_not_last = probs[:, :-1]
        max_prob_not_last, index_not_last = torch.max(prob_not_last, dim=1)
        
        threshold = 0.1 + probs[:, -1].item()
        if max_prob_not_last.item() < threshold:
            index = len(self.classes) - 1
        else:
            index = index_not_last.item()

        activity = self.classes[index]
        prob = max_prob_not_last.item() if index != len(self.classes) - 1 else probs[:, -1].item()
        return activity, prob

    def analyze_video(self, video_path, start_time=0, stop_time=4):
        print("Recording Vid segment")
        videoreader = VideoReader(video_path, num_threads=1)
        indices = self.sample_frame_indices(videoreader, start_time, stop_time)
        video = videoreader.get_batch(indices).asnumpy()
        inputs = self.label_context.processor(text=self.classes, videos=list(video), return_tensors="pt", padding=True)
        return inputs.to(self.label_context.device) # uses the GPU (or CPU if not available) to run the model

    def sample_frame_indices(self, vr, start_time, stop_time):
        total_frames = len(vr)
        start_idx = int(start_time * vr.get_avg_fps())
        stop_idx = int(stop_time * vr.get_avg_fps())
        start_idx = max(start_idx, 0)
        stop_idx = min(stop_idx, total_frames-1)
        skip = (stop_idx - start_idx) / 31
        indices = np.arange(start_idx, stop_idx+1, skip, dtype=np.int64)[:32]
        return indices        
            
    """ Infers possible human activity captured in a video located at video_file_path.
        If probablilty of activity is greater than a specified threshold, the video is copied to 
        the src/go/videos/good_vids directory for future review and an explanation is generated.
        The explanation is saved in the same directory as the video file. """    
    
    #### evaluate_and_save() that uses the explain service to generate explanations
    def evaluate_and_save(self, video_file_path, timestamp):
        print('Using model for inference...')
        clas, prob = self.infer_activity(video_file_path)
        print(prob)

        # Determine if the inference is positive and the video should be saved to 'good_vids'
        if prob > 0.7 and clas != 'an empty room' and clas != 'human is doing an unsure activity':
            good_path = os.path.join(self.dir_context.good_vids_dir, f"{clas}_{timestamp}.mp4")
            shutil.copy(video_file_path, good_path)   
            self.save_variables(good_path, clas, prob, timestamp)
            """ EXPLAIN feature components below """    
            # trigger explanation feature via explain service client-server communication
            # explain(good_path, clas, prob, timestamp, self.dir_context)  # sends the request to the EXPLAIN service
            print(f"Video saved and explanation request sent: {good_path}")

    def save_variables(self, good_path, clas, prob, timestamp, filename="inference_variables.json"):
        print("Saving variables...")
        save_filename = os.path.join(self.dir_context.inference_data_dir, filename)
        print(save_filename)
        data = {
            "good_path": good_path,
            "clas": clas,
            "prob": prob,
            "timestamp": timestamp
        }
        with open(save_filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Variables saved to {save_filename}")