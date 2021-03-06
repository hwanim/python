#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
#import ols

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

#    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# "https://api.korbit.co.kr/v1/ticker?currency_pair=$CURRENCY_PAIR"

def processRequest(req):
#    if req.get("result").get("action") != "yahooWeatherForecast":
#        return {}
    baseurl = "https://api.korbit.co.kr/v1/ticker?currency_pair="
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode(yql_query) #yql_query example = "btc_krw"
    result = urlopen(yql_url).read() #result example = {"timestamp":1498994744000,"last":"3021500"}
    data = json.loads(result) #json decoding
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    req = json.loads(req)
    result = req.get("result")
    parameters = result.get("parameters")
    bitcoinType = parameters.get("bitcoinType")
    if bitcoinType is None:
        return None

    return bitcoinType


def makeWebhookResult(data):
#    query = data.get('query')
#    if query is None:
#        return {}

#    result = query.get('results')
#    if result is None:
#        return {}

#    channel = result.get('channel')
#    if channel is None:
#        return {}
    price = data.get('last')

    if price is None:
         return {}

#    item = channel.get('item')
#    location = channel.get('location')
#    units = channel.get('units')
#    if (location is None) or (item is None) or (units is None):
#        return {}

#    condition = item.get('condition')
#    if condition is None:
#        return {}

    # print(json.dumps(item, indent=4))

#    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    speech = "the price of " + bitcoinType + " is " + price
#    print("Response:")
#    print(speech)

    returnValue = {"speech": speech, "displayText": speech}

    return returnValue


    # "data": data,
    # "contextOut": [],
    #"source": "apiai-weather-webhook-sample"


if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))

#    print("Starting app on port %d" % port)

#    app.run(debug=False, port=port, host='0.0.0.0')
    app.run()
