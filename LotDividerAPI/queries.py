from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value, Count
from .models import *
from datetime import date
import yfinance as yf
from itertools import chain

def getClosingPrices(closingDate=date.today().strftime("%Y-%m-%d")):
    tickers = list(Security.objects.values_list('ticker', flat=True).distinct())
    closingPrices = yf.download(tickers, closingDate)['Adj Close']
    return closingPrices.to_dict('records')[0]


