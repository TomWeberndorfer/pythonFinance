import unittest
from pandas import DataFrame

from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestSimplePatternNewsStrategy(unittest.TestCase):

    def test_run_strategy(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000),
                ('2016-09-14', 90, 90, 22.95, 100.11, 4000),
                ('2016-09-15', 90, 90, 100.14, 100.62, 4000)]

        df = DataFrame.from_records(data, columns=labels)

        aapl = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", "en"), 0, 0,
                                          "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf", 0)
        rwe = NewsDataContainerDecorator(StockDataContainer("RWE AG ST O.N.", "RWE", ""), 0, 0,
                                         "ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf", 0)
        aapl.set_historical_stock_data(df)
        rwe.set_historical_stock_data(df)

        rwe_stock_data_container = StockDataContainer("RWE AG ST O.N.", "RWE", "")
        rwe_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [aapl, rwe]

        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy",
                                                        stock_data_container_list, parameter_dict)

        results = news_strategy.run_strategy()

        self.assertEqual(results[0] in stock_data_container_list, True)
        apple_idx = results.index(aapl)
        rwe_idx = results.index(rwe)

        t1 = round(results[apple_idx].positive_prob_dist(), 2)
        self.assertEqual(results[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertGreater(0.7, t1)

        t1 = round(results[rwe_idx].positive_prob_dist(), 2)
        self.assertEqual(results[rwe_idx].get_stock_name(), "RWE AG ST O.N.")
        self.assertGreater(t1, 0.7)

    def test_run_strategy_with_two_news_for_one_stock(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000),
                ('2016-09-14', 90, 90, 22.95, 100.11, 4000),
                ('2016-09-15', 90, 90, 100.14, 100.62, 4000)]

        df = DataFrame.from_records(data, columns=labels)

        apple_stock_data_container = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                                "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf",
                                                                0)
        apple_stock_data_container2 = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                                 "ANALYSE-FLASH: Sparkasse nimmt Apple mit Buy wieder auf",
                                                                 0)

        apple_stock_data_container.set_historical_stock_data(df)
        apple_stock_data_container2.set_historical_stock_data(df)
        rwe_stock_data_container = NewsDataContainerDecorator(StockDataContainer("RWE AG ST O.N.", "RWE", ""), 0, 0,
                                                              "ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf",
                                                              0)
        rwe_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, rwe_stock_data_container]

        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy",
                                                        stock_data_container_list, parameter_dict)

        results = news_strategy.run_strategy()

        self.assertEqual(results[0] in stock_data_container_list, True)
        apple_idx = results.index(apple_stock_data_container)
        rwe_idx = results.index(rwe_stock_data_container)

        t1 = round(results[apple_idx].positive_prob_dist(), 2)
        self.assertEqual(results[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertGreater(0.7, t1)

        t1 = round(results[rwe_idx].positive_prob_dist(), 2)
        self.assertEqual(results[rwe_idx].get_stock_name(), "RWE AG ST O.N.")
        self.assertGreater(t1, 0.7)
