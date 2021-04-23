# import the necessary package

from functools import wraps
from flask import request
from PIL import Image
from io import BytesIO
from app.main import config
from app.main.service.auth_helper import Auth
import numpy as np
import base64
import cv2
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object ={
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401
        return f(*args, **kwargs)
    return decorated

def face_dir(username, data):
    """ save data in specified folder"""
    train_data = os.path.join(config.BASE_DATA_DIR, username)
    if not os.path.isdir(train_data):
        # create training data dir for system user
        os.mkdir(train_data)


    if not os.path.isdir(os.path.join(train_data, data['label'])):
        os.mkdir(os.path.join(train_data, data['label']))

    # save user's face images in specified directory
    """split face in decode before saving"""
    faces = data['face'].split('-----')
    saved = 0

    for i in range(len(faces)):
        img_string = faces[i].split(',')[1]
        img_decode = base64.b64decode(img_string)
        image_data = Image.open(BytesIO(img_decode))
        image = image_data.resize((160, 160))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.sep.join([train_data, data['label'],
                                      str(i) + '.jpg']), image,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        saved += 1

    # return nbr saved faces
    return saved
