#!/usr/bin/env python3

import os
import torch
from transformers import XCLIPProcessor, XCLIPModel

class DirectoryContext:
    def __init__(self, base_dir: str = os.path.dirname(os.path.realpath(__file__))):
        self.save_dir = base_dir
        self.outputs_dir = os.path.join(base_dir, "outputs")
        self.full_vids_dir = os.path.join(base_dir, "full_vids")
        self.good_vids_dir = os.path.join(base_dir, "good_vids")
        self.inference_data_dir = os.path.join(base_dir, "inference_data")
        self.create_dirs()

    def create_dirs(self):
        os.makedirs(self.outputs_dir,   exist_ok=True)
        os.makedirs(self.full_vids_dir, exist_ok=True)
        os.makedirs(self.good_vids_dir, exist_ok=True)

class LabelingContext:
    def __init__(self, model_name="microsoft/xclip-base-patch16-zero-shot"):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.processor = XCLIPProcessor.from_pretrained(model_name)
        self.model = XCLIPModel.from_pretrained(model_name).to(self.device)

if __name__ == "__main__":
    d = DirectoryContext()
    print(d.save_dir)    
    print(d.outputs_dir)
    print(d.full_vids_dir)
    print(d.good_vids_dir)    

    l = LabelingContext()
    print(l.device)
    print(l.processor)
    print(l.model)    