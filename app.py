from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from datetime import datetime, timedelta
import json

import data



app = Flask(__name__, static_folder='static')


db = data.init_db()
#job_listings = data.get_listings(db)


@app.route('/', methods=['GET', 'POST'])
def index(page='1', limit=21):
    job_listings = data.get_listings(db, role=None, start_after=None, limit=limit)

    # pagination
    previous_page = False
    start_after = request.args.get('start_after')
    end_before = request.args.get('end_before')
    forwards = 'True'

    if len(job_listings) > limit - 1:
        next_page = str(int(page) + 1)
        job_listings = job_listings[:limit-1]
        start_after = job_listings[-1]['job_id']
    else:
        next_page = False 

    return render_template('index.html', job_title='All', job_listings=job_listings, start_after=start_after, end_before=end_before, previous_page=previous_page, next_page=next_page, forwards=forwards)



@app.route('/<job_title>', methods=['GET', 'POST'])
def filtered_listings(job_title, limit=21):
    job_titles = {
        'Software-Engineer': 'swe',
        'Product-Manager': 'pm',
        'Data-Scientist': 'ds',
        'Data-Engineer': 'de',
        'Designer': 'dis',
        'Engineering-Manager': 'em'
    }

    start_after = request.args.get('start_after')
    end_before = request.args.get('end_before')
    forwards = request.args.get('forwards')
    page = request.args.get('page')

    # check if all or specific title is selected
    if job_title == 'All':
        job_listings = data.get_listings(db, role=None, start_after=start_after, end_before=end_before, forwards=forwards, limit=21) 
    else:
        job_listings = data.get_listings(db, role=job_titles[job_title], start_after=start_after, end_before=end_before, forwards=forwards, limit=21) 


    with open('track0.txt', 'w') as f:
        f.write(f'len: {len(job_listings)}, forwards: {forwards} type: {type(forwards)}, end_before: {end_before}, start_after: {start_after}')


    # previous page
    if int(page) > 1:
        previous_page = str(int(page) - 1)
    else:
        previous_page = False
    
    # next page
    if forwards == 'True' and len(job_listings) == limit:
        next_page = str(int(page) + 1)
    elif forwards == 'False':
        next_page = str(int(page) + 1)
    else:
        next_page = False

    # trimming listings if they are longer than 20
    if forwards == 'True' and len(job_listings) == limit:
        job_listings = job_listings[:limit-1]
               
    with open('track.txt', 'w') as f:
        f.write(f'len: {len(job_listings)}, forwards: {forwards} type: {type(forwards)}, end_before: {end_before}, previous_page: {previous_page}, start_after: {start_after}, next_page: {next_page}')

    
    return render_template('index.html', job_title=job_title, job_listings=job_listings, start_after=start_after, end_before=end_before, previous_page=previous_page, next_page=next_page)



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