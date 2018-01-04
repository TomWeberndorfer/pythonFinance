import pytz
from datetime import datetime
from zipline.api import order, symbol, record, order_target
from zipline.algorithm import TradingAlgorithm

import pandas as pd
# Load data manually from Yahoo! finance
filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'

# volume below 15k
file = filepath + 'avg_below.csv'
data = pd.read_csv(file)


def initialize(context):
    #context.security = symbol('AAPL')
    context.security = data

def handle_data(context, data):
    MA1 = data[context.security].mavg(50)
    MA2 = data[context.security].mavg(100)
    date = str(data[context.security].datetime)[:10]
    current_price = data[context.security].price
    current_positions = context.portfolio.positions[symbol('SPY')].amount
    cash = context.portfolio.cash
    value = context.portfolio.portfolio_value
    current_pnl = context.portfolio.pnl

    #code (this will come under handle_data function only)
    if (MA1 > MA2) and current_positions == 0:
        number_of_shares = int(cash/current_price)
        order(context.security, number_of_shares)
        record(date=date,MA1 = MA1, MA2 = MA2, Price=
        current_price,status="buy",shares=number_of_shares,PnL=current_pnl,cash=cash,value=value)

    elif (MA1 < MA2) and current_positions != 0:
        order_target(context.security, 0)
        record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="sell",shares="--",PnL=current_pnl,cash=cash,value=value)

    else:
        record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="--",shares="--",PnL=current_pnl,cash=cash,value=value)


algo_obj = TradingAlgorithm(initialize=initialize,handle_data=handle_data)
perf_manual = algo_obj.run(data)
perf_manual[["MA1","MA2","Price"]].plot()
