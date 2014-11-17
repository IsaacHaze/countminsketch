from random import randint


class CountMinSketch(object):
    """Count-Min Sketches

    Count-min sketches will keep track of and return approximate
    counts of elements. The elements can be any hashable Python
    object.

    The error of the count estimate is at most (2N / w) with
    probability at least (1 - (1/2)^d).

    Based on the gentle introduction by the inventors:
      Cormode and Muthukrishnan. "Approximating data with the
      count-min data structure."  IEEE Software, (2012)

    """
    def __init__(self, w, d):
        """`w` is the hash width in bits, `d` is the number of hash functions.

        """
        self.w = w
        self.d = d
        self.p = 2**31-1  # magic number from the paper

        self.counts = [[0 for _ in range(w)] for _ in range(d)]
        self.total = 0

        self._init_hash_params()

    def update(self, e, c):
        """Update (increment) the counts for element `e` by `c`."""
        self.total += c
        for i in range(self.d):
            h = self.hash(i, e)
            self.counts[i][h] += c

    def estimate(self, e):
        """Estimate the accumulated counts for element `e`."""
        estimates = [self.counts[i][self.hash(i, e)] for i in range(self.d)]
        return min(estimates)

    def _init_hash_params(self):
        self.a_b = []
        for i in range(self.d):
            a = randint(1, self.p-1)
            b = randint(1, self.p-1)
            self.a_b.append((a, b))

    def hash(self, i, e):
        """Apply the `i`th hash function to element `e`."""
        e_int = hash(e)
        a, b = self.a_b[i]

        return CountMinSketch.hash_cw(self.p, self.w, a, b, e_int)

    @staticmethod
    def hash_cw(p, w, a, b, e):
        """Auxillary hashing function for the CountMinSketch class.

        We use this parameterized hash function to obtain our
        pairwise-independent hash functions. `p` and `w` define the
        sub-family, `a` and `b` define the members.

        """
        # Universal hash functions from: Carter & Wegman "Universal
        # classes of hash functions" 1979
        #
        # a and b should be random integers in the range [1, p-1]
        return (((a*e + b) % p) % w)
