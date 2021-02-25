#!/usr/local/bin/python3.7

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import subprocess
from picamera import PiCamera
import time
import requests
#from openalpr import Alpr
import json
#import pickle
#app = FlaskAPI(__name__)
import csv
import pandas as pd

from flask import Blueprint
#from flask_paginate import Pagination, get_page_args
from flask import json, Flask, g, render_template, flash, request, Markup, redirect, url_for
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, RadioField




api = Blueprint('api', __name__, template_folder='templates')




@api.route('/', methods=['GET','POST'])
def api_index():
    return render_template("api/index.html")



def plate_repr(key):
    platedb =pd.read_csv("platedb.csv",index_col=0)
    #platedb = platedb.to_json(orient="records")
    platedb = platedb.to_dict(orient="index")
    plateupdate = {
        "url": request.host_url.rstrip("/") + url_for("api.plates_data")+"/"+str(key),
        "name": platedb[key]["name"],
        "title":platedb[key]["title"],
        "balance":platedb[key]["balance"],
        "plateNumber":platedb[key]["plateNumber"],
        "isParked":platedb[key]["isParked"],
        "parkCount":platedb[key]["parkCount"],
        "disabledSpot":platedb[key]["disabledSpot"]
    }
    print(plateupdate)
    return plateupdate


@api.route("/plates", methods=['GET', 'POST'])
def plates_data():
    platedb = pd.read_csv("platedb.csv", index_col=0)
    #platedb = platedb.to_json(orient="records")
    if request.method == 'POST':
        platedb_csv =pd.read_csv("platedb.csv",index_col=0)
        platedb = platedb_csv.to_dict(orient="index")
        name = str(request.data.get('name', ''))
        title = str(request.data.get('title', ''))
        balance = str(request.data.get('balance', ''))
        plateNumber = str(request.data.get('plateNumber', ''))
        isParking = str(request.data.get('isParked', ''))
        parkCount = str(request.data.get('parkCount', ''))
        disabledSpot = str(request.data.get('disabledSpot', ''))
        idx = str(request.data.get('id', ''))
        newPlate = [[idx,name,title,balance,plateNumber,isParking,parkCount,disabledSpot]]
        newDF = pd.DataFrame(newPlate, columns=["id","name","title","balance","plateNumber",
                                                "isParking","parkCount","disabledSpot"])
        newDF.to_csv("platedb.csv", mode='a', header=False,index=False)

        return plate_repr(int(idx)),status.HTTP_201_CREATED

    # request.method == 'GET'
    #pdb = platedb.to_json(orient="records")
    return platedb.to_dict(orient="index")


