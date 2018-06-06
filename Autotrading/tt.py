from hitbtc import *
import time
import uuid

import requests
from decimal import *

hitbtc_public_key = "e2f71ee3f6550a9f9af1b8ab215ea4d1"
sec="8001516ae9528515ad227c11c9dca253"

hitbtc=Client("https://api.hitbtc.com", hitbtc_public_key, sec)
balances=hitbtc.get_account_balance()


tbalances=hitbtc.get_trading_balance()
s_balance = 0.0
for balance in tbalances:
	if balance['currency'] == 'SBTC':
 		s_balance = float(balance['available'])

while True:

	# if eth_balance >= float(eth_btc['quantityIncrement']):
	client_order_id = uuid.uuid4().hex
	orderbook = hitbtc.get_orderbook('SBTCBTC')
	# set price a little high
	best_price = Decimal(orderbook['bid'][0]['price'])
	print("Selling at %s" % best_price)
	print(s_balance)
	order = hitbtc.new_order(client_order_id, 'SBTCBTC', 'sell', s_balance, best_price)
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

	time.sleep(3)