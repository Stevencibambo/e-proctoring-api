# import the necessary package

from keras.models import load_model
from app.main import db, config
from app.main.util.decorator import face_dir
from app.main.model.face_image import FaceImage
from app.main.model.tokens import Token
from app.main.service.user_service import get_a_user
from datetime import datetime
from PIL import Image
from io import BytesIO
import numpy as np
import pickle
import base64
import uuid
import os
import shutil


def save_faces(username, data):
    user = get_a_user(username)
    if user:
        # check if he used a valid access token
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            student = FaceImage.query.filter_by(label=data['label']).first()
            now = datetime.now()
            if not student:
                new_user = FaceImage(
                    uid=user.id,
                    label=data['label'],
                    accuracy=0.0,
                    recall=0.0,
                    active=1,
                    image=data['image'],
                    public_id=str(uuid.uuid4()),
                    registered_on= datetime.timestamp(now)
                )
                # save face in database
                db.session.add(new_user)
                db.session.commit()
                # save face in specific directory
                saved = face_dir(username, data)
                response_object = {
                    'status': 'success',
                    'message': 'Student successfully registered.',
                    'saved': '{} faces saved'.format(saved)
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'The label descriptor is already used by another user.',
                    'label': data['label']
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access token. Please login again !'
            }
            return response_object, 402
    else:
        response_object = {
            'status': 'fail',
            'message': 'error system user.'
        }
        return response_object, 403


def get_face(data):
    """get face for a given parameters username and face's label"""
    user = get_a_user(data['username'])
    if user:
        # be sure if the provide access token is valid
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            face = FaceImage.query.filter_by(uid=user.id, label=data['label']).first()
            if face:
                response_object = {
                    'status': 'success',
                    'message': 'face exists',
                    'active': face.active,
                    'verified': face.verified,
                    'image': face.image
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'face not exists'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access token. Please login again!'
            }
            return response_object, 402

def check_face(username, data):
    """face checking"""
    student = FaceImage.query.filter_by(label=data['label']).first()
    if not student:
        response_object = {
            'status': 'fail',
            'message': 'student face not registered yet'
        }
        return response_object, 401
    else:
        """check if system user exist before update student info """
        user = get_a_user(username)
        if user:
            # be sure that provided token is valid
            auth_token = Token.check_token(data['access_token'])
            if auth_token:
                face = FaceImage.query.filter_by(label=data['label']).first()
                face.verified = int(data['verified'])
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'face verification successful'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid access token. Please login again!'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'error system username'
            }
            return response_object, 402

def get_all_faces(data):
    """return all label's faces"""
    user = get_a_user(data['username'])
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'error, system username not exists'
        }
        return response_object, 401
    else:
        # be sure if the provided access token is valid
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            labels = str(data['labels']).split('-----')
            images = db.session.query(FaceImage).filter(FaceImage.label.in_(labels)).all()
            all_students = list()
            for elt in images:
                student = {
                    "label": elt.label,
                    "active": elt.active,
                    "verified": elt.verified,
                    "image": elt.image
                }
                all_students.append(student)
            response_object = {
                'status': 'success',
                'message': 'retrieve faces of given labels',
                'data': all_students
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access token. Please login again!'
            }
            return response_object, 401

def delete_face(username, data):
    """delete face user"""
    user = get_a_user(username)
    if user:
        # be sure that the provided toke is valid
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            student = FaceImage.query.filter_by(label=data['label'], uid=user.id).first()
            db.session.delete(student)
            db.session.commit()
            dir_path = os.path.sep.join([config.BASE_DATA_DIR, username, data['label']])
            if os.path.isdir(dir_path):
                # delete the image folder
                try:
                    print("[INFO] removing {} directory ...".format(dir_path))
                    shutil.rmtree(dir_path)
                except OSError as e:
                    print("Error : %s : %s" % (dir_path, e.strerror))
                    return e
            response_object = {
                'status': 'success',
                'message': 'face deleted successful',
                'face_label': data['label']
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access token. Please login again!'
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'error user name or password'
        }
        return response_object, 402

def update_face(data):
    """update face user"""
    return True


def predict(username, data):
    """make a prediction of the face given in parameter"""
    required_size = (160, 160)
    user = get_a_user(username=username)
    if user:
        # be sure if the access token is valid
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            model_facenet = load_model(os.path.join(config.MODEL_FACENET, 'facenet_keras.h5'))
            model = pickle.load(open(os.path.sep.join([config.MODEL_DIR, username,
                                                       'model.pickle']), 'rb'))
            encoder_label = pickle.load(open(os.path.join(config.PROCESS_DATA_DIR,
                                                          username, 'encoder_label.pickle'), 'rb'))

            face = data['face']
            face = face.split(",")[1]
            # face = face.replace("data:image/jpeg;base64,", "")
            # face = face.replace(" ", "+")
            # face = face.replace("b'", "'")

            decoded_image = base64.b64decode(face)
            image = Image.open(BytesIO(decoded_image))
            image = image.resize(required_size, Image.ANTIALIAS)
            face_array = np.asarray(image, dtype='uint8')

            # extract features from an image as did for training
            face_pixels = face_array.astype('float32')
            # standardize pixels values across channel (global)
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean)
            # transform face into one sample
            sample = np.expand_dims(face_pixels, axis=0)

            # make prediction and return embedding
            print("[INFO] features extraction ...")
            yhat = model_facenet.predict(sample)

            print("[INFO] make prediction ...")
            pred = model.predict(yhat)
            proba = model.predict_proba(yhat)
            index = pred[0]
            predict_name = encoder_label.inverse_transform(pred)
            print({'predict': predict_name, 'expect': data['label']})
            class_proba = (proba[0, index]) * 100
            # if the expected name match predicted
            if data['label'] in predict_name:
                # login user and generate token
                response_object = {
                    'status': 'success',
                    'message': 'result predict',
                    'predict_proba': class_proba,
                    'predict_name': predict_name[0],
                    'expect_name': data['label'],
                }
                return response_object, 201
            else:
                response_object = {
                    "status": "fail",
                    "message": "system can't predict for given data. please check "
                               "your user name or update your face or contact the admin system",
                    "predict_name": "",
                    "predict_proba": "",
                    "expect_name": ""
                }
                return response_object, 501
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access token. Please login again!'
            }
            return response_object, 401
    else:
        response_object = {
            "status": "fail",
            "message": "user does not exists"
        }
        return response_object, 401
