#import ccxt.async_support as ccxt
import ccxt
import pprint
# print a list of all available exchange classes
pprint.pprint(ccxt.exchanges)

# exchange = ccxt.okcoin () # default id
# okcoin1 = ccxt.okcoin({ 'id': 'okcoin1' })
# okcoin2 = ccxt.okcoin({ 'id': 'okcoin2' })
# id = 'binanceus'
# binanceus = eval ('ccxt.%s ()' % id)
# coinbasepro = getattr (ccxt, 'coinbasepro') ()

# #pprint.pprint(dir(coinbasepro))

# # from variable id
# binance_exchange = ccxt.binance({
#     'timeout': 15000,
# })
# print("---------------------------------------------")

# # 交易所数据结构
# print('交易所id：', binance_exchange.id)
# print('交易所名称：', binance_exchange.name)
# print('是否支持共有API：', binance_exchange.has['publicAPI'])
# print('是否支持私有API：', binance_exchange.has['privateAPI'])
# print('支持的时间频率：', binance_exchange.timeframes)
# print('最长等待时间(s)：', binance_exchange.timeout / 1000)
# print('访问频率(s)：', binance_exchange.rateLimit / 1000)
# # print('交易所当前时间：', binance_exchange.iso8601(binance_exchange.milliseconds()))

# #列出所有交易對數據
# binance_exchange_markets = binance_exchange.load_markets()
# #pprint.pprint(binance_exchange_markets)

# #列出所有交易對名稱
# pairs_name = binance_exchange_markets.keys()
# pprint.pprint(pairs_name)

# pairs = 'BTC/USDT'
# btc_to_usdt = binance_exchange_markets[pairs]
# pprint.pprint(btc_to_usdt)

# print("---------------------------------------------")
# btc_to_usdt_ticker = binance_exchange.fetchTicker(pairs)
# pprint.pprint(btc_to_usdt_ticker)
# print("---------------------------------------------")

# #pprint.pprint(dir(exchange))

