from LotDivider.celery import app
from LotDividerAPI import queries
from datetime import date

@app.task
def getClosingData(closingDate=date.today().strftime("%Y-%m-%d")):
    queries.getClosingPrices()