import plotly.graph_objects as gr_obj
import ccxt
import pandas as pd
from datetime import datetime


# connect an exchange
exchange = ccxt.binance()

names = ['USDT/TRY', 'BTC/USDT', 'ETH/USDT']
# the timeframe for the data (1 day candlesticks)
timeframe = '1d'

td = datetime.now()
today = td.strftime("%Y-%m-%d")
start = td.replace(year=td.year-1).strftime("%Y-%m-%d")
since = int(datetime.strptime(start, '%Y-%m-%d').timestamp() * 1000)


def get_data(name):

    # retrieve the data from the last two months
    data = exchange.fetch_ohlcv(symbol=name, timeframe=timeframe, since=since)

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # convert the timestamp column to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # each row of the DataFrame is identified by its timestamp
    df.set_index('timestamp', inplace=True)

    return df


def main():
    graph = gr_obj.Figure()

    for name in names:
        crypto = get_data(name)

        graph.add_trace(gr_obj.Candlestick(x=crypto.index,
                                           open=crypto.open,
                                           close=crypto.close,
                                           high=crypto.high,
                                           low=crypto.low,
                                           name=name))

    graph.update_layout(title='Cryptocurrency Prices')
    graph.show()


if __name__ == '__main__':
    main()

