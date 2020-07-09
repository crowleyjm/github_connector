from flask import Flask, request, Blueprint, render_template
import json

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('welcome/welcome.html')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)