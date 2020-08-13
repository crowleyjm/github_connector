from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint
import os
bp = Blueprint('api', __name__)


github_blueprint = make_github_blueprint(client_id=os.environ.get('CLIENT_ID', None),
                                         client_secret=os.environ.get('CLIENT_SECRET', None))

from app.api import users
