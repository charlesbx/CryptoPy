import numpy as np
from src.utils import bytes_to_hex_no_flatten, is_hex_string
from src.rsa import RSA
from src.aes import AES

class PGP:
    def __init__(self):
        pass
        
    def cipher(self, message, key):
        self.key = np.random.bytes(16)
        self.key = bytes_to_hex_no_flatten(self.key)
        self.receiver_key = key
        self.encrypted_key = RSA().cipher(self.key, key)
        if is_hex_string(message) == False:
            bytes_message = bytearray(message, 'utf-8')
            message = bytes_to_hex_no_flatten(bytes_message)
            
        aes = AES(self.key)
        result = "-----BEGIN PGP MESSAGE-----\n\n" + str(self.encrypted_key) + '\n' + str(aes.cipher(message)) + "\n\n-----END PGP MESSAGE-----"
        return result
    
    def decipher(self, message, key):
        message = message[:-1]
        if message.startswith("-----BEGIN PGP MESSAGE-----") == False:
            raise Exception("ERROR: invalid PGP message")
        if message.endswith("-----END PGP MESSAGE-----") == False:
            raise Exception("ERROR: invalid PGP message")
        
        message = message.split('\n')
        encrypted_key = message[2]
        encrypted_message = message[3]
        
        decrypted_key = RSA().decipher(encrypted_key, key)
        decrypted_key = bytearray.fromhex(decrypted_key)
        if len(decrypted_key) < 16:
            while len(decrypted_key) < 16:
                decrypted_key.insert(0, 0)
        decrypted_key = bytes(decrypted_key)
        decrypted_key = bytes_to_hex_no_flatten(decrypted_key)
        
    
        aes = AES(decrypted_key)
        decrypted_message = aes.decipher(encrypted_message)
        return decrypted_message
