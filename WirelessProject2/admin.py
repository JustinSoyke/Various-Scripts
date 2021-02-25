from flask import Blueprint, Response
#from flask_paginate import Pagination, get_page_args
from flask import json, Flask, g, render_template, abort, flash, request, Markup, redirect, url_for
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, RadioField
#from flask_login import LoginManager, UserMixin, login_required
import requests
import pandas as pd

admin = Blueprint('admin', __name__, template_folder='templates')


class UserForm(Form):
    userid = StringField("UserID: ", validators=[validators.required()])
    submit = SubmitField("Lookup")


@admin.route('/', methods=['GET','POST'])
def admin_index():
    return render_template("admin/index.html")

@admin.route('/profile', methods=["GET", "POST"])
def profile():
    form = UserForm(request.form)
    if request.method == "POST":
        userid = request.form['userid']

    if form.validate():
        apireq = checkUser(userid)

        return render_template("admin/results.html", apireq=apireq)

    return render_template("admin/profile.html",form=form)
def checkUser(userid):
    apireq = requests.get("http://127.0.0.1/api/plates/{}".format(userid)).json()
    return apireq

@admin.route('/platedb', methods=["GET","POST"])
def platedb():
    pReq = pd.read_json("http://127.0.0.1/api/plates")
    pHtml = pReq.to_dict(orient="index")
    return render_template("admin/plates.html",pHtml=pHtml,pReq=pReq)

@admin.route('/captures', methods=["GET","POST"])
def capturelog():
    cLog = pd.read_json("http://127.0.0.1/api/captures")
    return render_template("admin/capturelogs.html", cLog=cLog)





