from utils import Alice, Bob, generate_random_bin_string, Carol
import numpy as np

lk = 10
lc = 10
common_key = generate_random_bin_string(lk)
alice = Alice(common_key)
bob = Bob(common_key, lc)

ida = alice.step_1()
c, n = bob.step_2(ida)

#Intruder
carol = Carol(lc, n, c)
r_carol = carol.task3()

r = alice.step_3(c, n)
accepted = bob.step_4(r_carol)
print(f"Alice was accepted?: {accepted}")
