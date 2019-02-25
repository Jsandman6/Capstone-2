from dotenv import load_dotenv
import json
import csv
import os
import requests
import datetime

def to_usd(price):
    return "${0:,.2f}".format(price)
load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

query = input("What is the ticker (i.e. MSFT) of the equity you would like information about? (Enter 'Done' if you're finished querying): ")

while (query != 'Done'):
    #adapted from https://stackoverflow.com/questions/7141208/python-simple-if-or-logic-statement
    if not (0 < len(query) < 6):
        print("Sorry! That ticker is invalid. Please try again!")
        exit()
    #adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    elif any(q.isdigit() for q in query):
        print("Sorry! Tickers do not contains digits. Please try again!")
        exit()

    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(query) + "&apikey=api_key"
    response = requests.get(request_url)

    



    #print(type(response))
    #print(response.status_code)
    #print(response.text)

    parsed_response = json.loads(response.text)

    #adapted from https://stackoverflow.com/questions/44012811/python-requests-quickly-know-if-response-is-json-parsable
    try:
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    except KeyError:
        print("no good")
        print("Sorry! This ticker could not be found. Please try again!")
        exit()




    # see: https://www.alphavantage.co/support/#api-key
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    #print("API KEY: " + api_key)

    



    # see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
    # TODO: assemble the request url to get daily data for the given stock symbol...

    # TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

    # TODO: further parse the JSON response...

    # TODO: traverse the nested response data structure to find the latest closing price and other values of interest...
    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys()) # TODO: sort to ensure it's ordered

    latest_day = dates[0]

    latest_price_usd = tsd[latest_day]["4. close"]

    high_prices = []
    low_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)


    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", str(query) + " prices.csv")

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()
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

    # TODO: write response data to a CSV file

    # TODO: further revise the example outputs below to reflect real information
    print("-----------------")
    print(f"STOCK SYMBOL: {query}")
    #adapted from shopping cart project
    d = datetime.datetime.now()
    print("RUN AT:" + str(d.year) + "-" + str(d.month) + "-" + str(d.day) + " " + str(d.hour) + ":" + str(d.minute) + ":" + str(d.second))
    print("-----------------")
    print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
    print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")
    print(f"RECENT HIGH: {to_usd(recent_high)}")
    print(f"RECENT LOW: {to_usd(recent_low)}")
    print("-----------------")
    print("RECOMMENDATION: Buy!")
    print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
    print("-----------------")
    print("Writing data to CSV")

    query = input("What is the ticker (i.e. MSFT) of the equity you would like information about? (Enter 'Done' if you're finished querying): ")

