import requests
from flask import Flask, request, make_response
import json
from app.api import bp
import collections

@bp.route('/<git_name>')
def user_get_lang(git_name, token):
    github_url = 'https://api.github.com/users/' + git_name + '/repos'
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", github_url, headers=headers, data=payload)
    language_dict = {}

    new_bytes = response.content
    new_json = json.loads(new_bytes)

    for i in range(len(new_json)):
        new_url = new_json[i]["languages_url"]
        new_payload = {}
        new_url_response = requests.request("GET", new_url, headers=headers, data=new_payload)

        lang_cont = new_url_response.content
        lang_json = json.loads(lang_cont)

        for lang_name in lang_json:
            new_val = lang_json[lang_name]
            if lang_name not in language_dict:
                language_dict[lang_name] = new_val
            else:
                language_dict[lang_name] += new_val

    return language_dict


@bp.route('/<git_name>/repositories')
def user_get_repos(git_name, token):
    github_url = 'https://api.github.com/users/' + git_name + '/repos'
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", github_url, headers=headers, data=payload)
    repos_dict = {}

    new_bytes = response.content
    new_json = json.loads(new_bytes)

    for i in range(len(new_json)):
        html_url = new_json[i]["html_url"]
        name_url = new_json[i]["name"]
        repos_dict[name_url] = html_url

    return repos_dict
