from Trial.s_and_p_list_from_wiki import get_data_from_google_with_webreader

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'

stock52_w = get_data_from_google_with_webreader ('AAPL',  filepath + 'stock_dfs', False, False)
stock52_w