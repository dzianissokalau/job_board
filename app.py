from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from datetime import datetime, timedelta
import json

import data



app = Flask(__name__, static_folder='static')


db = data.init_db()
job_listings = data.get_listings(db)


@app.route('/', methods=['GET', 'POST'])
def index(job_listings=job_listings[0:20]):
    previous_page = False
    next_page = '2'

    return render_template('index.html', job_title='All', job_listings=job_listings, previous_page=previous_page, next_page=next_page)


@app.route('/<job_title>/<page>', methods=['GET', 'POST'])
def filtered_listings(job_title, page, job_listings=job_listings):
    job_titles = {
        'Software-Engineer': 'swe',
        'Product-Manager': 'pm',
        'Data-Scientist': 'ds',
        'Data-Engineer': 'de',
        'Designer': 'dis',
        'Engineering-Manager': 'em'
    }

    # check if all or specific title is selected
    if job_title == 'All':
        job_listings_filtered = job_listings
    else:
        job_listings_filtered = [job for job in job_listings if job[job_titles[job_title]]]
    
    # pagination
    page_int = int(page)
    if page_int == 1:
        previous_page = False
    else:
        previous_page = str(page_int - 1)

    start = (page_int - 1) * 20
    # if there are less elements in the list
    if len(job_listings_filtered) - 1 <= page_int * 20 - 1:
        stop = len(job_listings_filtered) - 1
        next_page = False
    else:
        stop =  page_int * 20 - 1
        next_page = str(page_int + 1)
    
    job_listings_filtered = job_listings_filtered[start:stop]

    return render_template('index.html', job_title=job_title, job_listings=job_listings_filtered, previous_page=previous_page, next_page=next_page)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<company_name>/jobs/<job_id>', methods=['GET', 'POST'])
def job_listing(company_name, job_id):
    job_data = data.get_listing(db, job_id)
    job_description = job_data['job_description']
    job_name = job_data['job_name']
    img_url = job_data['img_url']

    return render_template('job_listing.html', job_data=job_data, job_description=job_description, company_name=company_name, job_name=job_name, img_url=img_url)


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run()