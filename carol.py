import numpy as np
from collections import Counter
from utils import *
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

current_milli_time = lambda: int(round(time.time() * 1000))

class Carol():
    def __init__(self, lk, n, c):
        self.lk = lk
        self.n = n
        self.c = c

    def task3(self):
        #compute the decimal representation of c
        c_dec = bin_to_decimal(self.c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        #Compute st
        dist, used_alg = ts_distribution(self.n, self.n + 2**self.lk)
        if used_alg:
            st = np.argmax(dist)
        else:
            st = dist

        s = st*sc
        #converting s to base 2
        return  decimal_to_base_array(s, 2)

#Brute force version to compute the most probable value of k
def compute_probable_value(l, n):
    results = []
    #Compute the random number and adds the value of n
    #then it sums all the digits
    for _ in range(0, 100):
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
    carol = Carol(lk, n, c)
    r_carol = carol.task3()

    return bob.step_4(r_carol)


def probability_of_success_and_complexity(lc, lk, repetitions):
    successful_attacks = 0
    time = 0
    for _ in range(0, repetitions):
        start = current_milli_time()
        result = attack_with_carol(lc, lk)
        end = current_milli_time()
        time += (end-start)
        if result:
            successful_attacks += 1
    return successful_attacks/repetitions, time/repetitions


def complexity(lc, lk, repetitions):
    time = 0
    for _ in range(0, repetitions):
        start = current_milli_time()
        result = attack_with_carol(lc, lk)
        end = current_milli_time()
        time += (end-start)
    return time/repetitions


def plot_probabilities(lk):
    lcs = [10, 20, 30, 40, 50]
    probs = {lc: [] for lc in lcs}
    complexities = {lc:[] for lc in lcs}
    repetitions = 10**3
    fig, axs = plt.subplots(1, 2, figsize = (15, 5))
    colors = ["yellow", "orange", "red", "green", "blue"]
    for c, lc in tqdm(enumerate(lcs)):
        for i in range(0, 250, 10):
            prob, comp = probability_of_success_and_complexity(lc, lk + i, repetitions)
            probs[lc].append(prob*100)
            complexities[lc].append(comp)
        axs[0].plot(np.arange(10, 260, 10), probs[lc], label=f"lc = {lc}")
        axs[0].set_xlabel("lk")
        axs[0].set_ylabel("Success Probability [%]")
        axs[0].legend()
        axs[0].set_ylim([0, 15])

        axs[1].plot(
                np.arange(10, 65, 10),
                complexities[lc][:6],
                c=colors[c],
                label=f"lc = {lc} with alg"
        )
        axs[1].plot(
                np.arange(70, 260, 10),
                complexities[lc][6:],
                c=colors[c],
                label=f"lc = {lc} with approx",
                linestyle="--"
        )
        
        axs[1].set_xlabel("lk")
        axs[1].set_ylabel("Computational Complexity [ms]")
        axs[1].legend()

    plt.savefig("task_3.png")
