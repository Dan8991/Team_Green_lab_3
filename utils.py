import numpy as np

def generate_random_bin_string(l):
    return np.random.randint(2, size = l)

def bin_to_decimal(bin_arr):
    l = len(bin_arr)
    powers = np.array([2 ** (l - i - 1) for i in range(l)])
    res = bin_arr * powers
    return np.sum(res)

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
        c_dec = bin_to_decimal(c)
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        key_dec = bin_to_decimal(self.key)
        t = key_dec + n
        st = np.sum(decimal_to_base_array(t, 10))

        s = sc * st
        return decimal_to_base_array(s, 2)


class Bob():

    def __init__(self, key, lc, idb = 2):
        self.key = key
        self.idb = idb
        self.lc = lc
        self.n = 0
        self.c = 0

    def step_2(self, ida):
        self.c = generate_random_bin_string(self.lc)
        self.n += 1
        return self.c, self.n

    def step_4(self, r):
        c_dec = bin_to_decimal(self.c)
        sc = np.sum(decimal_to_base_array(c_dec, 10))

        key_dec = bin_to_decimal(self.key)
        t = key_dec + self.n
        st = np.sum(decimal_to_base_array(t, 10))

        s = sc * st
        r_hat = decimal_to_base_array(s, 2)

        return np.sum(np.abs(r-r_hat)) == 0



