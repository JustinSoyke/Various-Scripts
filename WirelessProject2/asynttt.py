import requests
import time

def main():
    try:
        req = requests.get("http://127.0.0.1/api/us_get_distance").json()
        #time.sleep(4)
        print(req)
        print(req["Distance"])
        if int(req["Distance"]) < 150:
            requests.get("http://127.0.0.1/api/take_photo")
        #print(reqNew)
            time.sleep(2)
        else:
            time.sleep(2)
    except:
        return

while True:
    main()
    time.sleep(5)
