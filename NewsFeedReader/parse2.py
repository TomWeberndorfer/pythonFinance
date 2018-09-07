import feedparser


# Function to fetch the rss feed and return the parsed RSS
def parse_RSS(rss_url):
    return feedparser.parse(rss_url)


# Function grabs the rss feed headlines (titles) and returns them as a list
def get_headlines(rss_url):
    headlines = []
    feed = parse_RSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])

    return headlines


# A list to hold all headlines
allheadlines = []

# List of RSS feeds that we will fetch and combine
newsurls = {
    #'apnews': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305',
    #'googlenews': 'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=US',
    #'yahoonews': 'http://news.yahoo.com/rss/'
    #'yahooFinance': 'http://finance.yahoo.com/rss/headline?s=msft'
    'boerse-online': 'http://www.boerse-online.de/rss'

}

# Iterate over the feed urls
for key, url in newsurls.items():
    # Call get_headlines() and combine the returned headlines with allheadlines
    allheadlines.extend(get_headlines(url))

# Iterate over the allheadlines list and print each headline
for hl in allheadlines:
    print(hl)


    # end of code