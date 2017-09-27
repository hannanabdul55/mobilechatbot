import re

def price_picker(start_price,end_price,sent):
	if end_price =="" or end_price==" ":
		word_lessthan=['lesser than','cheaper than','below','under']
		for i in word_lessthan:
			if i in sent:
				end_price=start_price
				start_price=0
				return{'start_price':start_price,'end_price':end_price}
		word_greaterthan=['more than','above','greater than','over','more']
		for i in word_greaterthan:
				if i in sent:
					start_price=start_price
					end_price=1000000
					return{'start_price':start_price,'end_price':end_price}
	if 'between' in sent:
		start_price=start_price
		end_price=end_price
		return{'start_price':start_price,'end_price':end_price}
	return{'start_price':start_price,'end_price':end_price}