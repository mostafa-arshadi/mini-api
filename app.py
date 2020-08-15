from flask import Flask
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
from requests import get

def getData():
    source = get("https://bitbarg.me/live-price").text
    soup = BeautifulSoup(source,'html.parser')
    tr = (soup.find('tr',attrs={"class":"lp-currency--row",'data-symbol':"BTCUSDT"}))
    sell_price = tr.find("span",attrs={"class":"sell-price"}).text
    buy_price = tr.find("span",attrs={"class":"buy-price"}).text
    return [sell_price, buy_price]

def getData2():
    source = get("https://pay98.cash/%D9%81%D8%B1%D9%88%D8%B4-%D9%88-%D8%AE%D8%B1%DB%8C%D8%AF-%D8%A8%DB%8C%D8%AA-%DA%A9%D9%88%DB%8C%D9%86-Buy-Bitcoin").text
    soup = BeautifulSoup(source,'html.parser')
    section = (soup.find('section',attrs={"id":"bazar-cap"}))
    buy_price = section.findAll("div")[0].findAll("div")[0].findAll("div")[0].find("b").text
    sell_price = section.findAll("div")[0].findAll("div")[0].findAll("div")[2].find("b").text
    return [sell_price, buy_price]

application = Flask(__name__)
api = Api(application)

spec = lambda x : "{:,}".format(int(x))
class ApiPrice(Resource):
    def get(self):
        data = getData()
        data2 = getData2()
        return [{
            'name':"BitBarg | بیت برگ",
            'sell':spec(data[0] if ',' not in data[0] else data[0].replace(",","")),
            'buy':spec(data[1] if ',' not in data[1] else data[1].replace(",",""))
        },
        {
            'name':"Pay98 | پی ۹۸",
            'sell':spec(data2[0] if ',' not in data2[0] else data2[0].replace(",","")),
            'buy':spec(data2[1] if ',' not in data2[1] else data2[1].replace(",",""))
        }
        ]

api.add_resource(ApiPrice,'/')

if __name__ == "__main__":
    app.run()