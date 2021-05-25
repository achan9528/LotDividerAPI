from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value, Count
from .models import *
from datetime import date
import yfinance as yf
from itertools import chain
import redis

def getClosingPrices(closingDate=date.today().strftime("%Y-%m-%d")):
    tickers = list(Security.objects.values_list('ticker', flat=True).distinct())
    closingPrices = yf.download(tickers, closingDate)['Adj Close']
    closingPrices = closingPrices.to_dict('records')[0]

    r= redis.Redis(host='localhost', port=6379, db=0)
    r.hset('closingPrices', mapping=closingPrices)

def getClosingPrice(ticker):
    r = redis.Redis(host='localhost', port=6379, db=0)
    print(r.hget('closingPrices', ticker))
    return (float(r.hget('closingPrices', ticker).decode('utf-8')))
