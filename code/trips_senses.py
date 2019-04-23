## TRIPS
import pytrips
from pytrips.ontology import load
from collections import defaultdict
ont = load()

## SupWSD
from it.si3p.supwsd.api import SupWSD
from it.si3p.supwsd.config import Model, Language

## Lesk
import nltk
from nltk.wsd import lesk

#### Sentence to wordnet senses ####
def sent_to_wn_senses(sent, system="supwsd", 
                      ims_object = None, 
                      word=None,
                     supwsd_apikey=None):
    '''
    Input: sent: A string of words
    Output: list containining wordnet-senses of each word in the sent
            with respective probabilities of those senses
    '''
    if system == "supwsd":
        ans = []
        for result in SupWSD(supwsd_apikey).disambiguate(sent, Language.EN, Model.SEMCOR, True):
            token=result.token
            if not result.miss():
                sense_lst = []
                for sense in result.senses:
                    sense_lst.append((sense.id, sense.probability))

                ans.append([token.word, sense_lst])
            else:
                ans.append([token.word, [(str(result.sense()), 1.0)]])
                

    elif system == "ims":
        sense_list = ims_object.disambiguate(sent, probs=True, synsets=True)
        ans = []
        for word, dct in sense_list:
            if dct:
                wordnet_sense_list = [(synset.lemmas()[0].key(), prob) for synset, prob in dct.items()]
                ## Reorder with decreasing probability
                wordnet_sense_list = sorted(wordnet_sense_list, key=lambda x: -x[1])
                ans.append([word, wordnet_sense_list])
            else:
                ans.append([word, [('U', 1.0)]])
       
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
            1. prob: order the final list wrt to probabilities
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
    
    if type(param) is str:
        if param=="sum":
            for trip_sense, prob in lst:
                curr_dct[trip_sense] += prob
            
        elif param=="max":
            for trip_sense, prob in lst:
                if prob > curr_dct[trip_sense]:
                    curr_dct[trip_sense] = prob
    else:
        curr_dct = param(lst)
                
    ans = list(curr_dct.items())
    
    if order == "prob":
        return sorted(ans, key=lambda x: -x[1])
    elif order == "wn_order":
        return ans
    
    
def sent_to_trips_senses(text, system="wsd", prob="combine", order="prob", 
                        param="sum", ims_object=None,
                       supwsd_apikey = None):
    '''
    Input: a string of words
    
    prob: combine or raw
    order: prob or wn_order
    
    Output: A list of trips senses for each word in the text
    '''
    ans = []
    sent_wn_senses = sent_to_wn_senses(text, system=system, ims_object=ims_object, supwsd_apikey=supwsd_apikey)
    
    for word, word_wn_senses in sent_wn_senses:
        if prob=="combine":
            ans.append([word, combine_probs(wnsense_to_tpsense(word_wn_senses), 
                                     order=order,
                                    param=param)])
        elif prob=="raw":
            ans.append([word, wnsense_to_tpsense(word_wn_senses)])
    return ans