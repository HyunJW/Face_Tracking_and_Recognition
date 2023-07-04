import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import cv2
import os
from module import SiameseNetwork, FaceDetectModule
import mediapipe as mp

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'


class FaceMatch():
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection

    def rotate(self):
        pass

    def load_face(self, dir):
        face_lis = []
        file_list = os.listdir(dir)[1:-1]

        # 배경 검출
        change_background_mp = mp.solutions.selfie_segmentation
        change_bg_segment = change_background_mp.SelfieSegmentation(model_selection=1)

        for file_name in file_list:
            file_path = os.path.join(dir, file_name)
            face = cv2.imread(file_path)

            # 배경 제거
            image_rgb = FaceDetectModule.FaceDetect().detect_face(face, 0)[0]
            result = change_bg_segment.process(image_rgb)
            binary_mask = result.segmentation_mask > 0.2  # 0.2 값이 1에 가까울수록 얼굴 인식 범위가 깐깐해짐
            binary_mask_3 = np.dstack((binary_mask, binary_mask, binary_mask))
            face_non_bg = np.where(binary_mask_3, image_rgb, 255)

            user_id = file_name.split('.')[0]
            face_lis.append([face_non_bg, user_id])

        return face_lis

    def match_face_1x1(self, face1, face2, min_distance):
        matching_model = torch.load('c:/model/face_match_model.pt')
        net = SiameseNetwork.SiameseNetwork().cuda()
        net.load_state_dict(matching_model)
        torch.cuda.manual_seed(1)

        # 사진을 데이터화
        transform = transforms.Compose([transforms.Resize((100, 100)),
                                        transforms.Grayscale(),
                                        transforms.ToTensor()])

        face1 = cv2.cvtColor(face1, cv2.COLOR_BGR2RGB)
        face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2RGB)

        # numpy 배열을 PIL 이미지로 변환
        face1 = Image.fromarray(face1)
        face2 = Image.fromarray(face2)

        # # 매칭 이미지를 확인하기 위한 저장
        # face1.save('d:/video/1.jpg')
        # face2.save('d:/video/2.jpg')

        # 변환된 PIL 이미지에 transforms 적용
        face1 = transform(face1)
        face2 = transform(face2)

        # 채널 차원 추가
        face1 = face1.unsqueeze(0)
        face2 = face2.unsqueeze(0)

        f1, f2 = net(Variable(face1).cuda(), Variable(face2).cuda())
        euclidean_distance = F.pairwise_distance(f1, f2)
        # print(euclidean_distance)
        if euclidean_distance <= min_distance:
            match = True
        else:
            match = False
        return match

    def match_face(self, face_list1, dir, min_distance=0.8):
        face_list2 = self.load_face(dir)

        id_list = []
        for f1 in face_list1:
            for f2 in face_list2:
                if self.match_face_1x1(f1, f2[0], min_distance):
                    id_list.append(f2[1])
        return id_list