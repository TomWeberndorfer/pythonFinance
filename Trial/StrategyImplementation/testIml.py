from unittest import TestCase

from pandas import DataFrame

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import GlobalVariables


class TestImpl(TestCase):

    def test_(self):
        parameter_dict = {'sma_timeperiod': 5, 'ema_timeperiod': 5, 'roc_timeperiod': 5,
                          'data_readers': {'HistoricalDataReader': {
                              'weeks_delta': 52, 'data_source': 'iex', 'reload_data': False, 'ticker_needed': True}}}

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        ##################################################
        # 52 w strategy
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare("StrategyAsta_SMA_and__EMA_or_RoC",
                                              stock_data_container_list=stock_data_container_list,
                                              analysis_parameters=parameter_dict)

        results = w52_hi_strat.run_strategy()
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].get_stock_name(), stock_data_container.get_stock_name())
