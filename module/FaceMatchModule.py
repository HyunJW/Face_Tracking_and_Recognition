import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
from torch.autograd import Variable
import PIL.ImageOps    
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import shutil
from torch.optim.lr_scheduler import ReduceLROnPlateau
import copy
import cv2
import os
import SiameseNetwork
import mediapipe as mp

os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

class FaceMatch():
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection

    def rotate():
        pass

    def load_face(self, dir):
        face_lis = []
        file_list = os.listdir(dir)

        # 배경 검출
        change_background_mp = mp.solutions.selfie_segmentation
        change_bg_segment = change_background_mp.SelfieSegmentation(model_selection=1)

        for file_name in file_list:
            file_path = os.path.join(dir, file_name)
            face = cv2.imread(file_path)

            # 배경 제거
            image_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            result = change_bg_segment.process(image_rgb)
            binary_mask = result.segmentation_mask > 0.2 # 0.2 값이 1에 가까울수록 얼굴 인식 범위가 깐깐해짐
            binary_mask_3 = np.dstack((binary_mask, binary_mask, binary_mask))
            face_non_bg = np.where(binary_mask_3, image_rgb, 255)

            user_id = file_name.split('.')[0]
            face_lis.append([face_non_bg, user_id])

        return face_lis
    
    def match_face_1x1(self, face1, face2, min_distance):
        matching_model = torch.load('./model_checkpoint.pt')
        net = SiameseNetwork().cuda()
        net.load_state_dict(matching_model)
        
        # 사진을 데이터화
        transform = transforms.Compose([transforms.Resize(100, 100),
                                        transforms.ToTensor()])
        face1 = transform(face1)
        face2 = transform(face2)

        f1, f2 = net(Variable(face1).cuda(), Variable(face2).cuda())
        euclidean_distance = F.pairwise_distance(f1, f2)
        if euclidean_distance <= min_distance:
            match = True
        else:
            match = False

        return match

    def match_face(self, face_list1, dir, min_distance=0.1):
        face_list2 = self.load_face(dir)
        for f1 in face_list1:
            for f2 in face_list2:
                if self.match_face_1x1(f1, f2[0], min_distance):
                    return f2[1]
                else:
                    return -1
            

    
