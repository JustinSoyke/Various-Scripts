from flask import Blueprint
#from flask_paginate import Pagination, get_page_args
from flask import json, Flask, g, render_template, flash, request, Markup, redirect, url_for
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, RadioField


index = Blueprint('index', __name__, template_folder='templates')





