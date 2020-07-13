from flask import Flask, request, Blueprint, render_template
import json
import profile_build

app = Flask(__name__)
app.register_blueprint(profile_build.bp)

@app.route('/')
def home():
    return render_template('welcome/welcome.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)