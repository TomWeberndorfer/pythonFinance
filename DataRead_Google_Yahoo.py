import json

# TODO from yahoo_finance import Share
import googlefinance.client as google_client
import urllib3

str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
str2 = "&region=1&lang="
str3 = "&callback=YAHOO.Finance.SymbolSuggest.ssCallback"


def read_data_from_google_with_client(stock_name, interval="86400", period="1M"):
    if stock_name is None:
        raise NotImplementedError

    param = {
        'q': stock_name,  # Stock symbol (ex: "AAPL")
        'i': interval,  # Interval size in seconds ("86400" = 1 day intervals)
        # 'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': period  # Period (Ex: "1Y" = 1 year)
    }
    # get price data (return pandas dataframe)
    df = google_client.get_price_data(param)
    return df

def get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks(name_abbr):
    """
    TODO
    name: name to convert
    :param name_abbr:
    :param name:
    :return:
    """
    if name_abbr is None:
        raise NotImplementedError

    names_to_get = [optimize_name_for_yahoo(name_abbr), optimize_name_for_yahoo(name_abbr, False),
                    optimize_name_for_yahoo(name_abbr, False, True)]

    for name in names_to_get:

        try:

            http = urllib3.PoolManager()
            # query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
            # ex: 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=BMW+AG&region=1&lang=de&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
            req = str1 + name + str2 + str3
            r = http.request('GET', req)  # build url

            result = r.data.decode('utf-8')
            result = result.replace(")", "")
            result = result.replace(";", "")
            # TODO 3: find a better solution to convert to json instead
            result  = result.replace("YAHOO.Finance.SymbolSuggest.ssCallback(", "")
            result = result.strip("'<>() ").replace('\'', '\"')
            json_struct = json.loads(result)
            result_set = json_struct['ResultSet']['Result']

            # gets the first result in the result set
            if len(result_set) > 0:
                first_stock = result_set[0]
                found_name = first_stock['name']
                found_symbol = first_stock['symbol']
                if "." in found_symbol:
                    found_symbol = found_symbol.split(".")[0]
                return found_name, found_symbol

        except Exception as e:
            continue

        raise Exception("Exception: no symbol found for " + str(name_abbr))


def optimize_name_for_yahoo(name, replace_whitespace=True, return_first_part=False):
    if name is None:
        raise NotImplementedError

    name = name.upper()
    if replace_whitespace:
        name = name.replace(" ", "+")
    name = name.replace(".", "")
    name = name.replace("\n", "")
    name = name.replace("Ü", "UE")
    name = name.replace("Ö", "OE")
    name = name.replace("Ä", "AE")

    if "ETR:" in name:
        name = name.replace("ETR:", "")
        name += ".DE"
    name = name.replace("FRA:", "")
    name = name.split("INC")[0]
    name = name.replace("^", "")
    if replace_whitespace:
        name_spl = name.split("+")
    else:
        name_spl = name.split(" ")

    if len(name_spl) > 2:
        name = name_spl[0] + "+" + name_spl[1]

    if return_first_part:
        name = name_spl[0]
    return name

