import requests
from os import path, mkdir

exchanges = [
    'binance',
    'coinbase'
]

quoted_assets = [
    'usd',
    'usdt'
]

market_type = 'spot'

begin_timestamp = '2022-03-04'
end_timestamp = '2022-03-05'


def create_folders(data, exchange, market):
    for trades in trades_data['data']:
        if path.isdir(exchange):
            if path.isdir(f'{exchange}/{market}'):
                pass
            else:
                mkdir(path.join(exchange, market))
        else:
            mkdir(exchange)
            mkdir(path.join(exchange, market))

        csv_path = f'{exchange}/{market}/{begin_timestamp}.csv'
        csv_column = (','.join(list(trades.keys())))
        csv_data = (','.join(list(trades.values())))

        collect_data(csv_path, csv_column, csv_data)


def collect_data(csv_path, column, data):
    if path.exists(csv_path):
        with open(csv_path, 'r+') as csv_file:
            if data not in csv_file:
                csv_file.write(f'{data}\n')
    else:
        with open(csv_path, 'w') as csv_file:
            csv_file.write(f'{column}\n')
            csv_file.write(f'{data}\n')


for exchange in exchanges:
    for quote in quoted_assets:
        specific_markets = requests.get(
            f'https://community-api.coinmetrics.io/v4/catalog-all/markets?&exchange={exchange}&quote={quote}&type={market_type}&include=trades').json()
        if specific_markets['data']:
            for markets in specific_markets['data']:
                market = markets['market']
                trades_data = requests.get(
                    f'https://community-api.coinmetrics.io/v4/timeseries/market-trades?&markets={market}&page_size=1&pretty=true&start_time={begin_timestamp}&end_time={end_timestamp}').json()
                if trades_data['data']:
                    data = trades_data['data']
                    print(f'Collecting data for: {market}')
                    create_folders(data, exchange, market)
                next_page = 1
                while 'next_page_url' in trades_data:
                    next_page_url = requests.get(
                        trades_data['next_page_url']).json()
                    next_page_of_data = next_page_url['data']
                    next_page += 1
                    print(f'Page {next_page}: {market}')
                    create_folders(next_page_of_data, exchange, market)
                    trades_data = next_page_url

print('\nIteration complete')
