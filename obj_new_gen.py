import re
from price_picker import *
#from fixedprice import *
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees","price","cheaper","expensive","cheapest","dollar","dollars"]

def indexOf(l, i):
	for p in range(len(l)):
		if l[p] == i:
			return p
	return -1
def make_num(possible_number):
		possible_number=possible_number.lower()
		if(len(possible_number.split(','))>1):
			str0=""
			possible_number=possible_number.split(',')
			for i in possible_number:
				str0+=str(i)
			possible_number=str0
			if int(str0)<100:
				possible_number=int(str0)*1000
				return str(possible_number) 
		if(len(possible_number.split('k'))>1):
			temp=possible_number.split('k')
			for i in temp:
				if   i != 'k':
					i=int(i)	
					if i<100:
						possible_number=i*1000
						return str(possible_number)

def modify_dict(new_dict):
	try:
		start_price=new_dict['start_price']
		end_price=new_dict['end_price']
		price_start=start_price
		prince_end=end_price
		if('k' in start_price):
			price_start=start_price.split('k')
			for i in range (0,price_start-1):
				if price_start[i]!='k' and price_start[i]!=' 'and price_start[i]!='' :
					price_start[i]=int(price_start[i])*1000
		if('K' in start_price):
			price_start=start_price.split('K')
			for i in range (0,len(price_start)-1):
				if price_start[i]!='K':
					price_start[i]=int(price_start[i])*1000
			new_dict['start_price']=str(price_start[0])
		if('k' in end_price):
			price_end=end_price.split('k')
			for i in range (0,price_end-1):
				if price_end[i]!='k':
					price_end[i]=int(price_end[i])*1000
		if('K' in end_price):
			price_end=end_price.split('K')
			for i in range (0,len(price_end)-1):
				if price_end[i]!='K':
					price_end[i]=int(price_end[i])*1000
			new_dict['end_price']=str(end_start[0])
		#print new_dict
	except Exception as e:
		abc=0
		print "Error"
def getUpdates(obj):
	res=[]

	try:
		#obj["updates"]
		res=obj["updates"]
	except Exception as e:
		abc = 0
		print "No updates in dict"
	return res
