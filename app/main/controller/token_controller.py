# import the necessary package

from flask_restplus import Resource
from flask import request
from app.main.util.dto import TokenDto, AuthDto
from app.main.service.token_service import check_token
from app.main.service.auth_helper import Auth

api = TokenDto.api
_token = TokenDto.token
_user_auth = AuthDto.user_auth

@api.route('/tokapi')
class Token(Resource):
    @api.doc("generate access token for a user")
    @api.expect(_user_auth, validate=True)
    def post(self):
        """for specified username return an access token"""
        data = request.json
        return Auth.login_user(data=data)

# @api.route('/')
# class Token(Resource):
#     @api.doc('close the user token by updating his status')
#     @api.expect(_token, validate=True)
#     def put(self):
#         """close student session"""
#         data = request.json
#         return Auth.logout_user(data=data)

# @api.route('/<string:token>')
# @api.param('token', 'Token')
# class Token(Resource):
#     @api.doc('check the opened token')
#     def get(self, token):
#         """check and return the opened token"""
#         return check_token(token)
