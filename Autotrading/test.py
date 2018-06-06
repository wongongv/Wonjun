from hitbtc import *
from client import *
from bittrexarb import *

hitbtc_public_key = "e2f71ee3f6550a9f9af1b8ab215ea4d1"
binance_public_key = "mPBvNGYhZZauYftQbAQsgFQQF3gK7a8YcY1xb7y70K4C5NKpZSPjZOkiVeHcmU0t" 
bittrex= Bittrex(api_key="aa227a3b7083448d85a611dda8b60a45", api_secret="18351cba6f6348d1b029ff36c6eafc13")
client = Client("https://api.hitbtc.com", hitbtc_public_key, None)

bclient=bClient(binance_public_key,None)

hcash={}
bcash={}
bitcash={}
lis=[]

husdt_ask={}
husdt_bid={}
hbtc_ask={}
hbtc_bid={}
heth_ask={}
heth_bid={}
#hitbtc
# currencies=client.get_currency()
# cash={}
# for currency in currencies:
# 	if currency["payinEnabled"] and currency["payoutEnabled"] and currency["transferEnabled"]:
# 		cash[currency["fullName"]]=currency["id"]
print("htobin,bintoh , bittobin, bintobit, bittoh,htobit")
def htobin():	
	tickers=client.get_alltickers()

	for result in tickers:
		if eval(result["volume"]) > 1 and result["symbol"][-3:]=="BTC" and result["ask"]:
			hcash[result["symbol"]]=result["ask"]

	#binance
	
	btickers=bclient.get_orderbook_tickers()
	for result in btickers:
		if result["symbol"][-3:] == "BTC":
			bcash[result["symbol"]]=result["bidPrice"]

	for sym in hcash:
		if sym in bcash:
			per=(eval(bcash[sym])-eval(hcash[sym]))*100/min(eval(hcash[sym]),eval(bcash[sym]))
			lis.append((per,sym))
			# if per >0: 
			# 	print(per, sym, "     binance to hitbtc")
			# else :
			# 	print(per, sym, "     Hitbtc to binance")
	slis=sorted(lis)
	[print(i) for i in slis]
	print("- Hitbtc to binance")
	hcash.clear()
	bcash.clear()
	del lis[:]
	return

def bintoh():	
	tickers=client.get_alltickers()

	for result in tickers:
		if eval(result["volume"]) > 1 and result["symbol"][-3:]=="BTC" and result["bid"]:
			hcash[result["symbol"]]=result["bid"]

	#binance
	
	btickers=bclient.get_orderbook_tickers()
	for result in btickers:
		if result["symbol"][-3:] == "BTC":
			bcash[result["symbol"]]=result["askPrice"]

	for sym in hcash:
		if sym in bcash:
			per=(eval(hcash[sym])-eval(bcash[sym]))*100/min(eval(hcash[sym]),eval(bcash[sym]))
			lis.append((per,sym))
			# if per >0: 
			# 	print(per, sym, "     binance to hitbtc")
			# else :
			# 	print(per, sym, "     Hitbtc to binance")
	slis=sorted(lis)
	[print(i) for i in slis]
	hcash.clear()
	bcash.clear()
	del lis[:]
	return

def bintobit():
	#binance

	btickers=bclient.get_orderbook_tickers()
	for result in btickers:
		if result["symbol"][-3:] == "BTC":
			bcash[result["symbol"]]=result["askPrice"]

	#bittrex
	bittrex_tickers=bittrex.get_market_summaries()
	for result in bittrex_tickers["result"]:
		if result["Market"]["BaseCurrency"]=="BTC":
			bitcash[result["Market"]["MarketCurrency"]+result["Market"]["BaseCurrency"]]=result["Summary"]["Bid"]
	for sym in bcash:
		if sym in bitcash:
			per=((bitcash[sym])-eval(bcash[sym]))*100/min(eval(bcash[sym]),(bitcash[sym]))
			lis.append((per,sym))	

	slis=sorted(lis)
	[print(i) for i in slis]
	bitcash.clear()
	bcash.clear()
	del lis[:]
	return



def bittobin():
	#binance

	btickers=bclient.get_orderbook_tickers()
	for result in btickers:
		if result["symbol"][-3:] == "BTC":
			bcash[result["symbol"]]=result["bidPrice"]

	#bittrex
	bittrex_tickers=bittrex.get_market_summaries()
	for result in bittrex_tickers["result"]:
		if result["Market"]["BaseCurrency"]=="BTC":
			bitcash[result["Market"]["MarketCurrency"]+result["Market"]["BaseCurrency"]]=result["Summary"]["Ask"]
	for sym in bcash:
		if sym in bitcash:
			per=(eval(bcash[sym])-(bitcash[sym]))*100/min(eval(bcash[sym]),(bitcash[sym]))
			lis.append((per,sym))	
	slis=sorted(lis)
	[print(i) for i in slis]
	bitcash.clear()
	bcash.clear()
	del lis[:]
	return

