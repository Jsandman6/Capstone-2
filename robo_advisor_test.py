from app.robo_advisor import *

def test_to_usd():
    assert to_usd(7) == "$7.00"

    assert to_usd(7.25) == "$7.25"

    assert to_usd(7.2) == "$7.20"

    assert to_usd(7.88888888) == "$7.89"

    assert to_usd(1000000) == "$1,000,000.00"

def test_get_response():
    ticker = "MSFT"

    parsed_response = get_response(ticker)

    assert isinstance(parsed_response, dict)
    assert "Time Series (Daily)" in parsed_response.keys()
    assert "Meta Data" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == ticker

def test_transform_response():


    parsed_response_example = {
    "Meta Data": {
        "1. Information": "Daily Time Series with Splits and Dividend Events",
        "2. Symbol": "MSFT",
        "3. Last Refreshed": "2019-05-08 16:00:01",
        "4. Output Size": "Full size",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2019-05-08": {
            "1. open": "125.4400",
            "2. high": "126.3700",
            "3. low": "124.7500",
            "4. close": "125.5100",
            "5. volume": "21077406"
        },
        "2019-05-07": {
            "1. open": "126.4600",
            "2. high": "127.1800",
            "3. low": "124.2200",
            "4. close": "125.5200",
            "5. volume": "35167000"
        },
        "2019-05-06": {
            "1. open": "126.3900",
            "2. high": "128.5600",
            "3. low": "126.1100",
            "4. close": "128.1500",
            "5. volume": "24239464"
        },
        "2019-05-03": {
            "1. open": "127.3600",
            "2. high": "129.4300",
            "3. low": "127.2500",
            "4. close": "128.9000",
            "5. volume": "24911126"
        }
    }
    }

    transformed_response = [
        {"timestamp": "2019-05-08", "open": "125.4400", "high": "126.3700", "low": "124.7500", "close": "125.5100", "volume": "21077406"},
        {"timestamp": "2019-05-07", "open": "126.4600", "high": "127.1800", "low": "124.2200", "close": "125.5200", "volume": "35167000"},
        {"timestamp": "2019-05-06", "open": "126.3900", "high": "128.5600", "low": "126.1100", "close": "128.1500", "volume": "24239464"},
        {"timestamp": "2019-05-03", "open": "127.3600", "high": "129.4300", "low": "127.2500", "close": "128.9000", "volume": "24911126"}
    ]

    assert transform_response(parsed_response_example) == transformed_response

