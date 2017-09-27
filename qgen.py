#from memm import *
from memm import *
from build_history import *
from build_history_1 import *
from feature_functions import *
from rer.mymaxent1 import *
from rer.feature_functions1 import *
import nltk
from price_query import *
from feature_query import *
from memm import *
from obj_new_gen import *
json_file = r"all_data1.json"
pickle_file = r"all_data.p"

def test(clf, history_list):
    result = []
    for history in history_list:
        mymap = wmap[history[0]["wn"]]
        #print mymap
        words = mymap
        index = history[0]["i"]
        val = clf.classify(history[0])
        print "word : " + words[index] + " , tags: " + val
    return result
supported_tags = ['Org','Family','Version','OS','Other','Price','Phone','Place','Feature']
#func_obj = FeatureFunctions(wmap, supported_tags)
def genq(sent):
    func_obj = FeatureFunctions([sent,], supported_tags)
    data = json.loads(open(json_file).read())['root']
    (history_list, wmap,exp) = build_history(data, supported_tags)

def build_tuple_rel(sent,toks,tags):
    h = {}
    h["reltags"] = []
    h['updates'] = []
    for i in range(len(toks)):
        t = {}
        t['word']=toks[i]
        t['tag'] = tags[i]
        h['updates'].append(t)
        if tags[i] not in h["reltags"]:
            h["reltags"].append(tags[i])
    h['sentences'] = toks
    return h

class QueryGen:
    def __init__(self):
        data = json.loads(open(json_file).read())['root']
        (self.history_list, self.wmap,exp) = build_history(data, supported_tags)
        self.func_obj = FeatureFunctions(self.wmap, supported_tags)
        self.clf = Memm(self.history_list, self.func_obj, pic_file = pickle_file)
        self.clf.train()
        data1 = json.loads(open("rer/all_data1.json").read())['root']
        (self.h_list,self.sent_rel,exp1) = build_history_1(data1,['irrelevant', 'price_query', 'feature_query', 'interest_intent', 'comparison'])
        self.func_obj_rel = FeatureFunctions1(self.sent_rel,['irrelevant', 'price_query', 'feature_query', 'interest_intent', 'comparison'])
        self.clf_rel = MyMaxEnt1(self.h_list,self.func_obj_rel,pic_file="rer.p")
        self.clf_rel.train()
    def query(self,sent):
        sent_toks = nltk.word_tokenize(sent)
        self.clf.func.set_wmap([sent_toks])
        tags = self.clf.tagw(sent_toks,0)
        #print tags
        h_tup = build_tuple_rel(sent,sent_toks,tags)
        self.clf_rel.func.set_wmap([sent])
        rel  = self.clf_rel.classify(h_tup)
        h_tup["rels"] = rel
        #print rel
        if rel == "feature_query":
            r = getFeatureQueryAttributes(sent,h_tup)
            return query_db_feature(r)
        elif rel == "price_query":
            r = getPriceQueryAttributes(sent,h_tup)
            return query_db_price(r,h_tup)
if __name__ == "__main__":
    #----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
    # ----------------------------------------------------------------

    #TRAIN = int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))

    #tag_set = {"Org": 0, "Other": 1}
    dims = 9
    trg_data_x = []
    trg_data_y = []
    trg_data = {'Org': [], 'Other': []}
    data = json.loads(open(json_file).read())['root']
    #print "num stu = ", len(data)
    #(history_list, wmap,exp) = build_history(data, supported_tags)
    print "After build_history"
    #func_obj = FeatureFunctions(wmap, supported_tags)
    #func_obj.ini()
    #clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
    #print clf.model
    #if TRAIN == 1:
    #    clf.train()
    qg = QueryGen()
    qg.query("What are the phone with a price between 10k and 15k?")
    qg.query("I want an iPhone 6 for 20k.")
    while True:
        inp = raw_input("Enter the query")
        qg.query(inp)
	#result = test(clf, history_list[-500:])
