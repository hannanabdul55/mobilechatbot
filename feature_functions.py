'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
from ner_client import *
import datetime
import re
client = NerClient("1PI11CS004","g08")

phones = ["phone", "phones", "smartphone", "smartphones", "mobile", "tablet", "tablets", "phablet", "phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry',
            'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio',
            'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list1 = [m.lower() for m in org_list]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list1 = [m.lower() for m in os_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
feature_list= ["bluetooth","cameras","wifi","front","camera","back","screen","hd","processor","accelerometer","barometer","gyro","memory","ram"]
brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
#for v in client.get_brand_product_bigrams_dict().values():
#    for v1 in v:
#        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
family_set = set()
for p in product_names:
    product_name_tokens.extend(p.split())
    family_set.union({p.split()[0],})

class FeatureFunctions(object):
    def __init__(self,sent, tag_list = None):
        self.wmap = {}
        self.set_wmap(sent)
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        self.supported_tags = self.fdict.keys() 
		
        return

    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return

    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats
    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0
    #------------------------------- Phone tag ---------------------------------------------------------
    # The following is an example for you to code your own functions
    # returns True if wi is in phones tag = Phone
    # h is of the form {'ta':xx, 'tb':xx, 'wn':xx, 'i':xx}
    # self.wmap provides a list of sentences (tokens) where each element in the list is a dict {'words': word_token_list, 'pos_tags': pos_tags_list}
    # each pos_tag is a tuple returned by NLTK tagger: (word, tag)
    # h["wn"] refers to a sentence number
    
    def fPhone_1(self, h, tag):
        if tag != "Phone":
            return 0
        words = self.wmap[h["wn"]]['words']        
        if (words[h["i"]].lower() in phones):
            return 1
        else:
            return 0
    def fPhone_2(self,h,tag):
        if tag != "Phone":
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['tb'] == "Org":
            return 1
        else:
            return 0
    def fPhone_3(self,h,tag):
        if tag !="Phone":
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['tb'] == 'Version' and h['ta']=='Other':
            return 1
        else:
            return 0
    #------------------------------- Functions for Org tag ---------------------------------------------------------
    def fOrg_1(self,h,tag):
        if tag !='Org':
            return 0
        words = self.wmap[h["wn"]]['words']
        if (words[h["i"]].lower() in org_list1):
            return 1
        else:
            return 0
    def fOrg_2(self,h,tag):
        if tag !='Org':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1].lower() in product_names:
                return 1
            else:
                return 0
        except:
            return 0
    def fOrg_3(self,h,tag):
        if tag !='Org':
            return 0
        words = self.wmap[h["wn"]]['words']
        if str.isupper(str(words[h['i']][0])):
            return 1
        else:
            return 0
    def fOrg_4(self,h,tag):
        if tag !='Org':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1] in phones:
                return 1
            else:
                return 0
        except:
            return 0
    def fOrg_5(self,h,tag):
        if tag !='Org':
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['tb'] == 'Other':
            return  1
        else:
            return 0

#------------------------------- Functions for Family tag ---------------------------------------------------------  
    def fFamily_1(self,h,tag):
        if tag !='Family':
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['tb'] == 'Org':
            return 1
        else:
            return 0
    def fFamily_2(self,h,tag):
        if tag !='Family':
            return 0
        words = self.wmap[h["wn"]]['words']
        if str.isupper(str(words[h['i']][0])):
            return 1
        else:
            return 0
    def fFamily_3(self,h,tag):
        if tag !='Family':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1] in product_name_token:
                return 1    
            else:
                return 0
        except:
            return 0
    def fFamily_5(self,h,tag):
        if tag !='Family':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1] in phones:
                return 1
            else:
                return 0
        except:
            return 0
    def fFamily_4(self,h,tag):
        if tag !='Family':
            return 0
        words = self.wmap[h["wn"]]['words']
        if words[h['i']] in family_set:
            return 1
        else:
            return 0	
