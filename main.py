from utils import Alice, Bob, generate_random_bin_string
import numpy as np
from carol import *

lk = 10
lc = 10
times_accepted = 0
"""
for i in range(0, 500):
    #Debug print to see if the machine is still Working
    if i%100 == 0 and i != 0:
        print("Working")

    common_key = generate_random_bin_string(lk)
    alice = Alice(common_key)
    bob = Bob(common_key, lc)

    ida = alice.step_1()
    c, n = bob.step_2(ida)

    #Intruder
    carol = Carol(lc, n, c)
    r_carol = carol.task3()
    if bob.step_4(r_carol):
        times_accepted += 1

#print(f"Alice was accepted?: {accepted}")
print("Times that the intruder was accepted:", times_accepted)
"""

plot_probabilities(lc, lk)