import numpy as np
from math import gcd
from src.utils import hex_to_bytes, bytes_to_hex_no_flatten, convert_to_big_endian
import random

class RSA:
    def __init__(self, p=None, q=None):
        if p != None and q != None:
            self.p = hex_to_bytes(p)
            self.q = hex_to_bytes(q)

            self.n = self.p * self.q
            self.n = convert_to_big_endian(self.n)

            self.phi = (self.p - 1) * (self.q - 1)
            self.phi = convert_to_big_endian(self.phi)

    def gcd_ext(self, a, b):
        x, x1 = 0, 1
        y, y1 = 1, 0

        while a:
            q = b // a
            x1, x = x - q * x1, x1
            y1, y = y - q * y1, y1
            a, b = b % a, a

        return b, x, y

    def inverse(self, a, m):
        b, x, y = self.gcd_ext(a, m)

        return (x % m + m) % m

    def generate_keys(self):
        t = self.phi[0]
        e = random.randint(2, t - 1)
        while gcd(e, t) != 1:
            e = random.randint(2, t - 1)

        d = self.inverse(e, t)
        n = bytes_to_hex_no_flatten(self.n)
        e = convert_to_big_endian(np.array([e]))
        e = bytes_to_hex_no_flatten(e)
        d = convert_to_big_endian(np.array([d]))
        d = bytes_to_hex_no_flatten(d)

        print("public key: " + str(e) + "-" + str(n))
        print("private key: " + str(d) + "-" + str(n))

    def expmod(self, m, e, n):
        res = 1
        m = m % n

        while e > 0:
            if e & 1:
                res = (res * m) % n
            m = (m * m) % n
            e >>= 1
        res = convert_to_big_endian(res)
        return res

    def cipher(self, message, key):
        message = hex_to_bytes(message)
        e, n = key.split('-')
        e = hex_to_bytes(e)
        message = convert_to_big_endian(message)
        e = convert_to_big_endian(e)
        n = convert_to_big_endian(n)
        return bytes_to_hex_no_flatten(self.expmod(message, e, n))

    def decipher(self, message, key):
        message = hex_to_bytes(message)
        d, n = key.split('-')
        d = hex_to_bytes(d)
        message = convert_to_big_endian(message)
        d = convert_to_big_endian(d)
        n = convert_to_big_endian(n)
        return bytes_to_hex_no_flatten(self.expmod(message, d, n))
