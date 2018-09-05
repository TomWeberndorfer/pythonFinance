import unittest
from pandas import DataFrame
from datetime import datetime, timedelta
from dateutil import parser
from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestDataContainerDecorator(unittest.TestCase):
    def test_NewsDataContainerDecorator_get_names_and_values__target_price_111__stockname_test1(self):
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.assertEqual(10, len(result_container))

        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        result_news_dec = news_dec.get_names_and_values()
        self.assertEqual(13, len(result_news_dec))
        self.assertEqual({}, result_news_dec["StrategyAndRecommendation"])
        self.assertEqual(111, result_news_dec["Target Price"])
        self.assertEqual("test1", result_news_dec["Stockname"])
        self.assertEqual(0.9, result_news_dec["Pos. Probability Distribution"])

    def test_NewsDataContainerDecorator_update_used_strategy_and_recommendation(self):
        container = StockDataContainer("test1", "t1", "en")
        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        res_dict = news_dec.get_recommendation_strategies()
        self.assertEqual(1, len(res_dict))

        rec_and_datetime = res_dict["TestStrategy"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("BUY", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.1), elapsed)

        news_dec.update_used_strategy_and_recommendation("TestStrategy_2", "SELL")

        res_dict = news_dec.get_recommendation_strategies()
        self.assertEqual(2, len(res_dict))

        rec_and_datetime = res_dict["TestStrategy"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("BUY", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)

        rec_and_datetime = res_dict["TestStrategy_2"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("SELL", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)

    def test_NewsDataContainerDecorator_test_rank(self):
        container = StockDataContainer("test1", "t1", "en")
        pos_prob_dist = 0
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "SELL")
        self.assertEqual(-3, news_dec.get_rank())

        pos_prob_dist = 0.49
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(0, news_dec.get_rank())

        pos_prob_dist = 0.51
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(2, news_dec.get_rank())

        pos_prob_dist = 0.76
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(3, news_dec.get_rank())

        pos_prob_dist = 1
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(3, news_dec.get_rank())

        pos_prob_dist = 1
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "SELL")
        self.assertEqual(1, news_dec.get_rank())

    def test_NewsDataContainerDecorator_set_stop_buy(self):
        container = StockDataContainer("test1", "t1", "en")
        container.set_stop_buy(10)
        self.assertEqual(10, container.get_stop_buy())
        news_dec = NewsDataContainerDecorator(container, 111, 1, "test news", 99)
        news_dec.set_stop_buy(20)
        self.assertEqual(20, news_dec.get_stop_buy())

    def test_NewsDataContainerDecorator_set_stop_loss(self):
        container = StockDataContainer("test1", "t1", "en")
        container.set_stop_loss(10)
        self.assertEqual(10, container.get_stop_loss())
        news_dec = NewsDataContainerDecorator(container, 111, 1, "test news", 99)
        news_dec.set_stop_loss(20)
        self.assertEqual(20, news_dec.get_stop_loss())

    def test_NewsDataContainerDecorator_set_position_size(self):
        container = StockDataContainer("test1", "t1", "en")
        container.set_position_size(100)
        self.assertEqual(100, container.get_position_size())
        news_dec = NewsDataContainerDecorator(container, 111, 1, "test news", 99)
        news_dec.set_position_size(20)
        self.assertEqual(20, news_dec.get_position_size())

    def test_NewsDataContainerDecorator_set_historical_stock_data(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000)]

        df = DataFrame.from_records(data, columns=labels)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)

        sd = apple_stock_data_container.historical_stock_data()

        for col in range(0, len(data[0])):
            cur_val = sd[sd.keys()[col]][0]
            des_val = data[0][col]
            self.assertEqual(des_val, cur_val)

        news_dec = NewsDataContainerDecorator(apple_stock_data_container, 111, 1, "test news", 99)

        data_2 = [('2017-11-11', 11, 22, 33, 44, 55)]
        df_2 = DataFrame.from_records(data_2, columns=labels)
        news_dec.set_historical_stock_data(df_2)

        sd = news_dec.historical_stock_data()

        for col in range(0, len(data_2[0])):
            cur_val = sd[sd.keys()[col]][0]
            des_val = data_2[0][col]
            self.assertEqual(des_val, cur_val)
