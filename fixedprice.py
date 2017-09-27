import re
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees","price","cheaper","expensive","cheapest","dollar","dollars"]
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

