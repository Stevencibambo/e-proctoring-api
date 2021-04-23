# import the necessary package

from .. import db

class Incident(db.Model):
    """Incident model for student events during the test"""
    __tablename__ = "incident"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    student = db.Column(db.Integer, nullable=False)
    quiz = db.Column(db.Integer, nullable=False)
    attempt = db.Column(db.Integer, nullable=False)
    captured_time = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(1024), nullable=False)
    image_file = db.Column(db.Integer, nullable=False)
    registered_on = db.Column(db.Integer, nullable=False)

