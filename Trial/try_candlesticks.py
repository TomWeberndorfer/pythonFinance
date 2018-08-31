from datetime import datetime
from datetime import timedelta

from matplotlib import style
from plotly import graph_objs as go, plotly as py

from Utils.GlobalVariables import GlobalVariables

style.use('ggplot')

end = datetime.now()
ago52_w = (end - timedelta(weeks=52))


# df = read_data_from_google_with_pandas("ADBE", ago52_w, end) # 2017-09-21
# df_ohlc = df['Close'].resample('10D').ohlc()
# df_volume = df['Volume'].resample('10D').sum()
#
# df_ohlc.reset_index(inplace=True)
# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
#
# ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
# ax1.xaxis_date()
#
# candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
# ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
# plt.show()

def plot_stock_as_candlechart_with_volume(stock_name, stock_data):
    """
    print the given stock data as candlestick OHLC chart + volume
    :param stock_name: name of the stock (for title to print)
    :param stock_data: data to print, from google or yahoo
    :return: nothing
    """
    # py.plotly.tools.set_credentials_file(username='webc', api_key='bWWpIIZ51DsGeqBXNb15')

    trace = go.Candlestick(x=stock_data.index,
                           open=stock_data[GlobalVariables.get_stock_data_labels_dict()['Open']],
                           high=stock_data[GlobalVariables.get_stock_data_labels_dict()['High']],
                           low=stock_data[GlobalVariables.get_stock_data_labels_dict()['Low']],
                           close=stock_data[GlobalVariables.get_stock_data_labels_dict()['Close']])
    data = [trace]
    py.plot(data, filename=stock_name)
    return

#plot_stock_as_candlechart_with_volume("AAPL", df)