@api.route("/plates/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def plate_detail(key):
    if request.method == "PUT":
        initDF = pd.read_csv("platedb.csv", index_col=0)
        name = str(request.data.get('name', ''))
        title = str(request.data.get('title', ''))
        balance = str(request.data.get('balance', ''))
        plateNumber = str(request.data.get('plateNumber', ''))
        isParking = str(request.data.get('isParked', ''))
        parkCount = str(request.data.get('parkCount', ''))
        disabledSpot = str(request.data.get('disabledSpot', ''))
        #idx = str(request.data.get('id', ''))

        if name:
            initDF.name[key] = name
        if title:
            initDF.title[key]= title
        if balance:
            initDF.balance[key] = balance
        if plateNumber:
            initDF.plateNumber[key] = plateNumber
        if isParking:
            initDF.isParking[key] = isParking
        if parkCount:
            initDF.parkCount[key] = parkCount
        if disabledSpot:
            initDF.disableSpot[key] = disabledSpot

        initDF.to_csv("platedb.csv")
    return plate_repr(int(key))


@api.route('/take_photo')
def takePhoto():
    if request.method == "GET":
        try:
            currentTime = time.strftime("%d-%b-%H:%M-%Y")
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.start_preview()
            time.sleep(2)
            capLocation = "static/plateimg/{}.jpg".format(currentTime)

            camera.capture(capLocation, resize=(640, 480))

        finally:
            camera.close()
               # alpr.unload()
            print("Image Captured. Returning to main function.")
            print("Checking Number Plate Info")
            return "PC", plateCheck(capLocation)


def plateCheck(capLocation):
    numRes = subprocess.getoutput("alpr -c au -p nsw -n 5 --json {}".format(capLocation))
    data = json.loads(numRes)
    print("\n1", data)
    results = data["results"]
    plateData = {"plate":"{}".format(results[0]["plate"]),
                 "confidence":"{}".format(results[0]["confidence"]),
                 "epochtime":"{}".format(data["epoch_time"]),
                 "imageLocation":"{}".format(capLocation)}
    requests.put("http://127.0.0.1/api/captures", data=plateData)
    plateLookup = requests.get("http://127.0.0.1/api/plates").json()
    for id,pdata in plateLookup.items():
        for plate in results[0]["candidates"]:
            if plate["plate"] in pdata["plateNumber"]:
#                print("\n2", pdata)
                pbal = pdata["balance"]
                pname = pdata["name"]
                pplate = pdata["plateNumber"]
    #            data2 = {"name":"{}".format(pdata["name"]),"balance":pbal-5,"plate":"{}".format(pdata["plateNumber"])}
                #data2 = '{"plate":"{}","name":"{}","balance":"{}"}'.format(pdata["name"],pdata["plateNumber"],int(pbal)-5)
 #               print("\n3", data2)
                requests.put("http://127.0.0.1/api/plates/{}".format(id),data={"balance":int(pbal)-5})
                requests.post("http://127.0.0.1:8080/display",data='{"plate":"%s","name":"%s","balance":"%d"}' % (pplate,pname,pbal-5))
               # requests.post("http://127.0.0.1:8080/display", data=pdata) #'{"name":"{}","plate":"{}","balance":{}}'.format(pdata["name"],results[0]["plate"],int(pbal)-5))


    return plateData

@api.route('/checkSpots', methods=["GET"])
def get_spots():
    if request.method == "GET":
        parkCheck = requests.get("http://192.168.43.190/dist").text
        #parkSpl = parkCheck.split(":")
        #parkSpl = "%.1f" % parkSplit[1]
        if float(parkCheck) > 100:
            print("Spot Available")
            return {"available":True} #"Spot Available. Distance: {}".format(parkCheck)
        if float(parkCheck) < 30:
            print("Spot Unavailable")
            return {"available":False} #"Spot Unavailable. Distance: {}".format(parkCheck)


@api.route('/us_get_distance', methods=["GET"])
def get_distance():
    if request.method == "GET":
        distance = subprocess.getoutput("python3 bb.py")

        dist = {"Distance":"{}".format(distance)}
        #dist = '{"Distance":"{}"}'.format(distance)
    return dist

@api.route('/spaces', methods=["GET","PUT"])
def spaces_available():
    if request.method == "GET":
        spaces = pd.read_csv("spaces.csv")
        spaces = spaces.to_dict(orient="index")
        return spaces
@api.route('/spaces/id/<int:id>/<string:key>', methods=["GET"])
def spaces_update(key=None,id=None):
    if request.method == "GET":                                #{"AvailableSpots":4}
        spaces = pd.read_csv("spaces.csv",index_col=0)
        #spaces = spaces.to_dict(orient="records")
        if key == "full":
            spaces.status[id] = "full"
            spaces.to_csv("spaces.csv")
        if key == "empty":
            spaces.status[id] = "empty"
            spaces.to_csv("spaces.csv")
        return spaces.to_dict(orient="index")

@api.route('/spaces/id/<int:bay>', methods=["GET"])
def spaces_bay(bay=None):
    if request.method == "GET":
        spaces = pd.read_csv("spaces.csv")
        if bay:
            return spaces.to_dict(orient="index")[bay-1]

@api.route('/captures', methods=["PUT","GET"])
def addLog():
    initCap = pd.read_csv("capturelog.csv", index_col=0)
    if request.method == "PUT":
        initCap = pd.read_csv("capturelog.csv", index_col=0)
        cid = len(initCap)+1
        capturedb = initCap.to_dict(orient="index")
        confidence = str(request.data.get('confidence', ''))
        plate = str(request.data.get('plate', ''))
        epochtime = str(request.data.get('epochtime', ''))
        imageLocation = str(request.data.get('imageLocation', ''))
        newPlate = [[cid,confidence,plate,epochtime,imageLocation]]
        print(newPlate)
        newCap = pd.DataFrame(newPlate, columns=["cid","confidence","plate","epochtime","imageLocation"])
        newCap.to_csv("capturelog.csv", mode='a', header=False, index=False)

        return newCap.to_dict(orient="index")

    return initCap.to_dict(orient="index")
 
