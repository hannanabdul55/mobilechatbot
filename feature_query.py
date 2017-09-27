import re
from ner_client import *
def query_db_feature(d):
	nr = NerClient("1PI11CS004","g08")
	os = "Android"
	org = "Samsung"
	product=""
	low_price = 0
	max_price = 100000
	family="None"
	feature = "size"
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
	if len(d['family'])>0:
		family = d['family'][0]
	if len(d['feature'])>0 and d['feature']=='size':
		feature = d['feature']
	if feature=="size":
		size_t = d['size_mentioned']
		size_rel = d['query']
	s = nr.get_products(org)
	count = 0
	result = []
	family=="None"
	if d['query']== 'less than':
		if family=="None":
			res = nr.get_spec(brand=org)
			for i in res:
				if i['category'] == 'Display':
					try:
						si = i['value'].split(',')[1].split()[0].strip()
						si = float(si)
						if int(size)<=int(si):
							result.append(i['product'])
							count+=1
					except:
						abcd =0
				if count>20:
					break			
	elif d['query']=='more than':
		if family=="None":
			res = nr.get_spec(brand=org)
			for i in res:
				if i['category'].lower() == 'display':
					try:
						si = i['value'].split(',')[1].split()[0].strip()
						si = float(si)
						#print si
						if size>=int(si):
							result.append(i['product'])
							count+=1
					except:
						#print "error"
						continue
				if count>20:
					break
	else:
		pass
	#print d['start_price'] , d['end_price']
	#print s
	#print low_price
	#print max_price
	res_string = "The "+ org + " products satisfying the screen size features are :\n"
	count = 1
	#str(res)
	for i in result:
		res_string+=str(count) + ": " + i + "\n"
		count+=1
		if count>20:
			break
	return res_string		