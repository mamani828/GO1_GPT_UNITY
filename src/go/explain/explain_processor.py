#!/usr/bin/env python3

import cv2
from openai import OpenAI
import base64
import os
import re
from speak_clnt import speak
""" Handles the processing logic for the EXPLAIN service. """

class ExplainProcessor:
        
    def __init__(self):
        
        self.model_name = "gpt-4o-mini"
        # self.model_name = "gpt-4o"
        self.frames_to_extract = 5  # number of frames to use for explanation
        # initialize the ExplainProcessor with an OpenAI API key
        self.api_key="INSERT KEY"
        self.use_speak_service = True  # set to False to disable the speak service
        
    def explain(self, video_path: str, activity: str, probability: float, timestamp: str, dir_context):
        # generate the explanation using the ExplainProcessor
        infrerence_results = {"activity": activity, "probability": probability}
        print(activity, probability)
        frames = self.process_video(video_path)
        explanation = self.generate_explanation(frames, infrerence_results)

        # send explanation to the speak service
        if self.use_speak_service:
            speak(explanation)
        
        # save the inference explanation alongside the video used for the inference in the good_vids directory
        explanation_path = os.path.join(dir_context.good_vids_dir, f"{activity}_{timestamp}_explanation.txt")
        with open(explanation_path, 'w') as file:
            file.write(explanation)
            print("Explanation generated and saved.")
        
        return explanation
    def is_valid_base64(self,s):
        return re.match('^[A-Za-z0-9+/]*={0,2}$', s) is not None
        
    def process_video(self, video_path):
        """ extracts key frames from the video """
        try:
            # open video file, count frames and get indices of key frames to extract
            video = cv2.VideoCapture(video_path)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            sample_frame_indices = self._select_key_frames(total_frames)
            # get sample frames from video and encode in base64 so they can be sent to OpenAI API
            base64_frames = []
            for index in range(total_frames):
                success, frame = video.read()
                if not success:
                    break
                if index in sample_frame_indices:
                    # Resize the frame to reduce prompt size
                    resized_frame = cv2.resize(frame, (768, 768))
                    _, buffer = cv2.imencode(".jpg", resized_frame)
                    base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
                    
            video.release()
            for base64_frame in base64_frames:
                if not self.is_valid_base64(base64_frame):
                    print(f"Invalid base64 encoding detected")
            return base64_frames
        except Exception as e:
            print(f"Error processing video: {e}")
            return []
            
        
    def _select_key_frames(self, total_frames):
        """ selects indices for key frames to extract """
        interval = max(1, total_frames // self.frames_to_extract)
        return list(range(0, total_frames, interval))[:self.frames_to_extract]  
    
    def generate_explanation(self, frames, inference_results):
        """ generates an explanation for human activity inference using the OpenAI API """
        
        prompt = self._build_prompt(frames, inference_results)
        response = self._call_openai_api(prompt)
        return response
    
    def _build_prompt(self, frames, inference_results):
        activity = inference_results.get("activity")
        probability = inference_results.get("probability")
        
        content = [
            {
                "type": "text",
                "text": f"An AI detected that the human activity in a video is {activity}, with an inference probability of {probability:.2f}. Based on the content of the video frames, please explain how the AI might have come to this conclusion. Keep first person connotation in your response, as if you made the inference, keep your response under 30 words. Concisely include the confidence probability."
            }
        ]
        
        for frame in frames:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame}"
                }
            })
        
        return [
            {
                "role": "user",
                "content": content
            }
        ]
    
    def _call_openai_api(self, prompt):
        try:           
            client = OpenAI(api_key=self.api_key)
            
            api_call_params = {
                "model": self.model_name,
                "messages": prompt,
                "max_tokens": 400,
            }
            
            response = client.chat.completions.create(**api_call_params)
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI API: {type(e).__name__}: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.content}")
            print(f"API call parameters: {api_call_params}")
            return "Failed to generate explanation."
        
    

    
