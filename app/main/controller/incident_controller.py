# import the necessary package

from flask import request
from flask_restplus import Resource

from ..util.dto import IncidentDto
from ..service.incident_service import save_incident
from ..service.incident_service import get_student_incident
from ..service.incident_service import get_same_incident
from ..service.incident_service import get_quiz_incidence

api = IncidentDto.api
_incident = IncidentDto.incident

@api.route('/')
class Incident(Resource):
    @api.doc('incident operations')
    @api.expect(_incident, validate=True)
    def post(self):
        """creates a new incident"""
        data = request.json
        return save_incident(data)

@api.route('/<username>,<student>,<quiz>')
class StudentIncident(Resource):
    @api.doc('student incident for a quiz')
    @api.param('username', 'Username')
    @api.param('student', 'student ID')
    @api.param('quiz', 'quiz ID')
    def get(self, username, student, quiz):
        """get student incidences on a quiz"""
        incidence = get_student_incident(username, student, quiz)
        if not incidence:
            api.abort(404)
        else:
            return incidence

@api.route('/<username>,<quiz>')
class QuizIncident(Resource):
    @api.doc('all incidents of a quiz')
    @api.param('username', 'Username')
    @api.param('quiz', 'Quiz ID')
    def get(self, username, quiz):
        """return all incident of a quiz"""
        incident = get_quiz_incidence(username, quiz)
        if not incident:
            api.abort(404)
        else:
            return incident

@api.route('/<username>,<quiz>,<action>')
class QuizSameIncidence(Resource):
    @api.doc("all same incidence of a quiz")
    @api.param('username', 'Username')
    @api.param('quiz', 'Quiz')
    @api.param('action', 'Action')
    def get(self, username, quiz, action):
        """ return all same incidence on a quiz"""
        incident = get_same_incident(username, quiz, action)
        if not incident:
            api.abort(404)
        else:
            return incident
