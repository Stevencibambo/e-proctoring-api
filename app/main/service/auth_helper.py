# import the necessary package
from flask import jsonify
from app.main import db
from app.main.model.user import User
from app.main.model.tokens import Token
from ..service.token_service import save_token, token_is_opened
from datetime import datetime
import jwt


class Auth:
    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(username=data.get('username')).first()
            if user and user.check_password(data.get('password')):
                if token_is_opened(user.id):
                    token = Token.query.filter_by(uid=user.id).first()
                    auth_token = token.token
                else:
                    token = Token.query.filter_by(uid=user.id).first()
                    if not token:
                        auth_token = user.encode_auth_token(user.id)
                        now = datetime.utcnow()
                        timestamp = int(datetime.timestamp(now))
                        new_token = Token(
                            uid=user.id,
                            token=auth_token,
                            start_on=timestamp,
                            status=1
                        )
                        save_token(new_token)
                    else:
                        auth_token = user.encode_auth_token(user.id)
                        token.token = auth_token
                        token.end_on = None
                        token.status = 1
                response_object = {
                    'status': 'success',
                    'message': 'login successful'
                }
                resp = jsonify(response_object)
                resp.headers['Authorization'] = auth_token
                resp.headers['Access-Control-Allow-Origin'] = '*'
                resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                # return resp
                return resp

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 501

    @staticmethod
    def logout_user(data):
        # logout the user
        token = Token.check_opened_token_by_token(data['token'])
        if token:
            try:
                token.status = 0
                token.end_on = datetime.datetime.utcnow()
                db.session.commit()
                response_object = {
                    'status': 'successful',
                    'message': 'session closed successful'
                }
                return response_object, 201

            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'error logout {}'.format(e)
                }
                return response_object, 500

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'registered_on': str(user.registered_on),
                        'max_connection': user.max_connection,
                        'connected': user.connected
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
