from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint

bp = Blueprint('api', __name__)


github_blueprint = make_github_blueprint(client_id='863e1284b52035734311',
                                         client_secret='9f23aa1f7ff8831063365c6e0d06b54e7bab9675')

# def create_app(config_class=Config):
#     app = Flask(__name__)
#
#     from app.api import bp as api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')

from app.api import users
