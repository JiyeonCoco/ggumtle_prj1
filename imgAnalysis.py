import torch
import yolov5


class Yolov5():
    def __init__(self):

        self.input_img = 'numpy.ndarray'
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True)


    def run(self, input_img):

        self.input_img = input_img
        results = self.model(self.input_img)

        return results



