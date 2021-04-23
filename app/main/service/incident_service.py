# import the necessary package

from app.main import db
from .user_service import get_a_user
from app.main.model.incident import Incident

def save_incident(data):
    user = get_a_user(data['username'])
    incident = Incident(
        uid=user.id,
        student=data['student'],
        quiz=data['quiz'],
        attempt = data['attempt'],
        captured_time = data['captured_time'],
        action = data['action'],
        image_file = data['image_file'],
        registered_on = data['registred_on']
    )
    save_change(incident)
    response_object = {
        'status': 'success',
        'message': 'Incident successfully registered'
    }
    return response_object, 201

def get_student_incident(username, student, quiz):
    """return all student incident on a specified quiz"""
    user = get_a_user(username)
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'error system user'
        }
        return response_object, 400
    else:
        uid = user.id
        incidence = Incident.query.filter_by(uid=uid, student=student, quiz=quiz)
        return incidence

def get_quiz_incidence(username, quiz):
    user = get_a_user(username)
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'error system user'
        }
        return response_object, 400
    else:
        return Incident.query.filter_by(uid=user.id, quiz=quiz)

def get_same_incident(username, quiz, action):
    user = get_a_user(username)
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'error system user'
        }
        return response_object, 400
    else:
        return Incident.query.filter_by(uid=user.id, quiz=quiz, action=action)

def save_change(data):
    db.session.add(data)
    db.session.commit()


