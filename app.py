#Chatbot Tutorial with Firebase
#Import Library
import json
import os
import requests
from flask import request
from flask import make_response
from function_chatbot import *
from flask import Flask,render_template
from requests.exceptions import HTTPError
#-------------------------------------

# Flask
app = Flask(__name__)
@app.route('/ACCOMMODATION/<place_id>')
def index(place_id):
    url = f"https://tatapi.tourismthailand.org/tatapi/v5/accommodation/{place_id}"

    try:
        Ac = requests.get(url,headers=my_headers).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        
    return render_template("GetAccommodationDetail.html",Ac=Ac['result'])


@app.route('/ATTRACTION/<place_id>')
def GetAttractionDetail(place_id):
    url = f"https://tatapi.tourismthailand.org/tatapi/v5/attraction/{place_id}"

    try:
        At = requests.get(url,headers=my_headers).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6

    
    return render_template("GetAttractionDetail.html",At=At['result'])


@app.route('/RESTAURANT/<place_id>')
def GetRestaurantDetail(place_id):
    url = f"https://tatapi.tourismthailand.org/tatapi/v5/restaurant/{place_id}"

    try:
        Re = requests.get(url,headers=my_headers).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        
    return render_template("GetRestaurantDetail.html",Re=Re['result'])

@app.route('/Route/<place_id>')
def GetRecommendedRouteDetail(place_id):
    url = f"https://tatapi.tourismthailand.org/tatapi/v5/routes/{place_id}"

    try:
        R = requests.get(url,headers=my_headers).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        
    return render_template("GetRecommendedRouteDetail.html",R = R['result'])


#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)

