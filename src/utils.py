import numpy as np
import random

def hex_to_bytes(hexa):
    return np.array([int(hexa[i:i+2], 16) for i in range(0, len(hexa), 2)])
    
def bytes_to_hex(bytes):
    bytes = bytes.flatten()
    
    str = ''.join('{:02x}'.format(byte) for byte in bytes)
    if len(str) % 2 != 0:
        str = '0' + str
    return str

def bytes_to_hex_no_flatten(bytes):
    str = ''.join('{:02x}'.format(byte) for byte in bytes)
    if len(str) % 2 != 0:
        str = '0' + str
    return str

def break_into_blocks(message):
    message = hex_to_bytes(message)
    nb_blocks = len(message) // 16
    blocks = np.zeros((nb_blocks, 4, 4), dtype=np.uint8)
    for i in range(nb_blocks):
        blocks[i] = message[i*16:(i+1)*16].reshape((4, 4))
    blocks = [bytes_to_hex(block) for block in blocks]
    return blocks

def convert_to_big_endian(bytes):
    if type(bytes) != str:
        bytes = bytes_to_hex_no_flatten(bytes)
    bytes = bytearray.fromhex(bytes)[::-1]
    bytes = int.from_bytes(bytes, byteorder='big')
    bytes = np.array([bytes])
    return bytes

def is_prime(nbr):
    if nbr == 2:
        return True
    if nbr % 2 == 0:
        return False
    r, s = 0, nbr - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(100):
        a = random.randrange(2, nbr - 1)
        x = pow(a, s, nbr)
        if x == 1 or x == nbr - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, nbr)
            if x == nbr - 1:
                break
        else:
            return False
    return True

def is_hex_string(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False