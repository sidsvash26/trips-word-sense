from pyims import PyIMS
from trips_senses import *
from tripsweb.query import InputTag, wsd as trips
from genesis.tools.spacy import nlp # ugh
import json


path_to_ims = "/Users/rik/projects/spring2019/tripswsd/sid/ims"
wsd_ims = PyIMS(path_to_ims, "models-MUN-SC-wn30")

def extent(w):
    return (w.idx, w.idx + len(w)+1)

def get_input_terms(sentence, url=None, verbose=True, dry=False):
    distribution = sent_to_trip_senses(sentence, system="ims", ims_object=wsd_ims, prob="combine", order="prob", param="sum")
    input_terms(sentence, distribution)
    if dry:
        print([str(i) for i in res])
        return
    parse = json.loads(trips(sentence, res, url, verbose)[0])
    old_parse = json.loads(trips(sentence, [], url, verbose)[0])
    if not sanity_checks(sent, parse, old_parse):
        print(distribution)
    return parse, dist

def input_terms(sentence, distribution):
    items = zip(nlp(sentence), distribution)
    res = []
    for s, dist in items:
        for d in dist:
            if not str(d[0]).startswith("ont::"):
                continue
            start, end = extent(s)
            res.append(InputTag(str(s), start, end, str(d[0]), 1-d[1]))
    return res

def sanity_checks(sentence, parse, old_parse):
    parse_nodes = []
    for n in parse:
        parse_nodes.extend(list(n.values()))
    roots = [p for p in parse_nodes if type(p) is str]
    parse_nodes = [p for p in parse_nodes if type(p) is dict]

    old_parse_nodes = []
    for n in old_parse:
        old_parse_nodes.extend(list(n.values()))
    old_roots = [p for p in old_parse_nodes if type(p) is str]
    old_parse_nodes = [p for p in old_parse_nodes if type(p) is dict]

 
    #2. Parse is changed
    #a. Set of types:
    new_parse = set([x['type'] for x in parse_nodes if 'type' in x])
    old_parse = set([x['type'] for x in old_parse_nodes if 'type' in x])
    common_nodes = new_parse.intersection(old_parse)
    if common_nodes == new_parse and common_nodes == old_parse:
        print("parses are p much the same")
        return True
    print("new\n", {p['word']: p['type'] for p in parse_nodes if 'type' in p and 'word' in p})
    print("old\n", {p['word']: p['type'] for p in old_parse_nodes if 'type' in p and 'word' in p})
    return False

texts = ["Despite everything, I like this sentence.",
          "They liked grilled bass.",
         "I found a boat at the bank.", 
          "I found a dollar at the bank.",
          "I found a fish at the bank.",
          "The bat hit the ball.",
         "The bat ate the fruit.",
          "Bats sleep in the afternoon.",
          "The bat was sleeping on a tree.",
          "The bat slept in the afternoon.",
         "Sachin hit the ball with the bat.",
         "The artist drew a picture."]

def test(data):
    for d in data:
        print(d)
        get_input_terms(d, url="http://localhost:8081/cgi/STEP", verbose=False)

