import numpy as np
from collections import Counter

#generates an l bits long binary string
def generate_random_bin_string(l):
    return np.random.randint(2, size = l)

#transforms a binary array into its decimal representation
def bin_to_decimal(bin_arr):
    l = len(bin_arr)
    powers = np.array([2 ** (l - i - 1) for i in range(l)])
    res = bin_arr * powers
    return np.sum(res)

'''
transforms a decimal number into an array with the numbers in the declared base
for example 
* 1233 in base 10 becomes [1, 2, 3, 3]
* 17 in base 2 becomes [1, 0, 0, 0, 1]
'''
def decimal_to_base_array(decimal, base):
    arr = []
    while decimal > 0:
        arr.append(decimal % base)
        decimal = decimal // base

    return np.flip(arr)




class Alice():

    def __init__(self, key, ida = 1):
        self.key = key
        self.ida = ida

    def step_1(self):
        return self.ida

    def step_3(self, c, n):
        #compute the decimal representation of c
        c_dec = bin_to_decimal(c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        #compute the decimal representation of the key
        key_dec = bin_to_decimal(self.key)
        #sum the decimal representation of the key with n
        t = key_dec + n
        #sum the decimal digits of t
        st = np.sum(decimal_to_base_array(t, 10))

        s = sc * st
        #converting s to base 2
        r = decimal_to_base_array(s, 2)

        return r


class Bob():

    def __init__(self, key, lc, idb = 2):
        self.key = key
        self.idb = idb
        self.lc = lc
        self.n = 0
        self.c = 0

    def step_2(self, ida):
        #generate random challenge
        self.c = generate_random_bin_string(self.lc)
        #increment counter
        self.n += 1
        return self.c, self.n

    def step_4(self, r):

        #compute the decimal representation of c
        c_dec = bin_to_decimal(self.c)
        #sum all the decimal digits of c
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        #compute the decimal representation of the key
        key_dec = bin_to_decimal(self.key)
        #sum the decimal representation of the key with n
        t = key_dec + self.n
        #sum the decimal digits of t
        st = np.sum(decimal_to_base_array(t, 10))

        s = sc * st
        #converting s to base 2
        r_hat =bin_to_decimal(decimal_to_base_array(s, 2))
        r = bin_to_decimal(r)


        #checking if r, r_hat are equal, if so true is returned
        return r-r_hat == 0

def get_decimal_sum_distribution(max_val):


    decomposition = decimal_to_base_array(max_val, 10)
    exp = len(decomposition) - 1
    vals = np.array([0 for _ in range((exp + 1)* 9 + 1)])
    bases = [[] for _ in range(exp + 2)]
    vals[0] = 1

    for i in range(1, exp + 2):
        end = 9 * (i - 1) + 1
        base = np.copy(vals[:end])
        bases[i - 1] = np.array(base)
        if i < exp + 1:
            limit = 10
        else:
            limit = decomposition[0]
        for j in range(1, limit):
            vals[j:(j + end)] += base

    cum_sum = 0
    for i in range(exp):
        cum_sum += decomposition[i]
        for j in range(decomposition[i + 1]):
            vals[(cum_sum + j):(cum_sum + j + len(bases[exp - i - 1]))] += bases[exp - i - 1]

    return vals

#use this function to compute the distribution
#min_val is the counter n, max_val is n + 2**lk i.e the maximum value of n + k
def ts_distribution(min_val, max_val):
    max_dist = get_decimal_sum_distribution(max_val)
    min_dist = get_decimal_sum_distribution(min_val)
    min_dist = np.append(min_dist, np.zeros(len(max_dist)-len(min_dist)))
    return max_dist - min_dist
