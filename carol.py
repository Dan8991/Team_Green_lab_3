import numpy as np
from collections import Counter
from utils import *
import time
import matplotlib.pyplot as plt

current_milli_time = lambda: int(round(time.time() * 1000))

class Carol():
    def __init__(self, lc, n, c):
        self.lc = lc
        self.n = n
        self.c = c

    def task3(self):
        #compute the decimal representation of c
        c_dec = bin_to_decimal(self.c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        #Compute st
        st = compute_probable_value(self.lc, self.n)

        s = st*sc
        #converting s to base 2
        return  decimal_to_base_array(s, 2)


def compute_probable_value(l, n):
    results = []
    #Compute the random number and adds the value of n
    #then it sums all the digits
    for i in range(0, 1000):
        dec_random_k = bin_to_decimal(generate_random_bin_string(l))
        t = dec_random_k + n
        results.append(np.sum(decimal_to_base_array(t, 10)))
    
    #Create a dictionary of the computed sums and return the key
    #with the highest value
    final_results = dict(sorted(Counter(results).items()))
    return max(final_results, key=final_results.get)


def attack_with_carol(lc, lk):
    common_key = generate_random_bin_string(lk)
    alice = Alice(common_key)
    bob = Bob(common_key, lc)

    ida = alice.step_1()
    c, n = bob.step_2(ida)

    #Intruder
    carol = Carol(lc, n, c)
    r_carol = carol.task3()

    return bob.step_4(r_carol)


def probability_of_success_and_complexity(lc, lk, repetitions):
    successful_attacks = 0
    time = 0
    for i in range(0, repetitions):
        start = current_milli_time()
        result = attack_with_carol(lc, lk)
        end = current_milli_time()
        time += (end-start)
        if result:
            successful_attacks += 1
    print("successfull attacks:", successful_attacks)
    return successful_attacks/repetitions, time/repetitions


def complexity(lc, lk, repetitions):
    time = 0
    for i in range(0, repetitions):
        start = current_milli_time()
        result = attack_with_carol(lc, lk)
        end = current_milli_time()
        time += (end-start)
    return time/repetitions


def plot_probabilities(lc, lk):
    changing_lc_prob = []
    changing_lc_complex = []
    for i in range(0, 10, 2):
        print("times")
        prob, comp = probability_of_success_and_complexity(lc+i, lk, 500)
        changing_lc_prob.append(prob)
        changing_lc_complex.append(comp)

    changing_lk_prob = []
    changing_lk_complex = []
    for i in range(0, 10, 2):
        print("times")
        prob, comp = probability_of_success_and_complexity(lc, lk+i, 500)
        changing_lk_prob.append(prob)
        changing_lk_complex.append(comp)

    changing_lc_lk_prob = []
    changing_lc_lk_complex = []
    for i in range(0, 10, 2):
        print("times")
        prob, comp = probability_of_success_and_complexity(lc+i, lk+i, 500)
        changing_lc_lk_prob.append(prob)
        changing_lc_lk_complex.append(comp)
    
    plt.plot(changing_lc_prob, "r", label="Varying lc")
    plt.plot(changing_lk_prob, "g", label="Varying lk")
    plt.plot(changing_lc_lk_prob, "b", label="Varying lc and lk")
    plt.show()

    plt.plot(changing_lc_complex, "r", label="Varying lc")
    plt.plot(changing_lk_complex, "g", label="Varying lk")
    plt.plot(changing_lc_lk_complex, "b", label="Varying lc and lk")
    plt.show()