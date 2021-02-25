#!/usr/local/bin/python3.7

from flask import Flask, render_template
from api import api
from admin import admin
from dashboard import dashboard
from flask_api import FlaskAPI
#from index import index
import subprocess
#from flask.ext.api.renderers import JSONRenderer
#from flask.ext.api.renderers import HTMLRenderer
#from flask.ext.api.decorators import set_renderers
#app = Flask('rpiweb')
from werkzeug.debug import DebuggedApplication

subprocess.Popen(["python3","asynttt.py"])
subprocess.Popen(["python3","qttcpserver.py"])

app = FlaskAPI('rpiweb-api')
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
#app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(dashboard,url_prefix='/dashboard')
app.register_blueprint(api, url_prefix='/api')



@app.route('/', methods=["GET"])
def mainIndex():
    return render_template("index.html")



if __name__ == "__main__":
    try:
        subprocess.Popen(["python3", "asynttt.py"])

        app.run(host="0.0.0.0",port=80, debug=True)
    finally:
        print("Done")
        subprocess.Popen(["sudo","pkill","-9","python3"])
