from flask import Flask,render_template,request
import requests
import json
import datetime
import random
import string
import time
import os


def genString(stringLength):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

url = 'https://api.cloudflareclient.com/v0a745/reg'


def run(referrer):
    install_id = genString(11)
    print("KEY USED =======",install_id)
    body = {"key": "{}=".format(genString(42)),
            "install_id": install_id,
            "fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
            "referrer": referrer,
            "warp_enabled": False,
            "tos": datetime.datetime.now().isoformat()[:-3] + "+05:30",
            "type": "Android",
            "locale": "zh-CN"}

    bodyString = json.dumps(body)

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Host': 'api.cloudflareclient.com',
               'Connection': 'Keep-Alive',
               'Accept-Encoding': 'gzip',
               'User-Agent': 'okhttp/3.12.1'
               }

    r = requests.post(url, data=bodyString, headers=headers)
    return r




app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        i=request.form['id']
        referrer=i
        c = 1
        while True:
            result = run(referrer)
            print("CODE HAS STARTED")
            print("*******************************************")
            if result.status_code == 200:
                print(c,"GB added successfully !")
                c = c + 1
            elif(c>=3):
                print("MAX REQUEST.......")
                break
            else:
                time.sleep(2)
                c = c + 1
                print("not Working")
        return render_template("index.html")
    
    return render_template("index.html")

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=os.getenv('PORT'),debug=True)
