import threading

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import datetime
import pandas as pd

#####################################################
from MyThread import MyThread
from Utils.common_utils import split_list
from Utils.file_utils import read_tickers_from_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.TextBlobAnalyseNews import TextBlobAnalyseNews

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
stocks_to_buy = []


##########################

# TODO maybe move to better place
def function_for_threading_news_analysis(news_to_check):
    print("Started with: " + str(news_to_check))

    for news in news_to_check:
        res_analysis = analysis.analyse_single_news(news)

        if res_analysis != " ":
            stocks_to_buy.append(res_analysis)


hash_file = "C:\\temp\\news_hashes.txt"
num_of_news_per_thread = 5

all_news = read_news_from_traderfox(hash_file)

if all_news != "" and len(all_news) > 1:
    res = read_tickers_from_file(tickers_file, stocknames_file)
    analysis = TextBlobAnalyseNews(res['names'], res['tickers'])

    news_screening_threads = MyThread("news_screening_threads")
    splits = split_list(all_news, num_of_news_per_thread)

    i = 0
    while i < len(splits):
        news_to_check = splits[i]
        news_screening_threads.append_thread(
            threading.Thread(target=function_for_threading_news_analysis,
                             kwargs={'news_to_check': news_to_check}))
        i += 1

    news_screening_threads.execute_threads()

    print("\n-------------------------\n")

if len(stocks_to_buy) == 0:
    print("No news")
else:
    for res in stocks_to_buy:
        if res != " ":
            print("pos: " + str(round(res['prob_dist'].prob("pos"), 2)) + " ,neg: " + str(
                round(res['prob_dist'].prob("neg"), 2)) + " " + str(res))
