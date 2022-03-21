#Import Library
import os
from flask import Flask
from flask import request
from flask import make_response,render_template
from function_chatbot import *
from requests.exceptions import HTTPError

#---- Google Sheet ----
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("Chatbot_notify").worksheet('Sheet1')

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

@app.route('/', methods=['POST']) #Using post as a method
def MainFunction():

    #Getting intent from Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    if question_from_dailogflow_raw["queryResult"]["intent"]["displayName"] == 'place_request':
        answer_from_bot = place_request(question_from_dailogflow_raw)
    elif question_from_dailogflow_raw["queryResult"]["intent"]["displayName"] == 'place_recommendation':
        answer_from_bot = place_recommendation(question_from_dailogflow_raw)
    elif question_from_dailogflow_raw["queryResult"]["intent"]["displayName"] == 'trip_recommendation':
        answer_from_bot = trip_recommendation(question_from_dailogflow_raw)
    else:
        #Call generating_answer fun
        answer_from_bot = generating_answer(question_from_dailogflow_raw)
    #Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #Setting Content Type
    return r


def generating_answer(question_from_dailogflow_dict):

    #Print intent that recived from dialogflow.
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"]

    #Select function for answering question
    if intent_group_question_str == 'หิวจัง':
        answer_str = menu_recormentation()
    elif intent_group_question_str == 'คำนวนน้ำหนัก':
        answer_str = BMI_calculation(question_from_dailogflow_dict)
    elif intent_group_question_str == 'info_schedule':
        answer_str = info_schedule(question_from_dailogflow_dict)
    elif intent_group_question_str == 'save_schedule - yes':
        answer_str = save_schedule(question_from_dailogflow_dict)
    #elif intent_group_question_str == 'event_list':
    #    answer_str = event_list(question_from_dailogflow_dict)
    else: answer_str = "ขอโทษนะคะ ไม่เข้าใจ คุณต้องการอะไร"

    #Build answer dict
    answer_from_bot = {"fulfillmentText": answer_str}

    #Convert dict to JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4)
    return answer_from_bot


def menu_recormentation(): #ฟังก์ชั่นสำหรับเมนูแนะนำ
    menu_name = 'ข้าวขาหมู'
    answer_function = menu_name + ' สิ น่ากินนะ'
    return answer_function

def BMI_calculation(respond_dict): #Function for calculating BMI

    #Getting Weight and Height
    weight_kg = float(respond_dict["queryResult"]["outputContexts"][0]["parameters"]["Weight.original"])
    height_cm = float(respond_dict["queryResult"]["outputContexts"][0]["parameters"]["Height.original"])

    #Calculating BMI
    BMI = weight_kg/(height_cm/100)**2
    if BMI < 18.5 :
        answer_function = "คุณผอมเกินไปนะ"
    elif 18.5 <= BMI < 23.0:
        answer_function = "คุณมีน้ำหนักปกติ"
    elif 23.0 <= BMI < 25.0:
        answer_function = "คุณมีน้ำหนักเกิน"
    elif 25.0 <= BMI < 30:
        answer_function = "คุณอ้วน"
    else :
        answer_function = "คุณอ้วนมาก"
    return answer_function

def info_schedule(respond_dict):
     time = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["time"][11:16]
     destination = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["destination"]
     date = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["date"][0:10]
     return f'คุณจะไปวันที่ {date} เวลา {time} น. ที่ {destination} ใช่มั้ยคะ?'


def save_schedule(respond_dict):
    time = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["time"][11:16]
    destination = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["destination"]
    date = respond_dict["queryResult"]["outputContexts"][0]["parameters"]["date"][0:10]
    userId = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    sheet.insert_row([userId,destination,date,time],2)
    return "บันทึกการแจ้งเตือนเรียบร้อยแล้วค่ะ"

#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)

