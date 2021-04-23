# import the necessary package
from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'max_connection': fields.Integer(required=True, description='maximum number of connection for a user')
    })
    user_update = api.model('update user', {
        'email': fields.String(description='user email address'),
        'username': fields.String(description='user username'),
        'max_connection': fields.Integer(description='maximum number of connection for a user')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operation')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description="the user's username"),
        'password': fields.String(required=True, description="the user's password")
    })
class FacesDto:
    api = Namespace('face', description='student face related operations')
    face = api.model('get_faces_details', {
        'label': fields.String(required=True, description='face label'),
        'access_token': fields.String(required=True, description='authorization key')
    })
    face_ver = api.model('face_verified', {
        'access_token': fields.String(required=True, description='valid access_token'),
        'label': fields.String(required=True, description='face label'),
        'verified': fields.Integer(required=True, description='face verification value')
    })
    face_regis = api.model('registration_details', {
        'label': fields.String(required=True, description='first and last name of the user'),
        'image': fields.String(required=True, desciption="face entire image"),
        'face': fields.String(required=True, description='all faces for a user'),
        'access_token': fields.String(required=True, description='registered access token')
    })
    face_auth = api.model('authentication_details', {
        'access_token': fields.String(required=True, description='valid access token'),
        'label': fields.String(description='student first and last name'),
        'face': fields.String(required=True, description='student face descriptor')
    })

class IncidentDto:
    api = Namespace('incident', description='incident related operations')
    incident = api.model('incident',{
        'username': fields.String(required=True, description='system username'),
        'student': fields.Integer(required=True, description='id student'),
        'quiz': fields.Integer(required=True, description='ID quiz'),
        'attempt': fields.Integer(required=True, description='number attempt'),
        'captured_time': fields.Integer(required=True, description='captured time'),
        'action': fields.String(required=True, description='incident name'),
        'image_file': fields.Integer(required=True, description='image file'),
        'registered_on': fields.Integer(required=True, description='registered time')
    })

class ModelDto:
    api = Namespace('model', description='model related operations')
    user = api.model('model', {
        'access_token': fields.String(required=True, description='valid access token')
    })

class TokenDto:
    api = Namespace('token', description='access token related operations')
    token = api.model('face_auth_details', {
        'token': fields.String(required=True, description='Session token')
    })