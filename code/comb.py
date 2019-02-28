# Collapsers:

# Collapser takes a weighted list [(a, score), (b, score), ...] and returns another weighted list.
# input list may have multiple entries

def _normalize_distribution(dist):
    norm = sum(dist.values())
    return {x: s/norm for x, s in dist.items()}

class Collapse:
    @staticmethod
    def sum(distribution):
        out_dist = {}
        for e, s in distribution:
            if e not in out_dist:
                out_dist[e] = 0
            out_dist[e] += s
        return _normalize_distribution(out_dist)

    @staticmethod
    def max(distribution):
        out_dist = {}
        for e, s in distribution:
            if e not in out_dist:
                out_dist[e] = s
            else:
                out_dist[e] = max(out_dist[e], s)
        return _normalize_distribution(out_dist)

    @staticmethod
    def average(distribution):
        out_dist = {}
        counter = {}
        for e, s in distribution:
            if e not in out_dist:
                out_dist[e] = 0
            if e not in counter:
                counter[e] = 0
            out_dist[e] += s
            counter[e] += 1
        for e in counter:
            out_dist[e] = out_dist[e]/counter[e]
        return _normalize_distribution(out_dist)

class Hint:
    @staticmethod
    def all(distribution):
        return _normalize_distribution(distribution)

    @staticmethod
    def nbest(n):
        """Hint.nbest(3)"""
        def f(distribution):
            keys = sorted(distribution.keys(), key=lambda x: -distribution[x])[:n]
            return _normalize_distribution({k: distribution[k] for k in keys})
        return f

    @staticmethod
    def threshold(thresh):
        """usage Hint.threshold(0.3)"""
        def f(distribution):
            return _normalize_distribution({k: distribution[k] for k in distribution if distribution[k] > thresh})
        return f

    @staticmethod
    def zipf(exp):
        def f(distribution):
            keys = sorted(distribution.keys(), key=lambda x: -distribution[x])
            norm = sum([1/((i+1)**exp) for i in range(len(keys))])
            return _normalize_distribution({k: (1/(i**exp))/norm for k, i in enumerate(keys)})
        return f


