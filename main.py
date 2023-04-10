from flask import Flask, render_template
app = Flask(__name__)
import json
import urllib.request
from decimal import *
@app.route('/')
def hello_world():
    return 'Halloooo World!'

@app.route('/h/<post_id>')
def post(post_id):
    # post = get_post(post_id)
    return post_id

@app.route('/stock/<post_id>')
def stocks(post_id):
    # post = get_post(post_id)

    url = "https://query1.finance.yahoo.com/v8/finance/chart/"+post_id+"?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    with open("data.json", "w") as outfile:
        json.dump(data, outfile)
      #reading a json file  
    with open('data.json') as f:
        data = json.load(f)


    #print(data)
    symbol_name = data['chart']['result'][0]['meta']['symbol']
    regular_market_price = data['chart']['result'][0]['meta']['regularMarketPrice']


    previous_close = data['chart']['result'][0]['meta']['previousClose']

    open_price = data['chart']['result'][0]['indicators']['quote'][0]['open'][0]
    # print(symbol_name)
    # print(regular_market_price)
    # print(round(open_price))
    # print(previous_close)
    #previousclose = round(previous_close[0], 2)
   

    sub = Decimal(regular_market_price) - Decimal(previous_close)
    #print(round(sub,2))

    change = round(sub,2)
    current_price = Decimal(regular_market_price)
    changepercentage = (change/current_price) * 100
    #change_percentage = (change/current_price) * Decimal('100')
    #print(round(changepercentage,2))

    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return json.JSONEncoder.default(self, obj)


    x = {"name": symbol_name, "price": regular_market_price, "open":round(open_price, 2), "close": previous_close , "change": round(sub,2), "change_percentage": round(changepercentage,2)}
    json_object = json.dumps(x, indent = 5,cls=JSONEncoder) 
    print(json_object)
    return json_object


@app.route('/ystock/<ys>')
def ystocks(ys):
    # post = get_post(post_id)

    url = "https://query1.finance.yahoo.com/v8/finance/chart/"+ys+"?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    with open("data.json", "w") as outfile:
        json.dump(data, outfile)
      #reading a json file  
    with open('data.json') as f:
        data = json.load(f)


    #print(data)
    symbol_name = data['chart']['result'][0]['meta']['symbol']
    regular_market_price = data['chart']['result'][0]['meta']['regularMarketPrice']


    previous_close = data['chart']['result'][0]['meta']['previousClose']

    open_price = data['chart']['result'][0]['indicators']['quote'][0]['open'][0]
    # print(symbol_name)
    # print(regular_market_price)
    # print(round(open_price))
    # print(previous_close)
    #previousclose = round(previous_close[0], 2)
   

    sub = Decimal(regular_market_price) - Decimal(previous_close)
    #print(round(sub,2))

    change = round(sub,2)
    current_price = Decimal(regular_market_price)
    changepercentage = (change/current_price) * 100
    #change_percentage = (change/current_price) * Decimal('100')
    #print(round(changepercentage,2))

    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return json.JSONEncoder.default(self, obj)

    x = [symbol_name, regular_market_price, round(open_price, 2), previous_close, round(sub,2), round(changepercentage,2)]
    yahoostocks = {"data" : x}
    # x = {"name": symbol_name, "price": regular_market_price, "open":round(open_price, 2), "close": previous_close , "change": round(sub,2), "change_percentage": round(changepercentage,2)}
    json_object = json.dumps(yahoostocks, indent = 4,cls=JSONEncoder) 
    print(json_object)
    return json_object

if __name__ == "__main__":
   app.run()
