from LotDivider.celery import app
from LotDividerAPI import queries
from datetime import date

@app.task
def getClosingData(closingDate=date.today().strftime("%Y-%m-%d")):
    print('huh')
    queries.getClosingPrices()

@app.task
def add(x,y):
    return x+y