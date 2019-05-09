#robo_advisor.py
#adapted from screencast
from dotenv import load_dotenv
import json
import csv
import os
import requests
import datetime

#adapted from https://github.com/ryanbeaudet/Exec-Dashboard-Project/blob/master/monthly_sales.py
def to_usd(price):
    return "${0:,.2f}".format(price)

def compile_url(ticker):
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(ticker) + "&apikey=api_key"
    return request_url

def get_response(request_url):
    #adapted from the screencast
    response = requests.get(request_url)
    print(response)
    parsed_response = json.loads(response.text)

    return parsed_response



def transform_response(parsed_response):
    #print(parsed_response)
    dates = parsed_response["Time Series (Daily)"]

    rows = []

    for date, daily_prices in dates.items():
        row = {
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        }
        rows.append(row)
    
    return rows


def write_to_csv(rows, csv_filepath):

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    #adapted from https://realpython.com/python-csv/
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

        writer.writeheader()

        for r in rows:
            writer.writerow(r)



load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

#adapted from screencast
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


if __name__ == "__main__":
    #adapted from https://github.com/ryanbeaudet/shopping-cart/blob/master/shopping_cart.py
    query = input("What is the ticker (i.e. MSFT) of the security you would like information about? (Enter 'done' if you're finished querying): ")


    #while loop was my own idea
    #adapted logic from https://opentechschool.github.io/python-beginners/en/logical_operators.html
    while (query != 'done'):
        #adapted from https://stackoverflow.com/questions/7141208/python-simple-if-or-logic-statement
        if not (0 < len(query) < 7):
            print("Sorry! That ticker is invalid. Please try again!")
            exit()
        #adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
        elif any(q.isdigit() for q in query):
            print("Sorry! Tickers do not contains digits. Please try again!")
            exit()

        request_url = compile_url(query)

        parsed_response = get_response(request_url)

        transformed_response = transform_response(parsed_response)

        #adapted from https://stackoverflow.com/questions/44012811/python-requests-quickly-know-if-response-is-json-parsable
        #I also used knowledge from other CS courses to implement an exception
        try:
            last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
            print(last_refreshed)
        except KeyError:
            print("Sorry! This ticker could not be found. Please try again!")
            exit()

        #adapted from https://stackoverflow.com/questions/14524322/how-to-convert-a-date-string-to-different-format
        # as well as https://stackoverflow.com/questions/6557553/get-month-name-from-number
        last_refreshed_new = datetime.datetime.strptime(last_refreshed, '%Y-%m-%d').strftime('%B %d, %Y')

        # see: https://www.alphavantage.co/support/#api-key
        api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

        #adapted from screencast
        tsd = parsed_response["Time Series (Daily)"]

        dates = list(tsd.keys())

        #adapted from https://stackoverflow.com/questions/17627531/sort-list-of-date-strings
        sorted(dates, key=lambda date: datetime.datetime.strptime(date, '%Y-%m-%d'))

        
        #adapted from screencast
        latest_day = dates[0]

        latest_price_usd = tsd[latest_day]["4. close"]

        high_prices = []
        low_prices = []

        #high prices adapted from screencast
        #I figured the low prices part out on my own, although I believe it closely mirrors the screencast
        for date in dates:
            high_price = tsd[date]["2. high"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3. low"]
            low_prices.append(float(low_price))

        recent_high = max(high_prices)
        recent_low = min(low_prices)



        #adapted from screencast
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", str(query) + " prices.csv")

        write_to_csv(transformed_response, csv_file_path)


        

        

        

    
        
        #adapted on my own from my understanding of value investing
        #stock prices often dip below their intrinsic value due to volatile variations in market sentiment
        #the code itself is my own adaptation
        benchmark_factor = 1.1
        benchmark = recent_low * benchmark_factor
        recommendation = ""
        justification = ""
        #adapted from https://www.programiz.com/python-programming/if-elif-else
        if (float(latest_price_usd) < benchmark):
            recommendation = "Buy"
            justification = "The security price is near its historical low and is likely undervalued. This means that risk adjusted returns will likely be higher."
        elif (float(latest_price_usd) > benchmark):
            recommendation = "Don't buy"
            justification = "The security price is relatively high compared to its historical low and there's no reason to think it's undervalued. Risk adjusted returns are unlikely to be high."


        
        #most of this is adapted from the screencast
        print("")
        print("-----------------")
        print(f"STOCK SYMBOL: {query}")
        #adapted from https://github.com/ryanbeaudet/shopping-cart/blob/master/shopping_cart.py
        d = datetime.datetime.now()
        #adapted from https://www.guru99.com/date-time-and-datetime-classes-in-python.html#3
        print("RUN AT: " + str(d.strftime('%I:%M%p %B %d, %Y')))
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

        query = input("What is the ticker (i.e. MSFT) of the next security you would like information about? (Enter 'done' if you're finished querying): ")