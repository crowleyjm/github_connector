import requests
from flask import Flask, request, Blueprint, make_response
import json

bp = Blueprint('profile', __name__, url_prefix='/profile')

github_url = 'https://api.github.com'


@bp.route('/<git_name>')
def user_get_lang(git_name):
    github_url = 'https://api.github.com/users/' + git_name + '/repos'
    print(github_url)
    payload = {}
    headers = {}

    response = requests.request("GET", github_url, headers=headers, data=payload)


    return response.content





            

