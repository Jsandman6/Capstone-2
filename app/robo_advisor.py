#robo_advisor.py
from dotenv import load_dotenv
import json
import csv
import os
import requests
import datetime

#adapted from https://github.com/ryanbeaudet/Exec-Dashboard-Project/blob/master/monthly_sales.py
def to_usd(price):
    return "${0:,.2f}".format(price)

#adapted from https://github.com/ryanbeaudet/Exec-Dashboard-Project/blob/master/monthly_sales.py
#but thank you to Caroline Feeney for originally giving me general guidance on this function!
def month_amend(month):
    month_adjust={'1':'January', '2':'February',
    '3':'March','4':'April','5':'May','6':'June',
    '7':'July','8':'August','9':'September','10':'October',
    '11':'November','12':'December'}
    new_month = month_adjust[month]
    return new_month


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

#adapted from screencast
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

#adapted from https://github.com/ryanbeaudet/shopping-cart/blob/master/shopping_cart.py
query = input("What is the ticker (i.e. 'MSFT') of the equity you would like information about? (Enter 'Done' if you're finished querying): ")

#while loop was my own idea
while (query != 'Done'):
    #adapted from https://stackoverflow.com/questions/7141208/python-simple-if-or-logic-statement
    if not (0 < len(query) < 7):
        print("Sorry! That ticker is invalid. Please try again!")
        exit()
    #adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    elif any(q.isdigit() for q in query):
        print("Sorry! Tickers do not contains digits. Please try again!")
        exit()

    #adapted from the screencast
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(query) + "&apikey=api_key"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    #adapted from https://stackoverflow.com/questions/44012811/python-requests-quickly-know-if-response-is-json-parsable
    #I also used knowledge from other CS courses to implement an exception
    try:
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    except KeyError:
        print("Sorry! This ticker could not be found. Please try again!")
        exit()

    

    #adapted from https://stackoverflow.com/questions/14524322/how-to-convert-a-date-string-to-different-format
    # as well as https://stackoverflow.com/questions/6557553/get-month-name-from-number
    last_refreshed_new = datetime.datetime.strptime(last_refreshed, '%Y-%m-%d').strftime('%B %d, %Y')

    # see: https://www.alphavantage.co/support/#api-key
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    #print("API KEY: " + api_key)

    
    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys())

    #adapted from https://stackoverflow.com/questions/17627531/sort-list-of-date-strings
    sorted(dates, key=lambda date: datetime.datetime.strptime(date, '%Y-%m-%d'))

    

    latest_day = dates[0]

    latest_price_usd = tsd[latest_day]["4. close"]

    high_prices = []
    low_prices = []

    #high prices adapted from screencast but I did low prices on my own
    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)



    #adapted from screencast
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", str(query) + " prices.csv")

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    #adapted from https://realpython.com/python-csv/
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()

        #adapted from screencast
        for date in dates:
            daily_prices = tsd[date]
            writer.writerow({
                "timestamp": date,
                "open": daily_prices["1. open"],
                "high": daily_prices["2. high"],
                "low": daily_prices["3. low"],
                "close": daily_prices["4. close"],
                "volume": daily_prices["5. volume"]
            })

    #
    # INFO OUTPUTS
    #

    #adapted on my own from my understanding of value investing
    #stock prices often dip below their intrinsic value due to volatile variations in market sentiment
    #the code itself is my own adaptation
    benchmark_factor = 1.1
    benchmark = recent_low * benchmark_factor
    recommendation = ""
    justification = ""
    if (float(latest_price_usd) < benchmark):
        recommendation = "Buy"
        justification = "The stock price is near its recent low and is likely undervalued. This means that risk adjusted returns will likely be higher."
    elif (float(latest_price_usd) > benchmark):
        recommendation = "Don't buy"
        justification = "The stock price is relatively high and there's no reason to think it's undervalued. Risk adjusted returns are unlikely to be high."
    

    
    #most of this is adapted from the screencast
    print("")
    print("-----------------")
    print(f"STOCK SYMBOL: {query}")
    #adapted from https://github.com/ryanbeaudet/shopping-cart/blob/master/shopping_cart.py
    d = datetime.datetime.now()
    month_print = month_amend(str(d.month))
    #adapted from https://github.com/ryanbeaudet/shopping-cart/blob/master/shopping_cart.py
    print("RUN AT: " + str(d.hour) + ":" + str(d.minute) + " " + month_print + " " + str(d.day) + ", " + str(d.year))
    print("-----------------")
    print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed_new}")
    print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")
    print(f"RECENT HIGH: {to_usd(recent_high)}")
    print(f"RECENT LOW: {to_usd(recent_low)}")
    print("-----------------")
    #I did this part on my own
    print(f"RECOMMENDATION: {recommendation}")
    print(f"RECOMMENDATION REASON: {justification}")
    print("-----------------")
    print("Writing data to CSV")
    print("-----------------\n")

    query = input("What is the ticker (i.e. MSFT) of the equity you would like information about? (Enter 'Done' if you're finished querying): ")

