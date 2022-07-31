from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from datetime import datetime, timedelta


app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run(debug=False)