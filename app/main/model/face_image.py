# import the necessary package

from app.main.model.tokens import Token
from .. import db, flask_bcryp
from ..config import key
import datetime
import jwt

class FaceImage(db.Model):
    """FaceImage Model for storing face details"""
    __tablename__ = 'face_image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    label = db.Column(db.String(100), nullable=False)
    accuracy = db.Column(db.Float)
    recall = db.Column(db.Float)
    image = db.Column(db.Text)
    active = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Integer, default=0)
    registered_on = db.Column(db.BigInteger)

    def __repr__(self):
        return "<Face {}>".format(self.label)