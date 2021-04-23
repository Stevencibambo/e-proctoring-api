# import the necessary package

from .. import db, flask_bcryp
from ..config import key
from app.main.model.tokens import Token
import jwt
import datetime

class User(db.Model):
    """User Model for storing user related details consider user as LMS"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(99), unique=True)
    username = db.Column(db.String(49), unique=True)
    password_hash = db.Column(db.String(99))
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    max_connection = db.Column(db.Integer, nullable=False, default=1)
    connected = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcryp.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return flask_bcryp.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generate the Auth Token
        :param face_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_token = Token.check_token(auth_token)
            if is_token:
                return 'Token blacklisted, please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'

        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


