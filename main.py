from flask import Flask, render_template
app = Flask(__name__)
import json
import urllib.request
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


    previous_close = data['chart']['result'][0]['indicators']['quote'][0]['close']


    open_price = data['chart']['result'][0]['indicators']['quote'][0]['open'][0]
    print(symbol_name)
    print(regular_market_price)
    print(round(open_price))
    print(previous_close)
    rounded_data = (round(previous_close[0], 2))
    datas = {'key':[symbol_name, regular_market_price, round(open_price), rounded_data], 'url':url}
    return datas

if __name__ == "__main__":
   app.run()