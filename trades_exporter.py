import requests
from os import path, mkdir

req = requests.get(
    'https://community-api.coinmetrics.io/v4/timeseries/market-trades?&markets=coinbase-*-usd-spot,coinbase-*-usdt-spot,binance-*-usd-spot,binance-*-usdt-spot&page_size=500&pretty=true&start_time=2022-02-21T00:00:00Z&end_time=2022-02-21T00:00:05Z').json()


def iterate_through_data(response):

    trades_data = response['data']

    for data in trades_data:
        market = data['market']
        exchange = data['market'].split('-')[0]
        if path.isdir(exchange):
            # in case an exchange directory is manually created
            if path.isdir(f"{exchange}/{market}"):
                convert_to_CSV(data)
            else:
                mkdir(path.join(exchange, market))
                convert_to_CSV(data)
        else:
            mkdir(exchange)
            mkdir(path.join(exchange, market))
            convert_to_CSV(data)

    if 'next_page_url' in response:
        global page_num
        page_num += 1
        next_page_url = requests.get(response['next_page_url']).json()
        print(f"Moving to page {page_num}")
        iterate_through_data(next_page_url)


def convert_to_CSV(data):

    market = data['market']
    exchange = data['market'].split('-')[0]
    time = data['time']
    coin_metrics_id = data['coin_metrics_id']
    amount = data['amount']
    price = data['price']
    database_time = data['database_time']
    side = data['side']

    csv_filename = time.split(":")[0][:10]
    csv_path = f"{exchange}/{market}/{csv_filename}.csv"
    csv_columns = "Market, Time, Coin Metrics ID, Amount, Price, Database Time, Side\n"
    csv_data = f"{market}, {time}, {coin_metrics_id}, {amount}, {price}, {database_time}, {side}\n"

    if path.exists(csv_path):
        with open(csv_path, "r+") as csv_file:
            if csv_data not in csv_file:
                csv_file.write(csv_data)
                csv_file.close()
    else:
        with open(csv_path, "w") as csv_file:
            csv_file.write(csv_columns)
            csv_file.write(csv_data)
            csv_file.close()


page_num = 1
iterate_through_data(req)

print("Iteration complete")
