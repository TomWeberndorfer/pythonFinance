
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import datetime
import pandas as pd

#####################################################
from Utils.file_utils import read_tickers_from_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.TextBlobAnalyseNews import TextBlobAnalyseNews

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
##########################


all_news = []
hash_file = "C:\\temp\\news_hashes.txt"

res_news = read_news_from_traderfox(hash_file)

if res_news != "" and len(res_news) > 1: #TODO länge checken
    all_news = res_news

    thr_start = datetime.datetime.now()
    res = read_tickers_from_file(tickers_file, stocknames_file)

    txt = "\n\nRuntime : " + str(datetime.datetime.now() - thr_start)
    print(txt)

    results = []
    analysis = TextBlobAnalyseNews(res['names'], res['tickers'])

    for news in all_news:
        r = analysis.analyse_single_news(news)
        results.append(r)

    print("\n-------------------------\n")
    for res in results:
        if res != " ":
            print("pos: " + str(round(res['prob_dist'].prob("pos"), 2)) + " ,neg: " + str(
                round(res['prob_dist'].prob("neg"), 2)) + " " + str(res))

