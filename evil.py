import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import random

from utils import generate_random_bin_string,Alice,Bob,bin_to_decimal,decimal_to_base_array

current_milli_time = lambda: int(round(time.time() * 1000))


def attack_with_evil(lk,lc, round_to_collect):

    common_key = generate_random_bin_string(lk)
    alice = Alice(common_key)
    bob = Bob(common_key, lc)
    
    bob.n = round_to_collect - 1
    ida = alice.step_1()
    c, n = bob.step_2(ida)
    r = alice.step_3(c, n)
    accepted = bob.step_4(r)

    print("Evil is collecting information about round ",n)
    evil = Evil(r, c, n)

    print("A and B are communicating")
    bob.n += 24

    print("Evil is trying to be A 25 round after")
    c, n = bob.step_2(ida)
    r = evil.attack(c)
    accepted = bob.step_4(r)
    print(f"Alice was accepted?: {accepted}")
    return accepted

def evaluate(lk, lc, round_to_collect, tests = 10**3):
    sys.stdout = open(os.devnull, 'w')
    n = 0
    for _ in range(tests):
        n += attack_with_evil(lk,lc,round_to_collect)
    sys.stdout = sys.__stdout__    
    return n/tests
    
def plot_probablities_and_complexity(lk):
    
    lcs = [10, 20, 30, 40, 50]
    probs = {lc:[] for lc in lcs}
    complexity = {lc: [] for lc in lcs}
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    
    for lc in tqdm(lcs):
        for i in range(lk, lk + 40, 2):
            #choosing a random round
            probab = evaluate(lk,lc,random.randint(0, 1000))
            probs[lc].append(probab)
            complexity[lc].append(evaluate_time(lk + i, lc, random.randint(0, 1000)))

        axs[0].plot(np.arange(10, 50, 2), probs[lc], label=f"lc = {lc}")
        axs[0].set_xlabel("lk")
        axs[0].set_ylabel("Success Probability [%]")
        axs[0].legend()
        axs[0].set_ylim([0, 1])

        axs[1].plot(np.arange(10, 50, 2), complexity[lc], label=f"lc = {lc}")
        axs[1].set_xlabel("lk")
        axs[1].set_ylabel("Complexity [ms]")
        axs[1].legend()
    plt.savefig("task2.png")

def evaluate_time(lk,lc,round_to_collect,tests=10**3):
    sys.stdout = open(os.devnull, 'w')
    mean_time = 0
    for _ in range(tests):
        start = current_milli_time()
        attack_with_evil(lk,lc,round_to_collect)
        end = current_milli_time()
        mean_time += end-start
    sys.stdout = sys.__stdout__    
    return mean_time/tests
    
class Evil():
    
    def __init__(self,r, c, n):
        self.n = n
        #compute the decimal representation of c
        c_dec = bin_to_decimal(c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))
        s = bin_to_decimal(r)
        #done in over to solve the case where c has all bits equal to zero
        #in this case we get no information about s_t so we can just set it at random
        if sc == 0:
            self.st = 10
        else: 
            self.st = int(s / sc )
        
        
    def attack(self, c):
        #compute the decimal representation of c
        c_dec = bin_to_decimal(c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))
        # t potrebbe essere aumentato di 7 (2+5)
        s = (self.st+7) * sc
        r = decimal_to_base_array(s, 2)
        return r
        
         
