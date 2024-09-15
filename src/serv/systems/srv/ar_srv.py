#!/usr/bin/env python3

from auto_labeler import AutoLabeler

if __name__ == "__main__":
    labeler = AutoLabeler("http://146.244.98.34:5000/video_feed")
    labeler.monitor_video_stream()
