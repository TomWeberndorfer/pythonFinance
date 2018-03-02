import feedparser
rsslist=["http://finance.yahoo.com/rss/headline?s=msft"]

def feed_modified_date(feed):
    # this is the last-modified value in the response header
    # do not confuse this with the time that is in each feed as the server
    # may be using a different timezone for last-resposne headers than it
    # uses for the publish date

    modified = feed.get('modified')
    if modified is not None:
        return modified

    return None

def max_entry_date(feed):
    entry_pub_dates = (e.get('published_parsed') for e in feed.entries)
    entry_pub_dates = tuple(e for e in entry_pub_dates if e is not None)

    if len(entry_pub_dates) > 0:
        return max(entry_pub_dates)

    return None

def entries_with_dates_after(feed, date):
    response = []

    for entry in feed.entries:
        if entry.get('published_parsed') > date:
            response.append(entry)

    return response

for feed_url in rsslist:
    print('--------%s-------' % feed_url)
    d = feedparser.parse(feed_url)
    print('feed length %i' % len(d.entries))

    if len(d.entries) > 0:
        etag = d.feed.get('etag', None)
        modified = feed_modified_date(d)
        print('modified at %s' % modified)

        d2 = feedparser.parse(feed_url, etag=etag, modified=modified)
        print('second feed length %i' % len(d2.entries))
        if len(d2.entries) > 0:
            print("server does not support etags or there are new entries")
            # perhaps the server does not support etags or last-modified
            # filter entries ourself

            prev_max_date = max_entry_date(d)

            entries = entries_with_dates_after(d2, prev_max_date)

            print('%i new entries' % len(entries))
        else:
            print('there are no entries')