import re
from ner_client import *
def query_db_price(d,h_tup):
	nr = NerClient("1PI11CS004","g08")
	os = "Android"
	org = "Samsung"
	product=""
	low_price = 0
	max_price = 100000
	if len(d["os_list"])>0:
		os = d['os_list'][0]
	if len(d["org"])>0:
		org = d["org"][0]
	elif os.lower()=="ios":
		org="Apple"
	elif os.lower() == "windows":
		org="Nokia"
	if 	len(d["family"])>0:
		family = d["family"][0]
	elif os=="Apple":
		family="iPhone"
	elif os=="Windows":
		family="Lumia"
	try:
		low_price = int(d['start_price'])
		max_price = int(d['end_price'])
	except:
		abcd=0
	model = ""
	for i in h_tup['updates']:
		if i['tag'] == "Model":
			model = i['word']
	#if model=="":	
	#print d['start_price'] , d['end_price']
	s = nr.get_products(org)
	if model!="":
		for i in s:
			if i['product']==model:
				return "The price of " + model + " is " + i['dummy_price']
	#print s
	#print low_price
	#print max_price
	res = []
	for i in s:
		if i["dummy_price"]<max_price and i['dummy_price']>low_price:
			res.append(i)
	res_string = "The "+ org + " products in your price range are :\n"
	count = 1
	#str(res)
	for i in res:
		res_string+=str(count) + ": " + i['product'] + "\n"
		count+=1
		if count>20:
			break
	res_string += "\n" + "It has been very well recieved and fits your requirements."
	return res_string	