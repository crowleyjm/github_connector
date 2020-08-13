from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint
import os
bp = Blueprint('api', __name__)


github_blueprint = make_github_blueprint(client_id=os.environ.ge('CLIENT_ID', None), client_secret=os.environ.get('CLIENT_SECRET', None))

# def create_app(config_class=Config):
#     app = Flask(__name__)
#
#     from app.api import bp as api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')

from app.api import users