def getPhone(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='phone':
					res.append(i['word'])
			except Exception as e:
				abc=0# print 0
	
	return res
def getFamily(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='family':
					res.append(i['word'])
			except Exception as e:
				abc=0# print 0
	
	return res

def getFeature(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='feature':
					res.append(i['tag'].lower())
			except Exception as e:
				abc=0# print 0
	
	return res

def getOrg(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='org':
					res.append(i['word'])
			except Exception as e:
				abc=0;# print 0
	
	return res

def getOs(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='os':
					res.append(i['word'])
			except Exception as e:
				abc=0;# print 0
	
	return res

def getVersion(updates):
	res=[]
	for i in updates:
			try:
				if i['tag'].lower()=='version':
					res.append(i['word'])
			except Exception as e:
				abc=0;# print 0
	
	return res

def getPrice(updates):
	#print'updates::::'
	#print updates
	res=[]
	for i in updates:
		try:
			if i['tag'].lower()=='price':
				#if i['word'].lower() not in currency_symbols:
				res.append(i['word'])
			#print "hi"
			
		except Exception as e:
			abc=0;# print 0
	for i in range(0,len(res)):
		res[i]=make_num(res[i])
	#print 'res'
	#print res	
	return res



def getRelation(obj):
	res=[]
	try:
		#obj["rels"]
		res=obj["rels"]
	except Exception as e:
		pass

	return res
def indexOf(l, i):
	s = l.split(" ")
	for p in range(len(s)):
		if i.lower() in s[p].lower():
			return p
	return -1

def getFeatureQueryAttributes(sent, obj):
	updates=getUpdates(obj)
	feature_list = getFeature(updates)
	version_list=getVersion(updates)
	os_list=getOs(updates)
	phone_list=getPhone(updates)
	org_list=getOrg(updates)
	family=getFamily(updates)
	new_obj = {'family':family,'org':org_list,'version_list':version_list,'os_list':os_list,'phone_list':phone_list}
	print new_obj
	if "feature" in feature_list:
		try:
			if "inches" in sent or "\"" in sent:
				size_mentioned = 0
				feature = "size"
				new_obj["feature"] = feature
				i = -1
				if "inches" in sent:
					i = indexOf(sent.lower(), "inches")
				elif "\"" in sent:
					i = indexOf(sent.lower(), "\"")
				if i != -1:
					if i < 2:
						size_mentioned = sent[i-1]
						new_obj['size_mentioned'] = size_mentioned
					elif i > 2:
						sent_split = sent.split(" ")
						size_mentioned = sent_split[i-1]
						new_obj['size_mentioned'] = size_mentioned
						if sent_split[i-2] == "than" and sent_split[i-3] == "more":
							query = "more than"
							print "hi"
						elif sent_split[i-2] == "than" and sent_split[i-3] == "less":
							query = "less than"
						elif sent_split[i-2] == "around":
							query = "around"
						new_obj['query'] = query
			else:
				p1 = "(\d+\.?\d*)\s?(\w\w\w?)"
				m = re.search(p1, sent)
				if m:
					grp = m.groups()
					spec = grp[0]
					new_obj["spec"] = spec
					unit = grp[1]
					if unit.lower() == "mp":
						new_obj["feature"] = "camera"
					elif unit.lower() == "gb" or "mb":
						new_obj["feature"] = "ram"
					elif unit.lower() == "mah":
						new_obj["feature"] = "battery_life"
					elif unit.lower() == "ghz":
						new_obj["feature"] = "speed"	
			print new_obj
			return new_obj
		except Exception as e:
			abc = 0
def getPriceQueryAttributes(sent, obj):
	updates=getUpdates(obj)
	price_list=getPrice(updates)
	version_list=getVersion(updates)
	os_list=getOs(updates)
	phone_list=getPhone(updates)
	org_list=getOrg(updates)
	start_price=end_price=""
	family=getFamily(updates)
	try:
		start_price=price_list[0]
	except Exception as e:
		abc=0;# print 0
	try:
		end_price=price_list[1]
	except Exception as e:
		abc=0;# print 0
	prices = {}
	prices = price_picker(start_price, end_price, sent)
	start_price = prices["start_price"]
	end_price = prices["end_price"]
	new_dict={'family':family,'start_price':str(start_price),'end_price':str(end_price),'org':org_list,'version_list':version_list,'os_list':os_list,'phone_list':phone_list}
	#modify_dict(new_dict)	#new_dict={'family':family,'start_price':str(start_price),'end_price':str(end_price),'org':org_list,'version_list':version_list,'os_list':os_list,'phone_list':phone_list}
	#modify_dict(new_dict)
	return new_dict

"""def getFeatureQueryAttributes(sent, obj):
	updates=getUpdates(obj)
	feature_list = getFeature(updates)
	version_list=getVersion(updates)
	os_list=getOs(updates)
	phone_list=getPhone(updates)
	org_list=getOrg(updates)
	family=getFamily(updates)
	new_obj = {'family':family,'org':org_list,'version_list':version_list,'os_list':os_list,'phone_list':phone_list}
	if "feature" in feature_list:
		#print "in updates"
		try:
			if "inch" in sent or "inches" in sent or "\"" in sent:
				size_mentioned = 0
				feature = "size"
				new_obj["feature"] = feature
				
			else:
				p1 = "(\d+\.?\d*)\s?(\w\w\w?)"
				m = re.search(p1, sent)
				if m:
					grp = m.groups()
					spec = grp[0]
					new_obj["spec"] = spec
					unit = grp[1]
					if unit.lower() == "mp":
						new_obj["feature"] = "camera"
					elif unit.lower() == "gb" or "mb":
						new_obj["feature"] = "ram"
					elif unit.lower() == "mah":
						new_obj["feature"] = "battery_life"
					elif unit.lower() == "ghz":
						new_obj["feature"] = "speed"	
			return new_obj
		except Exception as e:
			abc = 0
	return new_obj
"""
'''def getComparisonQueryAttributes(sent, obj):
	updates=getUpdates(obj)
	feature_list = getFeature(updates)
	version_list=getVersion(updates)
	os_list=getOs(updates)
	phone_list=getPhone(updates)
	org_list=getOrg(updates)
	family=getFamily(updates)
	new_obj = {'family':family,'org':org_list,'version_list':version_list,'os_list':os_list,'phone_list':phone_list}
	if "better than" in sent:
		i = '''



def getData(sent, obj):
	sent = sent.lower()
	reltype=obj['rels']
	for i in reltype:
		keys=i.keys()
	if(len(keys)>1):
		keys=obj['rels'][0].keys()
	#print keys

	if keys[0].lower() == "price_query":# or keys[0].lower()=="feature_query" or keys[0].lower()=="interest_intent" or keys[0].lower()=="comparison"):
		#its at price.
		getPriceQueryAttributes(sent, obj)
	elif keys[0].lower() == "feature_query":
		print getFeatureQueryAttributes(sent, obj)
	#elif keys[0].lower() == "interest_intent":
	#	getInterestQueryAttributes(sent, obj)
	elif keys[0].lower() == "comparison":
		getComparisonQueryAttributes(sent, obj)

#sent = "Does Samsung grand have a screen size of more than 5 inches ?"
#obj = {"rels": [{"feature_query": ["Other", "Org", "Model", "Other", "Feature", "Other"]}], "updates": [{"tag": "Other", "word": "Does"}, {"tag": "Org", "word": "Samsung"}, {"tag": "Model", "word": "grand"}, {"tag": "Other", "word": "have"}, {"tag": "Other", "word": "a"}, {"tag": "Other", "word": "screen"}, {"tag": "Other", "word": "size"}, {"tag": "Other", "word": "of"}, {"tag": "Other", "word": "more"}, {"tag": "Other", "word": "than"}, {"tag": "Feature", "word": "5"}, {"tag": "Size", "word": "inches"}, {"tag": "Other", "word": "?"}]}
#sent = "Is 4.4.4 Kitkat better than iOS 7?"
#obj = {"rels": [{"comparison": ["Version", "OS"]}], "updates": [{"tag": "Other", "word": "Is"}, {"tag": "Version", "word": "4.4.4"}, {"tag": "Version", "word": "Kitkat"}, {"tag": "Other", "word": "better"}, {"tag": "Other", "word": "than"}, {"tag": "OS", "word": "iOS"}, {"tag": "Version", "word": "7"}, {"tag": "Other", "word": "?"}]}#, "sentence": "Is 4.4.4 Kitkat better than iOS 7?"}, {"rels": [{"interest_intent": ["Org", "Family", "Phone", "Place"]}], "updates": [{"tag": "Other", "word": "Do"}, {"tag": "Other", "word": "I"}, {"tag": "Other", "word": "get"}, {"tag": "Org", "word": "Sony"}, {"tag": "Family", "word": "Xperia"}, {"tag": "Phone", "word": "devices"}, {"tag": "Other", "word": "in"}, {"tag": "Place", "word": "London"}, {"tag": "Other", "word": "?"}]}
#getData(sent, obj)

