import logging
logging.basicConfig()

from tripsweb.query import InputTag
from tripsweb.query import wsd as trips
from trips_senses import sent_to_wn_senses, wnsense_to_tpsense
import json
from genesis.tools.spacy import nlp
from comb import Hint, Collapse
from pyims import PyIMS
from match_parse import match, disassemble_parse, Span, extent

def input_terms(sentence, distribution):
    items = zip(nlp(sentence), distribution)
    res = []
    for s, dist in items:
        for d in dist.items():
            if not str(d[0]).startswith("ont::"):
                continue
            span = extent(s)
            res.append(InputTag(str(s), span.start, span.end, str(d[0]), 1-d[1]))
    return res

def estr(x):
    if x:
        return str(x)
    else:
        return "_None"

def dict_diff(d1, d2):
    res = {}
    for k1, v1 in d1.items():
        if k1 not in d2:
            res[k1] = (v1, None)
        elif d2[k1] != v1:
            res[k1] = (v1, d2[k1])
    for k2, v2 in d2.items():
        if k2 not in d1:
            res[k2] = (None, v2)
    return res

class EInstance:
    def __init__(self, sentence, experiment):
        self.sentence = sentence
        self.experiment = experiment
        self.ran = False

    def is_changed(self, explain=False):
        if not self.ran:
            self.run()
        plain = disassemble_parse(self.plain)[0]
        hints = disassemble_parse(self.hinted)[0]
        p = {estr(x['word']):x['type'] for x in plain if 'type' in x and 'word' in x}
        h = {estr(x['word']):x['type'] for x in hints if 'type' in x and 'word' in x}
        common = dict_diff(p, h)
        if not common:
            return False
        if explain:
            self.examine(common)
        return True
    
    def examine(self, common):
        for k, v in common.items():
            print(str(k), ":", str(v[0]), "->", str(v[1]))
        print(self.matched_plain)
        print(self.plain)

    def run(self):
        # 1. parse plain
        self.plain = self.experiment.parse(self.sentence, [])

        # 2. generate wn_distribution
        self.wn_distribution = self.experiment.wn_distribution(self.sentence)
        
        # 3. generate trips_distribution <- collapse/combine
        self.trips_distribution = self.experiment.trips_dist(self.wn_distribution)

        # 4. generate hints
        self.hints = input_terms(self.sentence, self.trips_distribution)

        # 5. parse hinted
        #print(" ".join([str(h) for h in self.hints]))
        self.hinted = self.experiment.parse(self.sentence, self.hints)

        # 5. a. align
        sent = nlp(self.sentence)
        self.matched_plain = match(sent, self.plain)
        self.matched_hinted = match(sent, self.hinted)

        # 6. decode senses


class Experiment:
    def __init__(self, collapse, hint, url, ims_object):
        self.collapse = collapse
        self.hint = hint
        self.url = url
        self.ims_object = ims_object

    def parse(self, sentence, hints):
        return json.loads(trips(sentence, hints, self.url)[0])

    def wn_distribution(self, sentence):
        return sent_to_wn_senses(sentence, system="ims", ims_object=self.ims_object)

    def trips_dist(self, distribution):
        return [self.hint(self.collapse(wnsense_to_tpsense(d))) for d in distribution]

def test(sentences, exp):
    data = [EInstance(sentence, exp) for sentence in sentences]
    for e in data:
        e.run()
        print(e.is_changed(explain=True), e.sentence)

    return data

def main():
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
    ims_object = PyIMS("/Users/rik/projects/spring2019/tripswsd/sid/ims", "models-MUN-SC-wn30")
    experiment = Experiment(Collapse.sum, Hint.all, "http://localhost:8081/cgi/STEP", ims_object)
    test(texts, experiment)

if __name__ == "__main__":
    main()
