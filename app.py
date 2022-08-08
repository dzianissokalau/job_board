from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from datetime import datetime, timedelta
import json


app = Flask(__name__, static_folder='static')


with open('json_listings.json') as json_file:
    job_listings = json.load(json_file)


with open('json_content.json') as json_file:
    job_content = json.load(json_file)


@app.route('/', methods=['GET', 'POST'])
def index(job_listings=job_listings):
    return render_template('index.html', job_title='All', job_listings=job_listings)


@app.route('/<job_title>', methods=['GET', 'POST'])
def filtered_listings(job_title, job_listings=job_listings):
    job_titles = {
        'Software-Engineer': 'swe',
        'Product-Manager': 'pm',
        'Data-Scientist': 'ds',
        'Data-Engineer': 'de',
        'Designer': 'dis',
        'Engineering-Manager': 'em'
    }

    job_listings_filtered = [job for job in job_listings if job[job_titles[job_title]]]

    return render_template('index.html', job_title=job_title, job_listings=job_listings_filtered)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<company_name>/jobs/<job_id>', methods=['GET', 'POST'])
def job_listing(company_name, job_id):
    job_data = job_content[company_name][job_id]
    job_description = job_content[company_name][job_id]['job_description']
    job_name = job_content[company_name][job_id]['job_name']
    img_url = job_content[company_name][job_id]['img_url']

    return render_template('job_listing.html', job_data=job_data, job_description=job_description, company_name=company_name, job_name=job_name, img_url=img_url)


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run(debug=True)