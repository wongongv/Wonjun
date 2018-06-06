from hitbtc import *
import time
import uuid
import datetime
import requests


hitbtc_public_key = "e2f71ee3f6550a9f9af1b8ab215ea4d1"
sec="8001516ae9528515ad227c11c9dca253"

hitbtc=Client("https://api.hitbtc.com", hitbtc_public_key, sec)
balances=hitbtc.get_account_balance()

def f():
	tbalances=hitbtc.get_trading_balance()
	dgb_balance = 0.0
	for balance in tbalances:
		if balance['currency'] == 'SBTC':
		    dgb_balance = float(balance['available'])


	while True:

		# if eth_balance >= float(eth_btc['quantityIncrement']):
		client_order_id = uuid.uuid4().hex
		orderbook = hitbtc.get_orderbook('SBTCBTC')
		# set price a little high
		best_price = Decimal(orderbook['bid'][0]['price'])
		print("Selling at %s" % best_price)

		order = hitbtc.new_order(client_order_id, 'SBTCBTC', 'sell', dgb_balance, best_price)
		if 'error' not in order:
		    if order['status'] == 'filled':
		        print("Order filled", order)
		    elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
		        print("Waiting order...")
		        for k in range(0, 3):
		            order = hitbtc.get_order(client_order_id, 20000)
		            print(order)

		            if 'error' in order or ('status' in order and order['status'] == 'filled'):
		                break

		        # cancel order if it isn't filled
		        if 'status' in order and order['status'] != 'filled':
		            cancel = hitbtc.cancel_order(client_order_id)
		            print('Cancel order result', cancel)

		time.sleep(1)
	return None









while True:

	for balance in balances:
		if balance["currency"]=="SBTC":
			transfer=hitbtc.transfer("SBTC",balance['available'],True)
			print("Transfer",transfer)
			print(balance["available"])
			print(datetime.datetime.now())
			if eval(balance['available'])<=300:
				f()

	time.sleep(3)

# tbalances=hitbtc.get_trading_balance()
# dgb_balance = 0.0
# for balance in tbalances:
# 	if balance['currency'] == 'DGB':
# 	    dgb_balance = float(balance['available'])


# while True:

# 	# if eth_balance >= float(eth_btc['quantityIncrement']):
# 	client_order_id = uuid.uuid4().hex
# 	orderbook = hitbtc.get_orderbook('DGBBTC')
# 	# set price a little high
# 	best_price = Decimal(orderbook['bid'][0]['price'])
# 	print("Selling at %s" % best_price)

# 	order = hitbtc.new_order(client_order_id, 'DGBBTC', 'sell', dgb_balance, best_price)
# 	if 'error' not in order:
# 	    if order['status'] == 'filled':
# 	        print("Order filled", order)
# 	    elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
# 	        print("Waiting order...")
# 	        for k in range(0, 3):
# 	            order = hitbtc.get_order(client_order_id, 20000)
# 	            print(order)

# 	            if 'error' in order or ('status' in order and order['status'] == 'filled'):
# 	                break

# 	        # cancel order if it isn't filled
# 	        if 'status' in order and order['status'] != 'filled':
# 	            cancel = hitbtc.cancel_order(client_order_id)
# 	            print('Cancel order result', cancel)

# 	time.sleep(1)