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
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

class FaceMatch():
    def __init__(self, db):
        self.db = db

    def load_face(self):
        conn = self.db  # db 연결
        cursor = conn.cursor()  # 커서 생성

        sql = ''
        cursor.execute(sql)
        rows = cursor.fetchall()

        return face
    
    def match_face(self, face1, face2):
        match = False
        return match

    
