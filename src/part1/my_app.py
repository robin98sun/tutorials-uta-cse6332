#!/usr/bin/env python3
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    message = "Congratulations, it's a web app!"
    return render_template(
            'index.html',  
            message=message,
    )

from flask import request
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    print(username)
    password= request.args.get('password')
    print(password)
    return username

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

