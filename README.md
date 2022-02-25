
# Trades Exporter

This Python script is designed to export trades data into CSV format. It will single out usd and usdt quoted spot markets from Coinbase and Binance, then create
a directory for each exchange. Each CSV file created will represent data for a specific market with a specific date.

## Requirements
####
You will need to install `requests` before you can send a request to the API.
```https://pypi.org/project/requests/
pip install requests
```

Run the script in your console with:
```
python3 trades_exporter.py
```

## API Reference
#### Returns trades for specified markets.

```https://community-api.coinmetrics.io/v4/timeseries/market-trades?start_time=2020-01-01&paging_from=start&markets=coinbase-btc-usd-spot&pretty=true
GET /timeseries/market-trades
```
# How To

The `markets` query parameter is set to only select the usd and usdt quoted spot markets from Binance and Coinbase. To collect trades data from different spot markets, here are various patterns you can use:
```
exchange-base-quote-spot
exchange-*-quote-spot
exchange-*-spot
exchange-*
```
#
To change the date range in the `start_time` and `end_time` query parameters, it is in this format:
```
2022-02-21T00:00:00Z
YYYY-MM-DDTHH:MM:SSZ
```
 By default, these time parameters are going off of the UTC timezone. You can change that by appending the `timezone` parameter. For example, if you live in New York, you can add:
 ```
timezone=America/New_York
 ```
 Here's a list of <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">other timezones</a> using the same format.
#
The `iterate_through_data(response)` function takes in an argument of the variable assigned to the trades data. That data will be used to create your exchange and market directories based off of the conditions you gave it in the `markets` query parameter. Once the proper folders are created, the next function will then be invoked. Lastly, it will check to see if the JSON object has a key of `'next_page_url'`. If so, the next pages will also be iterated through until there is no more trades data to collect. A counter has been added that will increment with each additional page so you can keep track in your console while the script is running.
#
In the `convert_to_CSV(data)` function, all the necessary variables have been created to successfully convert the data into CSV format. The last thing it will do is check to see if a CSV file exists for a specific market on a specific date. If not, it will create the file. If you want to reorganize the columns, just be sure to change both the `csv_columns` and `csv_data` variables in their respective order.
```
csv_columns = "Market, Time, Coin Metrics ID, Amount, Price, Database Time, Side\n"

csv_data = f"{market}, {time}, {coin_metrics_id}, {amount}, {price}, {database_time}, {side}\n"
```
#
## Important Notes
1. Make sure the `\n` stays intact at the end of the variables shown above.

2. Be sure not to change the `"r+"` and `"w"` in the `convert_to_CSV(data)` function inside of the open methods:
```
with open(csv_path, "r+") as csv_file:

with open(csv_path, "w") as csv_file:
```

3. If you manipulate the query parameters, accidentally break something and can't undo it, here's the original:
```
https://community-api.coinmetrics.io/v4/timeseries/market-trades?&markets=coinbase-*-usd-spot,coinbase-*-usdt-spot,binance-*-usd-spot,binance-*-usdt-spot&page_size=500&pretty=true&start_time=2022-02-21T00:00:00Z&end_time=2022-02-21T00:00:05Z
```