def htobit():

	tickers=client.get_alltickers()

	for result in tickers:
		if eval(result["volume"]) > 1 and result["symbol"][-3:]=="BTC" and result["ask"]:
			hcash[result["symbol"]]=result["ask"]

	#bittrex
	bittrex_tickers=bittrex.get_market_summaries()
	for result in bittrex_tickers["result"]:
		if result["Market"]["BaseCurrency"]=="BTC":
			bitcash[result["Market"]["MarketCurrency"]+result["Market"]["BaseCurrency"]]=result["Summary"]["Bid"]
	for sym in hcash:
		if sym in bitcash:
			per=((bitcash[sym])-eval(hcash[sym]))*100/min(eval(hcash[sym]),(bitcash[sym]))
			lis.append((per,sym))	

	slis=sorted(lis)
	[print(i) for i in slis]
	hcash.clear()
	bitcash.clear()
	del lis[:]
	return


def bittoh():

	tickers=client.get_alltickers()

	for result in tickers:
		if eval(result["volume"]) > 1 and result["symbol"][-3:]=="BTC" and result["bid"]:
			hcash[result["symbol"]]=result["bid"]




	#bittrex
	bittrex_tickers=bittrex.get_market_summaries()
	for result in bittrex_tickers["result"]:
		if result["Market"]["BaseCurrency"]=="BTC":
			bitcash[result["Market"]["MarketCurrency"]+result["Market"]["BaseCurrency"]]=result["Summary"]["Ask"]
	for sym in hcash:
		if sym in bitcash:
			per=(eval(hcash[sym])-(bitcash[sym]))*100/min(eval(hcash[sym]),(bitcash[sym]))
			lis.append((per,sym))	
	slis=sorted(lis)
	[print(i) for i in slis]
	hcash.clear()
	bitcash.clear()
	del lis[:]
	return

def harb():
	btoe=[]
	btou=[]
	etob=[]
	etou=[]
	utob=[]
	utoe=[]
	tickers=client.get_alltickers()



	for result in tickers:
		if eval(result["volume"]) > 1 and result["symbol"] != "ETHBTC" and result["symbol"][-3:]=="BTC" and result["bid"]:
			hbtc_bid[result["symbol"][:-3]]=result["bid"]
			hbtc_ask[result["symbol"][:-3]]=result["ask"]
		elif result["symbol"][-4:]=="USDT" and result["bid"]:
			husdt_bid[result["symbol"][:-4]]=result["bid"]
			husdt_ask[result["symbol"][:-4]]=result["ask"]
		elif result["symbol"][-3:]=="ETH" and result["bid"]:
			heth_bid[result["symbol"][:-3]]=result["bid"]
			heth_ask[result["symbol"][:-3]]=result["ask"]
		elif result["symbol"]=="BTCUSD":
			usd_btc=eval(result["last"])
		elif result["symbol"]=="ETHUSD":
			usd_eth=eval(result["last"])
		elif result["symbol"]=="ETHBTC":
			btc_eth=eval(result["last"])



	for sym in hbtc_ask:
		if sym in husdt_bid:
			per1=(eval(husdt_bid[sym])-eval(hbtc_ask[sym])*(usd_btc))*100/min(eval(husdt_bid[sym]),eval(hbtc_ask[sym])*(usd_btc))
			btou.append((per1,sym))
			per2=(eval(hbtc_bid[sym])*(usd_btc)-eval(husdt_ask[sym]))*100/min(eval(husdt_ask[sym]),eval(hbtc_bid[sym])*(usd_btc))
			utob.append((per2,sym))
		if sym in heth_bid:
			per3=(eval(heth_bid[sym])*(btc_eth)-eval(hbtc_ask[sym]))*100/min(eval(heth_bid[sym])*(btc_eth),eval(hbtc_ask[sym]))
			btoe.append((per3,sym))
			per4=(eval(hbtc_bid[sym])-eval(heth_ask[sym])*(btc_eth))*100/min(eval(heth_ask[sym])*(btc_eth),eval(hbtc_bid[sym]))
			etob.append((per4,sym))
	for sym in heth_ask:
		if sym in husdt_bid:
			per5=(eval(heth_bid[sym])*(usd_eth)-eval(husdt_ask[sym]))*100/min(eval(heth_bid[sym])*(usd_eth),eval(husdt_ask[sym]))
			utoe.append((per5,sym))
			per6=(eval(husdt_bid[sym])-eval(heth_ask[sym])*(usd_eth))*100/min(eval(heth_ask[sym])*(usd_eth),eval(husdt_bid[sym]))
			etou.append((per6,sym))
	sutoe=sorted(utoe)
	setou=sorted(etou)
	setob=sorted(etob)
	sbtoe=sorted(btoe)
	sutob=sorted(utob)
	sbtou=sorted(btou)
	print("USDT to E", sutoe[-3:])

	print("E to USDT", setou[-3:])

	print("USDT to B", sutob[-3:])

	print("B to USDT", sbtou[-3:])

	print("B to E", sbtoe[-3:])

	print("E to B", setob[-3:])



