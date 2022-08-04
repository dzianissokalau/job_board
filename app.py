from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from datetime import datetime, timedelta
import json


app = Flask(__name__, static_folder='static')


with open('json_data.json') as json_file:
    data = json.load(json_file)


@app.route('/', methods=['GET', 'POST'])
def index(data=data):
    return render_template('index.html', data=data)


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run(debug=False)