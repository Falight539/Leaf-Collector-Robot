import torch
import numpy as np
import matplotlib.pylab as plt
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

        return self.interperter(seg)

    def interperter(self, seg: np.array):
        patches_h, patches_w = (32, 32) # 1024 size
        im_h, im_w = seg.shape[0], seg.shape[1]

        direction = []

        for i in range(im_h, 0, -patches_h):

            seg_row = seg[i-32:i, :]

            l, r = int(im_w/2)-patches_w, int(im_w/2)+patches_w
            weight_l, weight_r = 0, 0

            while l >= 0 and r <= im_w:
                if weight_l and weight_r:
                    break

                if not weight_l:
                    ptype = int(np.argmax(np.bincount(seg_row[:, l:l+patches_w].ravel())))

                    if not ptype:
                        weight_l = int(l/patches_w)*10

                if not weight_r:
                    ptype = int(np.argmax(np.bincount(seg_row[:, r-patches_w:r].ravel())))

                    if not ptype:
                        weight_r = int((im_w-r)/patches_w)*10

                if weight_l == 30 and weight_r == 30:
                    sl, sr = 0, im_w
                    co_l, co_r = 0, 0
                    path_l, path_r = None, None

                    while sl < l and sr > r:
                        # check left
                        ptype = int(np.argmax(np.bincount(seg_row[:, sl: sl+patches_w].ravel())))
                        if ptype != 0:
                            co_l += 1
                        else:
                            co_l = 0

                        if co_l >= 2:
                            path_l = int(sl/patches_w)

                        # check right
                        ptype = int(np.argmax(np.bincount(seg_row[:, sr-patches_w: sr].ravel())))
                        if ptype != 0:
                            co_r += 1
                        else:
                            co_r = 0

                        if co_r >= 2:
                            path_r = int(sr/patches_w)-1

                        sl += patches_w
                        sr -= patches_w

                    # print(f"Row {int(i/patches_h)-1}: l {path_l}, r {path_r}")

                    if path_l is not None or path_r is not None:
                        # Left hand side cannot go
                        if path_l is None:
                            weight_r = 0
                            weight_l = path_r*10
                            break
                        # Right hand side cannot go
                        elif path_r is None:
                            weight_l = 0
                            weight_r = (7-path_l)*10
                            break
                        else:
                            # Turn right
                            if abs(3 - path_l) > abs(path_r - 4):
                                weight_r = 0
                                weight_l = path_r*10
                                break
                            # Turn left
                            elif abs(3 - path_l) < abs(path_r - 4):
                                weight_l = 0
                                weight_r = (7-path_l)*10
                                break
                            # Any direction
                            else:
                                weight_l = int(777)
                                weight_r = 0
                                break
                    # Cannot pass
                    else:
                        weight_l = 0
                        weight_r = int(777)
                        break

                l -= patches_w
                r += patches_w
            
            direction.append(weight_l-weight_r)
        
        return direction


        
        