# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from .main.controller.user_controller import api as user_ns
from .main.controller.face_controller import api as face_ns
from .main.controller.auth_helper import api as auth_ns
from .main.controller.incident_controller import api as incident_ns
from .main.controller.model_controller import api as model_ns
from .main.controller.token_controller import api as token_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Full Face E-Proc [REST API]',
          version='1.0.0',
          description='an e-proctoring api for full face authenticate'
          )
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(face_ns)
api.add_namespace(token_ns, path='/token')
api.add_namespace(incident_ns)
api.add_namespace(model_ns)