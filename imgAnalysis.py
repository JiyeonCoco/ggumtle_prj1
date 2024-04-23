import torch
import cv2
import pandas as pd

import yolov5


class Yolov5():
    def __init__(self):

        self.input_img = 'numpy.ndarray'
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True)


    def run(self, input_filename, input_img):

        self.input_img = input_img
        self.input_width = self.input_img.shape[1]
        self.input_height = self.input_img.shape[0]

        self.down_scale = 0.5

        yolo_results = pd.DataFrame(columns=['input', 'xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'name'])

        if self.input_img.shape[1] > 1920 and self.input_img.shape[0] > 1080:
            self.down_scale = 0.25

        ds_width    = int(self.input_width * self.down_scale)
        ds_height   = int(self.input_height * self.down_scale)

        cur_img = cv2.resize(self.input_img, dsize=(ds_width, ds_height), interpolation=cv2.INTER_AREA)
    

        yolo_result = self.model(cur_img).pandas().xyxy[0]
        # valid_result = yolo_result[(yolo_result['name']=='person')&(yolo_result['confidence']>=0.6)]
        valid_result = yolo_result[(yolo_result['name']=='person')]
        print('valid_result=', valid_result)

        for i, v in valid_result.iterrows():
            xmin, xmax, ymin, ymax = int(v['xmin']), int(v['xmax']), int(v['ymin']), int(v['ymax'])
            confidecne, name = round(v['confidence'], 1), v['name']

            yolo_results.loc[len(yolo_results)] = [input_filename, xmin, ymin, xmax, ymax, confidecne, name]

        return yolo_results