#------------------------------- Functions for OS tag ---------------------------------------------------------        
    def fOS_1(self,h,tag):
        if tag !='OS':
            return 0
        words = self.wmap[h["wn"]]['words']
        if words[h['i']].lower() in os_list1:
            return 1
        else:
            return 0
    def fOS_2(self,h,tag):
        if tag !='OS':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1].lower() in org_list1:
                return 1
            else:
                return 0
        except:
            return 0
    def fOS_3(self,h,tag):
        if tag !='OS':
            return 0
        words = self.wmap[h["wn"]]['words']
        try:
            if words[h['i']+1] in phones:
                return 1
            else:
                return 0
        except:
            return 0
    def fOS_4(self,h,tag):
        if tag !='OS':
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['ta'] == 'Version' and h['tb'] == 'Other':
            return 1
        else:
            return 0
    def fOS_5(self,h,tag):
        if tag !='OS':
            return 0
        words = self.wmap[h["wn"]]['words']
        if h['ta'] == 'Other' and h['tb'] == 'Other':
            return 1
        else:
            return 0
#------------------------------- Functions for Version tag ---------------------------------------------------------    
    def fVersion_1(self, h, tag):
        if h["tb"] == "Phone" and tag == "Version":
            return 1
        else:
            return 0

    def fVersion_2(self, h, tag):
        if h["tb"] == "Org" and tag == "Version":
            return 1
        else:
            return 0

    def fVersion_3(self, h, tag):
        if h["tb"] == "Family" and tag == "Version":
            return 1
        else:
            return 0

    def fVersion_4(self, h, tag):
        if h["tb"] == "OS" and tag == "Version":
            return 1
        else:
            return 0

    def fVersion_5(self, h, tag):
        if h["tb"] == "Version" and tag == "Version":
            return 1
        else:
            return 0

    #------------------------------- Functions for Other tag ---------------------------------------------------------
    #------------------------------- Functions for Price tag ---------------------------------------------------------  
    def fPrice_1(self, h, tag):
        if re.match("[0-9]+k", self.wmap[h["wn"]]["words"][h["i"]].lower()) and tag == "Price":
            return 1
        else:
            return 0

    def fPrice_2(self, h, tag):
        if h["tb"] == "Price" and tag == "Price":
            return 1
        else:
            return 0
   
    def fPrice_3(self, h, tag):
        p1 = re.compile("[0-9]+k")
        p2 = re.compile("[0-9]+")
        words = self.wmap[h["wn"]]['words']
        if p1.match(words[h["i"]]) or p2.match(words[h["i"]]) and tag=="Price":
             return 1
        if words[h["i"]-1].lower() == "between" and tag == "Price":
            return 1
        else:
            return 0

    def fPrice_4(self, h, tag):
        words = self.wmap[h["wn"]]['words']
        if words[h["i"]-1].lower() == "less" or words[h["i"]-1].lower() == "for" or words[h["i"]-1].lower() == "below" or words[h["i"]-1].lower() == "under" or words[h["i"]-1].lower() == "is" and tag == "Price":
            return 1
        else:
            return 0
    def fPrice_5(self,h,tag):
        words = self.wmap[h["wn"]]['words']
        if tag!="Price":
            return 0
        if words[h["i"]].lower() == "price":
            return 1
        else:
            return 0		
#5th PENDING

#------------------------------- Functions for Size tag ---------------------------------------------------------  


#------------------------------- Functions for Feature tag ---------------------------------------------------------  
    def fFeature_1(self, h, tag):
        words = self.wmap[h["wn"]]['words']
        if words[h["i"]].lower() == "camera" and h["tb"] == "Feature" and tag == "Feature":
            return 1
        else:
            return 0
    def fFeature_2(self, h, tag):
        words = self.wmap[h["wn"]]['words']
        if words[h["i"]].lower() in feature_list and tag == "Feature":
            return 1
        else:
            return 0
			
    def fFeature_3(self, h, tag):
        words = self.wmap[h["wn"]]['words']
        if words[h["i"]].lower() == "display" and tag == "Feature":
            return 1
        else:
            return 0		
#------------------------------- Functions for Other tag --------------------------------------------------------
    def fOther_1(self,h,tag):
        if tag =='Other':
            return 1
        else:
            return 0
    def fOther_2(self,h,tag):
        if tag!='Other':
            return 0
        if h['tb'] == 'Phone':
            return 1
        else:
            return 0
    def fOther_3(self,h,tag):
        if tag!='Other':
            return 0
        if h['ta'] == 'OS' and h['tb'] == 'Version':
            return 1
        else:
            return 0			
    #------------------------------- Functions for Price tag ---------------------------------------------------------  
    #------------------------------- Functions for Size tag ---------------------------------------------------------  
    #------------------------------- Functions for Feature tag ---------------------------------------------------------  

if __name__ == "__main__":
    pass
