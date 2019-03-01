from genesis.tools.spacy import nlp
from tripsweb.query import wsd
import json

def extent(w):
    if type(w) is dict:
        return Span(w["start"], w["end"])
    else:
        return Span(w.idx, w.idx + len(w) + 1)

class Span:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other):
        if type(other) is Span:
            return self.start <= other.start and self.end >= other.end
        return False

    def is_contained(self, other):
        if type(other) is Span:
            return other.contains(self)
        return False

    @property
    def length(self):
        return self.end - self.start

    def __eq__(self, obj):
        return isinstance(obj, Span) and obj.start == self.start and obj.end == self.end

    def __ne__(self, obj):
        return not self == obj

    @staticmethod
    def get_range(spans, key=lambda x: x):
        spans = [key(x) for x in spans]
        return Span(min(spans, key=lambda x: x.start).start, max(spans, key=lambda x: x.end).end)

    def __repr__(self):
        return "Span({}, {})".format(self.start, self.end)

    def __sub__(self, other):
        if not isinstance(other, Span):
            return self
        if self.start > other.end:
            x = self.start - other.length
            y = self.end - other.length
            return Span(x,y)
        return self

def disassemble_parse(parse):
    parse_nodes = []
    for n in parse:
        parse_nodes.extend(list(n.values()))
    roots = [p for p in parse_nodes if type(p) is str]
    parse_nodes = [p for p in parse_nodes if type(p) is dict]
    return parse_nodes, roots

def match(sentence, parse):
    parse_nodes, roots = disassemble_parse(parse)
    tokens = [(s, extent(s)) for s in sentence]
    tokens = [t for t in tokens if t[0].is_alpha]
    #non_alpha = sorted([t for t in tokens if not t[0].is_alpha], key=lambda x: -x[1].end)
    tokens[-1][1].end -= 1
    #for x, y in non_alpha:
    #    tokens = [(t, s - y) for t, s in tokens]
    nodes = {n["id"]: (n, extent(n)) for n in parse_nodes if n["word"]}
    # 1. map tokens to nodes
    token_range = Span.get_range(tokens, key=lambda x: x[1])
    nodes_range = Span.get_range(nodes.values(), key=lambda x: x[1])
    if token_range != nodes_range:
        s = " ".join([x["roles"]['LEX'] for x in parse_nodes if "roles" in x and 'LEX' in x["roles"] and x["roles"]['LEX']])
        return []

    comp = {}
    for l, n in nodes.items():
        comp[l] = [t for t in tokens if t[1].is_contained(n[1])]

    keys = sorted(comp.keys(), key=lambda x: nodes[x][1].length)
    used = []
    res = []
    for k in keys:
        for v in comp[k]:
            if v in used:
                continue
            if nodes[k][0]["roles"]["LEX"].lower() == str(v[0]).lower():
                used.append(v)
                res.append((nodes[k][0]["roles"]["LEX"], v[0]))
    return res


#    decisions = {}
#    def decide():
#        made = 0
#        for l, v in sorted(comp.items(), key=lambda x: nodes[x[0]][1].length):
#            if len(v) == 1 and v[0][1] == nodes[l][1]:
#                decisions[l] = v[0]
#                del comp[l]
#                for vl in comp.values():
#                    if v[0] in vl:
#                        vl.remove(v[0])
#                made += 1
#        return made
#    made = 1
#    while made:
#        made = decide()
#    return decisions, comp
#
