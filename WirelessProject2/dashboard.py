from flask import Blueprint, render_template, redirect
#from flask_paginate import Pagination, get_page_args
#from flask import json, Flask, g, render_template, flash, request, Markup, redirect, url_for
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, RadioField
from flask_api.renderers import HTMLRenderer
from flask_api.decorators import set_renderers, request
from flask_api import app
dashboard = Blueprint('dashboard', __name__, template_folder='templates')
import requests
import pandas as pd





@dashboard.route('/', methods=['GET','POST'])
@set_renderers(HTMLRenderer)
def dashboard_index():
    return render_template("dashboard/index.html")


@dashboard.route('/spaces', methods=["GET","POST"])
def checkParking():
    if request.method == "GET":
        bayid = 6
        full = 0
        empty = 0
        status = "empty"
        spaces = requests.get("http://127.0.0.1/api/spaces").json()
        for i in spaces:
            if spaces[i]["status"] == "full":
                full +=1
            if spaces[i]["status"] == "empty":
                empty +=1
        checkSpot = requests.get("http://127.0.0.1/api/checkSpots").json()
        if checkSpot["available"]:
            requests.get("http://127.0.0.1/api/spaces/id/6/empty")
            status = "empty"
        #if checkSpot["available"] == "false":
        else:
            requests.get("http://127.0.0.1/api/spaces/id/6/full")
            status = "full"



    return render_template("dashboard/spaces.html", spaces=spaces,empty=empty,full=full,status=status)




