import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import os

class FaceDetect():
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
    
    def mp4_to_avi(self, input_video, output_video):
       self.input_video = input_video
       self.output_video = output_video
       return output_video

    def detect_face(self, frame):

        img_lis = []
        return img_lis