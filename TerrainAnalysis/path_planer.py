import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from transformers import SamModel, SamConfig, SamProcessor

class analyzer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        model_config = SamConfig.from_pretrained(r'./BuildModel/weight/sam/config.json')
        model = SamModel(config=model_config)
        model.load_state_dict(torch.load(r'./BuildModel/weight/best.pth'))
        model.to(self.device)
        
        self.model = model

        self.model.eval()

        self.processor = SamProcessor.from_pretrained(r'facebook/sam-vit-base')

        size = (256, 256)
        points = []
        for i in range(0, int(size[0]/2), 16):
            for j in range(1, size[1], 16):
                points.append([j, i])
        for i in range(size[0]//2, size[0], 8):
            for j in range(0, size[1], 8):
                points.append([j, i])
        points = np.array(points)

        self.points = points

        self.img = None
        self.im_result = None
        self.path_result = None

        print("Finish setting up with no problem")

    def predicted(self, img: np.array):
        inputs = self.processor(img, input_points=[[self.points]], return_tensors='pt')
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs, multimask_output=False)

        prob = torch.sigmoid(outputs.pred_masks.squeeze(1))

        seg_prob = prob.cpu().numpy().squeeze()
        seg = np.where(seg_prob>0.95, 255, 0)
        
        