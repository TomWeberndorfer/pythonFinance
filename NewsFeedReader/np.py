from newspaper import Article

#url = 'http://finance.yahoo.com/q/h?s=msft'
#url = "https://www.investors.com/etfs-and-funds/etfs/apple-microsoft-amazon-lead-top-growth-stock-play-in-buy-range/?src=A00220&yptr=yahoo"
#url = "https://www.investors.com/etfs-and-funds/etfs/apple-microsoft-amazon-lead-top-growth-stock-play-in-buy-range/?src=A00220&yptr=yahoo"
url = "https://blog.onemarkets.de/feed/"
article = Article(url)
article.download()

article.html
article.parse()

print (article.text)