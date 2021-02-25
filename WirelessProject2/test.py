#!/usr/local/bin/python3

from flask import Flask, request, url_for
import sys
import logging
import re
#from flask.logging import default_handler
dApp = Flask("qtweb")
log = logging.getLogger('werkzeug')
#log.disabled = True
logging.basicConfig(level=logging.DEBUG)
#dApp.logger.disabled = True
#dApp.logger.removeHandler(default_handler)
import json

@dApp.route("/display", methods=['POST'])
def show_detail():
    if request.method == "POST":
        # data = request.data
        #self.test.setText(request.data)
        #print(request.data)
        data = request.get_data().decode()
        print(data) 
        sys.stdout.flush()
#       print(data.decode())
        return data

if __name__ == "__main__":
    try:
        dApp.run(host="0.0.0.0", port=8080,debug=True)
    finally:
        print("Done")
