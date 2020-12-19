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
    for i in range(0, 5000):
        dec_random_k = bin_to_decimal(generate_random_bin_string(l))
        t = dec_random_k + n
        results.append(np.sum(decimal_to_base_array(t, 10)))
    
    #Create a dictionary of the computed sums and return the key
    #with the highest value
    final_results = dict(sorted(Counter(results).items()))
    return max(final_results, key=final_results.get)
    