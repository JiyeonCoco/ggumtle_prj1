from pickle import FALSE, TRUE
from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import numpy as np
from PIL import Image, ExifTags
import io
import os
import glob
import base64
import pandas as pd
from datetime import datetime

import torch

from imgAnalysis import Yolov5


UPLOAD_FOLDER = 'uploaded_files/'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/', methods=['GET'])
def main():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = request.form['filename']

    if not file:
        return 'No selected file'
    
    try:
        # zip 파일명 변경하여 저장
        dt_now = datetime.now().strftime("%d%b%Y-%H%M%S")
        zip_name = f'{dt_now}_{filename}'
        file_path = os.path.join(UPLOAD_FOLDER, zip_name)
        file.save(file_path)

        # zip 파일 압축풀기
        zip_dir = file_path.replace('.zip', '')
        unzip_cmd = f"unzip {file_path} -d {zip_dir}"
        os.system(unzip_cmd)
        if os.path.exists(file_path):   os.remove(file_path)

        dir_list = os.listdir(zip_dir)
        dir_list.remove('__MACOSX')
        target_ext = ('jpg', 'jpeg', 'png', 'tiff', 'tif')
        target_ext += tuple(ext.upper() for ext in target_ext)

        yolo_results = pd.DataFrame()

        for cur_dir in dir_list:
            img_list = []

            for ext in target_ext:
                img_list += sorted(glob.glob(os.path.join(dir_path, zip_dir, cur_dir, '*.' + ext)))

            for img in img_list:
                filename = os.path.splitext(os.path.basename(img))[0]
                img = Image.open(img)
                img = img.convert('RGB')

                try:
                    exif = dict(img._getexif().items())

                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break

                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    pass

                input_np_img = np.array(img, dtype=np.uint8)

                cur_result = yolov5.run(filename, input_np_img)
                yolo_results = pd.concat([yolo_results, cur_result])

        yolo_results.reset_index(inplace=True, drop=True)
        print('yolo_results=', yolo_results)
        len_result = len(yolo_results)
    
    except Exception as e:
        print(e)
        return '파일에 문제가 있네요. 다시 올려주삼'
    
    # return jsonify([{"input": item[0], "data": item[1]} for item in yolo_results])
    return jsonify(yolo_results.to_dict(orient='records'))

    

if __name__ == '__main__':

    yolov5 = Yolov5()
    
    app.run(host="127.0.0.1", port="5000")

