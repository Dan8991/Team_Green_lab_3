
from utils import Alice, Bob, generate_random_bin_string
from evil import Evil,attack_with_evil,evaluate_success_probability,plot_probablities,evaluate_complexity,plot_time
import numpy as np
import carol

print("------------ TASK 1 -----------")
print("\n")

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
print("\n")
print("\n")

print("------------ TASK 2 -----------")
print("\n")
print("Attacking with lk=10, lc=10, n=1")
attack_with_evil(10,10,1)
print("\n")
print("Attacking with lk=10, lc=10, n=37")
attack_with_evil(10,10,37)
print("\n")
print("Attacking with lk=5, lc=5, n=12")
attack_with_evil(5,5,12)
print("\n")
print("Attacking with lk=30, lc=20, n=20")
attack_with_evil(30,20,20)
print("\n")
print("Attacking with lk=15, lc=10, n=55")
attack_with_evil(15,10,55)


#arr_n, arr_lk, arr_lc = evaluate_success_probability(20,20,1)

#plot_probablities(arr_n, arr_lk, arr_lc)


compl_var_lk,compl_var_lc,compl_var_lk_lc = evaluate_complexity()

plot_time(compl_var_lk,compl_var_lc,compl_var_lk_lc)


print("starting task 3")

carol.plot_probabilities(lc, lk)
