#http://feeds.reuters.com/reuters/companyNews

import feedparser
from datetime import datetime, date

feed = feedparser.parse("http://finance.yahoo.com/rss/headline?s=msft")
#feed = feedparser.parse("http://finance.yahoo.com/q/h?s=msft")
#feed = feedparser.parse("http://feeds.reuters.com/reuters/companyNews")

feed_title = feed['feed']['title']
feed_entries = feed.entries

for entry in feed.entries:

    article_published_at = entry.published  # Unicode string
    if article_published_at < datetime.today().date(): TODO
        article_title = entry.title
        article_link = entry.link
        description = entry.description


        article_published_at_parsed = entry.published_parsed # Time object
        #article_author = entry.author
        #print ("{} [{}], Published at {}".format(article_title, article_link, article_published_at))
        print (article_published_at + ": " + article_title + ": " + description + ": " + article_link)
        #print ("Published by {}".format(article_author))