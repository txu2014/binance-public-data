import datetime

YEARS = ['2023']  # ['2018', '2019', '2020', '2021']
INTERVALS = ["1m"]
DAILY_INTERVALS = ["1m"]
TRADING_TYPE = ["spot", "um", "cm"]
MONTHS = list(range(1, 13))
MAX_DAYS = 365
BASE_URL = 'https://data.binance.vision/'
START_DATE = datetime.date(int(YEARS[0]), MONTHS[0], 1)
END_DATE = datetime.datetime.date(datetime.datetime.now())
