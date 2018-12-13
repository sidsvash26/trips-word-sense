import nltk
from nltk.wsd import lesk
from supwsd.wsd import SupWSD
from genesis.tools import lextagger as LT
from genesis.tools.trips import ontology as ont
from collections import defaultdict

## SupWSD reference: http://www.aclweb.org/anthology/D17-2018

#### Sentence to wordnet senses ####
def sent_to_wn_senses(sent, word=None):
    '''
    Input: sent: A string of words
    Output: list containining wordnet-senses of each word in the sent
            with respective probabilities of those senses
    '''
    ans = []
    sense_object = SupWSD().senses(sent,True)
    for word in sense_object:
        wordnet_sense_list = []
        for result in word.results:
            wordnet_sense_list.append([result.key, result.prob])
        ans.append(wordnet_sense_list)
        
    return ans   

### Sentence to TRIP Senses ####
def wnsense_to_tpsense(lst_wn_senses):
    '''
    Input: lst_wn_senses: a list of wordnet senses of a some word
            with probabilities of each sense
     
    Output: A list of trip-senses of corresponding
            word-net senses with same probabilities
            (distributed uniformly for a particular word-net
            sense)
    '''
    
    ans = []
    for wn_sense, prob in lst_wn_senses:
        if wn_sense == "U":
            ans.append(['UNK1', prob])
        else:
            tp_senses = list(ont.get_wordnet(wn_sense))
            if tp_senses == []:
                ans.append(['UNK2', prob])
            else:
                assigned_prob = prob/len(tp_senses)
                for tp_sense in tp_senses:
                    ans.append([tp_sense, assigned_prob])
            
    return ans

def combine_probs(lst, order="prob", param="sum"):
    '''
    Input: lst of tuples: (trip_sense, prob)
            where there could be multiple instances
            of same trip_sense with different 
            probabilities
            
            order:
            1. order: order the final list wrt to probabilities
            2. wn_order: order the final list wrt to 
                        wn_sense prob order
            param:
            1. sum
            2. max
            
    Output: lst of tuples: (trip_sense, prob)
            with unique trip_sense where the different
            probabilities for that trip_sense has been
            summed up
    
    '''
    curr_dct = defaultdict(float)
    
    if param=="sum":
        for trip_sense, prob in lst:
            curr_dct[trip_sense] += prob
            
    elif param=="max":
        for trip_sense, prob in lst:
            if prob > curr_dct[trip_sense]:
                curr_dct[trip_sense] = prob
                
    ans = list(curr_dct.items())
    
    if order == "prob":
        return sorted(ans, key=lambda x: -x[1])
    elif order == "wn_order":
        return ans
    
    
def sent_to_trip_senses(text, prob="combine", order="prob", param="sum"):
    '''
    Input: a string of words
    
    prob: combine or raw
    order: prob or wn_order
    
    Output: A list of trip senses for each word in the text
    '''
    ans = []
    sent_wn_senses = sent_to_wn_senses(text)
    
    for word_wn_senses in sent_wn_senses:
        if prob=="combine":
            ans.append(combine_probs(wnsense_to_tpsense(word_wn_senses), 
                                     order=order,
                                    param=param))
        elif prob=="raw":
            ans.append(wnsense_to_tpsense(word_wn_senses))
    return ans
    
    