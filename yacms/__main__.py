#!/usr/bin/env python
from os import path
import re
from collections import Counter

from . import CountMinSketch



def tokenize(string):
    words = re.compile('(\w+)')

    for m in re.finditer(words, string):
        yield m.group(1)


def main():
    pkg_dir = path.join(path.dirname(__file__))
    #TODO: maybe i shouldn't include this file...
    with open(path.join(pkg_dir, 'ideal_hash.txt')) as f:
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
