from datetime import datetime
from datetime import timedelta

from matplotlib import style

style.use('ggplot')

from DataRead_Google_Yahoo import read_data_from_google_with_pandas

from Utils import plot_stock_as_candlechart_with_volume

end = datetime.now()
ago52_w = (end - timedelta(weeks=52))
df = read_data_from_google_with_pandas("ADBE", ago52_w, end) # 2017-09-21
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

plot_stock_as_candlechart_with_volume("AAPL", df)