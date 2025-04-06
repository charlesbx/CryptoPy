import numpy as np
from src.utils import hex_to_bytes, bytes_to_hex, break_into_blocks

class XOR:
    def __init__(self):
        pass
    
    def cipher_block(self, message, key):
        message = hex_to_bytes(message)
        key = hex_to_bytes(key)
        if len(message) != len(key):
            raise Exception('ERROR: message and key must be of the same size in block mode')
        ciphered = np.bitwise_xor(message, key)
        ciphered = bytes_to_hex(ciphered)
        return ciphered
    
    def decipher_block(self, message, key):
        message = hex_to_bytes(message)
        key = hex_to_bytes(key)
        if len(message) != len(key):
            raise Exception('ERROR: message and key must be of the same size in block mode')
        deciphered = np.bitwise_xor(message, key)
        deciphered = bytes_to_hex(deciphered)
        return deciphered
    
    def cipher(self, message, key):
        blocks = break_into_blocks(message)
        ciphered = ''
        for block in blocks:
            ciphered += self.cipher_block(block, key)
        return ciphered
        
    def decipher(self, message, key):
        blocks = break_into_blocks(message)
        deciphered = ''
        for block in blocks:
            deciphered += self.decipher_block(block, key)
        return deciphered