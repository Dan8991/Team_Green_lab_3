import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
from tqdm import tqdm

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

def evaluate(lk,lc,round_to_collect,tests):
    sys.stdout = open(os.devnull, 'w')
    n = 0
    for _ in range(tests):
        n += attack_with_evil(lk,lc,round_to_collect)
    sys.stdout = sys.__stdout__    
    return n/tests
    
def evaluate_success_probability(lk,lc,round_to_collect):
    
    print("\n")
    print("\n")
    print("Evaluating success probability varying n")
    probab_var_n = np.array([])
    for i in range(round_to_collect,round_to_collect+100,5):
        probab = evaluate(lk,lc,i,100)
        print("Success probability: ", probab)
        probab_var_n = np.append(probab_var_n,probab)

    print("\n")
    print("\n")
    print("Evaluating success probability varying lk")
    probab_var_lk = np.array([])
    for i in range(lk,lk+100,5):
        probab = evaluate(i,lc,round_to_collect,100)
        print("Success probability: ", probab)
        probab_var_lk = np.append(probab_var_lk,probab)
        
    print("\n")
    print("\n")
    print("Evaluating success probability varying lc")
    probab_var_lc = np.array([])
    for i in range(lc,lc+100,5):
        probab = evaluate(lk,i,round_to_collect,100)
        print("Success probability: ", probab)
        probab_var_lc = np.append(probab_var_lc,probab)
    print(probab_var_n)    
    return probab_var_n,probab_var_lk,probab_var_lc

def plot_probablities(probab_var_n,probab_var_lk,probab_var_lc):
    
    print(probab_var_n)
    plt.plot(probab_var_n)
    plt.ylabel('varying n')
    plt.show()    
    
    plt.plot(probab_var_lk)
    plt.ylabel('varying lk')
    plt.show() 
 
    plt.plot(probab_var_lc)
    plt.ylabel('varying lc')
    plt.show()


def evaluate_time(lk,lc,round_to_collect,tests):
    sys.stdout = open(os.devnull, 'w')
    mean_time = 0
    for _ in range(tests):
        start = current_milli_time()
        attack_with_evil(lk,lc,round_to_collect)
        end = current_milli_time()
        mean_time += end-start
    sys.stdout = sys.__stdout__    
    return mean_time/tests
    
def evaluate_complexity():
    
    print("\n")
    print("\n")
    print("Evaluating computational complexity increasing lk (from 10 to 60)")
    compl_var_lk = np.array([])
    for i in tqdm(range (50)):
        compl_var_lk = np.append(compl_var_lk, evaluate_time(i+10,10,10,20))
    
    
    print("\n")
    print("\n")
    print("Evaluating computational complexity increasing lc (from 10 to 60)")
    compl_var_lc = np.array([])
    for i in tqdm(range(50)):
        compl_var_lc = np.append(compl_var_lc,evaluate_time(10,i+10,10,20))
    
    print("\n")
    print("\n")
    print("Evaluating computational complexity increasing both lk and lc (from 10 to 60)")
    compl_var_lk_lc = np.array([])
    for i in tqdm(range(50)):
        compl_var_lk_lc = np.append(compl_var_lk_lc,evaluate_time(i+10,i+10,10,20))
    
    return compl_var_lk,compl_var_lc,compl_var_lk_lc


def plot_time(compl_var_lk,compl_var_lc,compl_var_lk_lc):
    
    plt.plot(compl_var_lk)
    plt.ylabel('varying lk')
    plt.show()    
    
    plt.plot(compl_var_lc)
    plt.ylabel('varying lc')
    plt.show() 
 
    plt.plot(compl_var_lk_lc)
    plt.ylabel('varying both lk and lc')
    plt.show()

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
        
         
