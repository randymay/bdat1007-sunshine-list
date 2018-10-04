# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request
#import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud import storage
from domain.SectorModule import Sector
from domain.EmployerModule import Employer
import json


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

#db = pymysql.connect(host="35.237.247.30",    # your host, usually localhost
#                     user="bdat1007",         # your username
#                     passwd="password",  # your password
#                     db="sunshine_list")        # name of the data base
# mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
#engine = create_engine('mysql+mysqldb://bdat1007:password@35.237.247.30/sunshine_list')
engine = create_engine('mysql+pymysql://bdat1007:password@/sunshine_list?unix_socket=/cloudsql/bdat1007-sunshine-list:us-east1:new-sunshine-db')
#engine = create_engine('mysql+pymysql://bdat1007:password@35.237.247.30/sunshine_list')
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()

# cur = db.cursor()

@app.route('/')
#def hello():
#    """Return a friendly HTTP greeting."""
#    return 'Hello World!'
def main():
    """Return a pre-defined web-template."""
    return render_template('index.html')

@app.route('/dashboard',methods=["GET", "POST"])
#def hello():
#    """Return a friendly HTTP greeting."""
#    return 'Hello World!'
def dashboard():
    """Return a dashboard webpage."""
    sectors=[]
    employers=[]
    if request.method == "GET":
        for sector in session.query(Sector).order_by(Sector.totalEmployers.desc()):
            sectors.append(sector.name)
            employers.append(sector.totalEmployers)
        return render_template('dashboards.html', values =employers, labels=sectors)
    else:
        return render_template('dashboards.html')

@app.route('/dashboard2',methods=["GET", "POST"])
#def hello():
#    """Return a friendly HTTP greeting."""
#    return 'Hello World!'
def dashboard2():
    """Return a dashboard webpage."""
    sectors=[]
    salaries=[]
    if request.method == "GET":
        for sector in session.query(Sector).order_by(Sector.totalSalaryPaid.desc()):
            sectors.append(sector.name)
            salaries.append(sector.totalSalaryPaid)
        return render_template('dashboards2.html', values =salaries, labels=sectors)
    else:
        return render_template('dashboards2.html')

@app.route('/about')
#def hello():
#    """Return a friendly HTTP greeting."""
#    return 'Hello World!'
def about():
    """Return a dashboard webpage."""
    return render_template('about.html')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]