# "Robo Advisor" Project - Starter Repository

A starter repository for the ["Robo Advisor" project](https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/projects/robo-advisor.md).

Issues requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/) in order to provide automated stock or cryptocurrency trading recommendations.

The basic purpose of this program is to track basic stock information at user-designated intervals. The user can get access to highs, lows, closes, etc. for the stocks of their choice. They can also write to a CSV all this relevant information for a number of days.

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Installation

Fork this [final repository](https://github.com/ryanbeaudet/robo-advisor-project) under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line:

```sh
cd robo-advisor-starter-py
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env". From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

## Setup

Before using or developing this application, take a moment to [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123").

After obtaining an API Key, copy the ".env.example" file to a new file called ".env", and update the contents of the ".env" file to specify your real API Key.

Don't worry, the ".env" has already been [ignored](/.gitignore) from version control for you!

## Usage

Run the recommendation script:

```py
python app/robo_advisor.py
```

The rest of the process is fairly simple. Just enter in the name of the stock for which you would like information, and then summary data will be printed and comprehensive data will be written to a CSV file.

## Testing

```
pytest
```

## [License](/LICENSE.md)
