# import the necessary package

from .. import db
import datetime

class Token(db.Model):
    """
    Token Model for storing user's JWT tokens
    """
    __tablename__ = 'access_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False, unique=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    start_on = db.Column(db.BigInteger, nullable=False)
    end_on = db.Column(db.BigInteger)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_token(auth_token):
        res = Token.query.filter_by(token=auth_token).first()
        if res:
            return True
        else:
            return False

    @staticmethod
    def check_opened_token_by_token(auth_token):
        token = Token.query.filter_by(token=str(auth_token), status=1).first()
        if token:
            return token
        else:
            return False

    @staticmethod
    def check_opened_user_token(uid):
        token = Token.query.filter_by(uid=uid, status=1).first()
        if token:
            return token
        else:
            return False