#!/usr/bin/env python
import re
from random import randint

from collections import Counter


def hash_cw(p, w, a, b, i):
    # Universal hash functions from: Carter & Wegman "Universal
    # classes of hash functions" 1979
    #
    # a and b should be random integers in the range [1, p-1]
    return (((a*i + b) % p) % w)


class CountMinSketch(object):
    """Count-Min Sketches

    Based on the gentle introduction by the inventors:
      Cormode and Muthukrishnan. "Approximating data with the
      count-min data structure."  IEEE Software, (2012)

    """
    def __init__(self, w, d):
        """Count-min sketches will keep track and return approximate counts
        elements.

        The error is at most 2N/w with probability at least 1 -
        (1/2)^d.

        """
        self.w = w
        self.d = d
        self.p = 2**31-1  # magic number from the paper

        self.counts = [[0 for _ in range(w)] for _ in range(d)]
        self.total = 0

        self._init_hash_params()

    def update(self, e, c):
        self.total += c
        for i in range(self.d):
            h = self.hash(i, e)
            self.counts[i][h] += c

    def estimate(self, e):
        estimates = [self.counts[i][self.hash(i, e)] for i in range(self.d)]
        return min(estimates)

    def _init_hash_params(self):
        self.a_b = []
        for i in range(self.d):
            a = randint(1, self.p-1)
            b = randint(1, self.p-1)
            self.a_b.append((a, b))

    def hash(self, i, e):
        e_int = hash(e)
        a, b = self.a_b[i]

        return hash_cw(self.p, self.w, a, b, e_int)


def tokenize(string):
    words = re.compile('(\w+)')

    for m in re.finditer(words, string):
        yield m.group(1)


def main():
    with open('ideal_hash.txt') as f:
        text = f.read().decode('utf-8')

    # counts = Counter(tok for tok in tokenize(text))
    counts = Counter()
    cm_sketch = CountMinSketch(1024, 3)

    for tok in tokenize(text):
        counts[tok] += 1
        cm_sketch.update(tok, 1)

    for e in counts:
        print "'%s' counter: %d, sketch: %d" % (e, counts[e],
                                                cm_sketch.estimate(e))

if __name__ == '__main__':
    main()
