#http://feeds.reuters.com/reuters/companyNews

import feedparser

from Utils.NewsUtils import NewsUtils

lastId = 0 #TODO temp solution
#TODO alternativ mit etag nud modified wann des geht

url = "http://finance.yahoo.com/rss/headline?s=msft"
url = "https://www.boersen-zeitung.de/xml_base/rss.php?dpasubm=unt"
url = "https://blog.onemarkets.de/feed/"

feed = feedparser.parse(url)
#feed = feedparser.parse("http://finance.yahoo.com/q/h?s=msft")
#feed = feedparser.parse("http://feeds.reuters.com/reuters/companyNews")

id = NewsUtils.generate_hash(url, feed.entries)

# 304 means no changes
if lastId == id:
    print ("no news")

else:

    print ("ID: " + str(id))
    feed_title = feed['feed']['title']
    feed_entries = feed.entries

    for entry in feed.entries:

        article_published_at = entry.published  # Unicode string
        from dateutil import parser

        #dt = parser.parse("Aug 28 1999 12:00AM")
        dt = parser.parse(article_published_at)
        #Thu, 22 Feb 2018 21:27:28 +0000:

        article_title = entry.title
        article_link = entry.link
        description = entry.description


        article_published_at_parsed = entry.published_parsed # Time object
        #article_author = entry.author
        #print ("{} [{}], Published at {}".format(article_title, article_link, article_published_at))
        print(article_published_at + ": " + article_title)
        #print (article_published_at + ": " + article_title + ": " + description + ": " + article_link)
        #print ("Published by {}".format(article_author))