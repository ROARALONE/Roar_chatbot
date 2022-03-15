import requests
from flask import Flask
import os
from requests.exceptions import HTTPError
    
app = Flask(__name__)
@app.route('/')
def index():
    my_headers = {'Authorization' : 'Bearer GUrPRVm8IIgIkclxZQ8wp9ptzoGsY()jYrNYYMtMi)xPo8fSSb0AxGxX4mT9)e0rDzgYG5s4TbfKkCqvuP)ALX0=====2',
              'Accept-Language' : 'th'}
    url = "https://tatapi.tourismthailand.org/tatapi/v5/places/search?keyword=วัด&location=&categorycodes=attraction&provinceName=กรุงเทพ&radius=20&numberOfResult=10&pagenumber=1&destination=&filterByUpdateDate=2019/09/01-2022/01/31"

    try:
        response = requests.get(url,headers=my_headers).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return f"<h2> call api successfully!! {response}</h2>"

if __name__ == "__main__":
    port = int(os.getenv('PORT', 443))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)