# import the necessary package

from flask import request
from flask_restplus import Resource
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
_user_auth = AuthDto.user_auth

@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @api.doc('user login')
    @api.expect(_user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)

@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)

