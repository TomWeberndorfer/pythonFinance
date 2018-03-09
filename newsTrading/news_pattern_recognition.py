import datetime
import pandas as pd
from Utils.common_utils import print_news_analysis_results
from newsTrading.TextBlobAnalyseNews import TextBlobAnalyseNews

filepath = 'C:\\temp\\'
##########################

#++++++++++ FOR SAMPLE NEWS
thr_start = datetime.datetime.now()
data = pd.read_csv(filepath + "Sample_news.txt")
all_news = data.News.tolist()

#++++++++++ FOR REAL NEWS
#hash_file = "C:\\temp\\news_hashes.txt"
#all_news = read_news_from_traderfox(hash_file)

text_analysis = TextBlobAnalyseNews()
results = text_analysis.analyse_all_news(all_news)
print_news_analysis_results (results)
