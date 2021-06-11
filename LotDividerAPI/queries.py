from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value, Count
from .models import *
from datetime import date
import yfinance as yf
from itertools import chain
import redis
import os

def getClosingPrices(closingDate=date.today().strftime("%Y-%m-%d")):
    tickers = list(Security.objects.values_list('ticker', flat=True).distinct())
    print(closingDate)
    closingPrices = yf.download(tickers, closingDate)['Adj Close']
    closingPrices = yf.download(tickers, start='2021-05-04', end='2021-05-04')['Adj Close']
    closingPrices = closingPrices.to_dict('records')[0]

    r= redis.Redis(host=os.environ.get('CACHE_HOST'), port=os.environ.get('CACHE_PORT'), db=0)
    r.hmset('closingPrices', mapping=closingPrices)
    print(closingPrices)
    print('Got Closing Prices')

def deleteClosingPrices():
    tickers = list(Security.objects.values_list('ticker', flat=True).distinct())
    r= redis.Redis(host=os.environ.get('CACHE_HOST'), port=os.environ.get('CACHE_PORT'), db=0)
    for ticker in tickers:
        r.hdel('closingPrices', ticker)
    print('Deleted Closing Prices')

def getClosingPrice(ticker):
    r = redis.Redis(host=os.environ.get('CACHE_HOST'), port=os.environ.get('CACHE_PORT'), db=0)
    print(r.hget('closingPrices', ticker))
    return (float(r.hget('closingPrices', ticker).decode('utf-8')))
