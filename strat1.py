from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import pandas_datareader.data as web
import datetime
import plotly.offline.graph_objs as go
import plotly.offline.plotly as py

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2017, 1, 1)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
apple = web.DataReader("AAPL", "google", start, end)

df = apple

trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
py.iplot(data, filename='simple_candlestick')