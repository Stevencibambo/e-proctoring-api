# import the necessary package

from flask_restplus import Resource
from flask import request
from app.main.util.dto import FacesDto
from app.main.service.face_service import \
    check_face, get_face, get_all_faces, delete_face, update_face, save_faces, predict

api = FacesDto.api
_face = FacesDto.face
_face_ver = FacesDto.face_ver
_face_regis = FacesDto.face_regis
_face_auth = FacesDto.face_auth

@api.route('/<username>/regisapi')
@api.param('username', 'Username')
@api.doc('register new student')
class FaceRegistration(Resource):
    @api.response(201, 'face saved successful')
    @api.expect(_face_regis, validate=True)
    def post(self, username):
        """registration of a new student"""
        data = request.json
        return save_faces(str(username), data)

@api.route('/<username>/predapi')
@api.param('username', 'Username')
@api.doc('predict a face given in parameter')
class Face(Resource):
    @api.expect(_face_auth, validate=True)
    def post(self, username):
        """predict a given face in parameter"""
        data = request.json
        return predict(username, data=data)

@api.route('/<username>/<labels>/<tokapi>')
@api.param('username', 'Username')
@api.param('labels', 'Labels')
@api.param('tokapi', 'Token')
@api.doc('return all faces of given labels')
class FaceAll(Resource):
    def get(self, username, labels, tokapi):
        """return all faces of given labels"""
        data = {
            'username': username,
            'labels': labels,
            'access_token': tokapi
        }
        return get_all_faces(data)

@api.route('/<username>/delapi')
@api.param('username', 'Username')
@api.doc('delete student with all faces')
class Face(Resource):
    """delete student faces"""
    @api.expect(_face, validate=True)
    def delete(self, username):
        """delete student face"""
        data = request.json
        return delete_face(username, data)

@api.route('/<username>/updatapi')
@api.param('username', 'Username')
class Face(Resource):
    @api.expect(_face, validate=True)
    def put(self, username):
        """update student face"""
        data = request.json
        return update_face(username, data)

@api.route('/<username>/verapi')
@api.param('username', 'Username')
@api.doc('face verification by authority')
class Face(Resource):
    @api.expect(_face_ver, validate=True)
    def post(self, username):
        """check the student face by the authority"""
        data = request.json
        return check_face(username, data)

@api.route('/<username>/faceapi/<label>/<tokapi>')
@api.param('username', 'Username')
@api.param('label', 'Label')
@api.param('tokapi', 'Token')
class FaceLabels(Resource):
    def get(self, username, label, tokapi):
        """return the student face"""
        data = {
            'username': username,
            'label': label,
            'access_token': tokapi
        }
        return get_face(data)