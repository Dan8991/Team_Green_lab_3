from utils import Alice, Bob, generate_random_bin_string
import numpy as np
from carol import *

lk = 10
lc = 10
common_key = generate_random_bin_string(lk)
alice = Alice(common_key)
bob = Bob(common_key, lc)

ida = alice.step_1()
c, n = bob.step_2(ida)
r = alice.step_3(c, n)
accepted = bob.step_4(r)
print(f"Alice was accepted?: {accepted}")

#ts_distribution(n, n+2**lk)

plot_probabilities(lc, lk)