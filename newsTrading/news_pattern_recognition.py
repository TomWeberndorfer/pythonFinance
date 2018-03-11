import time
from datetime import datetime

from Utils.common_utils import format_news_analysis_results, send_stock_email
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.TextBlobAnalyseNews import TextBlobAnalyseNews

filepath = 'C:\\temp\\'
##########################
text_analysis = TextBlobAnalyseNews()

while True:
    # ++++++++++ FOR SAMPLE NEWS
    # data = pd.read_csv(filepath + "Sample_news.txt")
    # all_news = data.News.tolist()

    # ++++++++++ FOR REAL NEWS
    # hash_file = "C:\\temp\\news_hashes.txt"
    thr_start = datetime.now()
    all_news = read_news_from_traderfox()
    results = text_analysis.analyse_all_news(all_news)
    res_str = format_news_analysis_results(results)

    if res_str is not None and len(res_str) > 0:
        print(res_str)
        send_stock_email(res_str, "News Trading: New news available")
    else:
        print("News analysis: no news")

    time.sleep(20)  # check for new news after x seconds
    print("Runtime check: " + str(datetime.now() - thr_start))
